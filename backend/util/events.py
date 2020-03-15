from util.utilFunctions import checkUser, checkEvent, makeConnection, callQuery
from util.societies import findSocID
from util.users import createUser
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

# NOTE: The dict below is for the "onThisWeek" statistics
# NOTE: CHANGE THE EVENT TABLE TO INCLUDE THE WEEK 
# FIXME: FIXME WHEN IT COMES TO 2021
week = datetime.strptime('2020-02-17', "%Y-%m-%d").date()
weekDate = {}
for counter in range(1, 12):
    weekDate[f'T1W{str(counter)}'] = str(week)
    week += relativedelta(days=7)

week = datetime.strptime('2020-06-01', "%Y-%m-%d").date()
for counter in range(1, 12):
    weekDate[f'T2W{str(counter)}'] = str(week)
    week += relativedelta(days=7)

week = datetime.strptime('2020-09-14', "%Y-%m-%d").date()
for counter in range(1, 12):
    weekDate[f'T3W{str(counter)}'] = str(week)
    week += relativedelta(days=7)

def findWeek(date: datetime):
    previousI = 0
    for i in weekDate.keys():
        currWeek = datetime.strptime(weekDate[i], "%Y-%m-%d").date()
        if (date < currWeek):
            if (previousI == 0):
                return None
            return previousI

        previousI = i
    return None


# Creting an event (single instance events)
@makeConnection
def createSingleEvent(zID, eventID, eventName, eventDate, qrFlag, societyID = None, location = None, description = None, startTime = None, endTime = None, conn = None, curs = None):

    if (checkUser(zID) == False):
        return "no such user"
    else:
        queryStatus = callQuery("SELECT * FROM socStaff WHERE society = (%s) AND zid = (%s) AND role >= 1;", conn, curs, (societyID, zID,))
        if (queryStatus == False): return None
        results = curs.fetchone()
        if (results is None):
            return "not an admin"

    if (checkEvent(eventID) != False):
        return "already exists"
    elif (societyID == None):
        societyID = findSocID("UNSW Hall")

    eventDate = datetime.strptime(eventDate, "%Y-%m-%d").date()
    week = findWeek(eventDate)
    if (week == None):
        return "Not a valid date for events"

    queryStatus = callQuery("INSERT INTO events(eventID, name, owner, eventDate, eventWeek, qrCode, description, startTime, endTime) VALUES ((%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s));", conn, curs, (eventID, eventName, zID, eventDate, week, qrFlag, description, startTime, endTime,))

    # NOTE: Currently, location defaults to UNSW Hall if one isnt provided
    queryStatus1 = callQuery("INSERT INTO host(location, society, eventID) VALUES ((%s), (%s), (%s));", conn, curs, ("UNSW Hall" if location is None else location, societyID if societyID is not None else -1, eventID,))
    if (queryStatus == False or queryStatus1 == False): return None
    conn.commit()
    conn.close()
    return eventID, True

'''
    # Creating a recurring event (need specification on what kind of recurrence)
    # Currently, accept four different recurrent parametres, startDate and endDate to indicate how muuch this recurrence will be
    # recurType indicates what kind of recurrence this is (accepts: "day", "week", "month")
    # recurInterval indicates how many of said recurType is inbetween each interval (accepts any int less than 365)
    # Example: startDate = 2020-01-30, endDate = 2020-05-30, recurType = "day", recurInterval = 14 
    # Example Cont.: The above indicates this event occurs every fortnightly starting with 30/1/2020 to 30/5/2020
'''
@makeConnection
def createRecurrentEvent(zID, eventID, eventName, eventStartDate, eventEndDate, recurInterval, recurType, qrFlag = None, location = None, societyID = None, description = None, startTime = None, endTime = None, conn = None, curs = None):
    if (checkUser(zID) == False):
        conn.close()
        return "no such user"
    else:
        queryStatus = callQuery("SELECT * FROM socStaff WHERE society = (%s) AND zid = (%s) AND role = 1;", conn, curs, (societyID, zID,))
        if (queryStatus == False): return None
        results = curs.fetchone()
        if (results is None):
            conn.close()
            return "not an admin"

    if (checkEvent(eventID) != False):
        conn.close()
        return "Event already exists"
    elif (societyID == None):
        societyID = findSocID("UNSW Hall")

    interval = None
    recurInterval = int(recurInterval)
    if (recurType == "day"):
        interval = relativedelta(days=recurInterval)
    elif (recurType == "week"):
        interval = relativedelta(weeks=recurInterval)
    elif (recurType == "month"):
        interval = relativedelta(months=recurInterval)
    else:
        conn.close()
        return "Unacceptable parametre"

    eventStartDate = datetime.strptime(eventStartDate, "%Y-%m-%d").date()
    eventEndDate = datetime.strptime(eventEndDate, "%Y-%m-%d").date()
    counter = 0
    eventIDLists = []
    previousWeek = None
    while eventStartDate < eventEndDate:
        currEventID = eventID + f"{counter:02d}"
        week = findWeek(eventStartDate)
        if (week is None):
            break
        elif (previousWeek == week):
            eventStartDate += interval
            continue

        queryStatus = callQuery("INSERT INTO events(eventID, name, owner, eventDate, eventWeek, qrCode, description, startTime, endTime) VALUES ((%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s));", conn, curs, (currEventID, eventName, zID, eventStartDate, week, qrFlag, description, startTime, endTime,))

        queryStatus2 = callQuery("INSERT INTO host(location, society, eventID) VALUES ((%s), (%s), (%s));", conn, curs, ("UNSW Hall" if location is None else location, societyID if societyID is not None else -1, currEventID,))
        if(queryStatus == False or queryStatus2 == False): return None

        eventIDLists.append({"date": str(eventStartDate), "eventID": currEventID})
        eventStartDate += interval
        counter += 1
        previousWeek = week
    conn.commit()
    conn.close()

    return eventIDLists[0]["eventID"], True

