from sqlite3 import Error
import init
import sqlite3
import hashlib

def createConnection():
    conn = None
    try:
        conn = sqlite3.connect(r'./database.db')
    except Error as e:
        print(e)
    return conn

# 8/1/2020: FIXME: Think about refactoring the five check functions below, too many duplicated code

# Check if a user exists in the table
def checkUser(zID):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select * from users where zid=?", (zID,))

    rows = curs.fetchall()
    conn.close()
    return False if rows == [] else True

def checkParticipation(zID, eventID):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select * from participation where user=? and eventid=?", (zID, eventID,))

    rows = curs.fetchall()
    conn.close()
    return False if rows == [] else True

# Check if an event exists in the table
def checkEvent(eventID):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select * from events where eventid=?", (eventID,))

    rows = curs.fetchall()
    conn.close()
    return False if rows == [] else True

# Check if a specified society already exists
def checkSoc(societyID):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select * from society where societyID = ?", (societyID,))

    rows = curs.fetchall()
    conn.close()
    return False if rows == [] else True

# Creating a user 
# 8/1/2020: TODO: To implement the login system, we need to store hashed passwords
def createUser(zID, name, password):
    if (checkUser(zID) != False):
        return "Failed"
    # FIXME: Perhaps, we should receive password hashed already from the frontend
    password = str(password).encode()
    pwHash = hashlib.sha256(password).hexdigest()

    conn = createConnection()
    curs = conn.cursor()
    curs.execute("insert into users(zid, name, password) values(?, ?, ?);", (zID, name, pwHash))
    conn.commit()
    conn.close()
    return "Success"

# Creting an event
# Event could maybe have a weight
def createEvent(zID, eventID, eventName, eventDate, qrFlag, societyID = None):
    # FIXME
    if (checkUser(zID) == False):
        createUser(zID, "Junyang Sim")

    if (checkEvent(eventID) != False):
        return "failed"
    elif (societyID == None):
        societyID = findSocID("UNSW Hall")
    
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("insert into events(eventID, name, owner, eventDate, qrCode) values (?, ?, ?, ?, ?);", (eventID, eventName, zID, eventDate, qrFlag))

    # Currently, location defaults to UNSW Hall
    curs.execute("insert into host(location, society, eventID) values (?, ?, ?);", ("UNSW Hall", societyID, eventID,))
    conn.commit()
    conn.close()
    return "success"

def findSocID(socName):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select societyID from society where societyName = ?;", (socName,))
    societyID = curs.fetchone()[0]

    return societyID

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
    eventQR = eventInformation[5]

    curs.execute("select user, points from participation where eventid=?", (eventID,))
    attendees = []
    rows = curs.fetchall()
    for row in rows:
        attendees.append([row[0], row[1]])

    participation = []
    for person in attendees:
        curs.execute("select * from users where zid=?", (person[0],))
        rows = curs.fetchall()
        participation.append([rows, person[1]])

    conn.close()
    return participation, eventName, eventQR

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

    curs.execute("select eventID, points from participation where user=?", (zid,))
    conn.commit()
    events = curs.fetchall()
    events_output = []
    for event in events:
        eventNum = event[0]
        curs.execute("select * from events where eventID=?", (eventNum,))
        conn.commit()
        events_info = curs.fetchall()
        #add points
        events_info.append(event[1])
        events_output.append(events_info)
        
    conn.close()
    return events_output, userName

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

# 20/12/2019: TODO Fix functions here that correspond to the changes being made to the database, add functions for the new tables


# Get all the events hosted by a society
def getEventForSoc(societyID):
    # 9/1/2020: TODO: Flask routing for this function
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select * from events join host on events.eventID = host.eventID and society = ?;", (societyID,))
    events = curs.fetchall()
    return events

# Get all the events in a society attended by a particular person
def getPersonEventsForSoc(zID, societyID):
    # TODO:
    return -1

def createSocStaff(zID, societyID, role = None):
    if (zID == None or societyID == None):
        return "failed, insufficient inputs"
    # TODO: Check for society and zID existance
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("insert into socstaff(society, zid, role) values (?, ?, ?);", (societyID, zID, role,))
    conn.commit()
    conn.close()
    return "success"

def createSociety(zID = None, societyName = None):
    # 20/19/2019: FIXME Change the function below to the UUID generator
    societyID = init.generateID(5).upper()
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("insert into society(societyID, societyName) values (?, ?);", (societyID, societyName,))
    conn.commit()
    conn.close()

    # If we didn't specify a staff when creating the soc
    if (zID == None):
        return "success"

    # Otherwise, we add a staff with the job title of "President"
    response = createSocStaff(zID, societyID, "President")
    return response

def changeRole(zID, societyID, role):
    conn = createConnection()
    curs = conn.cusor()
    try:
        curs.execute("update socstaff set role = ? where society = ? and zid = ?", (role, societyID, zID,))
        conn.commit()
        conn.close()
    except Error as e:
        return "failed"
    return "success"


def main():
    # Moving this section to init.py in the next patch lmao
    # add users
    # 8/1/2020: FIXME: Add some passwords to the accounts
    createUser("z5161616", "Steven Shen", "123456")
    createUser("z5161798", "Casey Neistat", "123456")
    createUser("z5111111", "Harrison Steyn", "123456")
    createUser("z5222222", "JunYang Sim", "123456")
    createUser("z5333333", "Ivan Velickovic", "123456")
    createUser("z5444444", "Oltan Sevinc", "123456")
    createUser("z5555555", "Will de Dassel", "123456")

    # TODO: Add some dummy societies and then fix the below add events dummy functions
    # NOTE: Might not be needed since the current version focuses on implementation just for Hall
    #add societies
    createSociety("z5111111", "CSESoc")
    createSociety("z5123123", "Manchester United FC")
    createSociety("z5555555", "UNSW Hall")

    # NOTE: Defaults to UNSW Hall (for the society field right now)
    #add events
    createEvent("z5161616", "1239", "Hackathon", "2019-11-19", True)
    createEvent("z5333333", "0000", "Gamer Juice Winery Tour", "2019-09-09", True)
    createEvent("z5555555", "1234", "Coffee Night", "2019-10-16", True)
    createEvent("z5111111", "4231", "LoL Appreciation", "2019-09-08", True)

    # register users:
    #   for Hackathon
    register("z5161616", "1239", 'Steven')
    register("z5161798", "1239", 'Casey Neistat')
    #   for Gamer Juice Winery Tour
    register("z5333333", "0000", 'Ivan Velickovic')
    register("z5161798", "0000", 'Casey Neistat')
    register("z5161616", "0000", 'Stevn')
    #   for Coffee Night
    register("z5161616", "1234", 'Steven')
    register("z5161798", "1234", 'Casey Neistat')
    register("z5111111", "1234", 'Harrison Steyn')
    register("z5222222", "1234", 'Junyang Sim')
    register("z5333333", "1234", 'Ivan Velickovic')
    register("z5444444", "1234", 'Oltan Sevinc')
    register("z5555555", "1234", 'Will de Dassel')

    getEventForSoc(findSocID("UNSW Hall"))
    # print(getAttendance("1234"))
    # print(getUserAttendance("z5161616"))

if __name__ == '__main__':
    main()
