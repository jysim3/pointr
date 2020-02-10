from util.utilFunctions import checkUser, createConnection
import hashlib

# Creating a user 
# 8/1/2020: TODO: To implement the login system, we need to store hashed passwords
def createUser(zID, name, password, role = None):
    if (checkUser(zID) != False):
        return "Failed"
    # FIXME: Perhaps, we should receive password hashed already from the frontend
    password = str(password).encode()
    pwHash = hashlib.sha256(password).hexdigest()

    conn = createConnection()
    curs = conn.cursor()
    curs.execute("insert into users(zid, name, password) values((%s), (%s), (%s));", (zID, name, pwHash,))
    conn.commit()
    conn.close()
    return "Success"

# return a list of events in the form of: [(points, eventID, eventName, date, societyName), (...)]
# Get all the events attended by the user ever in every society
def getUserAttendance(zid):
    if (checkUser(zid) == False):
        return "invalid user"
    conn = createConnection()
    curs = conn.cursor()

    curs.execute("select points, events.eventID, events.name, eventdate, societyName from participation join events join host join society on society = society.societyid and participation.eventID = events.eventID and host.eventID = events.eventid and user = (%s);", (zid,))
    results = curs.fetchall()

    curs.execute("select name from users where users.zid = (%s);", (zid,))
    name = curs.fetchone()

    conn.close()
    return results, name

# Get all the events in a society attended by a particular person
def getPersonEventsForSoc(zID, societyID):
    # 9/1/2020: TODO: Flask routing for this function
    # 9/1/2020: FIXME: Change the line below to select only the stuff that's required
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select name from users where zid = (%s);", (zID,))
    name = curs.fetchone()
    if (name is None):
        return "No such user"

    curs.execute("select societyName from society where societyID = (%s);", (societyID,))
    socName = curs.fetchone()
    if (socName is None):
        return None

    curs.execute("select * from events join host join participation on events.eventID = host.eventID and events.eventID = participation.eventID and society = (%s) and participation.zid = (%s);", (societyID, zID,))
    events = curs.fetchall()
    conn.close()
    return events, name[0], socName[0]
