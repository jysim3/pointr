from util.utilFunctions import checkUser, makeConnection
import random
import string

def generateID(number):
    id = ""
    for x in range(0, number):
        id += random.choice(string.hexdigits)
    return id

@makeConnection
def findSocID(socName, conn, curs):
    try:
        curs.execute("SELECT societyID FROM society WHERE societyName = (%s);", (socName,))
    except Exception as e:
        return "failed"
    societyID = curs.fetchone()[0]

    return societyID

@makeConnection
def createSocStaff(zID, societyID, role = 0, conn = None, curs = None):
    if (zID == None or societyID == None):
        return "failed, insufficient inputs"
    try:
        curs.execute("INSERT INTO socstaff(society, zid, role) VALUES ((%s), (%s), (%s));", (societyID, zID, role,))
    except Exception as e:
        return "failed"
    conn.commit()
    conn.close()
    return "success"

@makeConnection
def createSociety(zID = None, societyName = None, isCollege = False, conn = None, curs = None):
    societyID = generateID(5).upper()
    try:
        curs.execute("SELECT * FROM society WHERE societyName = (%s);", (societyName,))
    except Exception as e:
        return "failed"
    result = curs.fetchone()
    if (result != None):
        conn.close()
        return "exists already"

    try:
        curs.execute("INSERT INTO society(societyID, societyName, isCollege) VALUES ((%s), (%s), (%s));", (societyID, societyName, isCollege,))
    except Exception as e:
        return "failed"
    conn.commit()
    conn.close()

    # If we didn't specify a staff when creating the soc
    if (zID == None):
        return societyID

    # Otherwise, we add a staff with the job title of "President"
    createSocStaff(zID, societyID, 1)
    superAdmins = getSuperAdmins()
    for i in superAdmins:
        createSocStaff(i[0], societyID, 5)
    return societyID

@makeConnection
def isCollege(societyID, conn, curs):
    try:
        curs.execute("SELECT isCollege FROM society WHERE societyID = (%s);", (societyID,))
    except Exception as e:
        return "failed"
    result = curs.fetchone()
    return False if result is None else True

@makeConnection
def joinCollege(zID, societyID, floorGroup, conn, curs):
    try:
        curs.execute("INSERT INTO collegeUsers(societyID, zID, floorGroup) VALUES ((%s), (%s), (%s));", (societyID, zID, floorGroup))
    except Exception as e:
        conn.close()
        return "failed"
    conn.commit()
    conn.close()
    return "success"


@makeConnection
def registerToSoc(zID, societyID, conn, curs):
    try:
        curs.execute("INSERT INTO socStaff(society, zid, role) VALUES (%s, %s, %s);", (societyID, zID, 0))
    except Exception as e:
        return "failed"
    conn.commit()
    conn.close()

@makeConnection
def changeRole(zID, societyID, role, conn, curs):
    try:
        curs.execute("update socstaff set role = (%s) WHERE society = (%s) and zid = (%s);", (role, societyID, zID,))
        conn.commit()
        conn.close()
    except Exception as e:
        return "failed"
    return "success"

# BELOW ARE ALL THE QUERY FUNCTIONS
# Get all the events hosted by a society
@makeConnection
def getEventForSoc(societyID, conn, curs):
    # 9/1/2020: TODO: Flask routing for this function
    try:
        curs.execute("SELECT societyName FROM society WHERE societyID = (%s);", (societyID,))
        name = curs.fetchone()
        if (name == None):
            conn.close()
            return "No such society"

        curs.execute("SELECT events.eventID, name, eventDate, location, society FROM events join host on events.eventID = host.eventID and society = (%s);", (societyID,))
        events = curs.fetchall()
    except Exception as e:
        conn.close()
        return "failed"

    payload = {}
    payload['events'] = []
    payload['societyName'] = name[0]
    for event in events:
        eventJSON = {}
        eventJSON['eventID'] = event[0]
        eventJSON['name'] = event[1]
        eventJSON['society'] = event[3]
        eventJSON['eventDate'] = str(event[2])
        payload['events'].append(eventJSON)

    conn.close()
    return payload

@makeConnection
def getAllSocs(conn, curs):
    try:
        curs.execute("SELECT societyName, societyID FROM society;")
    except Exception as e:
        return "failed"
    names = curs.fetchall()
    payload = []
    for i in names:
        currSoc = {}
        currSoc['societyID'] = i[1]
        currSoc['societyName'] = i[0]
        payload.append(currSoc)
    return payload

