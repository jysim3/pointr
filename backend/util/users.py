from util.utilFunctions import checkUser, createConnection
import hashlib

# Creating a user 
# 8/1/2020: TODO: To implement the login system, we need to store hashed passwords
def createUser(zID, name, password, isArc = True):
    if (checkUser(zID) != False):
        return "Failed"
    password = str(password).encode('UTF-8')
    pwHash = hashlib.sha256(password).hexdigest()

    conn = createConnection()
    curs = conn.cursor()
    try:
        curs.execute("INSERT INTO users(zid, name, password, isArc, activationStatus) values((%s), (%s), (%s), (%s), False);", (zID, name, pwHash, isArc,))
    except Exception as e:
        print(e)
        return "Failed"
    conn.commit()
    conn.close()
    return "Success"

def getUserInfo(zID):
    conn = createConnection()
    curs = conn.cursor()
    try:
        curs.execute("SELECT name FROM users WHERE zID = (%s);", (zID,))
    except Exception as e:
        conn.close()
        return "failed"
    name = curs.fetchone()[0]
    try:
        curs.execute("SELECT * FROM userParticipatedEvents WHERE zID = (%s);", (zID,))
    except Exception as e:
        conn.close()
        return "failed"
    results = curs.fetchall()
    payload = {}
    payload['name'] = name
    payload['events'] = []
    for result in results:
        eventJSON = {}
        eventJSON['eventID'] = result[0]
        eventJSON['name'] = result[1]
        eventJSON['eventDate'] = result[2]
        eventJSON['location'] = result[3]
        eventJSON['societyName'] = result[4]
        eventJSON['societyID'] = result[5]
        payload['events'].append(eventJSON)
    return payload

def checkUserInfo(zID, password):
    password = hashlib.sha256(password.encode(encoding="utf-8")).hexdigest()

    conn = createConnection()
    curs = conn.cursor()
    curs.execute("SELECT * FROM users where zid = (%s) AND password = (%s);", (zID, password,))
    result = curs.fetchone()
    return False if result is None else True

# return a list of events in the form of: [(points, eventID, eventName, date, societyName), (...)]
# Get all the events attended by the user ever in every society
def getUserAttendance(zid):
    if (checkUser(zid) == False):
        return {"status": "Failed"}
    conn = createConnection()
    curs = conn.cursor()

    curs.execute("select points, events.eventid, name, eventdate, isarcmember, societyName from events join participation on (events.eventid = participation.eventid) join host on (events.eventid = host.eventid) join society on (society.societyID = host.society) where participation.zid = (%s);", (zid,))
    results = curs.fetchall()

    curs.execute("select name from users where users.zid = (%s);", (zid,))
    name = curs.fetchone()[0]

    conn.close()

    payload = {}
    payload['events'] = []
    payload['zID'] = zid.lower()
    payload['name'] = name
    for event in results:
        eventJSON = {}
        eventJSON['eventID'] = event[1]
        eventJSON['name'] = event[2]
        eventJSON['society'] = event[5]
        eventJSON['eventDate'] = str(event[3])
        eventJSON['points'] = event[0]
        eventJSON['isArc'] = event[4]
        payload['events'].append(eventJSON)
    

    return payload

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

    try:
        curs.execute("select societyName from society where societyID = (%s);", (societyID,))
    except Exception as e:
        conn.close()
        return "failed"
    socName = curs.fetchone()
    if (socName is None):
        return None

    try:
        curs.execute("select * from events join host on (events.eventID = host.eventID) join participation on (events.eventID = participation.eventID) where society = (%s) and participation.zid = (%s);", (societyID, zID,))
    except Exception as e:
        conn.close()
        return "failed"
    events = curs.fetchall()
    conn.close()

    payload = {}
    payload['userName'] = name
    payload['societyName'] = socName
    payload['events'] = []
    for event in events:
        eventJSON = {}
        eventJSON['eventID'] = event[0]
        eventJSON['name'] = event[1]
        eventJSON['society'] = event[3]
        eventJSON['eventDate'] = str(event[2])
        eventJSON['points'] = event[4]
        payload['events'].append(eventJSON)
    return payload

def checkArc(zID):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("SELECT isArc FROM USERS WHERE zid = (%s);", (zID,))
    name = curs.fetchone()
    return True if name != [] else False

def addActivationLink(zID, activationLink):
    conn = createConnection()
    curs = conn.cursor()
    try:
        curs.execute("UPDATE users SET activationLink = (%s) WHERE zID = (%s);", (activationLink, zID,))
        conn.commit()
    except Exception as e:
        conn.close()
        return "failed"
    return "success"

def activateAccount(zID):
    conn = createConnection()
    curs = conn.cursor()
    try:
        curs.execute("UPDATE users SET activationStatus = True WHERE zID = (%s);", (zID,))
    except Exception as e:
        return "failed"
    conn.commit()
    return "success"