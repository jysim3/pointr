import sqlite3 
from sqlite3 import Error
from flask import Flask, request
from flask_cors import CORS
import random
import string
from json import dumps
import utilFunctions
import re

app = Flask(__name__)
CORS(app)

def sanitize(input):
    return re.sub("[^\w ']", "", input)

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
# Usage: 
# POST /api/event
# Takes:
# { zID: "z5214808", name: "Coffee Night", eventDate: "2019-11-19"}
# Date is in YYYY-MM-DD
# Returns:
# { status: "success", eventID: "1234F"}
# or
# { status: "ERROR MESSAGE"}

@app.route('/api/event', methods=['POST'])
def createEvent():
    data = request.get_json()

    eventID = generateID(5).upper()
    if not 'hasQR' in data:
        data['hasQR'] = False
    elif data['hasQR'].lower() == "true":
        data['hasQR'] = True
    elif data['hasQR'].lower() == "false":
        data['hasQR'] = False
    else:
        data['hasQR'] = False
            
    payload = {}
    payload['status'] = utilFunctions.createEvent(sanitize(str(data['zID']).lower()), sanitize(str(eventID)), sanitize(str(data['name'])), sanitize(str(data['eventDate'])), data['hasQR'])
    if payload['status'] == 'success':
        payload['eventID'] = eventID
    return dumps(payload)

# For getting info on an event
# Usage:
# GET /api/event?eventID=ID
@app.route('/dummy/event', methods=['GET'])
def getEventDummy():
    eventID = request.args.get('eventID')
    payload = {}
    payload["eventID"] = eventID
    payload["name"] = "Coffee Night"
    payload["participants"] = [{
        "userID": "z5214808",
        "name": "Harrison",
        "points": "10000"
    }, {
        "userID": "z6273842",
        "name": "John",
        "points": "1"
    }, {
        "userID": "z1234567",
        "name": "Peter",
        "points": "1203"
    }]
    
    return dumps(payload)

# For getting info on an event
# Usage:
# GET /api/event?eventID=ID
# Returns: 
# {"eventID": "1239", "name": "Test Event 0", "participants": [{"zID": "z5161616", "name": "Steven Shen", "points": 1}, {"zID": "z5161798", "name": "Casey Neistat", "points": 1}]}
@app.route('/api/event', methods=['GET'])
def getEvent():
    eventID = request.args.get('eventID')
    payload = {}
    attendance = utilFunctions.getAttendance(sanitize(eventID))
    if attendance == "failed":
        payload['status'] = 'failed'
    else:
        payload['eventID'] = eventID
        payload['name'] = attendance[1]
        payload['hasQR'] = False
        payload['participants'] = []
        for person in attendance[0]:
            personJSON = {}
            print(person)
            # Fix Stevens shit formatting
            personJSON['zID'] = person[0][0][0].lower()
            personJSON['name'] = person[0][0][1]
            personJSON['points'] = person[1]
            payload['participants'].append(personJSON)
        payload['status'] = 'success'
    return dumps(payload)

# For adding a user to an event
# Usage:
# /api/attend
# Takes: 
# {'zID': z5214808, 'eventID': "12332"}
@app.route('/api/attend', methods=['POST'])
def attend():
    data = request.get_json()
    payload = {}
    
    payload['status'] = utilFunctions.register(sanitize(data['zID'].lower()), sanitize(data['eventID']), sanitize(data['name']))
    return dumps(payload)

