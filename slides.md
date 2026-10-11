<div class="cover">
<p class="eyebrow">CSS2026 / コンピュータセキュリティシンポジウム</p>
<h1>仕様どおりに実装すれば<br>安全か</h1>
<p class="subtitle">イーサリアムのコンセンサス仕様に明示されない<br>安全性の前提条件（予備調査）</p>
<p class="authors"><strong>村上 大岳</strong>（愛知総合工科高校）<br>神波 真聖・柳浜 万里（Nyx Foundation）<br>釘宮 由成（Independent Researcher）</p>
<p class="cover-claim">安全性の証明から前提を取り出し、確認項目にする。</p>
<p class="agenda-line">背景 ── 従来の問題点 ── 仮説 ── この研究の優位性</p>
</div>

Note:
村上です。本日は、イーサリアムを例に、共通仕様から作られる複数のソフトの確認方法をお話しします。
研究の提案は、安全性の証明から前提を取り出して、仕様を読むだけでは拾いにくい確認項目を補うことです。
背景、従来の問題点、仮説、この研究の優位性の順で話します。

---

<p class="section-tag">背景</p>

## イーサリアムについて

<div class="visual-story">
<img class="web-illustration" src="figs/web-connected-world.svg" alt="unDraw Connected world：世界各地がつながるネットワークのイラスト">
<div class="story-copy"><div class="brand-lockup"><img class="ethereum-logo" src="figs/ethereum.svg" alt="Ethereum 公式カラーロゴ"><h3>Ethereum</h3></div><p class="lead">世界中の第三者が運用する、<br>取引・プログラム実行の基盤。</p><p>全員が<mark>同じ取引履歴</mark>を保存・確認する。<br>管理者ではなく数学に依存。<br>だから、善良な参加者は<br><strong>全員同じ動きをしなければならない。</strong></p></div>
</div>
<p class="source">解説：<a href="https://ethereum.org/en/developers/docs/nodes-and-clients/">ethereum.org</a> ／ 公式Ethereumロゴ：<a href="https://ethereum.org/en/assets/">brand assets</a> ／ イラスト：Katerina Limpitsouni, <a href="https://undraw.co/illustration/connected-world_anke">unDraw</a></p>

Note:
イーサリアムは、世界中の第三者が運用するコンピュータで、取引やプログラムの実行結果を共有する基盤です。
全員が同じ取引履歴を保存し、互いに確認します。中央の管理者ではなく、数学、つまり計算と経済的な仕組みに依存して動きます。全員で決めるので、善良な参加者は全員が同じ動きをしなければなりません。
ここで重要なのは、この基盤を動かすソフトが、一つのチームが作った一種類のものではないという点です。

---

<p class="section-tag">背景</p>

## 一つの共通仕様から、別々のソフトが作られる

<p>実装者は<strong>仕様書を読んでコードを書く</strong>。別々の言語の実装が、同じネットワークで動く。</p>
<img class="architecture-visual" src="figs/illustration-clients.svg" alt="共通仕様からLighthouse、Nimbus、Teku、Lodestarへ分岐。Rust、Nim、Java、TypeScriptの各言語名の下にも公式言語ロゴを表示">
<p class="message">共通仕様をもとに、独立した実装が共存する<strong>多実装環境</strong>。</p>
<p class="source">合意を担当する4実装を例示。このソフトをクライアントと呼ぶ。実装・言語ロゴは公式素材（出典・権利者は補足と <code>figs/logo-sources.json</code>）。</p>

Note:
たとえば、RustのLighthouse、NimのNimbus、JavaのTeku、TypeScriptのLodestarがあります。上がソフトのロゴ、言語名の下が言語のロゴです。
開発の形は、共通の仕様書を読んで、それぞれのチームが自分の言語でコードを書く、というものです。こうして作られた実装が、同じネットワークに参加します。これを多実装環境と呼びます。今回のクライアントという語は、このネットワークを動かすソフトです。
そこで開発者や監査者は、何を基準に別々の実装を確認するのでしょうか。まず共通仕様を基準にします。

---

<p class="section-tag">背景</p>

## 開発・監査の出発点は、共通の仕様書

<p>実際の仕様書の抜粋。<strong>どの入力で、どの状態をどう更新するか</strong>が書かれている。</p>

```python
if previous_epoch_target_balance * 3 >= total_active_balance * 2:  # ← ここが「2/3」
    state.current_justified_checkpoint = Checkpoint(
        epoch=previous_epoch, root=get_block_root(state, previous_epoch)
    )
    state.justification_bits[1] = 0b1
```

<div class="flow">
<div class="panel"><h3>仕様の記述</h3><p>文章・Python仕様</p></div>
<div class="arrow">→</div>
<div class="panel"><h3>確認項目</h3><p>要求された処理</p></div>
<div class="arrow">→</div>
<div class="panel blue"><h3>実装を確認</h3><p>レビュー・テスト</p></div>
</div>
<p class="source">原典：<a href="https://github.com/ethereum/consensus-specs/blob/2359a5e/specs/phase0/beacon-chain.md#justification-and-finalization">consensus-specs @ 2359a5e</a>。このコードは票の支持を状態に反映する部分。EIP-3675 はこの詳細仕様を参照する。</p>

