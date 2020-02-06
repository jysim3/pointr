#from sqlite3 import Error
#import sqlite3
from psycopg2 import Error
import psycopg2

# This file contains the check functions and that's it

# FIXME: If we want a different database for each different set of users, change this function below
def createConnection():
    conn = None
    try:
        #conn = sqlite3.connect(r'./database.db')
        conn = psycopg2.connect(database = "pointrDB")
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


# General utilities functions
# Accepts a date in the form of "YYYY-MM-DD"
def onThisDay(date, socID = None):
    conn = createConnection()
    curs = conn.cursor()

    if socID == None:
        curs.execute("select * from events where eventdate = (%s);", (date,))
    else:
        result = checkSoc(socID)
        if result == False:
            return []
        curs.execute("select * from events join host on host.eventID = events.eventID and society = (%s) and eventDate = (%s);", (socID, date,))

    results = curs.fetchall()
    payload = []
    for event in results:
        eventJSON = {}
        eventJSON['eventID'] = event[0]
        eventJSON['name'] = event[1]
        eventJSON['date'] = event[2]

        curs.execute("select count(*) as count from participation where eventID = (%s);", (event[0],))
        eventJSON['attendance'] = curs.fetchone()[0]

        payload.append(eventJSON)

    conn.close()
    return payload


def main():
    #print(getPersonEventsForSoc("z5161616", findSocID("UNSW Hall")))
    # print(getAttendance("1234"))
    #print(getUserAttendance("z5161616"))
    # print(getAttendance(1234))
    #print("Entered")
    #print(getEventForSoc(findSocID("UNSW Hall")))
    #print(getPersonEventsForSoc("z5161616", findSocID("UNSW Hall")))
    #print(createRecurrentEvent("z5161616", "aaaaa", "coffee night", "2020-03-13", "2020-04-15", 7, "day", False))
    #print(fetchRecur("1FAEA00018"))
    return 0
    #print(onThisDay("2020-03-06"))

if __name__ == '__main__':
    main()