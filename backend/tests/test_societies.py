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
    def testSocietyValidCreate(self):
        c = self.c

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
    def testSocietyValidPatch(self):
        c = self.c

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
        
    def testSocietyInvalidID(self):
        c = self.c

        id = self.postValidSociety(c, "Gamersoc")

        response = self.getSociety(c, "1")
        self.assert400(response)
        payload = json.loads(response.data)
        self.assertContains(payload, "message", {"societyID": ["Not a valid UUID."]})

        response = self.getSociety(c, uuid.uuid4().hex)
        self.assert400(response)
        payload = json.loads(response.data)
        self.assertContains(payload, "message", {"societyID": ["That Society ID does not exist"]})

    def testSocietyDelete(self):
        c = self.c

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

    def testSocietyDuplicateName(self):
        c = self.c

        response = fetch(c, 'POST', '/society', data=self.getMockSocietyData('Gamersoc'))
        self.assertOK(response)
        
        response = fetch(c, 'POST', '/society', data=self.getMockSocietyData('Gamersoc'))
        payload = json.loads(response.data)

        self.assertContains(payload['message'], 'name', 'A society with that name already exists.')