Note:
合意を担当するソフトの詳細仕様は、consensus-specsという公開文書です。文章と、処理を定義するPythonのコードからなります。
開発者はこの疑似コードを読んで、RustやNimなど自分の言語で同じ処理を書きます。なお1行目の「支持する重み×3 ≥ 総重み×2」が、あの「2/3の支持」の判定です。変数名を覚える必要はありませんが、このように数値はコードにあるのに、「どの状態のどの集合を数えているか」は行の中に名前がありません。
そして最終行で更新している justification_bits こそが、のちの実例で出てくる Nimbus #461 がずらした状態そのものです。覚えておくと繋がります。
仕様から要求された処理を列挙し、各実装がそのとおり動くか確認する。これは必要な作業です。ただし、同じ計算をしているかだけで、確認が終わるでしょうか。

---

<p class="section-tag">背景</p>

## 仕様は、証明済みの設計を訳したもの

<p>みんなに<mark>安全に合意してほしい</mark>。そこから始まる話。</p>
<img class="pipeline-visual" src="figs/diagram-spec-pipeline.svg" alt="3者の会話。理論家「前提Pなら、この動きで安全」（証明 P⇒Q）。仕様書「こう動いてね」（手順Sのみ）。実装者・監査者「前提がない。いつ正しいの？」（基準はSだけ）。前提Pを持つのは上流だけで、届く道は2つとも閉ざされている。仕様経由は転記で落ち、直接読むにも証明はLeanで下流は読めない">
<p class="message"><strong>根本原因：</strong>仕様が成り立つ<strong>前提条件</strong>が、<br>実装者・監査者からは<strong>読めない</strong>。</p>
<p class="small">「仕様に書けばいい」——でも、書くべき前提の確かな一覧が無い。<strong>それが証明の中にだけある。</strong></p>
<p class="source">図は説明用の模式図。設計の安全性議論はCasper FFG・Gasper等の研究に、仕様はconsensus-specs（EIP）に存在。証明の機械化がgasper-lean4。</p>

Note:
そもそも仕様はどこから来たのでしょうか。先に理論家による研究と設計があり、そこでは安全性の証明、つまり「この前提ならこの保証」という議論が存在します。
その設計を、実装できる手順へ翻訳したものが仕様書です。実装者はこの手順に従ってコードを書き、監査者はこの手順を基準に確認します。
ここで大事なのは、前提を持っているのは上流の理論家だけだという点です。下流へ届く道は2つとも閉ざされています。仕様経由なら転記で落ちますし、直接読もうとしても、証明はLeanという形式言語で書かれており、実装者も監査者も読みません。
そして正確な形で書かれた前提は、証明の中にだけあります。ならば証明から機械的に取り出して、確認候補として渡せばよい。それがこの研究のアイデアです。
「仕様に前提を書けばよい」という意見は正しい方向ですが、誰が何を根拠に書くかが問題です。証明の仮説は、証明が受理された時点で抜け漏れなくそろっています。人が散文で書き足すのは第二の翻訳で、漏れや揺れが入ります。だから一次情報は証明から取ります。

---

<p class="section-tag">従来の問題点</p>

## 「2/3」は合っている。でも、何の2/3か？

<p>仕様：「2/3の重みの支持で正当化」　→　監査：「2/3の計算があるか」　→　コードは2/3。<mark>ヨシ</mark></p>
<p class="small">でも「誰が有権者か」は固定ではない——名簿はエポック毎に変わり、分岐中は枝ごとに別。<br>どの時点の名簿を使うかを散文は指名しないので、<strong>同じ仕様でも分母がずれうる</strong>。</p>
<p class="label">仮想例：8人・等しい重みで集計（色付き＝支持、白＝対象内で非支持、灰＝対象外）</p>
<img class="scenario-visual" src="figs/scenario-denominators.svg" alt="実装Aは1〜6を、実装Bは3〜8を有権者（分母）とする（破線枠）。同じ仕様でも使う名簿が違うと分母がずれる。両方4/6だが分母も分子も重ならない">
<p class="message">両方とも4/6 ＝ 2/3。でも母集団が違えば、<strong>同じ保証は使えない。</strong></p>
<p class="source">仮想例は説明用。</p>

Note:
監査で拾われない理由を先に示します。仕様に「2/3の重みの支持で正当化」とあれば、監査の確認は「2/3の計算があるか」になります。コードを見れば2/3の算術はあります。ヨシ。
ところが、その2/3は何を数えた2/3なのでしょうか。なぜ分母がずれうるかというと、仕様の「the validators」という言い方が、実は変数だからです。「誰が有権者か」は登録名簿で決まり、名簿はエポック毎に変動し、分岐中は枝ごとに文字通り別の名簿が存在します。現在の名簿か、その票が指す時点の名簿か——散文はどれかを指名しないので、同じ仕様でも実装ごとに使う名簿がずれえます。
仮想例では、実装Aは1番から6番、実装Bは3番から8番を対象にしています。どちらも4人を6人で割れば2/3ですが、母集団が違うので同じ保証は使えません。
そしてこのずれは、実際に起きています。次に実例を見ます。

---

<p class="section-tag">従来の問題点</p>

## 実例：計算は合った。でも状態がずれた

