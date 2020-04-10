from psycopg2 import Error
import psycopg2
from datetime import datetime
from dateutil import tz
import os

# This file contains the check functions and that's it

# NOTE: If we want a different database for each different set of users, change this function below
def createConnection():
    conn = None
    try:
        #conn = sqlite3.connect(r'./database.db')
        database_name = 'pointrDB'
        if (os.environ.get('FLASK_ENV') == 'test'):
            database_name = 'testPointrDB'
        conn = psycopg2.connect(database = database_name)
    except Error as e:
        print(e)
    return conn

# Check if a user exists in the table
def checkUser(zID):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select * from users where zid=(%s);", (zID,))

    rows = curs.fetchall()
    conn.close()
    return False if rows == [] else True

# Check if a specified society already exists
def checkSoc(societyID):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select * from society where societyID = (%s);", (societyID,))

    rows = curs.fetchall()
    conn.close()
    return False if rows == [] else True

# Check if an event exists in the table
def checkEvent(eventID):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select * from events where eventid=(%s);", (eventID,))

    rows = curs.fetchall()
    conn.close()
    return False if rows == [] else True

def makeConnection(func):
    def wrapper(*args, **kwargs):
        conn = createConnection()
        curs = conn.cursor()
        return func(conn=conn, curs=curs, *args, *kwargs)
    return wrapper

def getAESTTime():
    utc = datetime.utcnow()
    from_zone = tz.tzutc()
    utc = utc.replace(tzinfo=from_zone)
    toZone = tz.gettz('Australia/Sydney')
    time = utc.astimezone(toZone)
    return time

def callQuery(query, conn, curs, *args):
    try:
        curs.execute(query, *args)
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
        conn.close()
        return False
    conn.commit()
    return True

# General utilities functions
# Accepts either a date in the form of "YYYY-MM-DD", or a week in the form of "T[1-3]W[1-10]", or a month in the range of [1-12]
def onThisDay(interval, intervalType, socID = None):
    # TODO: Check user if they belong in this soc
    conn = createConnection()
    curs = conn.cursor()

    dataType = None
    if (intervalType == "day"):
        dataType = "eventDate"
    elif (intervalType == "week"):
        dataType = "eventWeek"
    elif (intervalType == "month"):
        # TODO: Finish this part
        return -1
    else:
        return None

    if socID == None:
        curs.execute(f"select * from events where {dataType} = (%s);", (interval,))
    else:
        result = checkSoc(socID)
        if result == False:
            return []
        curs.execute(f"select * from events join host on (host.eventID = events.eventID) where society = (%s) and {dataType} = (%s);", (socID, interval,))

    results = curs.fetchall()
    payload = []
    for event in results:
        eventJSON = {}
        eventJSON['eventID'] = event[0]
        eventJSON['name'] = event[1]
        eventJSON['date'] = str(event[2])

        curs.execute("select count(*) as count from participation where eventID = (%s);", (event[0],))
        eventJSON['attendance'] = curs.fetchone()[0]

        payload.append(eventJSON)

    conn.close()
    return payload
