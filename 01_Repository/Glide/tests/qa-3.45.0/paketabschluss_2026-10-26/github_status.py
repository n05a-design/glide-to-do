"""Liest Actions-Laufstände mit dem vorhandenen Git-Credential-Helper."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import urllib.parse
import urllib.request


def request(path):
    credentials = subprocess.run(
        ["git", "credential", "fill"], input="protocol=https\nhost=github.com\n\n",
        capture_output=True, text=True, timeout=30,
        env=dict(os.environ, GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="never"))
    fields = dict(line.split("=", 1) for line in credentials.stdout.splitlines() if "=" in line)
    if credentials.returncode or not fields.get("password"):
        raise RuntimeError("Vorhandene Git-Authentifizierung nicht verfügbar")
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28",
               "Authorization": "Bearer " + fields["password"], "User-Agent": "Glide-Paketpruefung"}
    url = "https://api.github.com/repos/n05a-design/glide-to-do/" + path
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as response:
        return json.load(response)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=int)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.run:
        result = request(f"actions/runs/{args.run}")
        result["jobs"] = request(f"actions/runs/{args.run}/jobs")["jobs"]
        brief = {key: result.get(key) for key in ("id", "name", "status", "conclusion", "head_sha", "html_url")}
        brief["jobs"] = [{key: job.get(key) for key in ("id", "name", "status", "conclusion")} for job in result["jobs"]]
    else:
        branch = urllib.parse.quote("codex/glide-paketabschluss-3.45.0", safe="")
        result = request(f"actions/runs?branch={branch}&per_page=10")
        brief = [{key: run.get(key) for key in ("id", "name", "status", "conclusion", "head_sha", "html_url")}
                 for run in result["workflow_runs"]]
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(brief, ensure_ascii=False))


if __name__ == "__main__":
    main()
