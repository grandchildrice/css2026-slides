<div class="cover">
<p class="eyebrow">CSS2026 / BWS ブロックチェーンワークショップ</p>
<h1>仕様どおりに実装すれば<br>安全か</h1>
<p class="subtitle">イーサリアムのコンセンサス仕様に明示されない<br>安全性の前提条件（予備調査）</p>
<p class="authors"><strong>村上 大岳</strong>（愛知総合工科高校）<br>神波 真聖・柳浜 万里（Nyx Foundation）<br>釘宮 由成（Independent Researcher）</p>
<p class="cover-claim">安全性の証明から前提を取り出し、確認項目にする。</p>
<p class="agenda-line">背景 ── 従来の問題点 ── 仮説 ── この研究の優位性</p>
</div>

Note:
本日は、イーサリアムを例に、共通仕様から作られる複数のソフトの確認方法をお話しします。
提案は、安全性の証明から前提を取り出し、仕様を読むだけでは拾いにくい確認項目を補うことです。
背景、従来の問題点、仮説、この研究の優位性の順で話します。

---

<p class="section-tag">背景</p>

## 「同じ仕様書」なのに、動きが違う

<p>ブロックチェーンの話の前に、エンジニアなら見覚えのある状況から始めます。</p>

<p class="label">例：身近な「仕様 × 複数実装」</p>
<table>
<thead><tr><th>分野</th><th>共通の仕様</th><th>複数の実装</th><th>ズレた所</th></tr></thead>
<tbody>
<tr><td>ブラウザ</td><td>HTML/JSの仕様</td><td>Chrome・Firefox・<strong>Safari</strong></td><td>Safariだけ表示がずれる</td></tr>
<tr><td>Cコンパイラ</td><td>言語規格</td><td>GCC・Clang・MSVC</td><td>未定義動作・拡張で結果が違う</td></tr>
<tr><td>SQL</td><td>標準SQL</td><td>MySQL・PostgreSQL・SQLite</td><td>方言があり、移植すると壊れる</td></tr>
</tbody>
</table>
<p class="message">書いてある所のズレはテストで潰せる。<mark>残るのは、書いていない所</mark>。<br>── もしこのズレが、<strong>資産を扱う基盤</strong>で起きたら？</p>

Note:
ブラウザ、Cコンパイラ、SQL。共通の仕様があって複数の実装があり、「仕様どおりのはずが片方でだけ動かない」経験は誰にでもあるはずです。
ズレが出るのは、仕様が明確に書いた部分ではなく、書いていない部分＝解釈の余地や暗黙の前提です。
もしこれが資産を扱う基盤で起きたら——次にイーサリアムを見ます。

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
全員が同じ取引履歴を保存し、互いに確認します。中央の管理者を置かず、計算と経済的インセンティブの仕組みに依存して動きます。
全員で決めるので、善良な参加者は全員が同じ動きをしなければなりません。
では、その動きが食い違ったら何が起きるのか。次に見ます。

---

<p class="section-tag">背景</p>

## 「食い違い」は、なぜ特別に危険なのか

<p style="margin: 6px 0 10px;">普通のソフトのバグは「利用者の問題」。<br>ここで壊れるのは、<strong>「全員が同じ履歴を持つ」という合意そのもの</strong>。</p>
<img class="diagram split-visual" style="height: 240px; margin: 6px auto; display: block;" src="figs/diagram-chain-split.svg" alt="暗黙前提の解釈差によるチェーン分裂（Chain Split）と資産喪失の危機を示す図解">
<p class="takeaway" style="margin-top: 10px; padding: 10px 18px; font-size: 24px;">各実装が「仕様どおり」に動くだけでは不十分。<br><strong>暗黙前提のわずかなズレが、不可逆なチェーン分裂を引き起こす。</strong></p>
<p class="small" style="margin-top: 6px;">Ethereumはあえて実装を多様化し、単一障害点を避ける設計。<br>ただし<strong>全実装が共通の前提を共有している</strong>ことが条件。</p>

Note:
普通のソフトのバグは使う人だけが困りますが、コンセンサス実装のずれは別格です。この基盤の商品は「全員が同じ履歴を持つこと」そのものだからです。
実装AとBが別々の履歴を「確定」すると履歴が二つに裂け、確定済みの取引が消え、預けた資産も危険にさらされます。
Ethereumは単一障害点を避けるため実装を多様化していますが、それには全実装が共通の前提を共有していることが条件です。

