import requests
import time
from sfdc_export import config
from sfdc_export.logger import log

def create_job(token: str, instance_url: str, query: str) -> str:
    log("🚀 Creating query job...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(
        f"{instance_url}/services/data/{config.SFDC_MYAPI}/jobs/query",
        headers=headers,
        json={"operation": "query", "query": query}
    )

    if response.status_code != 200:
        log(f"❌ Failed to create job: {response.text}")
        raise SystemExit()

    job_id = response.json()["id"]
    log(f"✅ Job created with ID: {job_id}")
    return job_id

def wait_for_completion(token: str, instance_url: str, job_id: str):
    headers = { "Authorization": f"Bearer {token}" }
    wait_time = 3
    log("⏳ Waiting for job completion...")

    while True:
        response = requests.get(f"{instance_url}/services/data/{config.SFDC_MYAPI}/jobs/query/{job_id}", headers=headers)
        state = response.json()["state"]
        log(f"⌛ Current job state: {state}")

        if state == "JobComplete":
            log("✅ Job completed successfully.")
            time.sleep(5)
            break
        elif state == "Failed":
            log("❌ Job failed.")
            raise SystemExit()

        time.sleep(wait_time)
        wait_time = min(wait_time + 2, 15)