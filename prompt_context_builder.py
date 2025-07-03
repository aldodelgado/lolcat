import os
import re

def extract_keywords(issue_body):
    # Very simple keyword heuristic: you can replace with LLM-based tagging later
    return re.findall(r'\b\w+\.py\b', issue_body)

def find_files(repo_dir, keywords):
    matches = []
    for root, _, files in os.walk(repo_dir):
        for f in files:
            if f.endswith(".py") and any(k in f for k in keywords):
                matches.append(os.path.join(root, f))
    return matches

def build_context_snippets(file_paths, max_lines=40):
    snippets = []
    for path in file_paths:
        try:
            with open(path, "r") as f:
                lines = f.readlines()
                snippet = "".join(lines[:max_lines])
                snippets.append(f"### File: {path}\n{snippet}")
        except Exception as e:
            print(f"⚠️ Skipping {path}: {e}")
    return "\n\n".join(snippets)

def create_prompt_context(issue_body, repo_dir="."):
    keywords = extract_keywords(issue_body)
    matched_files = find_files(repo_dir, keywords)
    context = build_context_snippets(matched_files)
    return context
