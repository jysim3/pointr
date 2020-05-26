import unittest
from app import app
from tests.utils import fetch
from pprint import pprint
from nose2.tools import params
from datetime import datetime, timezone
import json
import dateutil.parser

class PointrTest(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        pass

    def tearDown(self):
        pass

    def assertOK(self, response):
        try:
            self.assertEqual(response.status_code, 200)
        except AssertionError as e:
            print("Response returned:")
            print(str(response.data))
            raise AssertionError


class TestEvents(PointrTest):

    def setUp(self):
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        pass

    def tearDown(self):
        pass

    @params({})
    def test400(self, value):
        c = app.test_client()
        response = fetch(c, "POST", "/api/rework/event", data=value)
        self.assertEqual(response.status_code, 400)

    def testUnawareDatetime(self):
        pass

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
        id = data['id']

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
        id = data['id']

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
