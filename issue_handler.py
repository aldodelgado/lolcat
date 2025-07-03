import requests
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPO", "your-org/your-repo")

def get_latest_issue():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    url = f"https://api.github.com/repos/{REPO}/issues?state=open&sort=created&direction=desc"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    issues = response.json()

    if issues:
        issue = issues[0]
        print(f"Issue #{issue['number']}: {issue['title']}")
        return {
            "number": issue["number"],
            "title": issue["title"],
            "body": issue["body"]
        }
    return None

if __name__ == "__main__":
    issue = get_latest_issue()
    print(issue)