@makeConnection
def checkAdmin(socID, zID, conn, curs):
    try:
        curs.execute("SELECT * FROM userInSociety WHERE ZID = (%s) AND role = 1 AND societyID = (%s);", (zID, socID,))
    except Exception as e:
        return False
    results = curs.fetchone()
    if (results is None):
        return False
    return True

# Make this zID the admin of EVERY SOC IN OUR DB
@makeConnection
def makeSuperAdmin(zID, conn, curs):
    if (checkUser(zID) == False):
        return "no such user"

    allSocs = getAllSocs()
    for result in allSocs:
        try:
            curs.execute("INSERT INTO SOCSTAFF(society, zid, role) VALUES ((%s), (%s), (%s));", (result['societyID'], zID, 5))
        except Exception as e:
            conn.commit()
            conn.close()
            return "failed"

    conn.commit()
    return "success"

# Making this particular zID into a normal member
@makeConnection
def joinSoc(zID, socID, conn, curs):
    try:
        curs.execute("SELECT * FROM socStaff WHERE society = (%s) and zID = (%s);", (socID, zID,))
        conn.commit()
    except Exception as e:
        conn.close()
        print(e)
        return "failed"
    result = curs.fetchone()
    if result is not None:
        return "Already registered"

    try:
        curs.execute("INSERT INTO SOCSTAFF(society, zid, role) VALUES ((%s), (%s), (%s));", (socID, zID, 0,))
        conn.commit()
    except Exception as e:
        print(e)
        conn.close()
        return "failed"

    conn.close()
    return "success"

# Base user: socStaff -> Role -> 0, admin 1
@makeConnection
def makeAdmin(zID, socID, conn, curs):
    try:
        curs.execute("SELECT * FROM SOCSTAFF WHERE zID = (%s) AND society = (%s);", (zID, socID,))
    except Exception as e:
        conn.close()
        print(e)
        return "failed"
    result = curs.fetchone()
    if (result is not None):
        try:
            curs.execute("UPDATE SOCSTAFF SET ROLE = 1 WHERE zID = (%s) AND society = (%s);", (zID, socID,))
            conn.commit()
        except Exception as e:
            print(e)
            conn.close()
            return "failed"
    else:
        try:
            curs.execute("INSERT INTO SOCSTAFF(society, zid, role) VALUES ((%s), (%s), (%s));", (socID, zID, 1,))
            conn.commit()
        except Exception as e:
            conn.close()
            print(e)
            return "failed"

    conn.close()
    return "success"

# Check if a user is in a society, return True/False
@makeConnection
def checkUserInSoc(zID, socID, conn, curs):

    try:
        curs.execute("SELECT * FROM SOCSTAFF WHERE society = (%s) and zid = (%s);", (socID, zID,))
    except Exception as e:
        conn.close()
        return False

    results = curs.fetchone()
    return True if results == [] else False

# NOTE: Accepts a socID and a userType, returns a list of users or admins, accepts ["admin", "user"]
@makeConnection
def getAdminsForSoc(socID, userType = "admin", conn = None, curs = None):
    if (userType == "admin"):
        userType = 1
    else:
        userType = 0

    try:
        curs.execute("SELECT * FROM SOCSTAFF WHERE society = (%s) and role >= (%s) and role < 5;", (socID, userType,))
    except Exception as e:
        print(e)
        conn.close()
        return "failed"

    payload = {}
    for result in curs.fetchall():
        payload[result[1]] = "admin" if result[2] == 1 else "basic"
    
    return payload

# Returns either None (in case event doesn't exist), "Failed"(in case anything's fucked with the table) or socID(on success)
@makeConnection
def getSocIDFromEventID(eventID, conn, curs):
    try:
        curs.execute("SELECT society FROM host WHERE eventID = (%s);", ((eventID,)))
    except Exception as e:
        conn.close()
        return "Failed"

    results = curs.fetchone()
    return None if results is None else results[0]

# NOTE: This is a superAdmin related function, this should ONLY be used in the backend
@makeConnection
def getSuperAdmins(conn, curs):
    try:
        curs.execute("SELECT zID FROM USERS WHERE isSuperAdmin = True;")
    except Exception as e:
        return None
    
    results = curs.fetchall()
    return results