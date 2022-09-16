from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

Auth0_Domain = os.environ.get('AUTH0_DOMAIN')
Audience = os.environ.get('API_AUDIENCE')
Algorithm = os.environ.get('ALGORITHM')
Clientid = os.environ.get('CLIENTID')
Url = os.environ.get('URL')
