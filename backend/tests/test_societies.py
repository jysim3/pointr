import unittest
from app import app
from tests.utils import fetch, PointrTest
from pprint import pprint
from nose2.tools import params
from datetime import datetime, timezone
import json
import dateutil.parser
import uuid

class TestSocieties(PointrTest):

    # Test to create a society that just has the barebone requirements
    def testCreateValidSociety(self):
        c = app.test_client()

        # Data to send
        initialData = {
            "name": "Gamersoc",
            "type": 1,
            "tags": [1]
        }

        response = fetch(c, "POST", "/society", data=initialData)
        self.assertOK(response)
        payload =  json.loads(response.data)

        # Data from GET
        returnedData = self.getValidSociety(c, payload['data']['id'])

        self.assertDictContainsSubset(initialData, returnedData)

    # Attempts to create a society and 
    def testPatchValidSociety(self):
        c = app.test_client()

        societyID = self.postValidSociety(c, "Gamersoc")

        societyData = self.getValidSociety(c, societyID)

        patchData = {
            "description": "We are Gamersoc",
            "previewDescription": "MINECRAFTERS ONLY"
        }

        response = fetch(c, "PATCH", "/society", data=patchData, queries={
            "societyID": societyID
        })
        self.assertOK(response)
        payload = json.loads(response.data)
        returnedData = payload['data']

        self.assertDictContainsSubset(patchData, returnedData)
        
    def testInvalidSocietyID(self):
        c = app.test_client()

        id = self.postValidSociety(c, "Gamersoc")

        response = self.getSociety(c, "1")
        self.assert400(response)
        payload = json.loads(response.data)
        self.assertContains(payload, "message", {"societyID": ["Not a valid UUID."]})

        response = self.getSociety(c, uuid.uuid4().hex)
        self.assert400(response)
        payload = json.loads(response.data)
        self.assertContains(payload, "message", {"societyID": ["That Society ID does not exist"]})

    def testDeleteSociety(self):
        c = app.test_client()
        id = self.postValidSociety(c, "Gamersoc")
        response = fetch(c, "DELETE", "/society", queries={
            "societyID": id
        })
        self.assertOK(response)
        payload = json.loads(response.data)
        self.assertEqual(payload, {'status': 'success'})

        response = self.getEvent(c, id)
        payload = json.loads(response.data)
        
        self.assertEqual(payload, {"message": {"eventID": ["That Event ID does not exist"]}})