---

<p class="section-tag">背景</p>

## 仕様書は厳密なのに、多実装で読まれる

<p>共通仕様は<strong>型・フィールド・更新手順まで疑似コードで定義</strong>した詳細文書。各チームが<strong>この文書を読んで</strong>実装を書く。</p>
<div class="grid">
<div class="panel"><p class="label">仕様書に書いてある（実物抜粋）</p><div class="proof-code tight"><div>class Checkpoint(Container):  <span class="muted">#「確かな履歴」＝時刻＋指紋</span></div><div>justification_bits: Bitvector[4]  <span class="muted"># 確定判定の履歴</span></div><div>def process_epoch(state):  <span class="muted"># エポックごとの集計</span></div></div><p class="small">実行可能な疑似コード級の詳細設計。</p></div>
<div class="panel"><p class="label">独立した複数実装が共存</p><img class="architecture-visual" src="figs/illustration-clients.svg" alt="共通仕様からLighthouse、Nimbus、Teku、Lodestarへ分岐" style="height:130px"></div>
</div>
<p class="message">全チームが<strong>同じ文書</strong>を読み、別言語で実装 → <strong>多実装環境</strong>。</p>

Note:
合意を担当するソフトの詳細仕様は consensus-specs という公開文書で、文章と実行可能なPythonコードからなります。
開発者はこれを読み、RustやNimなど自分の言語で同じ処理を書きます。全チームが同じ文書を読む、これが多実装環境です。
では開発者や監査者は、何を基準に別々の実装を確認するのか。その前に、なぜズレるとまずいかを先に見ます。ここから確認の出発点を見ます。

---

<p class="section-tag">従来の問題点</p>

## 厳密なのは「手順」。書いていないのは「いつ安全か」

<div class="grid">
<div class="panel"><p class="label">仕様が定義するもの</p><p>型・フィールド・更新手順<br>実行可能な疑似コード<br>→ <strong>「どう動くか」（HOW）</strong></p></div>
<div class="panel"><p class="label">仕様に書いていないもの</p><p>その手順が安全に効く条件<br>想定している状況・適用範囲<br>→ <mark>「いつ正しいか」（WHEN）</mark></p></div>
</div>
<p class="message">＝ <strong>doc に事前条件のない関数</strong>を、各チームが読んで実装している状態。</p>
<p class="small">手順と意味は書いてある。でも「この前提を満たさない呼び出しは無効」という契約が無い——あの感覚。<br>文章に無い前提は、いくら精読しても出てきません。</p>

Note:
仕様書は「どう動くか」については極めて厳密で、型も手順も実行できるほど詳細です。
でも、ソフトでいう「この関数の事前条件」——その手順がいつ安全に効くかという契約は書かれていません。
docに前提の無い関数は、読み手ごとに前提の補い方が変わります。全実装がまさにその状態です。

---

<p class="section-tag">従来の問題点</p>

## 「仕様に準拠すれば良い」のでは？

<p>その通り——<strong>全チームがそうしています</strong>。問題は準拠ミスではなく、<strong>同じ記述でも解釈が分かれること</strong>。</p>
<div class="grid">
<div class="panel"><p class="label">ふつうの層：手順の記述</p><p>「この操作をこうする」と具体的<br>ずれる＝<strong>誰かのミス</strong><br>→ レビュー・テストで見つかる</p></div>
<div class="panel"><p class="label">今回の層：条件の記述（数学に近い）</p><p>「〜の2/3」「その時点の〜」<br>ずれる＝<strong>別々の妥当な読み</strong><br>→ 全員「準拠」なのに結果が違う</p></div>
</div>
<p class="message">確認項目は<strong>仕様の文章から列挙</strong>する。<br>文章に無い前提は、<strong>監査チェックリストの「行」にすら載らない。</strong></p>

Note:
「仕様どおりに実装すれば十分では？」——正しく、世界中の全チームが実際にそうしています。
ずれには二層あり、手順の層のずれは誰かのミスで、レビューやテストで見つかります。
もう一つ、数学に近い条件文の層では、何を指すかを読む人が決めるため、全員が準拠なのに結果が違うことが起きます。
そして確認項目は仕様の文章から作られるので、書いていない前提は誰も見ません。

---

<p class="section-tag">従来の問題点</p>

