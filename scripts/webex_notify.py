import os
import requests

token = os.environ.get("WEBEX_TOKEN")
room_id = os.environ.get("WEBEX_ROOM_ID")
status = os.environ.get("BUILD_STATUS", "UNKNOWN")
build_url = os.environ.get("BUILD_URL", "")
build_number = os.environ.get("BUILD_NUMBER", "")

if not token or not room_id:
    raise SystemExit("Missing WEBEX_TOKEN or WEBEX_ROOM_ID")

message = f"Jenkins build #{build_number} is {status}\n{build_url}"

resp = requests.post(
    "https://webexapis.com/v1/messages",
    headers={"Authorization": f"Bearer {token}"},
    json={"roomId": room_id, "text": message}
)
resp.raise_for_status()
print("Sent Webex notification.")
