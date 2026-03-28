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


def generate_svg(stats: list[dict], max_langs: int = 10) -> str:
    langs = stats[:max_langs]

    W = 400
    PAD = 16
    ROW_H = 24
    NAME_W = 110
    BAR_X = PAD + NAME_W
    BAR_W = W - BAR_X - 55 - PAD
    PCT_X = BAR_X + BAR_W + 8
    H = PAD + max(len(langs), 1) * ROW_H + PAD

    rows = []

    if not langs:
        rows.append(f'  <text x="{W // 2}" y="{H // 2 + 5}" fill="#999" font-size="13" font-family="sans-serif" text-anchor="middle">No data</text>')
    else:
        for i, item in enumerate(langs):
            cy = PAD + i * ROW_H + ROW_H // 2
            fill_w = max(BAR_W * item["percent"] / 100, 3)
            rows.append(f'  <text x="{PAD}" y="{cy + 5}" fill="#333" font-size="12" font-family="sans-serif">{item["lang"]}</text>')
            rows.append(f'  <rect x="{BAR_X}" y="{cy - 5}" width="{BAR_W}" height="10" rx="5" fill="#e0e0e0"/>')
            rows.append(f'  <rect x="{BAR_X}" y="{cy - 5}" width="{fill_w:.1f}" height="10" rx="5" fill="#4a9eff"/>')
            rows.append(f'  <text x="{PCT_X}" y="{cy + 5}" fill="#666" font-size="11" font-family="sans-serif">{item["percent"]}%</text>')

    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
        f'  <rect width="{W}" height="{H}" rx="8" fill="#fff" stroke="#e0e0e0" stroke-width="1"/>',
        *rows,
        "</svg>",
    ])


def main() -> None:
    username = os.environ["USERNAME"]
    token = os.environ.get("GH_TOKEN")

    stats = aggregate(username, token)

    base = os.path.join(os.path.dirname(__file__), "..")

    with open(os.path.join(base, "langs.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    with open(os.path.join(base, "langs.svg"), "w", encoding="utf-8") as f:
        f.write(generate_svg(stats))

    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
