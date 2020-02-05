from sqlite3 import Error
import sqlite3
import os
# Uncomment the five lines below when reinitialising the database is required
from util.events import createSingleEvent, createRecurrentEvent
from util.users import createUser
from util.participation import register
from util.societies import createSociety, createSocStaff, findSocID
from util.utilFunctions import checkEvent

def createConnection():
    conn = None
    try:
        conn = sqlite3.connect(r'./database.db')
    except Error as e:
        print(e)
    return conn

def createTable(conn, sql):
    try:
        curs = conn.cursor()
        curs.execute(sql)
    except Error as e:
        print(e)
        exit(1)

def runQuery(conn, sql, arg):
    try:
        curs = conn.cursor()
        curs.execute(sql, arg)
    except Error as e:
        print(e)
        exit(1)

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
    os.system("rm database.db")

    conn = None
    try:
        conn = createConnection()
        createUserSQL = '''
            create table if not exists users (
                zid text not null,
                name text not null,
                password text not null,
                primary key(zid)
            );'''
        createTable(conn, createUserSQL)
        createEventsSQL = '''
            create table if not exists events (
                eventID text not null,
                name text not null,
                eventdate date not null,
                owner text not null references users(id),
                qrCode boolean,
                description text,
                primary key(eventID)
            );'''
        createTable(conn, createEventsSQL)
        createPartcipationSQL = '''
            create table if not exists participation (
                points text not null,
                isArcMember boolean not null,
                user text not null references users(zid),
                eventID text not null references events(eventID),
                primary key (user, eventID)
            );'''
        createTable(conn, createPartcipationSQL)
        createSocietySQL = '''
            create table if not exists society (
                societyID text,
                societyName text not null unique,
                primary key (societyID)
            );'''
        createTable(conn, createSocietySQL)
        createSocietyHostSQL = '''
            create table if not exists host (
                location text,
                society integer references society(societyID),
                eventID text not null references events(eventID),
                primary key (society, eventID)
            );'''
        createTable(conn, createSocietyHostSQL)
        createSocStaffSQL = '''
            create table if not exists socstaff (
                society integer references society(societyID),
                zid text references users(zid),
                role text not null,
                primary key (society, zid)
            );'''
        createTable(conn, createSocStaffSQL)
        conn.close()
    # 20/12/2019: Added two new tables, added a FIXME when fixing the table dependencies
    except Error as e:
        print(e)
    
    initDatabase()

if __name__ == '__main__':
    main()