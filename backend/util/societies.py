from util.utilFunctions import checkUser, makeConnection, callQuery
from util.files import uploadImages
import random
import string
from json import dumps
import base64

def generateID(number):
    id = ""
    for x in range(0, number):
        id += random.choice(string.hexdigits)
    return id

@makeConnection
def findSocID(socName, conn, curs):
    results = callQuery("SELECT societyID FROM society WHERE societyName = (%s);", conn, curs, (socName,))
    if (results == False): return "failed"
    societyID = curs.fetchone()[0]

    conn.close()
    return societyID

@makeConnection
def createSocStaff(zID, societyID, role = 0, conn = None, curs = None):
    if (zID == None or societyID == None):
        return "failed, insufficient inputs"
    results = callQuery("INSERT INTO socstaff(society, zid, role) VALUES ((%s), (%s), (%s));", conn, curs, (societyID, zID, role,))
    if (results == False): return "failed"
    conn.commit()
    conn.close()
    return "success"

@makeConnection
def createSociety(zID = None, societyName = None, isCollege = False, file = None, conn = None, curs = None):
    societyID = generateID(5).upper()
    results = callQuery("SELECT * FROM society WHERE societyName = (%s);", conn, curs, (societyName,))
    if (results == False): return "failed"
    result = curs.fetchone()
    if (result != None):
        conn.close()
        return "exists already"

    if (file):
        uploadResult = uploadImages(file, societyID)
        if (isinstance(uploadResult, tuple) == False):
            return "bad file name"
        fileJSON = dumps({"logo": uploadResult[0]})
        results = callQuery("INSERT INTO society(societyID, societyName, isCollege, additionalInfomation) VALUES ((%s), (%s), (%s), (%s));", conn, curs, (societyID, societyName, isCollege, fileJSON, ))
    else:
        results = callQuery("INSERT INTO society(societyID, societyName, isCollege) VALUES ((%s), (%s), (%s));", conn, curs, (societyID, societyName, isCollege, ))

    if (results == False): return "failed"
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
    return societyID, 0

@makeConnection
def isCollege(societyID, conn, curs):
    results = callQuery("SELECT isCollege FROM society WHERE societyID = (%s);", conn, curs, (societyID,))
    if (results == False): return "failed"
    result = curs.fetchone()
    conn.close()
    return False if result is None or result[0] == False else True

@makeConnection
def joinCollege(zID, societyID, floorGroup, conn, curs):
    results = callQuery("INSERT INTO collegeUsers(societyID, zID, floorGroup) VALUES ((%s), (%s), (%s));", conn, curs, (societyID, zID, floorGroup))
    if (results == False): return "failed"
    conn.commit()
    conn.close()
    return "success"


# Default join soc option
@makeConnection
def registerToSoc(zID, societyID, conn, curs):
    results = callQuery("INSERT INTO socStaff(society, zid, role) VALUES (%s, %s, %s);", conn, curs, (societyID, zID, 0))
    if (results == False): return "failed"
    conn.commit()
    conn.close()

@makeConnection
def changeRole(zID, societyID, role, conn, curs):
    results = callQuery("update socstaff set role = (%s) WHERE society = (%s) and zid = (%s);", conn, curs, (role, societyID, zID,))
    if (results == False): return "failed"
    conn.commit()
    conn.close()
    return "success"

# BELOW ARE ALL THE QUERY FUNCTIONS
# Get all the events hosted by a society
@makeConnection
def getEventForSoc(societyID, conn, curs):
    # 9/1/2020: TODO: Flask routing for this function
    results = callQuery("SELECT societyName FROM society WHERE societyID = (%s);", conn, curs, (societyID,))
    if (results == False): return None
    name = curs.fetchone()
    if (name == None):
        conn.close()
        return "No such society"

    results = callQuery("SELECT events.eventID, name, eventDate, location, society FROM events join host on events.eventID = host.eventID and society = (%s);", conn, curs, (societyID,)) 
    if (results == False): return None
    events = curs.fetchall()

    payload = []
    for event in events:
        eventJSON = {}
        eventJSON['eventID'] = event[0]
        eventJSON['name'] = event[1]
        eventJSON['eventDate'] = str(event[2])
        eventJSON['location'] = event[3]
        eventJSON['societyID'] = societyID
        eventJSON['societyName'] = name[0]
        payload.append(eventJSON)

    conn.close()
    return payload

@makeConnection
def getAllSocs(conn, curs):
    results = callQuery("SELECT societyName, societyID FROM society;", conn, curs)
    if (results == False): return "failed"
    names = curs.fetchall()
    payload = []
    for i in names:
        currSoc = {}
        currSoc['societyID'] = i[1]
        currSoc['societyName'] = i[0]
        payload.append(currSoc)
    conn.close()
    return payload

@makeConnection
def checkAdmin(socID, zID, conn, curs):
    results = callQuery("SELECT * FROM userInSociety WHERE ZID = (%s) AND role = 1 AND societyID = (%s);", conn, curs, (zID, socID,))
    if (results == False): return False
    results = curs.fetchone()
    if (results is None): return False
    conn.close()
    return True