<p class="label">監査が見たもの</p>
<p>「2/3の計算があるか」→ コードには2/3があった。<mark>ヨシ</mark></p>
<p class="label">実際に起きたこと（Nimbus #461）</p>
<div class="bitstrip"><span class="bitname">justification_bits</span><div class="bit">1</div><div class="bit">0</div><div class="bit stale">0</div><div class="bit stale">1</div><span class="stale-label">← 古いビットが残った</span></div>
<p>正当化履歴を保持する4bitの更新で上位ビットが残り、<strong>確定判定に使う状態がずれた</strong>。<br>実バグDBでは <strong>chain split に至り得る</strong>と分類。</p>
<p class="message">算術は正しい。壊れていたのは、<strong>計算に渡す状態</strong>。</p>
<p class="source">Nimbus PR #461（公開・修正済、ethereum-vuln-dataset の impact_type=chain_split）。ずれた状態は、先ほどの仕様抜粋の最終行 justification_bits。前提の非明示が原因とは示していない。</p>

Note:
監査が見たのは「2/3の計算があるか」で、コードには確かに2/3がありました。
実際に起きたのは別の場所のずれです。Nimbusの修正#461は、正当化履歴を保持する4ビット、justification_bitsの更新で上位ビットが残り、確定判定に使う状態がずれた実バグです。このjustification_bitsは、先ほどの仕様抜粋の最終行で更新していた状態そのものです。公開データセットではチェーン分岐に至り得ると分類されています。
重要なのは、算術が間違っていたのではなく、計算に渡す状態が壊れていたことです。なお前提の非明示がこのバグの原因だったとは示していません。同じ処理領域に監査の盲点があった、という位置づけです。
では「何を数えるべきか」という前提はどこから集めるか。証明があれば、そこから落とせばよい。それが次の仮説です。

---

<p class="section-tag">仮説</p>

## 仕様に明示されない前提を、証明から取り出す

<p>証明は<mark>保証書</mark>と同じ構造。条件内は保証、<strong>条件外は対象外</strong>。</p>
<img class="scope-visual" src="figs/diagram-guarantee-scope.svg" alt="証明は保証書。「前提Pを満たすなら安全Qを保証」とあるが、届くのはPを満たす実装だけ。満たさない実装は保証対象外。どちらも仕様準拠だが、Pを満たすかは仕様に書かれていない">
<div class="route"><span>仮説</span><strong>前提には、仕様に書かれていないものがある</strong></div>
<div class="route"><span>提案</span><strong>証明から取り出して、確認項目として渡す</strong></div>
<p class="source">図は説明用の模式図。入力：Ethereumの安全性をLean 4で形式化した <strong>gasper-lean4 の証明</strong>。</p>

Note:
先ほどの例のように、何を全体として数えるか、どの状態を使うかなど、保証が成立するための条件があります。
証明は保証書と同じ構造です。「決められた条件で使うなら、これを保証する」と書いてある。条件の外では保証は効きませんが、「必ず壊れる」とも書いていません。図は、仕様に従う実装の中で、前提を満たす領域にだけ保証が効くことを示しています。そしてその境界は、仕様の手順には書かれていません。なお形式証明とは、条件から結論への導出を機械が検査したものです。
仕様の文章からしか確認項目を作らなければ、文章に現れない前提は拾いにくくなります。そこで、安全性の証明をもう一つの入力にします。証明は「この条件なら、この結論」という形で、必要な前提を持っています。
本研究の提案は、その前提を取り出し、実装や運用の確認に使える候補へ変換することです。証明を書くこと自体の紹介ではなく、証明の前提を現場へ渡す研究です。

---

<p class="section-tag">提案</p>

## 足すのは「証明 → 前提 → 確認候補」の経路

<div class="route"><span>従来の入力</span><strong>仕様の記述 → 確認項目</strong></div>
<div class="flow extraction-flow">
<div class="panel purple"><h3>安全性の証明</h3><p>条件 ⇒ 保証</p><p class="actor">理論家の成果</p></div>
<div class="arrow">→</div>
<div class="panel"><h3>前提を抽出</h3><p><mark>定理の仮説を列挙</mark></p><p class="actor">構文的・LLM不使用</p></div>
<div class="arrow">→</div>
<div class="panel blue"><h3>確認候補へ変換</h3><p>仕様・コードと対応付け</p><p class="actor">研究側が翻訳</p></div>
</div>
<p class="message">証明の専門家だけが読む成果を、<br><strong>実装者・監査者が参照できる前提一覧</strong>にする。</p>
<p class="small">実装者・監査者はLeanを読まない。<strong>翻訳済みの一覧を受け取り、自分のコード・モデルに対応付ける。</strong><br>抽出した条件には原典の定理への参照を残す。</p>

Note:
従来の、仕様から項目を作る経路を捨てるのではありません。証明から前提を列挙する経路を追加します。
なお、実装者や監査者がLeanを読む必要はありません。抽出と翻訳は研究側が済ませ、現場が受け取るのは日本語の前提一覧です。
理論家に新しいコードや文書を書かせる提案でもありません。前提は証明の中に既に正確に書かれています。やることは、その翻訳です。
本研究ではLean 4で形式化された成果を使います。その定理の仮説を機械的に取り出し、原典と照合しました。抽出した条件には、元の定理の参照も残します。
なお抽出はAIの生成ではありません。定理文の型シグネチャに並ぶ仮説を、Leanの構文として決定的に読み取る処理です。言い換えれば、コロンの手前に並んだ括弧を列挙するだけで、解釈や生成を挟みません。だから捏造が起きません。LLMが登場するのは、後段の「明示か」の判定の側だけです。
その後、意味と仕様の参照先を対応付けて、監査者が参照できる確認候補へ変換します。次に、どの部分を取り出すのかを実例で示します。

