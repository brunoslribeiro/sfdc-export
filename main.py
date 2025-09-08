import argparse

from sfdc_export.auth import authenticate
from sfdc_export.job import create_job, wait_for_completion
from sfdc_export.extractor import extract_results


def parse_args():
    parser = argparse.ArgumentParser(description="SFDC Bulk Export")
    parser.add_argument(
        "--format",
        choices=["jsonl", "csv"],
        default="jsonl",
        help="Output format (jsonl or csv)",
    )
    return parser.parse_args()

def main():
    args = parse_args()
    token, instance_url = authenticate()
    job_id = create_job(token, instance_url)
    wait_for_completion(token, instance_url, job_id)
    extract_results(token, instance_url, job_id, output_format=args.format)

if __name__ == "__main__":
    main()
