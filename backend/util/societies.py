from util.utilFunctions import createConnection
import random
import string

def generateID(number):
    id = ""
    for x in range(0, number):
        id += random.choice(string.hexdigits)
    return id

def findSocID(socName):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select societyID from society where societyName = ?;", (socName,))
    societyID = curs.fetchone()[0]

    return societyID

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
    societyID = generateID(5).upper()
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select * from society where societyName = ?;", (societyName,))
    result = curs.fetchone()
    if (result != None):
        conn.close()
        return "exists already"

    curs.execute("insert into society(societyID, societyName) values (?, ?);", (societyID, societyName,))
    conn.commit()
    conn.close()

    # If we didn't specify a staff when creating the soc
    if (zID == None):
        return societyID

    # Otherwise, we add a staff with the job title of "President"
    createSocStaff(zID, societyID, "President")
    return societyID

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

# BELOW ARE ALL THE QUERY FUNCTIONS
# Get all the events hosted by a society
def getEventForSoc(societyID):
    # 9/1/2020: TODO: Flask routing for this function
    conn = createConnection()
    curs = conn.cursor()

    curs.execute("select societyName from society where societyID = ?;", (societyID,))
    name = curs.fetchone()
    if (name == None):
        conn.close()
        return "No such society"

    curs.execute("select events.eventID, name, eventDate, location, society from events join host on events.eventID = host.eventID and society = ?;", (societyID,))
    events = curs.fetchall()

    conn.close()
    return events, name[0]
