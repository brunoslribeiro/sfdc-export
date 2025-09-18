# SFDC Bulk Export

This tool connects to Salesforce using the Bulk API 2.0, runs a SOQL query, and exports the results in newline-delimited JSON (JSONL) or CSV format.

## How to run

1. Create a `.env` file with your Salesforce credentials (see `.env.example`).
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run:
   ```
   python main.py --query "SELECT Id FROM Account" [--format jsonl|csv] [--directory output]
   ```

## Authentication configuration

The application supports the Salesforce OAuth password grant (default) and the
client credentials flow. Configure the `.env` file with the following
variables:

- `SFDC_MYORG`: OAuth token endpoint (for example,
  `https://login.salesforce.com/services/oauth2/token`).
- `SFDC_MYAPI`: Bulk API version path (for example, `v59.0`).
- `SFDC_CLIENT_ID` and `SFDC_CLIENT_SECRET`: Connected app credentials.
- `SFDC_GRANT_TYPE`: Optional. Use `password` (default) or
  `client_credentials`.
- `SFDC_USERNAME` and `SFDC_PASSWORD`: Required only when `SFDC_GRANT_TYPE` is
  `password`.
- `SFDC_CLIENT_AUDIENCE`: Required only when `SFDC_GRANT_TYPE` is
  `client_credentials`.

## Comparing Exported Files

Use `compare.py` to check if a given column value appears in two CSV or JSONL files.

```
python compare.py file1.csv file2.jsonl --column Id --output result.csv
```

The script reads the primary file (first argument) and adds a `status` column with
either `FOUND` or `NOT FOUND` depending on whether the value from the specified
column exists in the secondary file.

To limit the result file to only rows with a particular status, use the
`--filter` option:

```
python compare.py file1.csv file2.jsonl --column Id --output result.csv --filter FOUND
```

Valid filters are `FOUND` and `NOT_FOUND`.