## 安全性の核心：クォーラム交差の前提

<p style="margin: 6px 0 10px;">「仕様どおり」なのに結果が分かれる理由：合意仕様は<strong>数学的な安全性定理（クォーラム交差）</strong>に依存している。</p>
<img class="diagram votes-visual" style="height: 230px; margin: 6px auto; display: block;" src="figs/illustration-votes.svg" alt="同じ参加者集合と同じ票の重みなら、2つの3分の2の支持集合は少なくとも3分の1重なる">
<p class="takeaway" style="margin-top: 10px; padding: 10px 18px; font-size: 24px;">定理は「同じ参加者集合・同じ重み」を前提に安全を保証。<br><strong>その前提が仕様の文章に書かれていなければ、各実装で解釈が分かれる。</strong></p>
<p class="small" style="margin-top: 6px;">どれだけ算術（2/3）を正しく実装しても、前提が満たされなければ安全性は保証されない。</p>

Note:
合意仕様の安全性を支えるのはクォーラム交差という数学的定理です。2/3以上の支持を集めた決定が2つあれば、少なくとも1/3は重なり、「同時に2つの履歴は確定しない」が保証されます。
ただしそれには「同じ参加者集合を分母に、同じ重みで計算する」という前提が必要で、これは仕様の文章には書かれていません。
前提が共有されなければ、各実装が仕様どおりに2/3を計算しても保証は崩れます。

---

<p class="section-tag">従来の問題点</p>

## なぜ、仕様を読むだけでは見えないのか

<img class="pipeline-visual" src="figs/diagram-spec-pipeline.svg" alt="3者の会話。理論家「前提Pなら、この動きで安全」（証明 P⇒Q）。仕様書「こう動いてね」（手順Sのみ）。実装者・監査者「前提がない。いつ正しいの？」（基準はSだけ）。前提Pを持つのは上流だけで、届く道は2つとも閉ざされている。仕様経由は転記で落ち、直接読むにも証明はLeanで下流は読めない">
<p class="message"><strong>根本原因：</strong>仕様が成り立つ<strong>前提条件</strong>が、<br>実装者・監査者からは<strong>読めない</strong>。</p>
<p class="small">「証明」＝「この条件を満たせば保証が必ず成り立つ」を<strong>機械が検算</strong>した文書（Lean）。<br><strong>機械が受理した時点で、仮説に抜け漏れはない</strong>——書くべき前提の確かな一覧は証明の中にだけある。</p>
<p class="source">図は説明用の模式図。設計の安全性議論はCasper FFG・Gasper等の研究に、仕様はconsensus-specs（EIP）に存在。証明の機械化がgasper-lean4。</p>

Note:
クォーラム交差のような安全性の前提条件が、なぜ仕様書に書かれないのか。これは仕様書の欠陥というより、仕様書と証明の「役割分担」に起因する構造的ギャップです。
先に理論家による研究と設計があり、そこに安全性の証明（この前提が満たされるとき安全性が成立する＝WHEN）があります。その設計を実行可能な手順（HOW）へ書き下したのが仕様書です。
実装者は手順に従ってコードを書き、監査者は手順を基準に確認します。しかし安全性を保証する前提（WHEN）は証明側にのみあり、仕様書の手順記述には現れません。証明はLeanで書かれており、現場が直接読むことも困難です。
では、このギャップのせいで現場の確認はどう歪むのか。次に見ます。

---

<p class="section-tag">従来の問題点</p>

## 「2/3」は合っている。でも、何の2/3か？

<p class="label">仮想例（説明用）：8人・等しい重みで集計（色付き＝支持、灰＝対象外）</p>
<img class="scenario-visual" src="figs/scenario-denominators.svg" alt="実装Aは1〜6を、実装Bは3〜8を有権者（分母）とする。同じ仕様でも使う名簿が違うと分母がずれる。両方4/6だが分母も分子も重ならない">
<p class="message">両方とも4/6 ＝ 2/3。でも母集団が違えば、<strong>同じ保証は使えない。</strong></p>
<p class="label" style="margin-top:12px;">実例：Nimbus #461（justification_bits の更新）</p>
<div class="bitstrip"><span class="bitname">justification_bits</span><div class="bit">1</div><div class="bit">0</div><div class="bit stale">0</div><div class="bit stale">1</div><span class="stale-label">← 古いビットが残った</span></div>
<p class="small">算術は正しい。壊れていたのは<strong>計算に渡す状態</strong>。実バグDBでは chain split に至り得ると分類。<br>※前提の非明示が直接原因とは示していない（位置的共起）。</p>