---

<p class="section-tag">提案</p>

## 実例：定理に書かれた「条件」の部分を取り出す

<div class="grid">
<div><h3>定理文の、コロンの手前を抜き出す</h3><div class="proof-code tight"><div class="muted">theorem quorum_intersection_weight_lower</div><div class="muted">　{ qL qR vL vR : … }  -- 部品（除外）</div><div>　( hqLsub : <mark>qL ⊆ vL</mark> )</div><div>　( hqRsub : <mark>qR ⊆ vR</mark> )</div><div>　( hqLwt : <mark>τ.two_third (wt stake vL) ≤ wt stake qL</mark> )</div><div>　( hqRwt : <mark>τ.two_third (wt stake vR) ≤ wt stake qR</mark> )</div><div class="muted">　: 結論（保証）</div></div><p class="small">括弧群＝仮説。構文的に列挙し、部品を除く実体条件を選別。</p></div>
<div class="premise-list"><h3>取り出される前提の意味</h3><p><mark>支持した参加者が、<br>その側の集計対象に含まれる。</mark></p><p><mark>その対象の総重みに対して、<br>2/3以上の重みが支持する。</mark></p><p>この条件を、<strong>両側それぞれ</strong>で扱う。</p></div>
</div>
<p class="message">「2/3」という数字だけでなく、<br><strong>どの参加者集合・どの重みを使うか</strong>まで前提に含まれる。</p>
<p class="source">原典：<a href="https://github.com/NyxFoundation/gasper-lean4/blob/7650709/GasperBeaconChain/Core/Theories/SlashableBound.lean">quorum_intersection_weight_lower / gasper-lean4 @ 7650709</a>。原ソースの仮説4式を示す。日本語は説明用の要約。</p>

Note:
どうやって証明から降ってくるかを見せます。定理文は「theorem 名前（仮説）（仮説）…：結論」という形をしています。コロンの手前の括弧が、定理が依存する前提です。ツールはこれをLeanの構文として読み、型やモデルの部品（波括弧の引数）を除いた実体条件だけを選別します。解釈も生成も挟まない決定的な処理で、何度やっても同じ一覧が出ます。今回は8ファイル17定理から延べ57件が出ました。
この例では、左側と右側それぞれについて、支持した参加者が集計対象に含まれること、その集計対象の総重みに対して3分の2以上が支持していることを要求しています。記号を覚える必要はなく、右の意味を見てください。「誰を数えるか」「何を分母とするか」まで含む条件を、証明の側から取り出せます。
この定理は、集計対象の重なりに応じて、支持者の重なりを評価します。両側の参加者集合が同一であることを常に要求する定理ではありません。異なる場合の保証も、その関係を含めて評価するため、先ほどの仮想例と矛盾しません。

---

<p class="section-tag">提案</p>

## 前提を、監査で扱える確認候補へ変換する

<div class="grid tl">
<div><p class="label">人が読む形（確認一覧）</p><table>
<thead><tr><th>取り出した条件</th><th>確認候補（例）</th></tr></thead>
<tbody>
<tr><td>支持者が集計対象に含まれる</td><td>票の出所と参加者集合が対応しているか。</td></tr>
<tr><td>対象の総重みの2/3以上が支持</td><td>分母と分子の重みを、どの状態から計算しているか。</td></tr>
<tr><td>集合の関係に応じて保証を評価</td><td>参加者の入れ替わり時に、どの集合・重みをモデル化しているか。</td></tr>
</tbody>
</table></div>
<div><p class="label">ツールが読む形（SPECA等の入力）</p><pre class="json-snippet"><code class="language-json">{
 "property_id": "CHK-GEN-09",
 "severity": "CRITICAL",
 "lean_artifact": "AccountableSafety.lean#…",
 "spec_reference": "beacon-chain.md#…",
 "lean_must_establish": [
  "¬ q_intersection_slashed …",
  "k_finalized …", "justified …" ]
}</code></pre></div>
</div>
<p class="message">人には<strong>確認一覧</strong>、監査ツールには<strong>JSON</strong>を渡す。<br>どちらも、条件・原典の定理・仕様の参照先がつながっている。</p>
<p class="small">右は実際の成果物形式（実データ）。左の対応付けは使い方の例で、バグ検出性能は別途検証する。</p>

Note:
機械抽出して終わりではなく、その条件が仕様や実装のどこに対応するかを示します。画面左は、先ほどの前提を実務で確認するならどんな問いになるか、という使い方の例です。
画面右は実際に渡される成果物の形です。プロパティID、重要度、由来した定理、対応する仕様の箇所、前提条件がJSONでまとまっています。ただし監査者が素のJSONを読むわけではなく、これはSPECAのような監査パイプラインが次段（コード位置特定・検査）へ渡す入力形式です。人が読むのは左の確認一覧で、どちらもLeanを読む必要はありません。
研究の出力は、前提条件と、その来歴となる定理、対応する仕様箇所を持つ項目一覧です。左列の具体的なレビュー手順を自動生成し、その効果を評価したわけではありません。
候補を利用する人は、意味を確認して、コードのチェックなのか、モデル・運用条件の確認なのかを割り当てます。この候補が、仕様の文章だけから得る項目とどれだけ異なるかを調べました。

