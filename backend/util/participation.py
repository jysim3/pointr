from util.utilFunctions import createConnection, checkUser, checkEvent
from datetime import datetime
from dateutil.relativedelta import relativedelta

# TODO: CHANGE THIS FUNCTION TO REFLECT ON THE CHANGE IN THE EVENT TABLE
def register(zID, eventID, userName, isArc = False):
    if (checkUser(zID) == False):
        createUser(zID, userName)

    if checkEvent(eventID) == False:
        return "Event does not exist"

    if checkParticipation(zID, eventID) == True:
        return "Already registered"

    conn = createConnection()
    curs = conn.cursor()
    curs.execute("insert into participation(points, isArcMember, user, eventID) values (?, ?, ?, ?)", (1, isArc, zID, eventID,))
    conn.commit()
    conn.close()
    return "success"

def changePoints(zID, eventID, newPoints):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("update participation set points=? where eventID=? and user=?", (newPoints, eventID, zID,))
    conn.commit()
    error = curs.fetchone()
    conn.close()
    if error == []:
        return "failed"
    return "success"

def deleteUserAttendance(zID, eventID):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("delete from participation where user=? and eventid=?", (zID, eventID,))
    conn.commit()
    error = curs.fetchone()
    conn.close()
    if error == []:
        return "failed"
    return "success"

def checkParticipation(zID, eventID):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select * from participation where user=? and eventid=?", (zID, eventID,))

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
    curs.execute("select points, isArcMember, users.name, users.zid, qrcode from participation join events join users where participation.eventid = events.eventid and participation.user = users.zid and events.eventID = ?;", (eventID,))
    result = curs.fetchall()

    curs.execute("select name from events where eventid = ?;", (eventID,))
    name = curs.fetchone()

    conn.close()
    return result, name


def getRecurStat (timeInterval, eventID):
    # TODO:
    return 0


# TODO: Average Monthly/Weekly Attendance info (for recurring events)
# TODO: Average Monthly/Weekly Attendance info (for one society)
# TODO: Average Monthly/Weekly Attendance info (for one user)