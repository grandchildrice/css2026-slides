# css2026-slides

CSS2026 予備調査 発表スライド（本編18枚＋補足5枚）。

- 発表スライド（Reveal.js）: https://sururu-k.github.io/css2026-slides/
- 確認用プレビュー（Cloudflare Workers、main への push で自動更新）: https://css2026-slides.kingmasatojames.workers.dev
- 内容ドラフト（話し原稿つき）: [slides.md](slides.md)
- 構成一覧・対象読者・研究データ: [css2026-slides.json](css2026-slides.json)（本文は `slides.md`）

配信は `node build_site.mjs` が組み立てた `dist/` だけを対象にする。`wrangler deploy` がこのビルドを自動で呼ぶので、Workers Builds 側の設定はデプロイコマンドだけでよい。発表準備用の `materials/` と `docs/` は配信しない。

論文正本は `sururu-k/css2026-paper`（private）にあり、本リポジトリは発表用スライドのみを公開する。

https://www.linkedin.com/pulse/understanding-zero-knowledge-proofs-encoding-programs-soares-m-sc--dxdkf/