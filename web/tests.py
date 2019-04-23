import unittest
from io import BytesIO
import boto3
import requests

from app import app

from credentials import aws_access_key_id, aws_secret_access_key

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
        data = {'file': (BytesIO(b'my file content'), 'test_file.jpg')}
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
        data = {'file' : (BytesIO(b'my file content'), 'test_file.exe')}
        response = self.app.post('/', data=data,
                                follow_redirects=True,
                                content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)

    def test_upload_empty_name(self):
        data = dict(file=(BytesIO(b'my file content'), ''))
        response = self.app.post('/', data=data,
                                follow_redirects=True,
                                content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)

    def test_upload_file_too_large(self):
        data = {'file' : (BytesIO(bytearray(11 * 1024 * 1024)), 'too_big.jpg')}
        response = self.app.post('/', data=data,
                                follow_redirects=True,
                                content_type='multipart/form-data')
        self.assertEqual(response.status_code, 413)

    """ UPLOAD TESTS """

    def test_if_file_exists_files(self):
        file_content = BytesIO(b'my file content')
        data = {'file': (file_content, 'test_file.jpg')}
        response = self.app.post('/', data=data,
                                 follow_redirects=True,
                                 content_type='multipart/form-data')

        # test json response
        self.assertEqual("filename" in response.json, True)
        self.assertEqual("url" in response.json, True)

        # test if file exists on s3
        file_name = response.json['filename']
        s3 = boto3.client('s3',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)
        aws_response = s3.list_objects(Prefix='uploads/{}'.format(file_name), Bucket='upload-api-task')
        result = "Contents" in aws_response
        self.assertEqual(result, True)

        # test url
        s = requests.session()
        img_url_response = s.get(response.json['url'])
        self.assertEqual(img_url_response.status_code, 200)



if __name__ == "__main__":
    unittest.main()
