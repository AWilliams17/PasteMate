import unittest
import PasteMate
import requests
from sys import getdefaultencoding
from json import loads


class PingTestRequests(unittest.TestCase):
    def test_ping(self):
        response = requests.get('http://localhost/api/ping')
        self.assertEqual(response.json(), {'ping': 'Pong!'})

"""
class PingTestApp(unittest.TestCase):
    def setUp(self):
        PasteMate.flask_app.testing = True
        self.jwt_loaders = PasteMate.flask_app.test_client()

    def test_ping(self):
        response = self.jwt_loaders.get('/ping')
        self.assertEqual(
            loads(response.get_data().decode(getdefaultencoding())),
            {'ping': 'Pong!'}
        )
"""

if __name__ == '__main__':
    unittest.main()
