# Comment out the two lines below in production
import sys
sys.path.append('../')
from util.utilFunctions import checkUser, checkEvent, makeConnection, callQuery
from util.users import checkArc
from util.events import getEventTimes
from datetime import datetime
from dateutil.relativedelta import relativedelta
import csv

week = datetime.strptime('2020-02-17', "%Y-%m-%d").date()
#end = datetime.strptime('2021-01-01', "%Y-%m-%d").date()
weekDate = {}
for counter in range(0, 12):
    weekDate[f'T1W{str(counter)}'] = str(week)
    week += relativedelta(days=7)

# TODO: Check if eventID has a temporaryAccessCode enabled, if so check that field
@makeConnection
def register(zID, eventID, time, accessCode, conn = None, curs = None):
    if checkEvent(eventID) == False:
        return "Event does not exist"

    if checkParticipation(zID, eventID) == True:
        return "Already registered"

    isArc = checkArc(zID)

    eventTimes = getEventTimes(eventID)
    if (eventTimes != None):
        startTime, endTime = eventTimes[0], eventTimes[1]
        if (endTime != None):
            if (datetime.now() > endTime):
                return "Event closed already"
        if (startTime != None):
            if (datetime.now() < startTime):
                return "Event hasn't started yet"

    eventCode = getAccessCode(eventID)
    print(eventCode)
    if eventCode:
        if accessCode != eventCode: return "Wrong Access Code"

    results = callQuery("INSERT INTO participation(points, isArcMember, zid, eventID, time) VALUES ((%s), (%s), (%s), (%s), (%s))", conn, curs, (1, isArc, zID, eventID, time,))
    if (results == False): return "Database error, check backend log"
    conn.commit()
    conn.close()
    return "success"

@makeConnection
def getAccessCode(eventID, conn, curs):
    queryResults = callQuery("SELECT accessCode FROM events WHERE eventid = (%s);", conn, curs, (eventID,))
    if queryResults == False: return "Databse error, check backend log"

    code = curs.fetchone()
    conn.close()
    return code[0] if code is not None else None

@makeConnection
def changePoints(zID, eventID, newPoints, conn = None, curs = None):

    results = callQuery("update participation set points=(%s) WHERE eventID=(%s) and zid=(%s)", conn, curs, (newPoints, eventID, zID,))
    if (results == False): return "failed"
    conn.commit()
    conn.close()
    return "success"

@makeConnection
def deleteUserAttendance(zID, eventID, conn = None, curs = None):

    results = callQuery("DELETE FROM participation WHERE zid=(%s) and eventid=(%s)", conn, curs, (zID, eventID,))
    if (results == False): return "failed"
    conn.commit()
    conn.close()
    return "success"

@makeConnection
def checkParticipation(zID, eventID, conn = None, curs = None):

    results = callQuery("SELECT * FROM participation WHERE zid=(%s) and eventid=(%s)", conn, curs, (zID, eventID,))
    if (results == False): return False

    rows = curs.fetchall()
    conn.close()
    return False if rows == [] else True

@makeConnection
def getAttendanceCSV(eventID, conn = None, curs = None):
    if (checkEvent(eventID) == False):
        return "failed"

    results = callQuery("SELECT isArcMember, users.zID, users.firstName, users.lastName, time FROM PARTICIPATION JOIN EVENTS ON (participation.eventID = events.eventID) JOIN USERS ON (PARTICIPATION.ZID = USERS.zID) WHERE events.eventID = (%s);", conn, curs, (eventID,))
    if (results == False): return "failed"
    results = curs.fetchall()
    if results == []:
        return "No attendance"
    conn.commit()

    import os
    path = os.getcwd()
    path += f'/csvFiles/{eventID}.csv'
    try:
        with open(path, 'w', newline='') as file:
            file.write("IsArcMember,zID,FirstName,LastName,Time(AEST)\n")
            writer = csv.writer(file, delimiter=',')
            writer.writerows(results)
    except Exception as e:
        print(e)
        return "Failed"
    
    conn.close()
    return path

