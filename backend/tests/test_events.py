import unittest
from app import app
from tests.utils import fetch, PointrTest
from pprint import pprint
from nose2.tools import params
from datetime import datetime, timezone
import json
import dateutil.parser
import uuid

class TestEvents(PointrTest):

    def setUp(self):
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        pass

    def tearDown(self):
        pass

    def postValidEvent(self, c):

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

        postResponse = fetch(c, "POST", "/api/rework/event", data=sentData)
        self.assertOK(postResponse)

        data = json.loads(postResponse.data)

        return data['data']['id']

    def getEvent(self, c, id):
        return fetch(c, "GET", "/api/rework/event", queries={
            "eventID": id
        })

    def testCreateEvent(self):
        c = app.test_client()

        # POST data
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

        postResponse = fetch(c, "POST", "/api/rework/event", data=sentData)
        self.assertOK(postResponse)

        data = json.loads(postResponse.data)
        pprint(data)
        id = data['data']['id']

        # GET the data
        getResponse = fetch(c, "GET", "/api/rework/event", queries={
            "eventID": id
        })
        self.assertOK(getResponse)

        returnedData = json.loads(getResponse.data)
        
        # Check that the returned data contains the sent data (as some fields were left out)
        self.assertDictContainsSubset(sentData, returnedData)

    def testPatchEvent(self):
        c = app.test_client()

        # send original data
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

        postResponse = fetch(c, "POST", "/api/rework/event", data=sentData)
        self.assertOK(postResponse)

        data = json.loads(postResponse.data)
        id = data['data']['id']

        # send patch
        patchData = {
            "name": "Gamersoc Minecraft Night: The reckoning",
            "start": str(datetime.now(timezone.utc)),
            "end": str(datetime.now(timezone.utc))
        }
        patchResponse = fetch(c, "PATCH", "/api/rework/event", data=patchData, queries={
            "eventID": id
        })

        self.assertOK(patchResponse)

        patchReturnedData = json.loads(patchResponse.data)
        
        # get the event now
        getResponse = fetch(c, "GET", "/api/rework/event", queries={
            "eventID": id
        })
        self.assertOK(getResponse)
        returnedData = json.loads(getResponse.data)

        # Whatever the patch returned and the get returned should be the same
        self.assertDictEqual(patchReturnedData, returnedData)

        # Whatever the get returned should contain the patch
        self.assertDictContainsSubset(patchData, returnedData)

    def testInvalidEventID(self):
        c = app.test_client()

        id = self.postValidEvent(c)

        response1 = self.getEvent(c, "1")
        self.assert400(response1)
        
        response1Data = json.loads(response1.data)
        print(response1Data)
        self.assertEqual(response1Data, {"message": {"eventID": ["Not a valid UUID."]}})

        response2 = self.getEvent(c, uuid.uuid4().hex)
        self.assert400(response2)

        response2Data = json.loads(response2.data)

        print(response2Data)

        self.assertEqual(response2Data, {"message": {"eventID": ["That Event ID does not exist"]}})


