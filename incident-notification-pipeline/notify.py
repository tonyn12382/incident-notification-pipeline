import json
import requests
import datetime

WEBEX_TOKEN = "YWE0ZDc5MjEtOTljMy00NjViLWI1MjItMGM0MGNhM2M4ZDUwYWMxMmQyODEtNTg1_P0A1_e58072af-9d57-4b13-abf7-eb3b506c964d"
ROOM_ID = "09e40a50-8590-11f0-a6a6-01d219d77e7a"
SHEET_URL = "https://script.google.com/macros/s/AKfycbyspr748M5LtC2gP6NtN2KYIxHZpPbr8OdNM9SvA5UCu4fxnIp0uzSMo30yirTIA9xUYA/exec"

def read_results():
    with open("results.json") as f:
        data = json.load(f)

    passed = data["summary"].get("passed", 0)
    failed = data["summary"].get("failed", 0)
    status = "SUCCESS" if failed == 0 else "FAILED"

    return status, passed, failed

def send_webex(status, passed, failed):
    message = f"Build Status: {status}\nPassed: {passed}\nFailed: {failed}"

    requests.post(
        "https://webexapis.com/v1/messages",
        headers={"Authorization": f"Bearer {WEBEX_TOKEN}"},
        json={"roomId": ROOM_ID, "text": message}
    )

def log_to_sheet(status, passed, failed):
    payload = {
        "status": status,
        "passed": passed,
        "failed": failed,
        "timestamp": str(datetime.datetime.now())
    }

    requests.post(SHEET_URL, json=payload)

if __name__ == "__main__":
    status, passed, failed = read_results()
    send_webex(status, passed, failed)
    log_to_sheet(status, passed, failed)
