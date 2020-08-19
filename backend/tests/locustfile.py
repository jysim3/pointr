"""
    Load testing Flask with locust
"""

from random import choices
from string import digits
from locust import HttpUser, task, between

class TestingUser(HttpUser):
    # Make a new request every 0.25 to 0.5 seconds
    wait_time = between(0.25, 0.5)

    @task
    def registration(self):
        payload = {
            "zID": f"z0{''.join(choices(digits, k=6))}",
            "password": "00000000",
            "firstName": "Steven",
            "lastName": "Shen",
            "isArc": True
        }
        
        self.client.post("/api/auth/register", json=payload)

    @task
    def login(self):
        """
        TODO: Load test for the login route
        """
        pass

    @task
    def attend(self):
        """
        TODO: Load test for signing event attendance
        """
        pass

    @task
    def join(self):
        """
        TODO: Load test for joining societies
        """
        pass

    @task
    def checkEvent(self):
        """
        TODO: Load test for checking an event's information
        """
        pass

    @task
    def checkSoc(self):
        """
        TODO: Load test for checking a society's information
        """
        pass