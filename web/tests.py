import unittest
from io import BytesIO

from app import app


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

    """ GET test """

    def test_index_get(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    """ POST tests """

    # tests from earlier version
    # def test_index_post(self):
    #     mock_json = {"name" : "Test_name"}
    #     response = self.app.post('/', json=mock_json)
    #     self.assertEqual(response.status_code, 201)
    #
    # def test_index_post_no_json(self):
    #     response = self.app.post('/', data=None)
    #     self.assertEqual(response.status_code, 400)

    def test_upload(self):
        data = {'file': (BytesIO(b'my file content'), "test_file.jpg")}
        response = self.app.post('/', data=data,
                                 follow_redirects=True,
                                 content_type='multipart/form-data')
        self.assertEqual(response.status_code, 201)

    def test_upload_no_file(self):
        data = {}
        response = self.app.post('/', data=data,
                                 follow_redirects=True,
                                 content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)

    def test_upload_wrong_ext(self):
        data = {'file' : (BytesIO(b'my file content'), "test_file.exe")}
        response = self.app.post('/', data=data,
                                follow_redirects=True,
                                content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)

    def test_upload_empty_name(self):
        data = {'file' : (BytesIO(b'my file content'), "")}
        response = self.app.post('/', data=data,
                                follow_redirects=True,
                                content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)



if __name__ == "__main__":
    unittest.main()
