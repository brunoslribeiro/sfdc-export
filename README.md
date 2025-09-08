# SFDC Bulk Export

This tool connects to Salesforce using the Bulk API 2.0, runs a SOQL query, and exports the results in newline-delimited JSON (JSONL) format.

## How to run

1. Create a `.env` file with your credentials (see `.env.example`)
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run:
   ```
   python main.py
   ```