---

<p class="section-tag">仮説の検証</p>

## 抽出した前提は、仕様に明示されているか

<div class="flow">
<div class="panel purple"><span class="number">17</span><h3>対象の定理</h3><p class="small">定理ごとに仮説を列挙<br>原典と照合</p></div>
<div class="arrow">-></div>
<div class="panel"><span class="number">57</span><h3>延べ前提条件</h3><p class="small">複数の条件を対応付け<br>同一概念の反復を含む</p></div>
<div class="arrow">-></div>
<div class="panel blue"><span class="number">89</span><h3>仕様ファイル</h3><p class="small">文章の安全性要件と照合</p></div>
</div>
<div class="grid"><div class="panel"><h3>前提の抽出</h3><p>証明の仮説から機械的に列挙。<br>LLMで自由生成しない。</p></div><div class="panel"><h3>明示の判定</h3><p>キーワード照合器と6種類のLLM。<br>仕様の文章に等価な要件があるか。</p></div></div>
<p class="source">gasper-lean4 @ 7650709 / consensus-specs @ 2359a5e。57は重複を含む延べ件数。</p>

Note:
調査では17の定理に由来する延べ57件の前提条件を対象に、89の仕様ファイルを照合しました。
前提を取り出す段階は機械的な抽出です。一方、仕様の文章に安全性要件として等価な記述があるかの判定は、キーワード照合器と6種類のLLMによる自動判定です。抽出と判定は別の段階です。
57は原典の仮説行を単純に数えた総和でも、独立した57種類でもなく、確認項目に対応付けた前提一覧の延べ件数です。結果を見ます。

---

<p class="section-tag">この研究の優位性</p>

## 延べ57件中48件は、仕様の文章に非明示と判定

<img class="result-visual" src="figs/chart-premises.svg" alt="48/57件、84.2%のドーナツ図と57マス。青48マスは全自動判定で非明示、橙9マスは判定が分かれた">
<p class="message">仕様からの項目作りだけでは、<br><strong>証明の前提を拾いきれない可能性</strong>を示した。</p>
<p class="small">重複をまとめると10概念中7概念で非明示に一致。<br>実装のバグ数ではなく、仕様の文章との照合結果。</p>

Note:
延べ57件中48件、84.2パーセントが、すべての自動判定で「文章に安全性要件として明示されていない」と判定されました。橙の9件は判定が分かれたもので、明示と数えていません。
同じ概念の反復をまとめると10概念で、うち7概念が非明示で一致しました。コードや状態に対応物があっても、文章に安全性要件として書かれていない場合を含みます。
これは48個のバグを見つけた結果ではありません。仕様の文章だけを入力にする確認項目作りには、証明の前提を拾いきれない可能性がある、という研究結果です。
つまり、証明からの抽出は従来の経路では得られない確認候補を供給できます。これが本研究の優位性です。
なお「仕様に自然言語で書けばよい」は、まさに従来がやって拾いきれなかった方法です。書くべき内容の一次情報として証明を使うことが、この研究の出発点です。

---

<p class="section-tag">適用の一例</p>

## 前提を確認する領域に、実際の修正もある

<p class="small">次は、集計結果を保存する状態の扱い。<strong>Nimbus #461</strong>：4ビットの履歴に余分な桁が残る。</p>
<div class="grid">
<div class="panel orange"><div class="label">修正前 / PR差分</div><pre><code class="language-nim">state.justification_bits =
  state.justification_bits shl 1</code></pre><p>左へずらすだけ。</p><p class="small"><code>1000 → 10000</code></p></div>
<div class="panel blue"><div class="label">修正後 / PR差分</div><pre><code class="language-nim">const JUSTIFICATION_BITS_LENGTH = 4
state.justification_bits =
  (state.justification_bits shl 1) and
  cast[uint8](
    (2^JUSTIFICATION_BITS_LENGTH) - 1)</code></pre><p class="small">下位4ビットだけ残す。<br><code>1000 → 0000</code></p></div>
</div>
<p class="message">計算手順に加え、<strong>状態の表現範囲</strong>も確認する。</p>
<p class="source"><a href="https://github.com/status-im/nimbus-eth2/pull/461/files">Nimbus PR #461</a>（2019年、改行のみ調整）。抽出項目の一部と同じ処理領域に分類される事例。前提の非明示が原因だったとは示していない。</p>

Note:
抽出した確認候補の一部は、過去に修正があった処理領域にも対応します。ここではNimbusの公開済み修正を示します。
4ビットの履歴を整数で表していましたが、左シフトした後に4ビットの外へ情報が残ります。修正は、下位4ビットだけを残すマスクの追加でした。
この対応は、記録の支持・確定を扱う同じ分類領域にあるというものです。先ほどの前提の違いの仮想例が、このバグを引き起こしたという話ではありません。研究が当該バグを再検出できることも未評価です。

---

<p class="section-tag">実務への展開</p>

## 前提ごとに「誰が何を確認するか」を決める

