import requests
import csv
import json
from io import StringIO
import os

from sfdc_export import config
from sfdc_export.logger import log


def extract_results(
    token: str,
    instance_url: str,
    job_id: str,
    output_format: str = "jsonl",
    output_dir: str = "./output",
):
    headers = {"Authorization": f"Bearer {token}"}
    locator = None
    chunk = 0
    total = 0
    extension = "csv" if output_format == "csv" else "jsonl"
    output_file = os.path.join(output_dir, f"result.{extension}")
    os.makedirs(output_dir, exist_ok=True)

    file_kwargs = {"newline": ""} if output_format == "csv" else {}

    with open(output_file, "w", encoding="utf-8", **file_kwargs) as f:
        writer = None
        while True:
            url = f"{instance_url}/services/data/{config.SFDC_MYAPI}/jobs/query/{job_id}/results"
            if locator:
                url += f"?locator={locator}"

            response = requests.get(url, headers=headers)
            response.encoding = "utf-8"

            if response.status_code != 200:
                log(f"❌ Error fetching chunk: {response.text}")
                raise SystemExit()

            reader = csv.DictReader(StringIO(response.text))
            records = list(reader)

            if output_format == "csv":
                if writer is None:
                    writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
                    writer.writeheader()
                writer.writerows(records)
            else:
                for row in records:
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")

            chunk += 1
            total += len(records)
            log(f"📦 Chunk {chunk}: {len(records)} records converted")

            locator = response.headers.get("Sforce-Locator")
            if not locator or locator == "null":
                break

    log("✅ Extraction completed successfully.")
    log(f"📁 Total: {total} records in {chunk} chunks")
    log(f"📄 {output_format.upper()} file saved at: {output_file}")