# Returns a set of attendance numbers for each events
@makeConnection
def fetchRecur(eventID, conn, curs):
    baseID = eventID[:5]
    print(baseID)

    queryStatus = callQuery(f"select * from events where eventID like '{baseID}%';", conn, curs)
    if (queryStatus == False): return None
    results = curs.fetchall()
    payload = []
    for event in results:
        eventJSON = {}
        eventJSON['eventID'] = event[0]
        eventJSON['name'] = event[1]
        eventJSON['date'] = str(event[2])

        queryStatus = callQuery("select count(*) as count from participation where eventID = (%s);", conn, curs, (event[0],))
        if (queryStatus == False): return None
        eventJSON['attendance'] = curs.fetchone()[0]

        payload.append(eventJSON)
    conn.close()
    return payload

@makeConnection
def getEventTimes(eventID, conn, curs):

    results = callQuery("SELECT startTime, endTime FROM EVENTS WHERE EVENTID = (%s);", conn, curs, (eventID,))
    if results == False: return None

    result = curs.fetchall() 
    conn.close()
    return result[0] if result != [] else None

@makeConnection
def getAllEvents(conn, curs):

    currentDate = datetime.now().date()
    currentDate = str(currentDate)
    results = callQuery("SELECT eventID, name, eventDate, location, societyName, societyID FROM hostedEvents ORDER BY eventDate;", conn, curs)
    if results == False: return None

    results = curs.fetchall()
    if results == []:
        return None

    payload = []
    for result in results:
        eventJSON = {}
        eventJSON['eventID'] = result[0]
        eventJSON['name'] = result[1]
        eventJSON['eventDate'] = str(result[2])
        eventJSON['location'] = result[3]
        eventJSON['societyName'] = result[4]
        eventJSON['societyID'] = result[5]
        payload.append(eventJSON)
    conn.close()
    return payload

@makeConnection
def getAllEventID(conn, curs):

    currentDate = datetime.now().date()
    currentDate = str(currentDate)
    results = callQuery("SELECT eventID FROM events;", conn, curs)
    if (results == False): return None
    
    results = curs.fetchall()
    if results == []:
        return None

    payload = []
    for result in results:
        payload.append(result[0])
    conn.close()
    return payload

@makeConnection
def getPastEvents(socID, conn, curs):
    currentDate = datetime.now().date()
    currentDate = str(currentDate)
    results = callQuery("SELECT eventID, name, eventDate, location, societyName, societyID FROM hostedEvents WHERE eventdate < (%s) AND societyID = (%s) ORDER BY eventDate DESC;", conn, curs, (currentDate, socID,))
    if (results == False): return None

    results = curs.fetchall()
    if results == []:
        return None

    payload = []
    for result in results:
        eventJSON = {}
        eventJSON['eventID'] = result[0]
        eventJSON['name'] = result[1]
        eventJSON['eventDate'] = str(result[2])
        eventJSON['location'] = result[3]
        eventJSON['societyName'] = result[4]
        eventJSON['societyID'] = result[5]
        payload.append(eventJSON)
    conn.close()
    return payload