# Make this zID the admin of EVERY SOC IN OUR DB
@makeConnection
def makeSuperAdmin(zID, conn, curs):
    if (checkUser(zID) == False):
        return "no such user"

    allSocs = getAllSocs()
    for result in allSocs:
        results = callQuery("INSERT INTO SOCSTAFF(society, zid, role) VALUES ((%s), (%s), (%s));", conn, curs, (result['societyID'], zID, 5))
        if (results == False): return "failed"

    conn.commit()
    conn.close()
    return "success"

# Making this particular zID into a normal member
@makeConnection
def joinSoc(zID, socID, conn, curs):
    results = callQuery("SELECT * FROM socStaff WHERE society = (%s) and zID = (%s);", conn, curs, (socID, zID,))

    if (results == False): return "failed"
    result = curs.fetchone()
    if result is not None:
        return "Already registered"

    results = callQuery("INSERT INTO SOCSTAFF(society, zid, role) VALUES ((%s), (%s), (%s));", conn, curs, (socID, zID, 0,))
    if (results == False): return "failed"

    conn.commit()
    conn.close()
    return "success"

# Base user: socStaff -> Role -> 0, admin 1
@makeConnection
def makeAdmin(zID, socID, conn, curs):
    results = callQuery("SELECT * FROM SOCSTAFF WHERE zID = (%s) AND society = (%s);", conn, curs, (zID, socID,))
    if (results == False): return "failed"
    result = curs.fetchone()
    if (result is not None):
        results = callQuery("UPDATE SOCSTAFF SET ROLE = 1 WHERE zID = (%s) AND society = (%s);", conn, curs, (zID, socID,))
        if (results == False): return "failed"

        conn.commit()
    else:
        results = callQuery("INSERT INTO SOCSTAFF(society, zid, role) VALUES ((%s), (%s), (%s));", conn, curs, (socID, zID, 1,))
        if (results == False): return "failed"

        conn.commit()

    conn.close()
    return "success"

# Check if a user is in a society, return True/False
@makeConnection
def checkUserInSoc(zID, socID, conn, curs):

    results = callQuery("SELECT * FROM SOCSTAFF WHERE society = (%s) and zid = (%s);", conn, curs, (socID, zID,))
    if (results == False): return False

    results = curs.fetchone()
    conn.close()
    return False if results is None else True

# NOTE: Accepts a socID and a userType, returns a list of users or admins, accepts ["admin", "user"]
@makeConnection
def getAdminsForSoc(socID, userType = "admin", conn = None, curs = None):
    if (userType == "admin"):
        userType = 1
    else:
        userType = 0

    results = callQuery("SELECT * FROM SOCSTAFF WHERE society = (%s) and role >= (%s) and role < 5;", conn, curs, (socID, userType,))
    if (results == False): return "failed"

    payload = {}
    for result in curs.fetchall():
        payload[result[1]] = "admin" if result[2] == 1 else "basic"
    
    conn.close()
    return payload

# Returns either None (in case event doesn't exist), "Failed"(in case anything's fucked with the table) or socID(on success)
@makeConnection
def getSocIDFromEventID(eventID, conn, curs):
    results = callQuery("SELECT society FROM host WHERE eventID = (%s);", conn, curs, ((eventID,)))
    if (results == False): return "Failed"

    results = curs.fetchone()
    conn.close()
    return None if results is None else results[0]

# NOTE: This is a superAdmin related function, this should ONLY be used in the backend
@makeConnection
def getSuperAdmins(conn, curs):
    results = callQuery("SELECT zID FROM USERS WHERE isSuperAdmin = True;", conn, curs)
    if (results == False): return None
    
    results = curs.fetchall()
    conn.close()
    return results

# Function checks if a society has provided a logo or not, if exists return the file path, else False
@makeConnection
def checkLogo(socID, conn, curs):
    queryResult = callQuery("SELECT additionalinfomation FROM society WHERE societyid = (%s);", conn, curs, (socID,))
    if (queryResult == False): return False

    results = curs.fetchone()
    conn.close()
    if results == None: return False
    elif 'logo' not in results[0]: return False
    return results[0]['logo']

# Returns a base64 encoded string of the logo image
@makeConnection
def getSocLogo(socID, conn, curs):
    logoPath = checkLogo(socID)
    if (logoPath == False): return None

    try:
        with open(logoPath, "rb") as image:
            imageString = base64.b64encode(image.read())
    except IOError as e:
        # TODO: If this occurs, set the logo path to Null in the db
        return "File has been moved on the server, no longer avaliable"
    except Exception as e:
        return str(e)
    return logoPath, 0

@makeConnection
def updateLogo(socID, file, conn, curs):
    uploadResult = uploadImages(file, socID)
    if (isinstance(uploadResult, tuple) == False):
        return "bad file name"
    fileJSON = dumps({"logo": uploadResult[0]})
    results = callQuery("UPDATE society SET additionalInfomation = (%s) WHERE societyID = (%s);", conn, curs, (fileJSON, socID,))
    if (results == False): return "Database fault, check backend log"

    return "success"
