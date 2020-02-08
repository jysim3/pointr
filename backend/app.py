import sqlite3 
from sqlite3 import Error
from flask import Flask, request
from flask_cors import CORS
import random
import string
from json import dumps
#import util.utilFunctions as utilFunctions
from util import events, participation, societies, users, utilFunctions
import re
import os

app = Flask(__name__)
CORS(app)

def sanitize(input):
    return re.sub("[^\w '-]", "", input)

def generateID(number):
    id = ""
    for x in range(0, number):
        id += random.choice(string.hexdigits)
    return id

# Routes

@app.route('/')
def hello():
    return "Hello World!"

# For creating a recurrent event
# Usage: 
# POST /api/event
# Takes:
# { zID: "z5214808", name: "Coffee Night", location: "UNSW Hall", eventDate: "2020-01-01", endDate: "2020-04-04", recurType: "day", recurInterval: 6, "socID": "1DASD", "isRecur": "True"}
# NOTE: isRecur needs to be 1 for this to be a recurrentEvent creation, 0 for single instance event
# NOTE: For single instance events, everything after startDate is not required
# Date is in YYYY-MM-DD
'''
    # Currently, accept four different recurrent parametres, startDate and endDate to indicate how muuch this recurrence will be
    # recurType indicates what kind of recurrence this is (accepts: "day", "week", "month")
    # recurInterval indicates how many of said recurType is inbetween each interval (accepts any int less than 365)
    # Example: startDate = 2020-01-30, endDate = 2020-05-30, recurType = "day", recurInterval = 14 
    # Example Cont.: The above indicates this event occurs every fortnightly starting with 30/1/2020 to 30/5/2020
'''
# Returns:
# { status: "success", "msg": [{"date": 2020-04-04, "eventID": "1FAEA00001"}, {...}}
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

    location = sanitize(str(data['location'])).lower() if 'location' in data else None
    startDate = sanitize(str(data['eventDate'])).lower()
    endDate = sanitize(str(data['endDate']).lower()) if 'endDate' in data else None
    recurType = sanitize(str(data['recurType']).lower()) if 'recurType' in data else None
    recurInterval = sanitize(data['recurInterval']).lower() if 'recurInterval' in data else None
    zID = sanitize(str(data['zID']))
    eventName = sanitize(str(data['name']))
    hasQR = str(data['hasQR'])
    societyID = str(data['socID']) if 'socID' in data else None
    isRecur = str(data['isRecur']) if 'isRecur' in data and data['isRecur'] == 1 else False

    results = None
    if isRecur is not False:
        results = events.createRecurrentEvent(zID, eventID, eventName, startDate, endDate, recurInterval, recurType, hasQR, location, societyID)
    else:
        results = events.createSingleEvent(zID, eventID, eventName, startDate, hasQR, location, societyID)

    if (results == "Unacceptable parametre" or results == "Error encountered" or results == "Event already exists" or results == "failed"):
        return dumps({"status": "failed", "msg": results})
    return dumps({"status": "Success", "msg": results})

# For getting info on an event, i.e. participation information
# Usage:
# GET /api/event?eventID=ID
# Returns: 
# {"eventID": "1239", "name": "Test Event 0", "participants": [{"zID": "z5161616", "name": "Steven Shen", "points": 1}, {"zID": "z5161798", "name": "Casey Neistat", "points": 1}]}
@app.route('/api/event', methods=['GET'])
def getEvent():
    eventID = request.args.get('eventID')
    payload = {}
    attendance = participation.getAttendance(sanitize(eventID))
    if attendance == "failed":
        payload['status'] = 'failed'
    else:
        payload['eventID'] = eventID
        payload['name'] = attendance[1][0]
        payload['hasQR'] = attendance[0][0][4]
        payload['participants'] = []
        for person in attendance[0]:
            personJSON = {}
            personJSON['zID'] = person[3].lower()
            personJSON['name'] = person[2]
            personJSON['points'] = person[0]
            payload['participants'].append(personJSON)
        payload['status'] = 'success'
    return dumps(payload)

# For getting information on a set of recurrent events
# Usage:
# GET /api/stat/recurEvent?eventID=?
# Returns:
# {["eventID": "ASDA", "name": "AA meeting", "date": "2020-04-03", "attendance": 41], [...]}
@app.route('/api/stat/recurEvent', methods=['GET'])
def getRecurEventStats():
    eventID = request.args.get('eventID')
    if (eventID == None):
        return dumps({"status": "Failed", "msg": "No eventID"})

    return dumps(events.fetchRecur(eventID))


# For adding a user to an event
# Usage:
# /api/attend
# Takes: 
# {'zID': z5214808, 'eventID': "12332"}
@app.route('/api/attend', methods=['POST'])
def attend():
    data = request.get_json()
    payload = {}
    
    payload['status'] = participation.register(sanitize(data['zID'].lower()), sanitize(data['eventID']), sanitize(data['name']))
    return dumps(payload)

