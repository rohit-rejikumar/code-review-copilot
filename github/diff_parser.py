import jwt
import time
import requests

APP_ID = "4052189"
INSTALLATION_ID = "140261114"
OWNER = "rohit-rejikumar"
REPO = "code-review-copilot"

with open("private-key.pem", "r") as f:
    private_key = f.read()


def get_pr_diff(pr_number):

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

    token_response = requests.post(
        f"https://api.github.com/app/installations/{INSTALLATION_ID}/access_tokens",
        headers=headers,
    )

    token = token_response.json()["token"]

    repo_headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }

    files = requests.get(
        f"https://api.github.com/repos/{OWNER}/{REPO}/pulls/{pr_number}/files",
        headers=repo_headers,
    )

    diff_text = ""

    for file in files.json():
        diff_text += f"\nFile: {file['filename']}\n"
        diff_text += file.get("patch", "No patch available")
        diff_text += "\n"

    return diff_text