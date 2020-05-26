from json import dumps
import unittest

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

    def assert400(self, response):
        try:
            self.assertEqual(response.status_code, 400)
        except AssertionError as e:
            print("Response returned:")
            print(str(response.data))
            raise AssertionError

def fetch(c, method, route, queries=None, data=None, headers=None):
    if (method == 'GET'):
        return c.get(route + query(queries))
    elif (method == 'POST'):
        return c.post(route, data=dumps(data), content_type='application/json')
    elif (method == 'PATCH'):
        return c.patch(route + query(queries), data=dumps(data), content_type='application/json')
    elif (method == 'DELETE'):
        return c.delete(route + query(queries))
    elif (method == 'PUT'):
        return c.put(route + query(queries), data=data)
    else:
        print("INVALID METHOD")

def query(data):
    if data == None:
        return ""
    queries = []
    for (k,v) in data.items():
        queries.append(k + "=" + v)
    return "?" + "&".join(queries)