import jwt
import time
import requests

APP_ID = "4052189"

with open("private-key.pem", "r") as f:
    private_key = f.read()

payload = {
    "iat": int(time.time()) - 60,   # 1 minute ago
    "exp": int(time.time()) + 540,  # 9 minutes from now
    "iss": APP_ID,
}

jwt_token = jwt.encode(payload, private_key, algorithm="RS256")

headers = {
    "Authorization": f"Bearer {jwt_token}",
    "Accept": "application/vnd.github+json",
}

response = requests.get(
    "https://api.github.com/app/installations",
    headers=headers,
)

print("Status:", response.status_code)
print(response.json())