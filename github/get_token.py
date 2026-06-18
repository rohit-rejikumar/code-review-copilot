import jwt
import time
import requests

APP_ID = "4052189"
INSTALLATION_ID = "140261114"

with open("private-key.pem", "r") as f:
    private_key = f.read()

payload = {
    "iat": int(time.time()) - 60,
    "exp": int(time.time()) + 540,
    "iss": APP_ID,
}

jwt_token = jwt.encode(payload, private_key, algorithm="RS256")

headers = {
    "Authorization": f"Bearer {jwt_token}",
    "Accept": "application/vnd.github+json",
}

response = requests.post(
    f"https://api.github.com/app/installations/{INSTALLATION_ID}/access_tokens",
    headers=headers,
)

print("Status:", response.status_code)

data = response.json()

print("Token created:", "token" in data)

if "token" in data:
    print(data["token"][:30] + "...")