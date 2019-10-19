from sqlite3 import Error
import sqlite3

def createConnection():
    conn = None
    try:
        conn = sqlite3.connect(r'./database.db')
    except Error as e:
        print(e)
    return conn

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
    if (checkUser(userID) != False):
        return None

    conn = createConnection()
    curs = conn.cursor()
    curs.execute("insert into users(zid, name) values(?, ?);", (userID, name,))
    conn.commit()

# Creting an event
# Event could maybe have a weight
def createEvent(userID, eventID, eventName, eventDate):
    # FIXME
    if (checkUser(userID) == False):
        createUser(userID, "Junyang Sim")
    
    if (checkEvent(eventID) != False):
        return "Already created"
    
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("insert into events(eventID, name, society, owner, eventDate) values (?, ?, ?, ?, ?);", (eventID, eventName, "UNSW Hall", userID, eventDate,))
    conn.commit()

def fetchUserStatistics():
    # We fetch everything from the participation relationship
    return 1

def register(userID, userName, eventID, eventName, points):
    return 1

def main():
    createEvent("z5161616", "aslhfkjahsdf", "Test Event 0", "2019-11-19")

if __name__ == '__main__':
    main()