from sqlite3 import Error
# Uncomment the three lines below when reinitialising the database is required
# from util.events import createSingleEvent, createRecurrentEvent
# from util.users import createUser
# from util.societies import createSociety, createSocStaff
import sqlite3

# This file contains the check functions and that's it

# FIXME: If we want a different database for each different set of users, change this function below
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
    curs.execute("select * from users where zid=?;", (zID,))

    rows = curs.fetchall()
    conn.close()
    return False if rows == [] else True

# Check if a specified society already exists
def checkSoc(societyID):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select * from society where societyID = ?;", (societyID,))

    rows = curs.fetchall()
    conn.close()
    return False if rows == [] else True

# Check if an event exists in the table
def checkEvent(eventID):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select * from events where eventid=?;", (eventID,))

    rows = curs.fetchall()
    conn.close()
    return False if rows == [] else True


# General utilities functions
# Accepts a date in the form of "YYYY-MM-DD"
def onThisDay(date):
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select * from events where eventdate = ?;", (date,))

    results = curs.fetchall()
    payload = []
    for event in results:
        eventJSON = {}
        eventJSON['eventID'] = event[0]
        eventJSON['name'] = event[1]
        eventJSON['date'] = event[2]

        curs.execute("select count(*) as count from participation where eventID = ?;", (event[0],))
        eventJSON['attendance'] = curs.fetchone()[0]

        payload.append(eventJSON)

    conn.close()
    return payload








def initDatabase():
    # Moving this section to init.py in the next patch lmao
    # add users
    createUser("z5161616", "Steven Shen", "123456")
    createUser("z5161798", "Casey Neistat", "123456")
    createUser("z5111111", "Harrison Steyn", "123456")
    createUser("z5222222", "JunYang Sim", "123456")
    createUser("z5333333", "Ivan Velickovic", "123456")
    createUser("z5444444", "Oltan Sevinc", "123456")
    createUser("z5555555", "Will de Dassel", "123456")

    # TODO: Add some dummy societies and then fix the below add events dummy functions
    # NOTE: Might not be needed since the current version focuses on implementation just for Hall
    createSociety("z5111111", "CSESoc")
    createSociety("z5123123", "Manchester United FC")
    createSociety("z5555555", "UNSW Hall")

    # NOTE: Defaults to UNSW Hall (for the society field right now)
    createSingleEvent("z5161616", "1239", "Hackathon", "2019-11-19", True, findSocID("UNSW Hall"))
    createSingleEvent("z5333333", "0000", "Gamer Juice Winery Tour", "2019-09-09", True, findSocID("UNSW Hall"))
    createSingleEvent("z5555555", "1234", "Coffee Night", "2019-10-16", True, findSocID("UNSW Hall"))
    createSingleEvent("z5111111", "4231", "LoL Appreciation", "2019-09-08", True, findSocID("UNSW Hall"))

    # register users:
    #   for Hackathon
    register("z5161616", "1239", 'Steven')
    register("z5161798", "1239", 'Casey Neistat')
    #   for Gamer Juice Winery Tour
    register("z5333333", "0000", 'Ivan Velickovic')
    register("z5161798", "0000", 'Casey Neistat')
    register("z5161616", "0000", 'Stevn')
    #   for Coffee Night
    register("z5161616", "1234", 'Steven')
    register("z5161798", "1234", 'Casey Neistat')
    register("z5111111", "1234", 'Harrison Steyn')
    register("z5222222", "1234", 'Junyang Sim')
    register("z5333333", "1234", 'Ivan Velickovic')
    register("z5444444", "1234", 'Oltan Sevinc')
    register("z5555555", "1234", 'Will de Dassel')

def main():
    # Uncomment if required
    #initDatabase()

    #print(getPersonEventsForSoc("z5161616", findSocID("UNSW Hall")))
    # print(getAttendance("1234"))
    #print(getUserAttendance("z5161616"))
    # print(getAttendance(1234))
    #print("Entered")
    #print(getEventForSoc(findSocID("UNSW Hall")))
    #print(getPersonEventsForSoc("z5161616", findSocID("UNSW Hall")))
    '''
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("select eventdate from events;")
    results = curs.fetchall()
    date1 = datetime.strptime(results[0][0], '%Y-%m-%d').date()
    print(date1)
    print(date1 + relativedelta(months=3))
    '''
    #print(createRecurrentEvent("z5161616", "aaaaa", "coffee night", "2020-03-13", "2020-04-15", 7, "day", False))
    #print(fetchRecur("1FAEA00018"))
    print(onThisDay("2020-03-06"))


if __name__ == '__main__':
    main()