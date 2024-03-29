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

    def testCreateEvent(self):
        c = self.c

        # Data to send
        initialData = self.getMockEventData()
        societyID = self.postValidSociety(c, "Gamersoc")

        response = fetch(c, "POST", "/event", data=initialData, queries={
            "societyID": societyID
        })

        self.assertOK(response)
        payload =  json.loads(response.data)

        # Data from GET
        returnedData = self.getValidEvent(c, payload['data']['id'])

        self.assertDictContainsSubset(initialData, returnedData)

    def testEventPatch(self):
        c = self.c

        # make Event
        id = self.postValidEvent(c)
        initialData = self.getEvent(c, id)

        # send patch
        patchData = {
            "name": "Gamersoc Minecraft Night: The reckoning",
            "start": str(datetime.now(timezone.utc)),
            "end": str(datetime.now(timezone.utc)),
            "tags": [0, 1]
        }

        patchResponse = fetch(c, "PATCH", "/event", data=patchData, queries={
            "eventID": id
        })
        self.assertOK(patchResponse)

        patchReturnedPayload = json.loads(patchResponse.data)
        patchReturnedData = patchReturnedPayload['data']

        returnedData = self.getValidEvent(c, id)

        # Whatever the patch returned and the get returned should be the same
        self.assertDictEqual(patchReturnedData, returnedData)

        # Whatever the get returned should contain the patch
        self.assertDictContainsSubset(patchData, returnedData)

    def testEventInvalidID(self):
        c = self.c

        id = self.postValidEvent(c)

        response1 = self.getEvent(c, "1")
        self.assert400(response1)
        
        # FIXME: Event IDs are no longer UUIDs
        '''
        response1Data = json.loads(response1.data)

        self.assertEqual(response1Data, {"message": {"eventID": ["Not a valid UUID."]}})
        '''

        from random import choices
        from string import ascii_uppercase, digits
        response2 = self.getEvent(c, ''.join(choices(ascii_uppercase + digits, k=5)))
        self.assert400(response2)

        response2Data = json.loads(response2.data)

        self.assertEqual(response2Data, {"message": {"eventID": ["That Event ID does not exist"]}})


    def testEventPostInvalidSocietyID(self):
        c = self.c

        self.postValidSociety(c, "Gamersoc")

        response = fetch(c, 'POST', '/event', data=self.getMockEventData(), queries={
            'societyID': "1"
        })
        self.assert400(response)
        payload = json.loads(response.data)
        self.assertContains(payload, "message", {"societyID": ["Not a valid UUID."]})

        response = fetch(c, 'POST', '/event', data=self.getMockEventData(), queries={
            'societyID': uuid.uuid4().hex
        })
        self.assert400(response)
        payload = json.loads(response.data)
        self.assertContains(payload, "message", {"societyID": ["That Society ID does not exist"]})


    def testDeleteEvent(self):
        c = self.c
        societyID = self.postValidSociety(c, "Gamersoc")
        id = self.postValidEvent(c, societyID)
        response = fetch(c, "DELETE", "/event", queries={
            "eventID": id
        })
        self.assertOK(response)
        payload = json.loads(response.data)
        self.assertEqual(payload, {'status': 'success'})

        response = self.getEvent(c, id)
        payload = json.loads(response.data)
        
        self.assertEqual(payload, {"message": {"eventID": ["That Event ID does not exist"]}})
