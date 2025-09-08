import requests
from sfdc_export import config
from sfdc_export.logger import log

def authenticate():
    log("🔐 Authenticating with Salesforce...")
    response = requests.post(config.SFDC_MYORG, data={
        "grant_type": "password",
        "client_id": config.SFDC_CLIENT_ID,
        "client_secret": config.SFDC_CLIENT_SECRET,
        "username": config.SFDC_USERNAME,
        "password": config.SFDC_PASSWORD
    })

    if response.status_code != 200:
        log(f"❌ Authentication error: {response.text}")
        raise SystemExit()

    data = response.json()
    return data["access_token"], data["instance_url"]