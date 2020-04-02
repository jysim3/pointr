from util.utilFunctions import checkUser, makeConnection
from util.societies import makeSuperAdmin
#from util.files import uploadImages
import hashlib
from util.utilFunctions import callQuery
import base64
from util.files import uploadImages
from json import dumps

# Creating a user 
# 8/1/2020: TODO: To implement the login system, we need to store hashed passwords
# if not auth_services.register_user(zID, password, name, isArc, commencementYear, studentType, degreeType):

# Potential returns:
# 1. "Failed" on any psql error or if the user exists already
@makeConnection
def createUser(zID, firstName, lastName, password, isArc = True, commencementYear = 2020, studentType = "domestic", degreeType = "undergraduate", isSuperAdmin = False, conn = None, curs = None):
    password = str(password).encode('UTF-8')
    pwHash = hashlib.sha256(password).hexdigest()

    
    queryResults = callQuery("INSERT INTO users(zid, firstName, lastName, password, isArc, commencementYear, studentType, degreeType, isSuperAdmin, activationStatus) values((%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), False);", conn, curs, (zID, firstName, lastName, pwHash, isArc, commencementYear, studentType, degreeType, isSuperAdmin))
    if queryResults == False: return "failed"

    conn.commit()
    conn.close()

    if (isSuperAdmin == True):
        makeSuperAdmin(zID)
    return "success"

@makeConnection
def getUserInfo(zID, conn = None, curs = None):
    
    queryResults = callQuery("SELECT firstName, lastName FROM users WHERE zID = (%s);", conn, curs, (zID,))
    if queryResults == False: return "failed"

    name = curs.fetchone()
    if (name is None):
        return None
    firstName = name[0]
    lastName = name[1]
    
    queryResults = callQuery("SELECT * FROM userParticipatedEvents WHERE zID = (%s) ORDER BY societyID;", conn, curs, (zID,))
    if queryResults == False: return "failed"

    results = curs.fetchall()
    payload = {}
    payload['zID'] = zID
    payload['firstName'] = firstName
    payload['lastName'] = lastName
    payload['societies'] = getInvolvedSocs(zID)
    userImage = checkUserImage(zID)
    payload['image'] = userImage[0] if isinstance(userImage, tuple) == True else ''
    payload['events'] = []
    for result in results:
        eventJSON = {}
        eventJSON['eventID'] = result[0]
        eventJSON['name'] = result[1]
        eventJSON['eventDate'] = str(result[2])
        eventJSON['location'] = result[3]
        eventJSON['societyName'] = result[4]
        eventJSON['societyID'] = result[5]
        payload['events'].append(eventJSON)
    return payload

@makeConnection
def checkUserImage(zID, conn, curs):
    queryResult = callQuery("SELECT additionalinfomation -> 'logo' FROM users WHERE zID = (%s);", conn, curs, (zID,))
    if (queryResult == False): return False

    results = curs.fetchone()
    conn.close()
    return results[0] if results != None else False

@makeConnection
def getUserImage(zID, conn, curs):
    logoPath = checkUserImage(zID)
    if (logoPath == False): return None

    try:
        with open(logoPath, "rb") as image:
            imageString = base64.b64encode(image.read())
    except IOError as e:
        # TODO: If this occurs, set the logo path to Null in the db
        return "File has been moved on the server, no longer avaliable"

    return imageString.decode('utf-8'), 0

@makeConnection
def updateUserImage(zID, file, conn, curs):
    uploadResult = uploadImages(file, zID)
    if (isinstance(uploadResult, tuple) == False):
        return "bad file name"
    fileJSON = dumps({"logo": uploadResult[0]})
    results = callQuery("UPDATE users SET additionalInfomation = (%s) WHERE zID = (%s);", conn, curs, (fileJSON, zID,))
    if (results == False):
        return "Database fault, check backend log"
    return "success"


@makeConnection
def checkUserInfo(zID, password, conn = None, curs = None):
    password = hashlib.sha256(password.encode(encoding="utf-8")).hexdigest()

    queryResults = callQuery("SELECT * FROM users where zid = (%s) AND password = (%s);", conn, curs, (zID, password,))
    if queryResults == False: return False
    
    result = curs.fetchone()
    if result is None:
        return False
    if (checkActivation(zID) == False):
        return False
    queryResults = callQuery("SELECT * FROM socStaff where role = 5 and zID = (%s);", conn, curs, (zID,))
    if queryResults == False: return False

    superAdmins = curs.fetchall()
    if superAdmins == []:
        return 1
    return 5

