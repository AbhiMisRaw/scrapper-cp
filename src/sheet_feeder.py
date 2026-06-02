import jwt
import time
import json
import httpx
from football_extractor import payload as data


spreadsheet_id = "1gIq02lb9KmQlhORvfiDOHQJpcM3o-czKtmXT8uNUosU"

SHEETS_URL = (
    f"https://sheets.googleapis.com/v4/spreadsheets/"
    f"{spreadsheet_id}/values/Sheet1!A:A:append"
    "?valueInputOption=RAW"
)


with open("./creds.json") as f:
    creds = json.load(f)

now = int(time.time())
payload = {
    "iss": creds["client_email"],
    "scope": "https://www.googleapis.com/auth/spreadsheets",
    "aud": "https://oauth2.googleapis.com/token",
    "iat": now,
    "exp": now + 3600
}

jwt_token = jwt.encode(
    payload,
    creds["private_key"],
    algorithm="RS256"
)

print("Sending JWT...")
response = httpx.post(
    "https://oauth2.googleapis.com/token",
    data={
        "grant_type":
        "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt_token
    }
)

access_token = response.json()["access_token"]
print(f"Access Token : ", access_token)

print("DATA ==>", data)
x = httpx.post(
    SHEETS_URL,
    headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    },
    json=data
)
print(x)