Note:
仕様は「総重みの2/3が支持すれば正当化」と書きます。監査は「2/3の計算があるか」を見ますが、コードには確かに2/3があります。
でもその2/3は何を数えた2/3か。名簿はエポック毎に変動し、分岐中は枝ごとに別名簿です。どの集合・出席を想定した保証かは書かれていません。
仮想例では実装Aは1〜6、実装Bは3〜8を対象に、どちらも4/6＝2/3ですが母集団が違います。
実例では、Nimbus #461でjustification_bitsの上位ビットが残り、確定判定に使う状態がずれました。算術ではなく状態が壊れた例です。

---

<p class="section-tag">仮説</p>

## 仕様どおりの実装は、証明の前提まで満たさない

<p>証明は<mark>保証書</mark>と同じ構造。条件内は保証、<strong>条件外は対象外</strong>。</p>
<img class="scope-visual" src="figs/diagram-guarantee-scope.svg" alt="証明は保証書。「前提Pを満たすなら安全Qを保証」とあるが、届くのはPを満たす実装だけ。満たさない実装は保証対象外">
<div class="route"><span>問題</span><strong>同じ「仕様どおり」でも、前提が満たされるかは仕様を読むだけでは区別がつかない</strong></div>
<div class="route"><span>仮説</span><strong>前提には、仕様に書かれていないものがある</strong></div>
<div class="route"><span>提案</span><strong>証明から取り出して、確認項目として渡す</strong></div>
<p class="source">入力：Ethereumの安全性をLean 4で形式化した <strong>gasper-lean4 の証明</strong>。</p>

Note:
仕様を読んでそのとおり実装するだけでは不十分です。仕様は「こう動け」という手順は教えますが、「証明が要求する前提をあなたの実装が満たしているか」は教えてくれません。
証明は保証書と同じで、条件内は保証、条件外は対象外です。その境界は仕様の手順には書かれていません。
そこで安全性の証明をもう一つの入力にします。提案は、証明が要求する前提を取り出し、実装・監査で使える確認候補へ変換することです。

---

<p class="section-tag">提案</p>

## 足すのは「証明 → 前提 → 確認候補」の経路

<div class="flow extraction-flow">
<div class="panel purple"><h3>安全性の証明</h3><p>条件 ⇒ 保証</p></div>
<div class="arrow">→</div>
<div class="panel"><h3>前提を抽出</h3><p><strong>定理の前提を列挙</strong></p><p class="actor">構文的・LLM不使用</p></div>
<div class="arrow">→</div>
<div class="panel blue"><h3>確認候補へ変換</h3><p>仕様・コードと対応付け</p></div>
</div>
<p class="message">抽出は<strong>機械的・LLM不使用</strong>（生成すると証明に無い前提が混ざるが、構文を読むだけなら捏造が起きない）。<br>LLMは後段の「仕様に明示か」の判定のみ。<strong>監査での実効性は未検証</strong>。</p>

Note:
従来の、仕様から項目を作る経路を捨てるのではなく、証明から前提を列挙する経路を追加します。実装者・監査者はLeanを読む必要はありません。
前提は証明の中に既に正確に書かれており、やることはその翻訳です。抽出はAIの生成ではなく、定理文の仮説をLeanの構文として決定的に読み取る処理なので捏造が起きません。
LLMが登場するのは後段の「仕様に明示されているか」の判定だけです。そして、出した確認候補が実際の監査でバグを拾えるかはまだ評価していません。

---

<p class="section-tag">提案</p>

## 実例：定理に書かれた「条件」の部分を取り出す

