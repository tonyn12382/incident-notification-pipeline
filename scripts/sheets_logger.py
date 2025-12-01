import os, sys, datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

def append_log(sheet_id, tab_name, values):
    creds_path = os.environ.get("GCP_SA_JSON_PATH")
    if not creds_path or not os.path.exists(creds_path):
        print("Service account JSON not found at GCP_SA_JSON_PATH", file=sys.stderr)
        sys.exit(1)

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = service_account.Credentials.from_service_account_file(creds_path, scopes=scopes)
    service = build("sheets", "v4", credentials=creds)

    body = {"values": [values]}
    range_name = f"{tab_name}!A:Z"
    service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range=range_name,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()

if __name__ == "__main__":
    sheet_id = os.environ.get("SHEET_ID", "")
    tab_name = os.environ.get("SHEET_TAB", "Logs")
    build_number = os.environ.get("BUILD_NUMBER", "")
    build_url = os.environ.get("BUILD_URL", "")
    status = os.environ.get("BUILD_STATUS", "UNKNOWN")

    # Read log excerpt written by Jenkins
    log_excerpt = ""
    if os.path.exists("log_excerpt.txt"):
        with open("log_excerpt.txt", "r", encoding="utf-8", errors="ignore") as f:
            log_excerpt = f.read()
    if len(log_excerpt) > 5000:  # truncate for readability
        log_excerpt = log_excerpt[:5000] + "\n...[truncated]"

    now = datetime.datetime.utcnow().isoformat()
    row = [now, build_number, status, build_url, log_excerpt]
    append_log(sheet_id, tab_name, row)
    print("Appended row to Google Sheet.")
