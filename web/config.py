import os

class BaseConfig(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = True

    """ DB """
    DB_NAME = os.environ['DB_KEY']
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}'.format(DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    """ FILE SETTINGS """
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