<div class="grid" style="margin-bottom: 10px;">
<div><h3 style="margin: 0 0 8px;">定理文の、コロンの手前を抜き出す</h3><div class="proof-code tight" style="padding: 8px 12px; font-size: 15px;"><div class="muted">theorem quorum_intersection_weight_lower</div><div class="muted">　{ qL qR vL vR : … }  -- 部品（除外）</div><div>　( hqLsub : <mark>qL ⊆ vL</mark> )</div><div>　( hqRsub : <mark>qR ⊆ vR</mark> )</div><div>　( hqLwt : <mark>τ.two_third (wt stake vL) ≤ wt stake qL</mark> )</div><div>　( hqRwt : <mark>τ.two_third (wt stake vR) ≤ wt stake qR</mark> )</div><div class="muted">　: 結論（保証）</div></div><p class="small" style="margin: 4px 0 0; font-size: 18px;">括弧群＝前提（Leanでは仮説）。構文的に列挙し実体条件を選別。</p></div>
<div class="premise-list"><h3 style="margin: 0 0 8px;">取り出される前提の意味</h3><div class="premise" style="padding: 6px 10px; margin-bottom: 6px; font-size: 20px;"><p style="margin: 0;"><strong>① 参加者集合の包含：</strong><br>支持した参加者が、その側の集計対象に含まれる。</p></div><div class="premise" style="padding: 6px 10px; margin-bottom: 6px; font-size: 20px;"><p style="margin: 0;"><strong>② クォーラムの重み閾値：</strong><br>その対象の総重みに対して、2/3以上の重みが支持する。</p></div><p class="small" style="margin: 4px 0 0; font-size: 18px;">この条件を、<strong>両側（フォーク双方）</strong>で満たす必要がある。</p></div>
</div>
<p class="message" style="margin: 10px 0 6px; font-size: 28px;">「2/3」という数字だけでなく、<br><strong>どの参加者集合・どの重みを使うか</strong>まで前提に含まれる。</p>
<p class="source" style="margin-top: 6px;">原典：<a href="https://github.com/NyxFoundation/gasper-lean4/blob/7650709/GasperBeaconChain/Core/Theories/SlashableBound.lean">gasper-lean4 @ 7650709</a>。原ソースの仮説4式を示す。日本語は説明用の要約。</p>

Note:
左の記号は細かく読む必要はありません。要点は右の日本語2行です。「支持した人が名簿に入っているか」「全体の2/3以上いるか」。
定理文は「theorem 名前（仮説）…：結論」という形で、コロンの手前の括弧が前提です。ツールはこれをLeanの構文として読み、型やモデルの部品を除いて実体条件だけを選別します。
解釈も生成も挟まない決定的な処理で、何度やっても同じ一覧が出ます。今回は8ファイル17定理から延べ57件が出ました。

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
 "lean_status": "descends-from-proved",
 "lean_artifact": "AccountableSafety.lean#…",
 "spec_reference": "beacon-chain.md#…",
 "lean_must_establish": [
  "¬ q_intersection_slashed …",
  "k_finalized …",
  "justified …",
  "bj ≠ bf" ]
}</code></pre></div>
</div>
<p class="message">人には<strong>確認一覧</strong>、監査ツールには<strong>JSON</strong>を渡す。<br>どちらも、条件・原典の定理・仕様の参照先がつながっている。</p>

Note:
機械抽出して終わりではなく、その条件が仕様や実装のどこに対応するかを示します。右のJSONは監査ツールへ渡すデータ形式で、現場のエンジニアが確認するのは左の日本語一覧表だけで十分です。
重要度は仕様書の記述量ではなく安全性定理の構造に由来するため、仕様に書かれていない前提でも優先度が落ちません。
こうした項目が全部で27あり、そのうち17項目が前提条件を持ちます。この候補が、仕様の文章だけから得る項目とどれだけ異なるかを調べました。

---

<p class="section-tag">仮説の検証</p>

## 抽出した前提は、仕様に明示されているか

<div class="flow">
<div class="panel purple"><span class="number">17</span><h3>対象の定理</h3><p class="small">仮説を列挙・原典照合</p></div>
<div class="arrow">-></div>
<div class="panel"><span class="number">57</span><h3>延べ前提条件</h3><p class="small">同一概念の反復を含む</p></div>
<div class="arrow">-></div>
<div class="panel blue"><span class="number">89</span><h3>仕様ファイル</h3><p class="small">文章の安全性要件と照合</p></div>
</div>
<img class="result-visual" src="figs/chart-premises.svg" alt="48/57件、84.2%のドーナツ図と57マス。青48マスは全自動判定で非明示、橙9マスは判定が分かれた" style="height:150px">
<p class="message">延べ57件中<strong>48件（84.2%）</strong>が非明示。<strong>「明示」と全員一致した条件は0件。</strong></p>