@makeConnection
def getUpcomingEvents(zID, conn = None, curs = None):

    results = getUserSocieties(zID)

    payload = []
    if results == []:
        conn.close()
        return payload

    today = str(datetime.now().date())
    for soc in results:
        results = callQuery("SELECT eventid, name, eventdate, location FROM hostedEvents WHERE societyid = (%s) AND eventDate >= (%s) ORDER BY eventDATE;", conn, curs, (soc['societyID'], today,))
        if (results == False): return "failed"
        result = curs.fetchall()

        if result == []:
            continue

        for i in result:
            eventJSON = {}
            eventJSON['eventID'] = i[0]
            eventJSON['name'] = i[1]
            eventJSON['eventDate'] = str(i[2])
            eventJSON['location'] = i[3]
            eventJSON['societyID'] = soc['societyID']
            eventJSON['societyName'] = soc['societyName']
            payload.append(eventJSON)
    
    conn.close()
    return payload

@makeConnection
def getUserSocieties(zID, conn = None, curs = None):

    results = callQuery("SELECT societyID, societyName FROM userInSociety where zID = (%s);", conn, curs, (zID,))
    if (results == False): return "failed"
    results = curs.fetchall()

    payload = []
    for society in results:
        societyJSON = {}
        societyJSON['societyID'] = society[0]
        societyJSON['societyName'] = society[1]
        payload.append(societyJSON)

    conn.close()
    return payload

@makeConnection
def getUserParticipation(zID, socID = None, conn = None, curs = None):
    if socID == None:
        results = callQuery("SELECT eventID, name, eventDate, location, societyName, societyID FROM userParticipatedEvents WHERE zid = (%s) ORDER BY eventDate DESC;", conn, curs, (zID,))
    else:
        results = callQuery("SELECT eventID, name, eventDate, location, societyName, societyID FROM userParticipatedEvents WHERE zid = (%s) AND societyID = (%s) ORDER BY eventDate DESC;", conn, curs, (zID, socID,))
    if (results == False): return None

    results = curs.fetchall()
    if (results == []):
        return None

    payload = []
    for event in results:
        eventJSON = {}
        eventJSON['eventID'] = event[0]
        eventJSON['name'] = event[1]
        eventJSON['eventDate'] = str(event[2])
        eventJSON['location'] = event[3]
        eventJSON['societyName'] = event[4]
        eventJSON['societyID'] = event[5]
        payload.append(eventJSON)
    conn.close()
    return payload

# TODO: Average Monthly/Weekly Attendance info (for recurring events)

# TODO: Average Monthly/Weekly Attendance info (for one society)
# NOTE: Accept two arguments, dataType must be in ['week', 'month'], inputting either will display the results of the calendar year 2020
@makeConnection
def averageAttendance(dateType, socID, conn = None, curs = None):

    payload = {}
    for i in range(0, len(weekDate) - 1):
        results = callQuery("SELECT * FROM events JOIN host ON (host.eventID = events.eventID) WHERE eventDate >= (%s) and eventDate < (%s) and society = (%s);", conn, curs, (weekDate[f'T1W{str(i)}'], weekDate[f'T1W{str(i + 1)}'], socID,))
        if (results == False): return "failed"
        #conn.commit()
        results = curs.fetchall()
        currPayload = []
        for event in results:
            eventJSON = {}
            eventJSON['eventID'] = event[0]
            eventJSON['name'] = event[1]
            eventJSON['date'] = str(event[2])

            # TODO: Change this to average
            results = callQuery("SELECT count(*) AS count FROM participation WHERE eventID = (%s);", conn, curs, (event[0],))
            if (results == False): return "failed"
            eventJSON['attendance'] = curs.fetchone()[0]

            currPayload.append(eventJSON)
        if currPayload != []:
            payload[f'T1W{str(i)}'] = currPayload
    conn.close()
    return payload
    
# TODO: Average Monthly/Weekly Attendance info (for one user)
'''
@makeConnectiondef main():
    print(averageAttendance('week', '74DF2'))

if __name__ == '__main__':
    main()
'''
