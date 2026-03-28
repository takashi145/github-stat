# GitHub Stats

公開リポジトリの言語割合を集計し、GitHub Pages で公開する。  
現在は毎週（日曜 00:00 UTC）に実行（`.github/workflows/update-langs.yml` の cron を編集)

## セットアップ

1. リポジトリをフォーク
2.  **Settings → Pages → Source** を `GitHub Actions` に設定

## 出力

| ファイル | 内容 | URL |
|---|---|---|
| `langs.json` | 言語別バイト数・割合の集計データ | `https://<username>.github.io/github-stats/langs.json` |
| `langs.svg` | 言語割合を棒グラフで可視化した画像 | `https://<username>.github.io/github-stats/langs.svg` |

### langs.json
```json
{
  "schema_version": 1,
  "generated_at": "ISO8601",
  "username": "string",
  "repo_count": number,
  "total_bytes": number,
  "languages": [
    {
      "lang": "string",
      "bytes": number,
      "percent": number
    }
  ]
}
```

### langs.svg
上位10件。表示件数は `scripts/aggregate_langs.py` の `max_langs` で変更可。
![GitHub Languages](https://takashi145.github.io/github-stats/langs.svg)