# return a list of events in the form of: [(points, eventID, eventName, date, societyName), (...)]
# Get all the events attended by the user ever in every society
@makeConnection
def getUserAttendance(zid, conn = None, curs = None):
    if (checkUser(zid) == False):
        return {"status": "Failed"}

    queryResults = callQuery("select points, events.eventid, name, eventdate, isarcmember, societyName from events join participation on (events.eventid = participation.eventid) join host on (events.eventid = host.eventid) join society on (society.societyID = host.society) where participation.zid = (%s);", conn, curs, (zid,))
    if queryResults == False: return {"status": "Failed"}

    results = curs.fetchall()

    queryResults = callQuery("select firstName, lastName from users where zid = (%s);", conn, curs, (zid,))
    if queryResults == False: return {"status": "Failed"}

    result = curs.fetchone()
    firstName = result[0]
    lastName = result[1]

    conn.close()

    payload = {}
    payload['attendedEvents'] = []
    payload['zID'] = zid.lower()
    payload['firstName'] = firstName
    payload['lastName'] = lastName
    for event in results:
        eventJSON = {}
        eventJSON['eventID'] = event[1]
        eventJSON['name'] = event[2]
        eventJSON['society'] = event[5]
        eventJSON['eventDate'] = str(event[3])
        eventJSON['points'] = event[0]
        eventJSON['isArc'] = event[4]
        payload['attendedEvents'].append(eventJSON)

    return payload

# Get all the events in a society attended by a particular person
@makeConnection
def getPersonEventsForSoc(zID, societyID, conn = None, curs = None):
    if (checkUser(zID) == False):
        return "no such user"

    queryResults = callQuery("select firstName, lastName from users where zid = (%s);", conn, curs, (zID,))
    if queryResults == False: return "failed"
  
    name = curs.fetchone()
    firstName = name[0]
    lastName = name[1]

    
    queryResults = callQuery("select societyName from society where societyID = (%s);", conn, curs, (societyID,))
    if queryResults == False: return "failed"

    socName = curs.fetchone()
    if (socName is None):
        return None

    
    queryResults = callQuery("select * from events join host on (events.eventID = host.eventID) join participation on (events.eventID = participation.eventID) where society = (%s) and participation.zid = (%s);", conn, curs, (societyID, zID,))
    if queryResults == False: return "failed"
        
    events = curs.fetchall()
    conn.close()

    payload = {}
    payload['firstName'] = firstName
    payload['lastName'] = lastName
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

@makeConnection
def checkArc(zID, conn = None, curs = None):
    queryResults = callQuery("SELECT isArc FROM USERS WHERE zid = (%s);", conn, curs, (zID,))
    if queryResults == False: return False

    name = curs.fetchone()
    return True if name != [] else False

@makeConnection
def addActivationLink(zID, activationLink, conn = None, curs = None):

    queryResults = callQuery("UPDATE users SET activationLink = (%s) WHERE zID = (%s);", conn, curs, (activationLink, zID,))
    if (queryResults == False): return "failed"

    return "success"

@makeConnection
def activateAccount(zID, conn = None, curs = None):
    # TODO: Remove the next 8 lines, already implemented in checkActivation
    
    queryResults = callQuery("SELECT activationStatus FROM users WHERE zID = (%s);", conn, curs, (zID,))
    if queryResults == False: return "failed"

    result = curs.fetchone()
    if (result[0]) == True:
        return "already activated"
    
    queryResults = callQuery("UPDATE users SET activationStatus = True WHERE zID = (%s);", conn, curs, (zID,))
    if queryResults == False: return "failed"

    conn.commit()
    return "success"

@makeConnection
def checkActivation(zID, conn = None, curs = None):
    
    queryResults = callQuery("SELECT activationStatus FROM USERS WHERE zID = (%s);", conn, curs, (zID,))
    if queryResults == False: return False

    result = curs.fetchone()
    if (result is None):
        return False
    return result[0]

@makeConnection
def getInvolvedSocs(zID, conn = None, curs = None):
    
    queryResults = callQuery("SELECT societyID, societyName, role FROM userInSociety WHERE role = 0 AND zid = (%s);", conn, curs, (zID,))
    if queryResults == False: return None
    normalMember = curs.fetchall()
    queryResults = callQuery("SELECT societyID, societyName, role FROM userInSociety WHERE role = 1 and zid = (%s);", conn, curs, (zID,))
    if queryResults == False: return None
    staffMember = curs.fetchall()

    payload = {}
    payload['member'] = []
    for i in normalMember:
        currI = {}
        currI['societyID'] = i[0]
        currI['societyName'] = i[1]
        payload['member'].append(currI)
    payload['staff'] = []
    for i in staffMember:
        currI = {}
        currI['societyID'] = i[0]
        currI['societyName'] = i[1]
        payload['staff'].append(currI)
    return payload

@makeConnection
def changePassword(zID, oldPassword, password, conn = None, curs = None):
    results = checkUserInfo(zID, oldPassword)
    if (results == False):
        return 'failed'
    password = str(password).encode('UTF-8')
    pwHash = hashlib.sha256(password).hexdigest()

    queryResults = callQuery("UPDATE users SET password = (%s) WHERE zID = (%s);", conn, curs, (pwHash, zID,))
    if queryResults == False: return "failed"

    conn.close()
    return "success"

@makeConnection
def deleteAccount(zID, conn = None, curs = None):
    queryResults = callQuery("DELETE FROM users WHERE zID = (%s);", conn, curs, (zID,))
    if queryResults == False: return "failed"

    conn.close()
    return "success"