from sqlite3 import Error
import sqlite3
from init import createConnection

# Check if a user exists in the table
def checkUser(userID):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select * from users where zid=?", (userID,))
    
    rows = curs.fetchall()
    if (rows == []):
        return False

    return True

# Check if an event exists in the table
def checkEvent(eventID):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select * from events where eventid=?", (eventID,))

    rows = curs.fetchall()
    if (rows == []):
        return False
    
    return True

# Creating a user 
def createUser(userID, name):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("insert into users(zid, name) values(?, ?);", (userID, name,))
    conn.commit()

# Creting an event
# Event could maybe have a weight
def createEvent(userID, eventID, eventName, eventDate, eventPoints):
    # FIXME
    if (checkUser(userID) == False):
        createuser(userID)
    
    if (checkEvent(eventID) != False):
        return "Already created"
    
def fetchUserStatistics():
    # We fetch everything from the participation relationship
    return 1

def register(userID, userName, eventID, eventName, points):
    sqlUser = ''' 
        insert into users(name, zid)
        values(?, ?);'''

def main():
    checkUser("z5161616")
    createUser("z5161616", "Steven Shen")
    checkUser("z5161616")

if __name__ == '__main__':
    main()