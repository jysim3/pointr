import unittest
from app import app
from tests.utils import fetch
from pprint import pprint
from nose2.tools import params
from datetime import datetime, timezone
import json
import dateutil.parser

class TestEvents(unittest.TestCase):

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
        initialData = {
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

        response = fetch(c, "POST", "/api/rework/event", data=initialData)

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        id = data['id']

        response = fetch(c, "GET", "/api/rework/event", queries={
            "eventID": id
        })

        returnedData = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset(initialData, returnedData)

    def testPatchEvent(self):
        pass

    def testGet(self):
        c = app.test_client()
        response = fetch(c, "GET", "/api/rework/event/test")
        pprint(response.data)
