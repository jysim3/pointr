# Comment out the two lines below in production
import sys
sys.path.append('../')
from util.utilFunctions import createConnection, checkUser, checkEvent
from util.users import checkArc
from util.events import getEndTime
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
    endTime = getEndTime(eventID)
    if (endTime != None):
        if (datetime.now().time() > endTime):
            return "Event closed already"
    try:
        curs.execute("INSERT INTO participation(points, isArcMember, zid, eventID, time) VALUES ((%s), (%s), (%s), (%s), (%s))", (1, isArc, zID, eventID, datetime.now() if time == None else time))
    except Exception as e:
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
    error = curs.fetchone()
    conn.close()
    if error is None:
        return "failed"
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
# return a list of attendees in the form of: [(points, isArcMember, name, zid), (...)]
# NOTE: isArcMember is bool, 0 == False, 1 == True
# NOTE: Potentially we dont need to return the name of the user here
def getAttendance(eventID):
    if (checkEvent(eventID) == False):
        return "failed"
    conn = createConnection()
    curs = conn.cursor()
    try:
        curs.execute("SELECT qrCode FROM events WHERE eventid = (%s);", (eventID,))
    except Exception as e:
        return "failed"
    qrCode = curs.fetchone()
    qrCode = qrCode[0] if qrCode is not None else None
    try:
        curs.execute("SELECT points, isArcMember, users.name, users.zid FROM participation JOIN (SELECT * FROM events) AS events ON (participation.eventid = events.eventid) JOIN (SELECT * FROM users) AS users ON (participation.zid = users.zid) WHERE events.eventID = (%s);", (eventID,))
    except Exception as e:
        return "failed"
    result = curs.fetchall()

    curs.execute("SELECT name FROM events WHERE eventid = (%s);", (eventID,))
    name = curs.fetchone()

    conn.close()
    return result, name, qrCode

def getAttendanceCSV(eventID):
    if (checkEvent(eventID) == False):
        return "failed"
    conn = createConnection()
    curs = conn.cursor()
    try:
        curs.execute("SELECT isArcMember, users.zID, users.name, time FROM PARTICIPATION JOIN EVENTS ON (participation.eventID = events.eventID) JOIN USERS ON (PARTICIPATION.ZID = USERS.zID) WHERE events.eventID = (%s);", (eventID,))
    except Exception as e:
        return "failed"
    results = curs.fetchall()
    if results is None:
        return "No attendance"
    conn.commit()

    import os
    path = os.getcwd()
    path += f'/csvFiles/{eventID}.csv'
    try:
        with open(path, 'w', newline='') as file:
            file.write("isArcMember,zID,name,time\n")
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
    try:
        curs.execute("SELECT * FROM userparticipatedEvents where zID = (%s) order by eventDate;", (zID,))
    except Exception as e:
        return "failed"
    results = curs.fetchall()

    payload = []
    for event in results:
        eventJSON = {}
        eventJSON['eventID'] = event[0]
        eventJSON['name'] = event[1]
        eventJSON['date'] = str(event[2])
        eventJSON['location'] = event[3]
        eventJSON['societyName'] = event[4]
        eventJSON['societyID'] = event[5]

        payload.append(eventJSON)

    return payload

def getUserSocieties(zID):
    conn = createConnection()
    curs = conn.cursor()
    try:
        curs.execute("SELECT * FROM userInSociety where zID = (%s);", (zID,))
    except Exception as e:
        #print(e)
        return "failed"
    results = curs.fetchall()

    payload = []
    for society in results:
        societyJSON = {}
        societyJSON['societID'] = society[0]
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