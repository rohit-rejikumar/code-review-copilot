import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

def review_diff(diff_text):

    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-15-preview",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    prompt = f"""
You are a senior code reviewer.

Review this GitHub pull request diff.

Focus on:
- Bugs
- Security issues
- Code quality
- Missing error handling

Diff:

{diff_text}

Provide concise review comments.
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content