<div class="grid">
<div class="panel blue"><h3>実装で確認する</h3><p>票の出所と集計対象の対応。<br>総重み・支持重みの計算。<br>状態の表現範囲。</p><p class="small">コード・テスト・レビューへ。</p></div>
<div class="panel purple"><h3>モデル・環境として確認する</h3><p>参加者の入れ替わり。<br>想定する違反者の規模。<br>どの条件下の保証を使うか。</p><p class="small">設計・運用・証明の適用範囲へ。</p></div>
</div>
<p class="message"><strong>前提を全部assertにするのではない。</strong><br>条件の意味と、確認責任を割り当てる。</p>

Note:
取り出した前提には、実装で保つ条件と、モデルや環境についての仮定が含まれます。すべてをassertに置き換えるのではありません。
票と集計対象の対応や、計算、状態の表現範囲はコードに結び付けられます。一方、攻撃者がどれだけの重みを持つかは、関数のassertで確立するものではありません。
前提一覧を受け取ったら、意味と担当、確認方法を決める。この分担が、証明から得た条件を実務で使うために必要です。

---

<p class="section-tag">実務への展開</p>

## 実装者：前提をテスト・レビューへ落とす

<div class="grid">
<div class="panel"><h3>例：更新後も4ビットに収まる</h3><p>整数表現へ移植しても、<br>仕様の配列操作と結果が一致するか。</p><p class="small">4ビットなら全16状態を比較できる。<br>条件がどの保証・処理に対応するかも残す。</p></div>
<div class="panel blue"><div class="label">提案するテスト例 / Nimbusの実コードではない</div><pre><code class="language-python">def unpack(bits):
    return [(bits &gt;&gt; i) &amp; 1
            for i in range(4)]
for bits in range(16):
    actual = (bits &lt;&lt; 1) &amp; 0b1111
    expected = [0] + unpack(bits)[:3]
    assert 0 &lt;= actual &lt; 16
    assert unpack(actual) == expected</code></pre></div>
</div>
<p class="message">前提 → 対応する状態・処理 → テスト／レビュー。</p>

Note:
実装者向けの使い方の例です。更新後の状態が4ビットに収まるという条件なら、仕様の配列操作と整数での操作を比較するテストにできます。
右は説明用のテストで、Nimbusの実コードではありません。16通りについて表現範囲と操作結果を確認しています。
このように条件を確認方法へつなげます。複雑なモデルの仮定はテストだけで扱えないため、レビューや設計確認へ割り当てます。本研究では、これによる監査性能の改善はまだ評価していません。

---

<p class="section-tag">実務への展開</p>

## 仕様を書く人：前提と手順を対応付ける

<table>
<thead><tr><th>記すもの</th><th>投票集計を例にした記述案</th></tr></thead>
<tbody>
<tr><td><strong>手順</strong></td><td>支持する重みを集計し、閾値と比較する。</td></tr>
<tr><td><strong>対象・状態の前提</strong></td><td>どの参加者集合を対象に、どの状態の総重みを分母に使うかを参照できるようにする。</td></tr>
<tr><td><strong>保証との接続</strong></td><td>保証の前提を示す証明・モデルと、確認すべき仕様箇所を対応付ける。</td></tr>
<tr><td><strong>環境の仮定</strong></td><td>参加者の入れ替わりや攻撃者の規模を、実装の処理要件とは区別して記す。</td></tr>
</tbody>
</table>
<p class="message">実装者が<strong>「何を・どこで・どう確認するか」</strong>をたどれる仕様へ。</p>

Note:
仕様を書く人への提案は、前提と手順の対応をたどれるようにすることです。投票を集計するなら、対象の参加者集合と分母に使う状態も分かる形にします。
保証を説明する証明やモデルがあるなら、その前提と仕様箇所を接続します。一方、攻撃者の規模などの環境の仮定は、実装が確立する処理要件とは区別します。
すべての前提を仕様の処理手順に押し込むのではなく、実装者が必要な確認をたどれるようにする提案です。
「仕様に分かりやすく書けばいい」は本提案と同じ方向です。違いは、何を書くかの出所を証明の仮説に置く点です。機械が検査した一次情報を土台にすれば、書き手の記憶や解釈に頼りません。

---

<p class="section-tag">実務への展開</p>

## 共通仕様から作る、他のシステムでも考えられる

<div class="grid three">
<div class="panel"><h3>分散合意<br>Raft</h3><p>投票後に再起動したら？</p><p class="hypothesis"><strong>確認候補：</strong><br>投票済みの状態を失い、<br>同じ任期に再び投票<br>できないか。</p></div>
<div class="panel"><h3>金融通信<br>FIXでの注文</h3><p>注文が再送されたら？</p><p class="hypothesis"><strong>確認候補：</strong><br>同じ注文を新規注文と<br>誤認し、二度執行<br>しないか。</p></div>
<div class="panel"><h3>OS基盤<br>POSIXのファイル更新</h3><p>更新直後に電源断したら？</p><p class="hypothesis"><strong>確認候補：</strong><br>原子的な置き換えと、<br>障害後にもデータが残る<br>ことを区別しているか。</p></div>
</div>
<p class="message">C言語の複数処理系や通信規格にも、<strong>共通仕様＋独立実装</strong>の構造がある。</p>
<p class="source">説明用の仮想例。これらの対象での仕様不備や監査効果を、本研究が実証したわけではない。</p>

