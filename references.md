# BWS2026 参考資料まとめ

「仕様どおりに実装すれば安全か — イーサリアムのコンセンサス仕様に明示されない安全性の前提条件（予備調査）」

---

## 元となる論文・原点（一次資料）

| 資料 | 役割 | 場所 |
|---|---|---|
| **Casper FFG 原論文**<br>Buterin & Griffith, "Casper the Friendly Finality Gadget" | 安全性の証明の原点。Accountable Safety・Plausible Liveness・Slashable Bound を証明。「2つの矛盾したチェックポイントが確定するには ≥1/3 のバリデータがスラッシュ条件を破る必要」 | arXiv:1710.09437 |
| **Gasper 論文**<br>"Combining GHOST and Casper" | Casper FFG を動的バリデータ集合・フォークチョイスと統合した現行設計 | arXiv:2003.03052 |
| **Runtime Verification の Coq 形式化** | Ethereum Foundation と協働で Gasper の finality を Coq で機械検証。Accountable Safety / Plausible Liveness / Slashable Bound を証明 | runtimeverification.com ブログ・GitHub |
| **gasper-lean4**（NyxFoundation） | **本研究の証明入力**。Gasper を Lean 4 で形式化した成果物。`SlashableBound.lean` の `quorum_intersection_weight_lower` 等を含む | github.com/NyxFoundation/gasper-lean4 @ 7650709 |
| **consensus-specs**（ethereum） | **本研究の照合対象の仕様書**。Markdown + Python 疑似コード。`beacon-chain.md` の Justification and finalization 節 | github.com/ethereum/consensus-specs @ 2359a5e |

## SPECA 関係の成果物（本研究の前提となる監査パイプライン）

| 成果物 | 内容 | 場所 |
|---|---|---|
| **SPECA 論文 1（事例研究）**<br>"SPECA: Specification-to-Checklist Agentic Auditing for Multi-Implementation Systems — A Case Study on Ethereum Clients" | 仕様→プロパティチェックリスト→実装への写像。Fusaka 監査コンテストで評価。Strategy B（実装横断チェック）が全有効報告の 76.5%（17件中13件）。無効報告の 56.8% は脅威モデルの不整合 | arXiv:2602.07513 |
| **SPECA 論文 2（本論文）**<br>"Beyond Code Reasoning: Specification-Anchored Auditing of Multi-Implementation Distributed Protocols"（Kamba, Murakami, Sannai） | 仕様から型付きプロパティ（不変条件・事前/事後条件・信頼仮定）を導出し proof-attempt 推論で監査。Fusaka で15/15のH/M/L脆弱性を回収+修正済み4件を独立発見。RepoAudit ベンチで precision 88.9%・recall 100% | arXiv:2604.26495 |
| **speca リポジトリ** | 6フェーズパイプライン（01a仕様収集 → 01bサブグラフ → 01eプロパティ生成 → 02cコード位置解決 → 03監査 → 04レビュー）。RFC 2119 の MUST/SHOULD を不変条件注釈に使う | github.com/NyxFoundation/speca |
| **speca-lean4-plugin** | **本研究と最も近い先行成果**。gasper-lean4 の Casper FFG 定理から 01e 形式の監査プロパティを機械生成（v0.1.0: 25定理 → 61プロパティ）。SPECA の `lean` プロバイダ経由で接続 | github.com/NyxFoundation/speca-lean4-plugin |
| **SPECA ドキュメント** | パイプライン仕様・RQ1/RQ2 ベンチマーク詳細 | speca.pages.dev |
| **ベンチマーク** | RQ1: Sherlock Fusaka コンテスト（10クライアント・366投稿）／RQ2: RepoAudit（15 OSS C/C++）／RQ2b: ProFuzzBench（探索的） | speca/benchmarks/ |

## 事故・データの出典

| 資料 | 内容 |
|---|---|
| **Nimbus PR #461** | justification_bits の4ビット履歴更新で上位ビットが残った実バグ（2019年・修正済）。公開脆弱性データセットで impact_type=chain_split と分類 |
| **Lighthouse PR #4576** | もう一つの実バグ例（データ移行のロック処理。原因は Nimbus と別） |
| **ethereum-vuln-dataset** | Nimbus #461 の chain split 分類の根拠 |
| **eth2book.info / ethereum.github.io/consensus-specs** | 注釈付き仕様書（Ben Edgington）・公式レンダリング版仕様。スライドのスクショ元 |
| **EIP-3675** | The Merge の EIP。consensus-specs の詳細仕様を参照する証拠 |