Note:
17の定理に由来する延べ57件の前提条件を、89の仕様ファイルと照合しました。抽出は機械的、明示の判定はキーワード照合器と6種類のLLMによる自動判定です。
結果、48件（84.2%）が全会一致で「仕様に安全性要件として明示されていない」と判定され、逆に全員が「明示」と同意した条件は0件でした。
概念でまとめると10概念中7概念が非明示です。これはバグを見つけた数ではなく、仕様の文章だけを入力にすると証明の前提を拾いきれない可能性を示す結果です。判定は正解ラベルではなく判定器間の一致である点は限界です。

---

<p class="section-tag">実務への展開</p>

## 前提ごとに「誰が何を確認するか」を決める

<p>取り出した前提を、仕様・コードへ対応付け、<strong>担当と確認方法を割り当てる</strong>。</p>
<div class="grid">
<div class="panel blue"><h3>実装で確認する</h3><p>票の出所と集計対象の対応。<br>総重み・支持重みの計算。<br>状態の表現範囲。</p><p class="small">コード・テスト・レビューへ。</p></div>
<div class="panel purple"><h3>モデル・環境として確認する</h3><p>参加者の入れ替わり。<br>想定する違反者の規模。<br>どの条件下の保証を使うか。</p><p class="small">設計・運用・証明の適用範囲へ。</p></div>
</div>
<p class="message"><strong>すべての前提を単一のassertに変換するわけではない。</strong><br>条件の意味に応じて、確認の責任と手法を正しく割り当てる。</p>

Note:
取り出した前提には、実装で保つ条件と、モデルや環境についての仮定が含まれます。すべてをassertに置き換えるのではありません。
票と集計対象の対応や計算、状態の表現範囲はコードに結び付けられます。一方、攻撃者がどれだけの重みを持つかは関数のassertで確立するものではありません。
前提一覧を受け取ったら、意味と担当、確認方法を決める。この分担が、証明から得た条件を実務で使うために必要です。同じ枠組みはRaftやBFT系など、共通仕様＋独立複数実装のシステム全般に広げられます。

---

<p class="section-tag">まとめ</p>

## まとめ：安全性の証明から、前提を取り出そう

<img class="architecture-visual" style="height: 118px; margin: 4px auto; display: block;" src="figs/diagram-proof-handoff.svg" alt="形式証明から抽出された前提条件を、現場が使えるテスト項目・監査チェックリストへ変換するパイプライン">
<p class="summary" style="font-size:34px; margin:16px 0;">仕様を読むだけの確認に、<br>証明が要求する前提を足す。</p>
<div class="grid three">
<div class="panel"><h3>提案</h3><p>定理の前提を機械抽出し、確認候補へ変換する。</p></div>
<div class="panel blue"><h3>調査結果</h3><p>延べ57件中48件は、仕様の文章に非明示と判定。</p></div>
<div class="panel"><h3>次の行動</h3><p>前提を仕様・コードへ対応付け、担当と確認方法を決める。</p></div>
</div>

Note:
研究の中心は、安全性の証明から前提を取り出し、仕様に基づく確認を補うことです。対象の証明から延べ57件を抽出・対応付け、48件が仕様に非明示と判定されました。
現場のエンジニア全員がLeanを習得する必要はありません。前提条件の自動抽出が、研究と実装・監査をつなぐインターフェースになります。
今後は、人手の正解ラベルによる検証と、実バグを一切参照せずに作った項目で修正前のバグを再検出できるかの実験、そして他のBFT系への横展開を予定しています。ご清聴ありがとうございました。

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
仮想例は、2/3の計算だけでは、全体の定義や参加者の入れ替わりを確認できないことを示します。
異なる集合を使うこと自体が常に違反なのではありません。原典の定理は異なる参加者集合も扱い、集合の交差に応じた下限を与えます。
この例の集計対象は4人で重なりますが、支持者は0人で重なります。その場合に1/3の重なりを無条件に期待することが誤りです。

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
本研究の57件は、確認項目に対応付けたmust-establish一覧の延べ件数であり、原典のすべての仮説行を単純に数えたものではありません。
安全性の核心を示す定理と、前提の抽出を説明する例の役割を区別してください。Leanのカーネルが受理しても、モデルが現実を忠実に表すことまで自動的に保証されるわけではありません。

---

<p class="section-tag">補足</p>

## 補足：結果の意味と、まだ評価していないこと

