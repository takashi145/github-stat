# GitHub Stats

自分の公開リポジトリの使用言語割合を集計し、`langs.json` と `langs.svg` を自動更新します。
（フォークしたリポジトリや Organization のリポジトリは対象外です）

## セットアップ

1. このリポジトリをフォーク
2. Actions タブで GitHub Actions を有効化

毎週日曜に自動実行されます。実行スケジュールを変更したい場合は [`.github/workflows/update-langs.yml`](.github/workflows/update-langs.yml) の `cron` を編集してください。

## 出力

- `langs.json` — 言語名と割合（%）が多い順で保存されます
- `langs.svg` — 使用言語を棒グラフで可視化したSVGです（上位10件、変更する場合は `generate_svg` の `max_langs` を編集してください）

## 使用例
GitHub Pagesを利用し、自分のプロフィールに使用言語の割合を表示することができます。例えば、以下のようにMarkdownに埋め込むことができます：
```markdown
![Languages](https://<username>.github.io/github-stats/langs.svg)
```
