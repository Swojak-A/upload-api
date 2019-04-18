from credentials import db_key

class BaseConfig(object):
    SECRET_KEY = 'hi'

    #DB
    SQLALCHEMY_DATABASE_URI = db_key
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # FILE SETTINGS
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024