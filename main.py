from sfdc_export.auth import authenticate
from sfdc_export.job import create_job, wait_for_completion
from sfdc_export.extractor import extract_results

def main():
    token, instance_url = authenticate()
    job_id = create_job(token, instance_url)
    wait_for_completion(token, instance_url, job_id)
    extract_results(token, instance_url, job_id)

if __name__ == "__main__":
    main()