# Default Configuration (inheriting from object is not necessary in python3)
class Config(object):
	# If modifying these scopes, delete your previously saved credentials
	# at ~/.credentials/SAVED_CREDENTIAL_NAME
	SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
	CLIENT_SECRET_FILE = 'client_secret.json'
	APPLICATION_NAME = 'Receipts API'
	SAVED_CREDENTIAL_NAME = 'drive-python-receipts.json'
