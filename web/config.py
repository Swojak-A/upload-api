

class BaseConfig(object):
	SECRET_KEY = 'hi'


	# FILE SETTINGS
	UPLOAD_FOLDER = 'uploads'
	ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
	MAX_CONTENT_LENGTH = 10 * 1024 * 1024