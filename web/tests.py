import unittest
from io import BytesIO

from app import app


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def test_index_get(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_index_post(self):
        mock_json = {"name" : "Test_name"}
        response = self.app.post('/', json=mock_json)
        self.assertEqual(response.status_code, 201)

    def test_index_post_no_json(self):
        response = self.app.post('/', data=None)
        self.assertEqual(response.status_code, 400)



if __name__ == "__main__":
	unittest.main()