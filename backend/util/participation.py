# Comment out the two lines below in production
import sys
sys.path.append('../')
FROM util.utilFunctions import createConnection, checkUser, checkEvent
FROM datetime import datetime
FROM dateutil.relativedelta import relativedelta

week = datetime.strptime('2020-02-17', "%Y-%m-%d").date()
#end = datetime.strptime('2021-01-01', "%Y-%m-%d").date()
weekDate = {}
for counter in range(0, 12):
    weekDate[f'T1W{str(counter)}'] = str(week)
    week += relativedelta(days=7)

# TODO: CHANGE THIS FUNCTION TO REFLECT ON THE CHANGE IN THE EVENT TABLE
def register(zID, eventID, isArc = False):
    if (checkUser(zID) == False):
        createUser(zID, userName)

    if checkEvent(eventID) == False:
        return "Event does not exist"

    if checkParticipation(zID, eventID) == True:
        return "Already registered"

    conn = createConnection()
    curs = conn.cursor()
    curs.execute("INSERT INTO participation(points, isArcMember, zid, eventID) VALUES ((%s), (%s), (%s), (%s))", (1, isArc, zID, eventID,))
    conn.commit()
    conn.close()
    return "success"

def changePoints(zID, eventID, newPoints):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("update participation set points=(%s) WHERE eventID=(%s) and zid=(%s)", (newPoints, eventID, zID,))
    conn.commit()
    error = curs.fetchone()
    conn.close()
    if error == []:
        return "failed"
    return "success"

def DELETEUserAttendance(zID, eventID):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("DELETE FROM participation WHERE zid=(%s) and eventid=(%s)", (zID, eventID,))
    conn.commit()
    error = curs.fetchone()
    conn.close()
    if error == []:
        return "failed"
    return "success"

def checkParticipation(zID, eventID):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("SELECT * FROM participation WHERE zid=(%s) and eventid=(%s)", (zID, eventID,))

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
    curs.execute("SELECT points, isArcMember, users.name, users.zid, qrcode FROM participation JOIN (SELECT * FROM events) AS events ON (participation.eventid = events.eventid) JOIN (SELECT * FROM users) AS users ON (participation.zid = users.zid) WHERE events.eventID = (%s);", (eventID,))
    result = curs.fetchall()

    curs.execute("SELECT name FROM events WHERE eventid = (%s);", (eventID,))
    name = curs.fetchone()

    conn.close()
    return result, name

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