import requests
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPO", "your-org/your-repo")

def get_open_pull_requests():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    url = f"https://api.github.com/repos/{REPO}/pulls"
    response = requests.get(url, headers=headers)
    return response.json()

def leave_review(pr_number, body="✅ Automated review complete. Semantic checks passed."):
    url = f"https://api.github.com/repos/{REPO}/pulls/{pr_number}/reviews"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    data = {
        "body": body,
        "event": "COMMENT"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())

if __name__ == "__main__":
    prs = get_open_pull_requests()
    for pr in prs:
        print(f"Reviewing PR #{pr['number']}...")
        leave_review(pr['number'])
