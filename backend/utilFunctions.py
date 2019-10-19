from sqlite3 import Error
import sqlite3

def createConnection():
    conn = None
    try:
        conn = sqlite3.connect(r'./database.db')
    except Error as e:
        print(e)
    return conn

# Check if a user exists in the table
def checkUser(zID):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select * from users where zid=?", (zID,))
    
    rows = curs.fetchall()
    return False if rows == [] else True

def checkParticipation(zID, eventID):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select * from participation where user=? and eventid=?", (zID, eventID,))
    
    rows = curs.fetchall()
    return False if rows == [] else True

# Check if an event exists in the table
def checkEvent(eventID):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select * from events where eventid=?", (eventID,))

    rows = curs.fetchall()
    return False if rows == [] else True

# Creating a user 
def createUser(zID, name):
    if (checkUser(zID) != False):
        return "Failed"

    conn = createConnection()
    curs = conn.cursor()
    curs.execute("insert into users(zid, name) values(?, ?);", (zID, name,))
    conn.commit()
    return "Success"

# Creting an event
# Event could maybe have a weight
def createEvent(zID, eventID, eventName, eventDate):
    # FIXME
    if (checkUser(zID) == False):
        createUser(zID, "Junyang Sim")

    if (checkEvent(eventID) != False):
        return "Event does not exist"
    
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("insert into events(eventID, name, society, owner, eventDate) values (?, ?, ?, ?, ?);", (eventID, eventName, "UNSW Hall", zID, eventDate,))
    conn.commit()
    return "success"

def fetchUserStatistics():
    # We fetch everything from the participation relationship
    return 1

def register(zID, eventID):
    if (checkUser(zID) == False or checkEvent(eventID) == False):
        return "User or Event does not exist"

    if (checkParticipation(zID, eventID) == True):
        return "Already registered"

    conn = createConnection()
    curs = conn.cursor()
    curs.execute("insert into participation(points, user, eventID) values (?, ?, ?)", (1, zID, eventID,))
    conn.commit()

def getAttendance(eventID):
    if (checkEvent(eventID) == False):
        return "failed"
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select * from events where eventid=?", (eventID,))
    conn.commit()
    eventInformation = curs.fetchone()
    # Need to return eventName
    eventName = eventInformation[1]

    curs.execute("select user from participation where eventid=?", (eventID,))
    attendees = []
    rows = curs.fetchall()
    for row in rows:
        attendees.append(row[0])

    participation = []
    for person in attendees:
        curs.execute("select * from users where zid=?", (person,))
        rows = curs.fetchall()
        participation.append([rows, 1])

    return participation, eventName

def getUserAttendance(zid):
    if (checkUser(zid) == False):
        return "invalid user"
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select * from users where zid=?", (zid,))
    conn.commit()
    userInformation = curs.fetchone()
    # Need to return userName
    userName = userInformation[1]

    curs.execute("select eventID from participation where user=?", (zid,))
    conn.commit()
    events = curs.fetchall()
    events_output = []
    for event in events:
        #events_output.append(event[0])
        eventNum = event[0]
        curs.execute("select * from events where eventID=?", (eventNum,))
        conn.commit()
        events_info = curs.fetchall()
        events_output.append(events_info)
        
    return events_output

def main():
    createUser("z5161616", "Steven Shen")
    createUser("z5161798", "Casey Neistat")
    createEvent("z5161616", "1239", "Test Event 0", "2019-11-19")
    register("z5161616", "1239")
    register("z5161798", "1239")
    print(getAttendance("1239"))
    print(getUserAttendance("z5161616"))

if __name__ == '__main__':
    main()