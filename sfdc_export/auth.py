import requests

from sfdc_export import config
from sfdc_export.logger import log


def _build_auth_payload() -> dict:
    """Create the payload for the authentication request."""
    grant_type = (config.SFDC_GRANT_TYPE or "password").strip().lower()
    payload = {
        "grant_type": grant_type,
        "client_id": config.SFDC_CLIENT_ID,
        "client_secret": config.SFDC_CLIENT_SECRET,
    }

    if grant_type == "password":
        if not (config.SFDC_USERNAME and config.SFDC_PASSWORD):
            log("❌ SFDC_USERNAME and SFDC_PASSWORD are required for password grant type.")
            raise SystemExit()
        payload.update(
            {
                "username": config.SFDC_USERNAME,
                "password": config.SFDC_PASSWORD,
            }
        )
    elif grant_type == "client_credentials":
        if not config.SFDC_CLIENT_AUDIENCE:
            log("❌ SFDC_CLIENT_AUDIENCE is required for client_credentials grant type.")
            raise SystemExit()
        payload["audience"] = config.SFDC_CLIENT_AUDIENCE
    else:
        log(f"❌ Unsupported SFDC_GRANT_TYPE: {config.SFDC_GRANT_TYPE}")
        raise SystemExit()

    return payload


def authenticate():
    log("🔐 Authenticating with Salesforce...")
    payload = _build_auth_payload()
    response = requests.post(config.SFDC_MYORG, data=payload)

    if response.status_code != 200:
        log(f"❌ Authentication error: {response.text}")
        raise SystemExit()

    data = response.json()
    try:
        return data["access_token"], data["instance_url"]
    except KeyError:
        log(f"❌ Unexpected authentication response: {data}")
        raise SystemExit()
