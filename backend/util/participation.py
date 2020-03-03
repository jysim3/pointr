# Comment out the two lines below in production
import sys
sys.path.append('../')
from util.utilFunctions import createConnection, checkUser, checkEvent
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

def register(zID, eventID, time = None):
    if checkEvent(eventID) == False:
        return "Event does not exist"

    if checkParticipation(zID, eventID) == True:
        return "Already registered"

    isArc = checkArc(zID)

    conn = createConnection()
    curs = conn.cursor()
    # NOTE: DEFAULTS TO THE CURRENT TIME, unless a time argument has been provided
    # TODO: FIXME: If this is a multi-day event, we need to consider both eventdate and eventtime
    eventTimes = getEventTimes(eventID)
    if (eventTimes != None):
        startTime, endTime = eventTimes[0], eventTimes[1]
        if (endTime != None):
            if (datetime.now().time() > endTime):
                return "Event closed already"
        elif (startTime != None):
            if (datetime.now().time() < startTime):
                return "Event hasn't started yet"
    try:
        curs.execute("INSERT INTO participation(points, isArcMember, zid, eventID, time) VALUES ((%s), (%s), (%s), (%s), (%s))", (1, isArc, zID, eventID, datetime.now() if time == None else time))
    except Exception as e:
        print(e)
        return "failed"
    conn.commit()
    conn.close()
    return "success"

def changePoints(zID, eventID, newPoints):
    conn = createConnection()
    curs = conn.cursor()
    try:
        curs.execute("update participation set points=(%s) WHERE eventID=(%s) and zid=(%s)", (newPoints, eventID, zID,))
    except Exception as e:
        return "failed"
    conn.commit()
    conn.close()
    return "success"

def deleteUserAttendance(zID, eventID):
    conn = createConnection()
    curs = conn.cursor()
    try:
        curs.execute("DELETE FROM participation WHERE zid=(%s) and eventid=(%s)", (zID, eventID,))
    except Exception as e:
        return "failed"
    conn.commit()
    error = curs.fetchone()
    conn.close()
    if error is not None:
        return "failed"
    return "success"

def checkParticipation(zID, eventID):
    conn = createConnection()
    curs = conn.cursor()
    try:
        curs.execute("SELECT * FROM participation WHERE zid=(%s) and eventid=(%s)", (zID, eventID,))
    except Exception as e:
        return False

    rows = curs.fetchall()
    conn.close()
    return False if rows == [] else True

# Get the attendance information of one particular event
# return a list of attendees in the form of: [(points, isArcMember, name, zid, time), (...)]
# NOTE: isArcMember is bool, 0 == False, 1 == True
# NOTE: Potentially we dont need to return the name of the user here
def getAttendance(eventID):
    if (checkEvent(eventID) == False):
        return "failed"
    conn = createConnection()
    curs = conn.cursor()
    try:
        curs.execute("SELECT name, eventdate, location, societyname, societyID FROM hostedEvents where eventID = (%s);", (eventID,))
    except Exception as e:
        conn.close()
        return "failed"
    results = curs.fetchone()
    if (results is None):
        return "failed"
    payload = {}
    payload['eventName'] = results[0]
    payload['eventDate'] = str(results[1])
    payload['location'] = results[2]
    payload['societyName'] = results[3]
    payload['societyID'] = results[4]
    payload['attendance'] = []
    try:
        curs.execute("SELECT points, isArcMember, users.name, users.zID, participation.time FROM PARTICIPATION JOIN EVENTS ON (participation.eventID = events.eventID) JOIN USERS ON (PARTICIPATION.ZID = USERS.zID) WHERE events.eventID = (%s);", (eventID,))
    except Exception as e:
        conn.close()
        return "failed"
    results = curs.fetchall()
    if results == []:
        return payload
    for result in results:
        personJSON = {}
        personJSON['points'] = result[0]
        personJSON['isArcMember'] = result[1]
        personJSON['userName'] = result[2]
        personJSON['zID'] = result[3]
        personJSON['attendanceTime'] = result[4]
        payload['attendance'].append(personJSON)
    return payload

def getAttendanceCSV(eventID):
    if (checkEvent(eventID) == False):
        return "failed"
    conn = createConnection()
    curs = conn.cursor()
    try:
        curs.execute("SELECT isArcMember, users.zID, users.firstName, users.lastName, time FROM PARTICIPATION JOIN EVENTS ON (participation.eventID = events.eventID) JOIN USERS ON (PARTICIPATION.ZID = USERS.zID) WHERE events.eventID = (%s);", (eventID,))
    except Exception as e:
        return "failed"
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

def getUpcomingEvents(zID):
    conn = createConnection()
    curs = conn.cursor()
    results = getUserSocieties(zID)

    payload = []
    if results == []:
        conn.close()
        return payload

    today = str(datetime.now().date())
    for soc in results:
        curs.execute("SELECT eventid, name, eventdate, location FROM hostedEvents WHERE societyid = (%s) AND eventDate > (%s);", (soc['societyID'], today,))
        result = curs.fetchall()

        if result == []:
            continue

        for i in result:
            eventJSON = {}
            eventJSON['eventID'] = i[0]
            eventJSON['name'] = i[1]
            eventJSON['eventDate'] = i[2]
            eventJSON['location'] = i[3]
            eventJSON['societyID'] = soc['societyID']
            eventJSON['societyName'] = soc['societyName']
            payload.append(eventJSON)
    
    return payload

def getUserSocieties(zID):
    conn = createConnection()
    curs = conn.cursor()
    try:
        curs.execute("SELECT societyID, societyName FROM userInSociety where zID = (%s) and role = 0;", (zID,))
    except Exception as e:
        #print(e)
        return "failed"
    results = curs.fetchall()

    payload = []
    for society in results:
        societyJSON = {}
        societyJSON['societyID'] = society[0]
        societyJSON['societyName'] = society[1]
        payload.append(societyJSON)

    return payload

# TODO: Average Monthly/Weekly Attendance info (for recurring events)

# TODO: Average Monthly/Weekly Attendance info (for one society)
# NOTE: Accept two arguments, dataType must be in ['week', 'month'], inputting either will display the results of the calendar year 2020
def averageAttendance(dateType, socID):
    conn = createConnection()
    curs = conn.cursor()

    payload = {}
    for i in range(0, len(weekDate) - 1):
        curs.execute("SELECT * FROM events JOIN host ON (host.eventID = events.eventID) WHERE eventDate > (%s) and eventDate < (%s) and society = (%s);", (weekDate[f'T1W{str(i)}'], weekDate[f'T1W{str(i + 1)}'], socID,))
        #conn.commit()
        results = curs.fetchall()
        currPayload = []
        for event in results:
            eventJSON = {}
            eventJSON['eventID'] = event[0]
            eventJSON['name'] = event[1]
            eventJSON['date'] = str(event[2])

            # TODO: Change this to average
            curs.execute("SELECT count(*) AS count FROM participation WHERE eventID = (%s);", (event[0],))
            eventJSON['attendance'] = curs.fetchone()[0]

            currPayload.append(eventJSON)
        if currPayload != []:
            payload[f'T1W{str(i)}'] = currPayload
    conn.close()
    return payload
    
# TODO: Average Monthly/Weekly Attendance info (for one user)
def main():
    print(averageAttendance('week', '74DF2'))

if __name__ == '__main__':
    main()