<div class="grid">
<div class="panel"><h3>測ったこと</h3><p>証明由来の前提が、<br>仕様の文章に安全性要件として<br>明示されているか。</p></div>
<div class="panel orange"><h3>まだ測っていないこと</h3><p>実装のバグ数。<br>追加項目のバグ検出性能。<br>他分野でも同じ割合になるか。</p></div>
</div>
<p class="small">延べ57件・10概念。48件（7概念）は非明示に一致、9件は判定が分かれた。判定器はすべて自動で、正式な人手評価は今後の課題。判定器間の一致率は0.913（PABAK 0.826）だが、判定器「間」の一致であって正解との一致ではない。判定器の設計者は著者であり利益相反も否定できない。</p>
<p class="small">非明示は「コードにも存在しない」とは限らない。前提には実装で保つ条件、脅威モデルの仮定、証明の補助条件が含まれる。仕様には安全性の帰結を非形式に述べる文書（弱主観性・高速確定）はあるが、分解された前提を検査可能な要件としては与えていない。</p>

Note:
結果は、自動判定による仕様の文章との照合です。同じ概念の反復があるため、独立した57種類の安全性要件ではありません。
判定器間の一致率は0.913、偶然を補正したPABAKでも0.826ですが、あくまで判定器どうしの一致であり、正解ラベルとの一致ではありません。
また、仕様に安全性の概念が一切ないわけではありません。非明示が意味するのは、証明が要求する分解された前提が、検査可能な要件として与えられていない、ということです。

---

<p class="section-tag">補足</p>

## 補足：同じ処理領域にあることと、同じ原因は別

<div class="grid">
<div class="panel"><h3>Nimbus #461</h3><p>正当化履歴のビット処理を修正。<br>下位4ビットを残すマスクを追加。</p></div>
<div class="panel"><h3>Lighthouse #4576</h3><p>確定に伴うデータ移行で、<br>同じロックを二度取得する<br>デッドロックを修正。<span class="small">※並行処理バグで別種</span></p></div>
</div>
<p class="message">一部項目と実バグは同じ分類領域へ対応付けられる。<br>ただし領域の一致は「同じ種類のバグ」を意味しない。</p>
<p class="small">対応はデータセットの分類ラベルに基づく。コードパスの一致や、前提の非明示がバグを生んだという因果は示していない。前提の違いの仮想例とも別の話。</p>
<p class="source"><a href="https://github.com/status-im/nimbus-eth2/pull/461">Nimbus #461</a> ／ <a href="https://github.com/sigp/lighthouse/pull/4576">Lighthouse #4576</a></p>

Note:
この対応付けで示せるのは、同じ分類領域に位置することです。二つの修正は原因も障害クラスも違います。
Nimbusはビット表現の処理、Lighthouseはデータ移行のロック処理です。同じ処理領域に実バグが起きているという動機づけ以上の意味はありません。
抽出した項目がこれらのバグを検出できたかは未評価です。

---

<p class="section-tag">補足</p>

## 適用の一例：前提を確認する領域に、実際の修正もある

<p class="small">集計結果を保存する状態の扱い。<strong>Nimbus #461</strong>：4ビットの履歴に余分な桁が残る。</p>
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
<p class="source"><a href="https://github.com/status-im/nimbus-eth2/pull/461/files">Nimbus PR #461</a>（justification bits の整数オーバーフロー修正、impact type=chain split）。同一ラベルへの位置的共起のみで、因果は主張しない。</p>

Note:
抽出した確認候補の一部は、過去に修正があった処理領域にも対応します。ここではNimbusの公開済み修正を示します。
4ビットの履歴を整数で表していましたが、左シフトした後に4ビットの外へ情報が残ります。修正は、下位4ビットだけを残すマスクの追加でした。
この事例は因果関係を直接立証するものではなく、同一の処理領域で事故が起きていたという動機づけの一例です。

---

<p class="section-tag">補足</p>

## 実務への展開：共通仕様から作る、他のシステムでも考えられる

