import sqlite3 
from sqlite3 import Error
from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app, version='0.02', title='Pointr backend',
    description='Backend for pointr web servers',
)

import random
import string
from json import dumps
#import util.utilFunctions as utilFunctions
from util import events, participation, societies, users, utilFunctions
import re
import os

from namespaces.event import api as event
from namespaces.stats import api as stats
from namespaces.user import api as user
from namespaces.auth import api as auth

api.add_namespace(event, path='/api/event')
# api.add_namespace(stats, path='/api/stats')
api.add_namespace(user, path='/api/user')
api.add_namespace(auth, path='/api/auth')

CORS(app)

def sanitize(input):
    return re.sub("[^\w '-]", "", input)

def generateID(number):
    id = ""
    for x in range(0, number):
        id += random.choice(string.hexdigits)
    return id

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

    print(events.fetchRecur(eventID))
    return dumps(events.fetchRecur(eventID))

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
        eventJSON['eventDate'] = str(event[2])
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
    payload['events'] = []
    for event in eventsAttended[0]:
        eventJSON = {}
        eventJSON['eventID'] = event[0]
        eventJSON['name'] = event[1]
        eventJSON['society'] = event[3]
        eventJSON['eventDate'] = str(event[2])
        eventJSON['points'] = event[4]
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
    
def main():
    app.run()

if __name__ == '__main__':
    main()
