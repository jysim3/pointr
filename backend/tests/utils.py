import json
import unittest
import uuid
from app import app, db
from datetime import datetime, timezone

URL_BASE = '/api/rework'

class PointrTest(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.session.commit()
        db.drop_all()
        db.create_all()

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

    def postValidEvent(self, c, societyID=None):
        
        if societyID == None:
            societyID = self.postValidSociety(c, "Gamersoc")

        sentData = {
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

    def postValidSociety(self, c, name):

        response = fetch(c, "POST", "/society", data={
            "name": name,
            "type": 1,
            "tags": [1]
        })
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