<div class="grid three">
<div class="panel"><h3>分散合意<br>Raft / Paxos</h3><p>メンバーシップ動的変更</p><p class="hypothesis"><strong>確認候補：</strong><br>新旧構成の共存期でも、<br>クォーラム交差の前提が<br>満たされているか。</p></div>
<div class="panel"><h3>BFT合意<br>Tendermint 等</h3><p>有権者集合の動的変動</p><p class="hypothesis"><strong>確認候補：</strong><br>各エポックでアクティブな<br>有権者集合の定義が<br>全実装で一致しているか。</p></div>
<div class="panel"><h3>分散プロトコル<br>形式仕様モデル</h3><p>ネットワーク環境前提</p><p class="hypothesis"><strong>確認候補：</strong><br>部分同期性や通信順序の<br>数学的前提がコードの<br>仮定と合致しているか。</p></div>
</div>
<p class="message">「共通仕様＋独立した複数実装」を持つシステム全般で、<strong>証明の前提を抽出する枠組み</strong>が有効。</p>
<p class="source">単一仕様とマルチクライアント構成を持つ分散システム一般への適用可能性の考察。</p>

Note:
この三つは、本アプローチが適用可能な分散システム一般の例です。Raftなどの分散合意プロトコルでも、メンバーシップ変更の過渡期におけるクォーラム交差条件など、証明側で要求される前提と実装時の手順との間にギャップが生じ得ます。
単一の共通仕様に基づいて複数の開発チームが独立に実装を行うアーキテクチャでは、どのシステムでも「手順の記述」と「安全性の数学的前提」の乖離がリスクとなります。
本研究が提案する枠組みは、イーサリアムに限らず、安全性が最重要視される分散システム全般に拡張可能です。

---

<p class="section-tag">補足</p>

## 想定される反論と答え

<table>
<thead><tr><th>反論</th><th>答え</th></tr></thead>
<tbody>
<tr><td>「単一実装なのに『実装差』は概念破綻」</td><td>2013年のBDB事故は0.7系と0.8系が<strong>同時にネットワークを走った</strong>事案。アップグレードの過渡期は事実上の複数実装状態で、「異なるルールブックのノードが同居してチェーンが裂けた」構造は本題と同型。</td></tr>
<tr><td>「理想化された前提は現場を救えない」</td><td>「1/3未満のビザンチン」「部分同期」はまさに<strong>運用で監視すべき環境前提</strong>。保証が効かない条件を現場が把握していなければ、クライアント集中リスクの警告も意味をなさない。既存の堅牢化の代替ではなく補完。</td></tr>
<tr><td>「差分ファジングで解決」</td><td>差分ファジングが見つけるのは<strong>実装間の不一致</strong>。全実装が同じ見えない前提を共有して同じ方向に間違える<strong>common-mode failure</strong>は検出できない。「正解」のオラクルは証明の前提が担う。併用するもので代替ではない。</td></tr>
<tr><td>「仕様書は手順書。前提が無いのは自明」</td><td>問題は「書かれていないこと」ではなく<strong>「確認項目の原料がどこにも無いこと」</strong>。仕様から監査項目を作る以上、そこに無い前提は検査されない。辞書の文法証明と違い、クォーラム交差の前提は実装の正当性に必須の事前契約。</td></tr>
</tbody>
</table>

Note:
想定される反論に先回りして答えます。一つ目、単一実装に実装差は概念破綻という指摘。2013年の事故はバージョン間の非互換で、新旧クライアントが同居した事実上の複数実装状態です。
二つ目、理論の前提は理想化しすぎという指摘。だからこそ、その前提は運用で監視すべき項目です。保証が効かない条件を把握できないことが問題です。
三つ目、差分ファジングで解決という指摘。ファジングは実装間の不一致を見つけますが、全実装が同じ前提で同じ方向に間違える場合は検出できません。
四つ目、仕様書は手順書だから前提が無いのは当たり前という指摘。問題は書かれていないこと自体ではなく、監査項目の原料が現場に届かないことです。

---

<p class="section-tag">補足</p>

## 参照資料・イラスト・公式ロゴの出典

<div class="grid">
<div><p class="label">仕様・証明・データ</p><p class="small">gasper-lean4（Nyx Foundation, commit 7650709）／ consensus-specs（commit 2359a5e）／ speca-lean4-plugin（tag 20260723-gasper）／ ethereum-vuln-dataset（commit c7c4ccb）</p></div>
<div><p class="label">イラスト・ロゴ</p><p class="small">公式Ethereumロゴ（ethereum.org brand assets）／ クライアント・言語ロゴ（各公式素材、詳細は <code>figs/logo-sources.json</code>）／ イラスト：Katerina Limpitsouni, unDraw</p></div>
</div>

Note:
参照資料と素材の出典です。