# Returns a list of events this person has attended
# Usage:
# GET /api/user?zID=z5214808
# Returns:
# [{"eventID": "1239", "name": "Test Event 0", "society": "UNSW Hall", "eventDate": "2019-11-19"}, {"eventID": "1240", "name": "Coffee Night", "society": "UNSW Hall", "eventDate": "2019-11-20"}]
@app.route('/api/user', methods=['GET'])
def getUser():
    zID = request.args.get('zID')
    attendance = users.getUserAttendance(sanitize(zID.lower()))
    if attendance == 'invalid user': 
        return dumps({"status": "failed"})
    payload = {}
    payload['events'] = []
    payload['zID'] = zID.lower()
    payload['name'] = attendance[1][0]
    for event in attendance[0]:
        eventJSON = {}
        eventJSON['eventID'] = event[1]
        eventJSON['name'] = event[2]
        eventJSON['society'] = event[4]
        eventJSON['eventDate'] = event[3]
        eventJSON['points'] = event[0]
        payload['events'].append(eventJSON)
    return dumps(payload)

# Get all the events hosted by a society
@app.route('/api/soc/eventsHosted', methods=['GET'])
def getHostedEvents():
    societyID = request.args.get('societyID')
    if (societyID is None):
        return dumps({"status": "Failed", "msg": "No societyID inputted"})
    eventsList = societies.getEventForSoc(societyID)
    if (eventsList == "No such society"):
        return dumps({"status": "Failed", "msg": "No such society"})
    
    payload = {}
    payload['events'] = []
    payload['societyName'] = eventsList[1]
    for event in eventsList[0]:
        eventJSON = {}
        eventJSON['eventID'] = event[0]
        eventJSON['name'] = event[1]
        eventJSON['society'] = event[3]
        eventJSON['eventDate'] = event[2]
        payload['events'].append(eventJSON)
    return dumps(payload)

# TODO: Implement society related flask routings
# Creates a society
# Returns the societyID as part of the result JSON in the "msg" field
@app.route('/api/soc/create', methods=['POST'])
def createSoc():
    data = request.get_json()
    
    result = societies.createSociety(sanitize(data['founder'] if data['founder'] is not None else 'Not Applicable'), sanitize(data['societyName']))
    if (result == "exists already"):
        return dumps({"status": "Failed", "msg": "A society with this name already exists"})
    return dumps({"status": "Success", "msg": result})

# TODO: Add a two layer system (i.e. admins), thus a flask route for adding admins

# Returns a list of events attended by a person in one society
@app.route('/api/stats/userSocAttendance', methods=['GET'])
def userAllAttendance():
    zID = request.args.get('zID')
    socID = request.args.get('societyID')
    if (zID is None):
        return dumps({"status": "Failed", "msg": "No zID provided"})
    elif (socID is None):
        return dumps({"status": "Failed", "msg": "No socID provided"})

    eventsAttended = users.getPersonEventsForSoc(zID, socID)
    if (eventsAttended == "No such user"):
        return dumps({"status": "Failed", "msg": "No such user"})

    payload = {}
    payload['userName'] = eventsAttended[1]
    payload['societyName'] = eventsAttended[2]
    for event in eventsAttended[0]:
        eventJSON = {}
        eventJSON['eventID'] = event[0]
        eventJSON['name'] = event[1]
        eventJSON['society'] = event[3]
        eventJSON['eventDate'] = event[2]
        eventJSON['points'] = event[4]
        payload['events'].append(eventJSON)
    return dumps(payload)

# Will probably be involved in some kind of a "today's events" type of thing
# GET /api/events/onthisday?date=2020-04-04&socID=1AEF0 (Note: socID optional)
# Returns:
# [{"eventID": "1239", "name": "Test Event 0", "society": "UNSW Hall", "eventDate": "2019-11-19"}, {"eventID": "1240", "name": "Coffee Night", "society": "UNSW Hall", "eventDate": "2019-11-20"}]
@app.route('/api/events/onthisday', methods=['GET'])
def onThisDay():
    date = request.args.get('date')
    socID = request.args.get('socID')

    if (date is None):
        return dumps({"status": "Failed", "msg": "No date provided"})

    return dumps(utilFunctions.onThisDay(date)) if socID == None else dumps(utilFunctions.onThisDay(date, socID))

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
    payload['status'] = participation.deleteUserAttendance(sanitize(data['zID'].lower()), sanitize(data['eventID']))
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
    payload['status'] = participation.changePoints(sanitize(data['zID'].lower()), sanitize(data['eventID']), sanitize(str(data['points'])))
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
    returnVal = users.createUser(sanitize(data['zID'].lower()), sanitize(data['name']))
    payload = {}
    payload['status'] = returnVal
    return dumps(payload)


def main():
    app.run()

if __name__ == '__main__':
    main()