## 参考になる周辺成果（聴衆が関連づけそうなもの）

### Lean × Ethereum エコシステム
- **leanSpec / leanMultisig / leanMetrics**（leanEthereum）— 実行可能な Lean ベースの仕様実装
- **formal-leanSpec**（NyxFoundation）— leanSpec の Lean4 形式検証。命題カタログ Tier 1/2/3
- **verity**（NyxFoundation）— Lean 4 で全行を証明するコンセンサスクライアント
- **docs2formalspec**（NyxFoundation）— 文書→RFC2119仕様→Leanモデルの自動化ツール

### 仕様/コード監査の関連研究
- **PropertyGPT**（NDSS'25 Distinguished Paper）— プロパティ生成による監査
- **GPTScan / iAudit** — LLMによるスマートコントラクト監査
- **FormalBench** — 多段階パイプライン＋構造化レビューの必要性を示したベンチマーク
- **RepoAudit**（ICML 2025）— SPECA 評価で使ったベンチマーク
- **ProFuzzBench / ChatAFL**（NDSS 2024）— プロトコル実装のファジング基盤

### 本研究との差分
SPECA系は「仕様文書 → プロパティ → 監査」。**本研究は「証明の仮説 → 前提 → 確認項目」というもう一本の経路を追加する**。speca-lean4-plugin が既に定理→プロパティ生成を実装しており、本研究の57件はその一次情報の供給元（証明側）を検証した調査という位置づけ。

---

## 予測される質問と答え（Q&A 対策）

**Q1. 「仕様に前提を自然言語で書けばいいのでは？」**
→ 方向は正しい。違いは**出所**：「何を書くか」の正しさ・網羅性を保証できる一次情報は証明の仮説だけ。人が散文で書き足すのは検査不能な第二の翻訳で、実際に48/57件が拾えていないという実測がある。

**Q2. 「48件はバグか？」**
→ 違う。バグの個数ではなく「仕様の文章に安全性要件として明示されていない」の判定結果。下流の監査への効果は別途検証（未評価）。

**Q3. 「Nimbus #461 は前提の非明示が原因か？」**
→ 因果は示していない。同じ処理領域（正当化履歴・確定判定）に監査の盲点があったという位置づけ。

**Q4. 「LLMが抽出を間違えるのでは？」**
→ 抽出段はLLMを使わない。定理文の型シグネチャから仮説を構文的に列挙する決定的処理（speca-lean4-plugin も fixture フォールバックを実物照合で検出した実績あり）。LLMは後段の「明示/非明示」判定だけ。

**Q5. 「仮想例（8人・2/3）は実際のEthereumか？」**
→ 説明用の模式例。実際のバリデータは数十万人規模で重みも不均等。「分母の定義が違いうる」ことを示す図。

**Q6. 「57件は独立した条件か？」**
→ 延べ件数。同一概念の反復をまとめると10概念、うち7概念が非明示で一致。

**Q7. 「Coq での形式化（Runtime Verification）との違いは？」**
→ 検証対象は同じ Gasper の核心定理。本研究は Lean 4 版（gasper-lean4）を入力にした。抽出手法は証明系を選ばず適用可能。

**Q8. 「前提を全部 assert にすればいいのでは？」**
→ しない。前提には実装で保つ条件と、モデル・環境の仮定（攻撃者の規模等）が混ざる。条件の意味と確認責任を割り当てるのが提案。

**Q9. 「差分テストで実装間の違いは拾えるのでは？」**
→ 実装が**揃って間違える**（同じ誤解で一致する）場合に差分は出ない。SPECA 論文でも「correlated misinterpretations」として同じ問題が指摘されている。

**Q10. 「Lean を現場の人が読めないのでは？」**
→ 読まない設計。翻訳済みの前提一覧（日本語の確認項目 or JSON）を渡す。本研究は「証明の成果を現場へ渡す」研究であり、証明の書き方の話ではない。

**Q11. 「手順（2/3の計算）は合っているのに何が問題？」**
→ 算術ではなく**何の集合・どの状態を数えたか**がずれうる。Nimbus #461 も算術は正しく、確定判定に渡す状態が壊れていた。

**Q12. 「仕様書自体が間違っているという話か？」**
→ 違う。仕様の手順は正しいが、「その手順が成り立つ前提条件」が下流に届いていないという構造の問題。仕様の非難ではなく情報経路の補完の話。
