# src/tools.py
from typing import Optional
import requests
import time

GITHUB_API_README = "https://api.github.com/repos/{owner}/{repo}/readme"
RAW_README = "https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.md"

def fetch_readme_via_api(repo_url: str, timeout: int = 10) -> Optional[str]:
    """
    Try the GitHub API (returns raw content when requested).
    repo_url examples:
        https://github.com/owner/repo
        git@github.com:owner/repo.git
    """
    # Extract owner/repo
    try:
        parts = repo_url.rstrip("/").split("/")
        owner = parts[-2]
        repo = parts[-1].replace(".git", "")
    except Exception:
        return None

    url = GITHUB_API_README.format(owner=owner, repo=repo)
    headers = {"Accept": "application/vnd.github.v3.raw"}
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        if resp.status_code == 200 and resp.text.strip():
            return resp.text
    except Exception:
        # fallback to raw path (default branch = main/master tries)
        pass

    # fallback try direct raw README on main and master
    for branch in ("main", "master"):
        raw_url = RAW_README.format(owner=owner, repo=repo, branch=branch)
        try:
            r2 = requests.get(raw_url, timeout=timeout)
            if r2.status_code == 200 and r2.text.strip():
                return r2.text
        except Exception:
            continue

    return None

def safe_call(func, *args, tries: int = 3, base_delay: float = 1.0, **kwargs):
    last_err = None
    delay = base_delay
    for _ in range(tries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_err = e
            time.sleep(delay)
            delay *= 2
    raise last_err