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
def checkUser(zID):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select * from users where zid=?", (zID,))
    
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
def createUser(zID, name):
    if (checkUser(zID) != False):
        return "Failed"

    conn = createConnection()
    curs = conn.cursor()
    curs.execute("insert into users(zid, name) values(?, ?);", (zID, name,))
    conn.commit()
    return "Success"

# Creting an event
# Event could maybe have a weight
def createEvent(zID, eventID, eventName, eventDate):
    # FIXME
    if (checkUser(zID) == False):
        createUser(zID, "Junyang Sim")

    if (checkEvent(eventID) != False):
        return "Event does not exist"
    
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("insert into events(eventID, name, society, owner, eventDate) values (?, ?, ?, ?, ?);", (eventID, eventName, "UNSW Hall", zID, eventDate,))
    conn.commit()
    return "success"

def fetchUserStatistics():
    # We fetch everything from the participation relationship
    return 1

def register(zID, eventID):
    if (checkUser(zID) == False or checkEvent(eventID) == False):
        return "User or Event does not exist"

    conn = createConnection()
    curs = conn.cursor()
    curs.execute("insert into participation(points, user, eventID) values (?, ?, ?)", (1, zID, eventID,))
    conn.commit()

def main():
    createUser("z5161616", "Steven Shen")
    createEvent("z5161616", "1239", "Test Event 0", "2019-11-19")
    register("z5161616", "1239")

if __name__ == '__main__':
    main()