Note:
この三つは、他分野で考えられる確認候補の仮想例です。再起動して投票履歴を失わないか、再送された注文を二度執行しないか、更新完了の後に電源が落ちても必要なデータが残るか、という条件です。
C言語にも、共通規格とGCCやClangなどの独立した処理系があります。通信規格にも別々のベンダーの実装があります。分野が違っても、共通仕様から項目を作るという構造はあります。
持ち帰ってほしいのは、本研究の割合を他の分野へ当てはめることではありません。保証が依存する前提を探し、仕様由来の項目と照合するという問いです。形式証明がある対象では、その前提を追加の入力として利用できます。

---

<p class="section-tag">まとめ</p>

## 証明の成果を、現場が参照できる形へ

<div class="visual-story">
<img class="web-illustration" src="figs/web-infrastructure.png" alt="ethereum.org Infrastructure：イーサリアムを支えるコンピュータのイラスト">
<div class="story-copy"><p class="lead">証明を書くのは専門家。<br>前提一覧を使うのは現場。</p><p>条件とその来歴を受け取り、<br>仕様・コードと対応付け、<br>確認責任と方法を決める。</p></div>
</div>
<p class="message"><strong>全員がLeanを学ぶのではなく、証明の前提を共有する。</strong></p>
<p class="source">イラスト：WT, <a href="https://ethereum.org/en/assets/">ethereum.org / Infrastructure</a></p>

Note:
前提抽出の意義は、証明の成果を専門家だけが読むものにしないことです。現場の人全員にLeanを勉強してもらう、という提案ではありません。
受け取るのは、条件と、その条件の来歴である定理、対応する仕様の参照先です。それを自分の実装や運用に対応付け、誰がどう確認するかを決めます。
本研究が示したのは、この前提を供給する経路と、仕様の文章との照合結果です。下流の監査への効果は次の検証課題です。

---

<p class="section-tag">まとめ</p>

## まとめ：安全性の証明から、前提を取り出そう

<p class="summary">仕様を読むだけの確認に、<br>証明が要求する前提を足す。</p>
<div class="grid three">
<div class="panel"><h3>提案</h3><p>定理の前提を機械抽出し、<br>確認候補へ変換する。</p></div>
<div class="panel blue"><h3>調査結果</h3><p>延べ57件中48件は、<br>仕様の文章に非明示と判定。</p></div>
<div class="panel"><h3>次の行動</h3><p>前提を仕様・コードへ対応付け、<br>担当と確認方法を決める。</p></div>
</div>
<p class="small">今後：人手での判定と、前提一覧を使った監査の効果検証。　ご清聴ありがとうございました。</p>

Note:
まとめます。研究の中心は、安全性の証明から前提を取り出し、仕様に基づく確認を補うことです。
対象の証明から延べ57件の条件を抽出・対応付け、48件が仕様の文章に安全性要件として明示されていないと自動判定されました。
前提の一覧を、仕様やコードのどこで確認するかにつなげる。これが現場で使うための次の行動です。人手での判定と下流の監査効果は今後検証します。ご清聴ありがとうございました。

---

<p class="section-tag">補足</p>

## 補足：仮想例は、何を示しているか

<table>
<thead><tr><th></th><th>集計対象</th><th>支持者</th><th>対象に対する割合</th></tr></thead>
<tbody><tr><td>実装A</td><td>1, 2, 3, 4, 5, 6</td><td>1, 2, 3, 4</td><td>4/6 = 2/3</td></tr><tr><td>実装B</td><td>3, 4, 5, 6, 7, 8</td><td>5, 6, 7, 8</td><td>4/6 = 2/3</td></tr></tbody>
</table>
<p>支持者の重なりは0人。全8人に対しては、両方とも4/8。</p>
<div class="panel"><p>同じ全体を使う場合の「重なりは1/3以上」という直感を、<br>違う分母の集計に無条件で適用できない。</p></div>
<p class="small">集計部分を切り出した仮想例。この対象選択が仕様に準拠するとも主張していない。Ethereumの確定には投票間の関係・状態更新・検証など追加の条件があり、実ネットワークの事故を再現していない。</p>

Note:
仮想例は、2/3の計算だけでは、全体の定義や参加者の入れ替わりを確認できないことを示します。異なる集合を使うこと自体が常に違反なのではありません。
原典の定理は異なる参加者集合も扱い、集合の交差に応じた下限を与えます。この例の集計対象は4人で重なりますが、支持者は0人で重なります。その場合に1/3の重なりを無条件に期待することが誤りです。

---

<p class="section-tag">補足</p>

## 補足：原典の定理と、抽出する仮説

<table>
<thead><tr><th>定理・補題</th><th>保証の意味</th></tr></thead>
<tbody>
<tr><td><code>quorum_intersection_weight_lower</code></td><td>二つの支持者集合の重なりを、参加者集合の重なりと閾値から下側に評価する。本編の抽出例。</td></tr>
<tr><td><code>k_safety'</code></td><td>両立しない履歴が確定したなら、二つの支持集合の交差がモデル上の違反判定の対象になる。</td></tr>
<tr><td><code>slashable_bound</code></td><td>違反判定対象の重みを、参加者の入れ替わりも含めて下側に評価する。</td></tr>
<tr><td><code>no_k_finalized_justified_same_height</code></td><td>指定した前提のもとで、確定した記録と別の支持された記録は同じ高さに並ばない。CHK-GEN-09の母定理。</td></tr>
</tbody>
</table>
<p class="source">gasper-lean4 @ 7650709。確定を支える投票ルールは Casper FFG と呼ばれる。定理の成立と、実装・現実へのモデルの適用は区別する。</p>

