import unittest
from io import BytesIO
from PIL import Image
import boto3
import requests

from app import app, db, filename_ext
from models import *

from credentials import aws_access_key_id, aws_secret_access_key



""" HELPER functions """

def create_test_image(filename='test.jpg', size=(500, 500)):
    # size is a tuple of width and height
    file = BytesIO()
    image = Image.new(mode='RGB', size=size, color=(155, 37, 47))
    image.save(file, filename_ext(filename).replace('jpg', 'jpeg')) # PIL only accepts "JPEG" file format
    file.name = filename
    file.seek(0)
    return file



""" TEST CASES """

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
        data = {'file': create_test_image()}
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

    """ UPLOAD tests """

    def test_if_file_exists_files(self):
        original_filename = 'test.jpg'
        file = create_test_image(filename=original_filename)
        data = {'file': file}
        response = self.app.post('/', data=data,
                                 follow_redirects=True,
                                 content_type='multipart/form-data')

        # test json response
        self.assertEqual("filename" in response.json, True)
        self.assertEqual("url" in response.json, True)

        # test if file exists on s3
        filename = response.json['filename']
        s3 = boto3.client('s3',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)
        aws_response = s3.list_objects(Prefix='uploads/{}'.format(filename),
                                       Bucket='upload-api-task')
        result = "Contents" in aws_response
        self.assertEqual(result, True)

        # test url
        s = requests.session()
        img_url_response = s.get(response.json['url'])
        self.assertEqual(img_url_response.status_code, 200)

        # test db values
        testUpload = Upload.query.filter_by(filename=response.json['filename']).one()
        self.assertEqual(response.json['url'], testUpload.url)
        self.assertEqual(original_filename, testUpload.original_filename)
        self.assertEqual(create_test_image(filename=original_filename).read(), testUpload.file)


if __name__ == "__main__":
    unittest.main()
