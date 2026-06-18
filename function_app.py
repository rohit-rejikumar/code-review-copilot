import json
import logging
import azure.functions as func

from github.diff_parser import get_pr_diff
from github.reviewer import review_diff
from github.comments import post_comment

app = func.FunctionApp()


@app.route(
    route="github-webhook",
    auth_level=func.AuthLevel.FUNCTION
)
def github_webhook(req: func.HttpRequest) -> func.HttpResponse:

    event = req.headers.get("X-GitHub-Event")

    if event != "pull_request":
        return func.HttpResponse(
            "Ignored",
            status_code=200
        )

    try:
        payload = req.get_json()
    except ValueError:
        payload = {}

    action = payload.get("action")

    if action not in ["opened", "synchronize"]:
        return func.HttpResponse(
            "Ignored",
            status_code=200
        )

    pr_number = payload["pull_request"]["number"]

    logging.info(f"Reviewing PR #{pr_number}")

    diff_text = get_pr_diff(pr_number)

    review = review_diff(diff_text)

    post_comment(pr_number, review)

    return func.HttpResponse(
        "Review completed",
        status_code=200
    )