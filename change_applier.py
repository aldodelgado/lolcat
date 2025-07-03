import openai
import subprocess
import os
import tempfile
from issue_handler import get_latest_issue
from prompt_context_builder import create_prompt_context

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_patch(issue_body, context):
    prompt = f"""You are an AI software engineer. Given the issue below and the current code context, generate a patch in unified diff format (.patch).

### ISSUE:
{issue_body}

### CONTEXT:
{context}

### PATCH:
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

def apply_patch(patch_content, repo_dir="."):
    patch_file = os.path.join(repo_dir, "temp.patch")
    with open(patch_file, "w") as f:
        f.write(patch_content)
    subprocess.run(["git", "apply", patch_file], check=True)

def semantic_check():
    try:
        subprocess.run(["prompt", "pack", "orig.prompt"], check=True)
        subprocess.run(["prompt", "pack", "edited.prompt"], check=True)
        result = subprocess.run(
            ["prompt", "diff", "orig.prompt.pp.json", "edited.prompt.pp.json", "--threshold", "0.8", "--json"],
            capture_output=True, text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Semantic diff failed: {e}")
        return False

def run_tests_and_lint():
    return (
        subprocess.call(["pytest"]) == 0 and
        subprocess.call(["flake8", "."]) == 0
    )

def main():
    issue = get_latest_issue()
    if not issue:
        print("No issue found.")
        return

    context = create_prompt_context(issue["body"])

    MAX_ATTEMPTS = 3
    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"🔁 Attempt {attempt} of {MAX_ATTEMPTS}")
        patch = generate_patch(issue["body"], context)

        try:
            subprocess.run(["git", "checkout", "-b", f"auto-fix-attempt-{attempt}"], check=True)
            apply_patch(patch)

            if not semantic_check():
                print("❌ Semantic check failed.")
                continue

            if not run_tests_and_lint():
                print("❌ Tests or linting failed.")
                continue

            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"Auto-patch from issue #{issue['number']}"], check=True)
            subprocess.run(["git", "push", "-u", "origin", f"auto-fix-attempt-{attempt}"], check=True)
            print("✅ Patch successfully pushed.")
            return
        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed: {e}")
            subprocess.run(["git", "reset", "--hard"], check=True)

    print("❌ All attempts failed.")

if __name__ == "__main__":
    main()
