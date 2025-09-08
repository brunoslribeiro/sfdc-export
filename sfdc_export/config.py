import os
from dotenv import load_dotenv

load_dotenv()

SFDC_MYORG = os.getenv("SFDC_MYORG")
SFDC_MYAPI = os.getenv("SFDC_MYAPI")
SFDC_CLIENT_ID = os.getenv("SFDC_CLIENT_ID")
SFDC_CLIENT_SECRET = os.getenv("SFDC_CLIENT_SECRET")
SFDC_USERNAME = os.getenv("SFDC_USERNAME")
SFDC_PASSWORD = os.getenv("SFDC_PASSWORD")
SFDC_QUERY = os.getenv("SFDC_QUERY")
SFDC_DIRECTORY = os.getenv("SFDC_DIRECTORYFILES", "./output")