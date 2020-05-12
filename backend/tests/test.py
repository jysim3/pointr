import sys
sys.path.append("../")

import pytest
from app import app

def login(username, password):
    return app.test_client().post('/api/auth/login', data=dict(
        zID=username,
        password=password
    ))

def test_example():
    response = login("z5161616", "mamamama")
    assert b'Malformed Request' in response.data
    assert response.status_code == 400