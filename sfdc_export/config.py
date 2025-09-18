import os
from dotenv import load_dotenv

load_dotenv()

SFDC_MYORG = os.getenv("SFDC_MYORG")
SFDC_MYAPI = os.getenv("SFDC_MYAPI")
SFDC_CLIENT_ID = os.getenv("SFDC_CLIENT_ID")
SFDC_CLIENT_SECRET = os.getenv("SFDC_CLIENT_SECRET")
SFDC_USERNAME = os.getenv("SFDC_USERNAME")
SFDC_PASSWORD = os.getenv("SFDC_PASSWORD")
SFDC_GRANT_TYPE = os.getenv("SFDC_GRANT_TYPE", "password")
SFDC_CLIENT_AUDIENCE = os.getenv("SFDC_CLIENT_AUDIENCE")
# Query and output directory are now provided via command-line arguments
