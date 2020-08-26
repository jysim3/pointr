import json
import unittest
import uuid
from app import app, db
from datetime import datetime, timezone
import os
from models.user import Users
from hashlib import sha256
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

URL_BASE = '/api'

SERVER_TEST_SECRET = 'secret'

class PointrTest(unittest.TestCase):

    userSuperAdmin = {
        'zID': 'z1111111',
        'password': 'password'
    }

    mockEventData = {
        "name": "Gamersoc Minecraft Night",
        "start": str(datetime.now(timezone.utc)),
        "end": str(datetime.now(timezone.utc)),

        "location": "My place",

        "status": 0,
        "tags": [0, 1],

        "hasQR": True,
        "hasAccessCode": True,
        "hasAdminSignin": True
    }

    mockSocietyData = {
        "name": "Gamersoc",
        "type": 1,
        "tags": [1]
    }

    def setUp(self):
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        os.environ['POINTR_SERVER_SECRET'] = SERVER_TEST_SECRET

        database_name = "testPointrDB"
        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{os.environ.get('SQLPassword')}@localhost/{database_name}"
        db = SQLAlchemy(app)
        migrate = Migrate(app, db)

        db.session.commit()
        db.drop_all()
        db.create_all()
        self.c = app.test_client()
        self.registerUsers()

    def tearDown(self):
        pass

    def assertOK(self, response):
        try:
            self.assertEqual(response.status_code, 200)
        except AssertionError as e:
            print(f"Response returned {response.status_code}:")
            print(str(response.data))
            raise AssertionError

    def assert400(self, response):
        try:
            self.assertEqual(response.status_code, 400)
        except AssertionError as e:
            print(f"Response returned {response.status_code}:")
            print(str(response.data))
            raise AssertionError

    def assertContains(self, dict, key, value):
        self.assertEqual(dict.get(key), value)

    def assertSuccess(self, dict):
        self.assertContains(dict, "status", "success")

    def assertFailed(self, dict):
        self.assertContains(dict, "status", "failed")

    def postValidEvent(self, c, societyID=None):
        
        if societyID == None:
            societyID = self.postValidSociety(c, "Gamersoc")
            
        sentData = self.getMockEventData()
        
        response = fetch(c, "POST", "/event", data=sentData, queries={
            "societyID": str(societyID)
        })

        self.assertOK(response)

        payload = json.loads(response.data)

        return payload['data']['id']

    def getValidEvent(self, c, id):
        response = fetch(c, "GET", "/event", queries={
            "eventID": id
        })
        self.assertOK(response)

        payload = json.loads(response.data)

        return payload['data']

    def getEvent(self, c, id):
        return fetch(c, "GET", "/event", queries={
            "eventID": id
        })

    def getSociety(self, c, id):
        return fetch(c, "GET", "/society", queries={
            "societyID": id
        })

    def postValidSociety(self, c, name):

        response = fetch(c, "POST", "/society", data=self.getMockSocietyData(name))
        self.assertOK(response)

        payload =  json.loads(response.data)

        return payload['data']['id']

    def getValidSociety(self, c, id):
        response = fetch(c, "GET", "/society", queries={
            "societyID": id
        })
        self.assertOK(response)

        payload = json.loads(response.data)

        return payload['data']
    
    def getMockEventData(self):
        return self.mockEventData

    def getMockSocietyData(self, name):
        data = self.mockSocietyData
        data['name'] = name
        return data

    def loginValidUser(self, loginDetails):
        c = self.c
        response = fetch(c, 'POST', '/auth/login', data=loginDetails)
        payload = json.loads(response.data)
        return payload['data']['token']

    def createUser(self, details):
        user = Users(**details)
        db.session.add(user)
        db.session.commit()

    def registerUsers(self):
        superAdmin = {
            "firstName": "Harrison",
            "lastName": "Steyn",
            "zID": "z1111111",
            "isArc": True,
            "password": sha256("password".encode('utf-8')).hexdigest(),
            "superadmin": False,
            "activated": True
        }

        self.createUser(superAdmin)

def fetch(c, method, route, queries=None, data=None, headers=None):
    if (method == 'GET'):
        return c.get(URL_BASE + route + query(queries))
    elif (method == 'POST'):
        return c.post(URL_BASE + route + query(queries), data=json.dumps(data), content_type='application/json')
    elif (method == 'PATCH'):
        return c.patch(URL_BASE + route + query(queries), data=json.dumps(data), content_type='application/json')
    elif (method == 'DELETE'):
        return c.delete(URL_BASE + route + query(queries))
    elif (method == 'PUT'):
        return c.put(URL_BASE + route + query(queries), data=data)
    else:
        print("INVALID METHOD")

def query(data):
    if data == None:
        return ""
    queries = []
    for (k,v) in data.items():
        queries.append(k + "=" + v)
    return "?" + "&".join(queries)