# For getting the points of a user
# Usage:
# GET /api/user?zID=z5214808
# Returns:
# [{"eventID": "1239", "name": "Test Event 0", "society": "UNSW Hall", "eventDate": "2019-11-19"}, {"eventID": "1240", "name": "Coffee Night", "society": "UNSW Hall", "eventDate": "2019-11-20"}]
@app.route('/api/user', methods=['GET'])
def getUser():
    zID = request.args.get('zID')
    attendance = utilFunctions.getUserAttendance(sanitize(zID.lower()))
    if attendance == 'invalid user': 
        return dumps({"status": "failed"})
    payload = {}
    payload['events'] = []
    payload['zID'] = zID.lower()
    payload['name'] = attendance[1]
    print(attendance[0])
    for event in attendance[0]:
        eventJSON = {}
        # Dont ask what this does
        eventJSON['eventID'] = event[0][0]
        eventJSON['name'] = event[0][1]
        eventJSON['society'] = event[0][2]
        eventJSON['eventDate'] = event[0][3]
        eventJSON['points'] = event[1]
        payload['events'].append(eventJSON)
    return dumps(payload)

# Delete user attendance
# Usage: 
# DELETE /api/points
# Takes:
# {zID: "z5214808", eventID: "13287"}
# Returns: 
# {"status": "success"}
@app.route('/api/points', methods=['DELETE'])
def deletePoints():
    data = request.get_json()
    
    payload = {}
    payload['status'] = utilFunctions.deleteUserAttendance(sanitize(data['zID'].lower()), sanitize(data['eventID']))
    return dumps(payload)
    
# Update user attendance
# Usage: 
# POST /api/points
# Takes: 
# {zID: "z5214808", eventID: "13287", points: "10"}
# Returns: 
# {"status": "success"}  "points": 1000

@app.route('/api/points', methods=['POST'])
def updatePoints():
    data = request.get_json()
    payload = {}
    payload['status'] = utilFunctions.changePoints(sanitize(data['zID'].lower()), sanitize(data['eventID']), sanitize(str(data['points'])))
    return dumps(payload)

# For creating a user
# Usage: 
# POST /api/user
# Takes: 
# {zID: "z1234567", name: "Harrison Steyn"}
# Returns: 
# {"status": "success"}
@app.route('/api/user', methods=['POST'])
def postUser():
    data = request.get_json()
    returnVal = utilFunctions.createUser(sanitize(data['zID'].lower()), sanitize(data['name']))
    payload = {}
    payload['status'] = returnVal
    return dumps(payload)

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
        # TODO: Add a field here to store passwords
        createUserSQL = '''
            drop table if exists users;
            create table if not exists users (
                zid text not null,
                name text not null,
                primary key(zid)
            );'''
        createTable(conn, createUserSQL)
        createEventsSQL = '''
            drop table if exists events;
            create table if not exists events (
                eventID text not null,
                name text not null,
                societyID integer references society(societyID),
                eventdate date not null,
                owner text not null references users(id),
                qrCode boolean,
                primary key(eventID)
            );'''
        createTable(conn, createEventsSQL)
        createPartcipationSQL = '''
            drop table if exists participation;
            create table if not exists participation (
                points text not null,
                isArcMember boolean not null,
                user text not null references users(zid),
                eventID text not null references events(eventID),
                primary key (user, eventID)
            );'''
        createTable(conn, createPartcipationSQL)
        createSocietySQL = '''
            drop table if exists society;
            create table if not exists society (
                societyID integer primary key,
                societyName text not null,
            );'''
        createTable(conn, createSocietySQL)
        createSocietyHostSQL = '''
            drop table if exists host;
            create table if not exists host (
                society integer references society(societyID),
                eventID text not null references events(eventID),
                primary key (society, eventID)
            );'''
        createTable(conn, createSocietyHostSQL)
        createSocStaffSQL = '''
            drop table if exists socstaff (
                society integer references society(societyID),
                zid text references users(zid),
                role text not null,
                primary key (society, zid)
            );'''
        createTable(conn, createSocStaffSQL)
    # 20/12/2019: Added two new tables, added a FIXME when fixing the table dependencies
    except Error as e:
        print(e)
        exit(1)
    
    app.run()

# 20/12/2019: Think about refactoring parts of the code (i.e. Flask related features into app.py to keep the functionalities separate)

if __name__ == '__main__':
    main()
