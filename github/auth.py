import jwt
import time

APP_ID = "4052189"

with open("private-key.pem", "r") as f:
    private_key = f.read()

payload = {
    "iat": int(time.time()),
    "exp": int(time.time()) + 600,
    "iss": APP_ID,
}

token = jwt.encode(payload, private_key, algorithm="RS256")

print("JWT generated successfully!")
print(token[:50] + "...")