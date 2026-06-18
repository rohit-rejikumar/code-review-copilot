import jwt
import time
import requests

APP_ID = "4052189"
INSTALLATION_ID = "140261114"

with open("private-key.pem", "r") as f:
    private_key = f.read()


def post_comment(pr_number, comment_text):

    payload = {
        "iat": int(time.time()) - 60,
        "exp": int(time.time()) + 540,
        "iss": APP_ID,
    }

    jwt_token = jwt.encode(
        payload,
        private_key,
        algorithm="RS256"
    )

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json",
    }

    token_response = requests.post(
        f"https://api.github.com/app/installations/{INSTALLATION_ID}/access_tokens",
        headers=headers,
    )

    token = token_response.json()["token"]

    repo_headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }

    response = requests.post(
        "https://api.github.com/repos/rohit-rejikumar/code-review-copilot/issues/"
        f"{pr_number}/comments",
        headers=repo_headers,
        json={
            "body": comment_text
        }
    )

    print("Status:", response.status_code)
    print(response.json())