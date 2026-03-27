import json
import os
import urllib.error
import urllib.request
from typing import Any

GITHUB_API = "https://api.github.com"
PER_PAGE = 100


def request(url: str, token: str | None = None) -> tuple[Any, str]:
    headers = {"User-Agent": "github-stats-bot"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read()), res.headers.get("Link", "")


def fetch_repos(username: str, token: str | None = None) -> list[dict]:
    repos = []
    url = f"{GITHUB_API}/users/{username}/repos?per_page={PER_PAGE}&type=owner"
    while url:
        data, link = request(url, token)
        repos.extend(data)
        url = next(
            (p.split(";")[0].strip().strip("<>") for p in link.split(",") if 'rel="next"' in p),
            None,
        )
    return repos


def aggregate(username: str, token: str | None = None) -> list[dict]:
    lang_bytes: dict[str, int] = {}
    for repo in fetch_repos(username, token):
        try:
            langs, _ = request(f"{GITHUB_API}/repos/{username}/{repo['name']}/languages", token)
            for lang, count in langs.items():
                lang_bytes[lang] = lang_bytes.get(lang, 0) + count
        except urllib.error.HTTPError:
            pass

    total = sum(lang_bytes.values())
    return [
        {"lang": lang, "percent": round(count / total * 100, 1)}
        for lang, count in sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)
    ]


def main() -> None:
    username = os.environ["USERNAME"]
    token = os.environ.get("GH_TOKEN")

    stats = aggregate(username, token)

    out = os.path.join(os.path.dirname(__file__), "..", "langs.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