Note:
本編の例はSlashableBound.leanにある定理の仮説です。包含の仮説2式、重みの閾値の仮説2式を抜粋しました。
本研究の57件は、確認項目に対応付けたmust-establish一覧の延べ件数であり、原典のすべての仮説行を単純に数えたものではありません。型・モデルのパラメータ等の部品も区別しています。
安全性の核心を示す定理と、前提の抽出を説明する例の役割を区別してください。定理を検査するLeanのカーネルが受理しても、モデルが現実を忠実に表すことまで自動的に保証されるわけではありません。

---

<p class="section-tag">補足</p>

## 補足：結果の意味と、まだ評価していないこと

<div class="grid">
<div class="panel"><h3>測ったこと</h3><p>証明由来の前提が、<br>仕様の文章に安全性要件として<br>明示されているか。</p></div>
<div class="panel orange"><h3>まだ測っていないこと</h3><p>実装のバグ数。<br>追加項目のバグ検出性能。<br>他分野でも同じ割合になるか。</p></div>
</div>
<p class="small">延べ57件・10概念。48件（7概念）は非明示に一致、9件は判定が分かれた。判定器はすべて自動で、正式な人手評価は今後の課題。</p>
<p class="small">非明示は「コードにも存在しない」とは限らない。前提には実装で保つ条件、脅威モデルの仮定、証明の補助条件が含まれる。</p>

Note:
結果は、自動判定による仕様の文章との照合です。同じ概念の反復があるため、独立した57種類の安全性要件ではありません。
仕様に非明示であることは、実装に脆弱性があることや、仕様の誤りを直接証明しません。下流の監査に役立つかは、正式な人手判定やバグの再検出実験で確認する必要があります。

---

<p class="section-tag">補足</p>

## 補足：同じ処理領域にあることと、同じ原因は別

<div class="grid">
<div class="panel"><h3>Nimbus #461</h3><p>正当化履歴のビット処理を修正。<br>下位4ビットを残すマスクを追加。</p></div>
<div class="panel"><h3>Lighthouse #4576</h3><p>確定に伴うデータ移行で、<br>同じロックを二度取得する<br>デッドロックを修正。</p></div>
</div>
<p class="message">CHK-GEN-09などの一部項目と、<br>実バグは同じ分類領域へ対応付けられる。</p>
<p class="small">対応はデータセットの分類ラベルに基づく。コードパスの一致や、前提の非明示がバグを生んだという因果は示していない。前提の違いの仮想例とも別の話。</p>
<p class="source"><a href="https://github.com/status-im/nimbus-eth2/pull/461">Nimbus #461</a> ／ <a href="https://github.com/sigp/lighthouse/pull/4576">Lighthouse #4576</a></p>

Note:
この対応付けで示せるのは、同じ分類領域に位置することです。二つの修正は原因も違います。
Nimbusはビット表現の処理、Lighthouseはデータ移行のロック処理です。Lighthouseを確定計算の式の不整合と説明するのは誤りです。
抽出した項目がこれらのバグを検出できたかは未評価です。仮想例を、これらの事故の原因説明として使っていません。

---

<p class="section-tag">補足</p>

## 参照資料・イラスト・公式ロゴの出典

<div class="grid">
<div class="panel"><h3>仕様・証明・修正PR</h3><p class="small"><a href="https://github.com/ethereum/consensus-specs/tree/2359a5e">consensus-specs @ 2359a5e</a><br><a href="https://eips.ethereum.org/EIPS/eip-3675">EIP-3675</a><br><a href="https://github.com/NyxFoundation/gasper-lean4/tree/7650709">gasper-lean4 @ 7650709</a><br><a href="https://github.com/status-im/nimbus-eth2/pull/461">Nimbus #461</a> / <a href="https://github.com/sigp/lighthouse/pull/4576">Lighthouse #4576</a></p><p class="small">研究の対象・数値・限界は論文正本に基づく。</p></div>
<div class="panel"><h3>イラスト・ブランド素材</h3><p class="small"><a href="https://ethereum.org/en/assets/">ethereum.org / WT</a><br><a href="https://undraw.co/illustrations">unDraw / Katerina Limpitsouni</a>（<a href="https://undraw.co/license">利用条件</a>）<br><a href="https://github.com/rust-lang/rust-artwork/">Rust Foundation / Rust project</a>（<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>、変更なし）<br><a href="https://github.com/nim-lang/assets">Nim project</a> / <a href="https://dev.java/">Oracle / Java</a><br><a href="https://www.typescriptlang.org/branding/">Microsoft / TypeScript</a></p><p class="small">ロゴは各ブランドの識別用。推薦・提携を示さない。<br>取得元・ハッシュ・利用条件は <code>figs/*-sources.json</code>。</p></div>
</div>

Note:
原典と素材の出典です。イラストはネットから取得した素材をそのまま使い、数量を示すグラフと仮想例の図は、本発表のデータに基づいています。
Ethereum、実装、言語のロゴは公式サイトまたは公式アートワークから取得しました。RustはCC BY 4.0で、変更せず使用しています。各ブランドの推薦や提携を示すものではありません。
