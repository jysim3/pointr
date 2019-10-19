import sqlite3 
from sqlite3 import Error
from flask import Flask, request
from flask_cors import CORS
import random
import string
from json import dumps

app = Flask(__name__)
CORS(app)


def generateID(number):
    id = ""
    for x in range(0, number):
        id += random.choice(string.hexdigits)
    return id

# Routes

@app.route('/')
def hello():
    return "Hello World!"

# For creating an event
@app.route('/api/event', methods=['POST'])
def createEvent():
    data = request.get_json()
    print(data)
    return generateID(5).upper()

# For getting info on an event
@app.route('/api/event', methods=['GET'])
def getEvent():
    data = request.get_json()
    eventID = data.eventID
    return generateID(5).upper()
    
@app.route('/api/attend', methods=['POST'])
def attend():
    data = request.get_json()
    print(data)
    return dumps({
        "status": "success"
    })

# SQL Shit

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

def main():
    conn = None
    try:
        conn = createConnection()
        createUserSQL = '''
            create table if not exists users (
                zid text not null,
                name text not null,
                primary key(zid)
            );'''
        createTable(conn, createUserSQL)
        createEventsSQL = '''
            create table if not exists events (
                eventID text not null,
                name text not null,
                society text,
                owner text not null references users(id),
                primary key(eventID)
            );'''
        createTable(conn, createEventsSQL)
        createPartcipationSQL = '''
            create table if not exists participation (
                points text not null,
                user text not null references users(id),
                eventID text not null references events(id),
                primary key (user, eventID)
            );'''
        createTable(conn, createPartcipationSQL)
    except Error as e:
        print(e)
        exit(1)
    
    app.run()


if __name__ == '__main__':
    main()
