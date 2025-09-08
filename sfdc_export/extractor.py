import requests
import csv
import json
from io import StringIO
import os
from sfdc_export import config
from sfdc_export.logger import log

def extract_results(token: str, instance_url: str, job_id: str):
    headers = { "Authorization": f"Bearer {token}" }
    locator = None
    chunk = 0
    total = 0
    output_file = os.path.join(config.SFDC_DIRECTORY, "result.jsonl")
    os.makedirs(config.SFDC_DIRECTORY, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        while True:
            url = f"{instance_url}/services/data/{config.SFDC_MYAPI}/jobs/query/{job_id}/results"
            if locator:
                url += f"?locator={locator}"

            response = requests.get(url, headers=headers)
            response.encoding = 'utf-8'

            if response.status_code != 200:
                log(f"❌ Error fetching chunk: {response.text}")
                raise SystemExit()

            reader = csv.DictReader(StringIO(response.text))
            records = list(reader)

            for row in records:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")

            chunk += 1
            total += len(records)
            log(f"📦 Chunk {chunk}: {len(records)} records converted")

            locator = response.headers.get("Sforce-Locator")
            if not locator or locator == "null":
                break

    log(f"✅ Extraction completed successfully.")
    log(f"📁 Total: {total} records in {chunk} chunks")
    log(f"📄 JSONL file saved at: {output_file}")