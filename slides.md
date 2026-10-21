<div class="cover">
<p class="eyebrow">CSS2026 / BWS ブロックチェーンワークショップ</p>
<h1>仕様どおりに実装すれば<br>安全か</h1>
<p class="subtitle">イーサリアムのコンセンサス仕様に明示されない<br>安全性の前提条件（予備調査）</p>
<p class="authors"><strong>村上 大岳</strong>（愛知総合工科高校）<br>神波 真聖・柳浜 万里（Nyx Foundation）<br>釘宮 由成（Independent Researcher）</p>
</div>

Note:
本日は、イーサリアムを例に、共通仕様から作られる複数のソフトの確認方法をお話しします。
提案は、安全性の証明から前提を取り出し、仕様を読むだけでは拾いにくい確認項目を補うことです。
背景、先行研究、手法、分析結果、まとめの順で話します。

---

<!-- .slide: data-section="目次" -->

## 目次

<div class="agenda-list">
<div class="agenda-row"><span class="no">1</span><span class="name">背景</span><span class="desc">Ethereumは複数の実装で動き、食い違いは実害になる</span></div>
<div class="agenda-row"><span class="no">2</span><span class="name">先行研究</span><span class="desc">チェックリスト生成が、監査の質を決める。その限界</span></div>
<div class="agenda-row"><span class="no">3</span><span class="name">過去の事例</span><span class="desc">Ethereumの合意の安全性は、Leanで書かれつつある</span></div>
<div class="agenda-row"><span class="no">4</span><span class="name">RQ</span><span class="desc">Leanの前提は、仕様の文章にどれだけ明示されているか</span></div>
<div class="agenda-row"><span class="no">5</span><span class="name">提案手法</span><span class="desc">Leanの前提を取り出し、仕様の文章と突き合わせる</span></div>
<div class="agenda-row"><span class="no">6</span><span class="name">実験結果</span><span class="desc">前提は、仕様にどれだけ明示されていたか</span></div>
<div class="agenda-row"><span class="no">7</span><span class="name">考察</span><span class="desc">実際のバグと前提の非明示は、どう関係しうるか</span></div>
<div class="agenda-row"><span class="no">8</span><span class="name">まとめ</span><span class="desc">分かったことと、まだ言えないこと</span></div>
</div>

Note:
この流れで進めます。

---

<p class="section-tag">背景</p>

## 研究背景：Ethereumは、共通仕様から複数の実装が作られる

<div class="brand-lockup"><img class="ethereum-logo" src="figs/ethereum.svg" alt="Ethereum 公式カラーロゴ"><h3>Ethereum：全員が同じ履歴を持つ基盤</h3></div>
<img class="architecture-visual short" src="figs/illustration-clients.svg" alt="共通仕様からLighthouse、Nimbus、Teku、Lodestarへ分岐。Rust、Nim、Java、TypeScriptの各言語名の下にも公式言語ロゴを表示">
<p class="message">各チームが<strong>同じ仕様書</strong>を読み、別々の言語で実装する。<strong>仕様が土台</strong>。</p>

Note:
このスライドで話すこと：Ethereumは複数言語の実装が動き、土台は共通の仕様書。
Ethereumは、世界中の第三者が運用するコンピュータで、全員が同じ取引履歴を持つ基盤です。
このソフトは、一つのチームが作ったものではありません。Rust、Nim、Java、TypeScriptなど、複数の言語で、別々のチームが実装しています。
全チームが読む土台が、共通の仕様書です。だから、この仕様書に何が書かれているかが、とても大事になります。

---

<p class="section-tag">背景</p>

## パブリックチェーンでは、実装の食い違いが実害として表に出る

<p class="lead-in">互いに信用しない不特定多数が、それぞれの実装で同じ履歴を確認する。<br>だから食い違いは、「どの履歴が確定したか」として表に出る。</p>
<img class="diagram split-visual" src="figs/diagram-chain-split.svg" alt="ブロック1〜3は全実装が共有。実装Aは4〜6、実装Bは4′〜6′を確定し、履歴が二つに分かれる。確定は戻せず、巨額資産の停止・取引停止に直結する">
<p class="takeaway compact">確定した分岐は<strong>戻せない</strong>。巨額資産の停止・取引停止に直結する。</p>

Note:
このスライドで話すこと：食い違いは、パブリックチェーンでは実害として表に出る。
普通のソフトのバグは、そのソフトを使う人だけが困ります。
パブリックチェーンでは、実装AとBがそれぞれ別の履歴を確定すると、履歴が二つに分かれます。
図では、ブロック1〜3は全員が共有しています。その後、AとBが違うブロックを確定しています。
この分岐は後から戻せません。確定済みの取引が一方で消え、取引や担保が止まります。
実装を複数にするのは、一つの不具合で全体が止まらないようにするためです。ただしそれには、全実装が同じ前提を共有していることが条件になります。
では、そうした食い違いを防ぐための確認は、今どう行われているのか。次に見ます。

---

<p class="section-tag">先行研究</p>

## 先行研究：SPECAでは、プロパティ生成が監査の質を決める

<p class="term-line"><span class="term">仕様駆動の監査</span><br>仕様からチェックリストを大量に作り、それに照らして監査する。<br>その一つが、私たちの先行研究 SPECA（チェックリストを「プロパティ」と呼ぶ）。</p>
<img class="speca-visual" src="figs/diagram-speca-architecture.svg" alt="SPECAの構成。仕様、仕様の探索、サブグラフ抽出、プロパティ生成、コード箇所の特定、証明試行による監査、レビューの順。プロパティ生成が監査の質を決める">
<p class="message">監査で重要なのは、チェックリスト（プロパティ）を<strong>生成する過程</strong>。</p>

Note:
このスライドで話すこと：SPECAの構成と、性能を決める箇所。
仕様駆動の監査とは、仕様の要求からチェックリスト（プロパティ）をたくさん作って、各実装がそれを満たすかを確認していく監査です。SPECAはその一つで、私たちの先行研究です。
構成は、仕様の探索、サブグラフの抽出、プロパティの生成、コード箇所の特定、証明試行による監査、レビューの順です。
この中で、監査の質を決めるのは、プロパティの生成だと考えています。何をプロパティにするかで、何を確認できるかが決まるからです。
なお、脆弱性の発見数での比較は、条件をそろえた比較にならないので、ここでは扱いません。今後の課題です。

---

<p class="section-tag">先行研究</p>

## 先行研究の限界：プロパティ生成の入力は、仕様の文章だけ

<div class="grid">
<div class="panel"><p class="label">仕様の文章から生成（現在）</p><p>文章に書かれたことだけが、<br>プロパティの元になる。<br>書かれていない前提は拾えない。</p></div>
<div class="panel blue"><p class="label">だったら</p><p>仕様の文章以外にも、<br>安全性の前提が明示された<br><strong>入力</strong>を使えないか。</p></div>
</div>
<p class="message">プロパティ生成の入力は、<strong>仕様の文章だけ</strong>に限られている。</p>

Note:
このスライドで話すこと：先行研究（仕様駆動の監査）の限界。
プロパティ生成は、今は仕様の文章だけが入力です。文章に書かれていることしか、プロパティの元にできません。
仕様の全体をグラフにして全部たどる方法もありますが、規模が大きくなると重くなる、というのが私たちの見立てです。ここは測定していません。
では、仕様の文章以外に、安全性の前提がすべて明示された入力はないか。そこで目を付けたのがLeanです。

---

<p class="section-tag">過去の事例</p>

## Lean: 定理の証明を機械が検査する言語

<div class="grid three">
<div class="panel purple"><h3>定理</h3><p>仮説（条件）と<br>結論（保証）の組。</p></div>
<div class="panel"><h3>カーネルが検査</h3><p>証明に穴があれば、<br>受理されない。</p></div>
<div class="panel blue"><h3>Ethereumでは</h3><p>合意の安全性の定理が、<br>Leanで書かれつつある。</p></div>
</div>
<p class="message">Ethereumの合意の安全性は、<strong>Leanの定理</strong>として書かれようとしている。</p>

Note:
このスライドで話すこと：Leanとは何か、Ethereumでどう使われているか。
Leanは、定理の証明を機械が検査する言語です。定理は、仮説と結論の組です。
証明に穴があると、Leanのカーネルが受理しません。通らなければ危ない、という機械的な検査に使われます。
Ethereumの世界では、合意の安全性を示す定理を、Leanで書く取り組みが進んでいます。まだ書き切られてはいません。私たちが使ったのは、その一つのgasper-lean4です。

---

<p class="section-tag">RQ</p>

## RQ：Leanの前提は、仕様の文章にどれだけ明示されているか

<div class="grid">
<div class="panel purple"><p class="label">Leanの定理</p><p>仮説（前提）が、<br>すべて書かれている。</p></div>
<div class="panel blue"><p class="label">仕様の文章</p><p>その前提は、<br>どこまで書かれているか。</p></div>
</div>
<p class="message">Leanの前提が、仕様の文章に<strong>どれだけ明示されているか</strong>を調べた。</p>

Note:
このスライドで話すこと：案を試すために立てた問い。
SPECAの側にも、Leanの定理を確認項目へ変換するプラグインがあります。
これを進めるうちに、定理の前提が、仕様の文章にどのくらい明示されているのかが気になりました。
これが今回の研究内容です。Leanの定理には前提がすべて書かれています。その前提が、仕様の文章に書かれているかを調べました。

---

<p class="section-tag">提案手法</p>

## 提案手法：Leanの前提を取り出し、仕様の文章と突き合わせる

<p class="lead-in">Leanの定理：<strong>仮説（条件） ⇒ 結論（保証）</strong></p>
<div class="grid">
<div class="panel"><p class="step-label">Step 1</p><h3>前提を抽出</h3><p><strong>仮説を列挙</strong></p><p class="actor">構文的・LLM不使用</p></div>
<div class="panel blue"><p class="step-label">Step 2</p><h3>仕様の文章と照合</h3><p>書かれているかを判定</p><p class="actor">キーワード照合器＋6種類のLLM</p></div>
</div>
<p class="message">抽出は構文を読むだけで、生成は入らない。<br>判定は自動で、正解ラベルとの照合は<strong>未実施</strong>。</p>

Note:
このスライドで話すこと：問いにどう答えたか。前提を取り出す段階と、仕様に書かれているかを判定する段階は別。
手法は二段です。
一段目は、Leanの定理文から仮説を取り出す処理です。定理文の構文を読むだけで、AIの生成は入りません。だから、証明に無い前提が混ざることはありません。
二段目は、取り出した前提が、仕様の文章に安全性の要件として書かれているかの判定です。ここは、キーワード照合器と6種類のLLMによる自動判定です。
判定器どうしの一致は見ていますが、人が付けた正解ラベルとの照合は、まだしていません。

---

<p class="section-tag">提案手法</p>

## 実験手法：定理に書かれた「条件」の部分を取り出す

<div class="grid" style="margin-bottom: 4px;">
<div><h3 style="margin: 0 0 8px;">定理文のコロンの手前を抜き出す</h3><div class="proof-code tight" style="padding: 8px 12px; font-size: 15px;"><div class="muted">theorem quorum_intersection_weight_lower</div><div class="muted">　{ qL qR vL vR : … }  -- 部品（除外）</div><div>　( hqLsub : <mark>qL ⊆ vL</mark> )</div><div>　( hqRsub : <mark>qR ⊆ vR</mark> )</div><div>　( hqLwt : <mark>τ.two_third (wt stake vL) ≤ wt stake qL</mark> )</div><div>　( hqRwt : <mark>τ.two_third (wt stake vR) ≤ wt stake qR</mark> )</div><div class="muted">　: 結論（保証）</div></div><p class="small" style="margin: 4px 0 0; font-size: 18px;">括弧群＝前提（Leanでは仮説）。構文的に列挙し実体条件を選別。</p></div>
<div class="premise-list"><h3 style="margin: 0 0 8px;">取り出される前提の意味</h3><div class="premise" style="padding: 6px 10px; margin-bottom: 6px; font-size: 20px;"><p style="margin: 0;"><strong>① 参加者集合の包含：</strong><br>支持した参加者が、その側の集計対象に含まれる。</p></div><div class="premise" style="padding: 6px 10px; margin-bottom: 6px; font-size: 20px;"><p style="margin: 0;"><strong>② クォーラムの重み閾値：</strong><br>クォーラムの総重みに対して、2/3以上の重みが支持する。</p></div><p class="small" style="margin: 4px 0 0; font-size: 18px;">この条件を、<strong>両側（フォーク双方）</strong>で満たす必要がある。</p></div>
</div>
<p class="message" style="margin: 4px 0 0; font-size: 28px;">「2/3」という数字だけでなく、<br><strong>どの参加者集合・どの重みを使うか</strong>まで前提に含まれる。</p>

Note:
このスライドで話すこと：定理の仮説が、どの条件を指すかを具体例で示す。
左の記号は細かく読む必要はありません。要点は右の日本語2行です。「支持した人が名簿に入っているか」「全体の2/3以上いるか」。
定理文は「theorem 名前（仮説）…：結論」という形で、コロンの手前の括弧が前提です。ツールはこれをLeanの構文として読み、型やモデルの部品を除いて実体条件だけを選別します。
解釈も生成も挟まない決定的な処理で、何度やっても同じ一覧が出ます。今回は8ファイル17定理から延べ57件が出ました。

---

<p class="section-tag">実験結果</p>

## 抽出結果：Leanの前提は、仕様の文章に明示されていなかった

<p class="lead-in">Leanの定理から取り出した前提を、仕様の文章（89ファイル）と照合した。</p>
<img class="result-visual" src="figs/chart-premises.svg" alt="48/57件、84.2%のドーナツ図と57マス。青48マスは全自動判定で非明示、橙9マスは判定が分かれた" style="height:220px">
<p class="message"><strong>10概念中7概念</strong>が非明示と判定。<strong>「明示」と全員一致は0件。</strong></p>

Note:
このスライドで話すこと：抽出した前提は、仕様の文章に明示されていたか。自動判定の結果。
17の定理に由来する延べ57件の前提条件を、89の仕様ファイルと照合しました。「概念」の数え方は補足で説明します。
主な数字は、10概念中7概念が、すべての自動判定で「仕様の文章に安全性要件として明示されていない」と判定されたことです。
延べ件数では57件中48件で、全員が「明示」と同意した条件は0件でした。57件は同じ概念の反復を含むので、独立した57種類ではありません。
これはバグの数ではありません。判定はキーワード照合器と6種類のLLMによる自動判定で、正解ラベルとの照合はまだです。判定器どうしが一致した、という意味です。
次のスライドで、この非明示の前提の一つが、実際のバグと同じラベル圏にあった例を見ます。

---

<p class="section-tag">実験結果</p>

## 前提①の具体例：「2/3」は合っている。でも、何の2/3か？

<p class="lead-in">前のスライドで非明示と判定した「クォーラムの重み閾値」について、何が起きうるかを示す。</p>
<p class="label">仮想例（説明用）：8人・等しい重みで集計（色付き＝支持、灰＝対象外）</p>
<img class="scenario-visual" src="figs/scenario-denominators.svg" alt="実装Aは1〜6を、実装Bは3〜8を有権者（分母）とする。同じ仕様でも使う名簿が違うと分母がずれる。両方4/6だが分母も分子も重ならない">
<p class="message">両方とも4/6 ＝ 2/3。でも母集団が違えば、<strong>同じ保証は使えない。</strong></p>

Note:
このスライドで話すこと：抽出結果のうち「クォーラムの重み閾値」という非明示の前提1つを、具体例で掘り下げる。
仕様は「総重みの2/3が支持すれば正当化」と書きます。監査は「2/3の計算があるか」を見ますが、コードには確かに2/3があります。
でもその2/3は何を数えた2/3か。名簿はエポック毎に変動し、分岐中は枝ごとに別名簿です。どの集合・出席を想定した保証かは、仕様の文章からは読み取りにくい。
仮想例では実装Aは1〜6、実装Bは3〜8を対象に、どちらも4/6＝2/3ですが母集団が違います。

---

<p class="section-tag">考察</p>

## 前提②の具体例：Nimbus #461。壊れていたのは、計算ではなく状態

<p class="lead-in">抽出結果で非明示と判定した前提の一つが、実際のバグとどう関係しうるかを見る。</p>
<p class="label">justification_bits の更新（4ビットの履歴）</p>
<div class="bitstrip"><span class="bitname">justification_bits</span><div class="bit">1</div><div class="bit">0</div><div class="bit stale">0</div><div class="bit stale">1</div><span class="stale-label">← 古いビットが残った</span></div>
<p class="message">算術は正しい。壊れていたのは、<strong>計算に渡す状態</strong>。</p>
<p>非明示と判定した前提「クォーラム交差が未スラッシュ」と、このバグは<strong>同じラベル圏</strong>（justification-and-finality）を共有する。<br>前提の非明示が原因だとは示していない。確認項目にあれば気づけた可能性がある、という動機付けの一例。</p>

Note:
このスライドで話すこと：同じラベル圏で、実際に修正されたバグがある。
実際に修正された例です。Nimbus #461では、justification_bitsの上位ビットが残り、確定判定に使う状態がずれました。
算術ではなく、計算に渡す状態が壊れた例です。公開データセットでは、チェーン分岐に至り得ると分類されています。
このバグと、非明示と判定した前提「クォーラム交差が未スラッシュ」は、同じラベル（beacon-chain:justification-and-finality）を共有します。
ただし、前提の非明示がこのバグの原因だったとは示していません。コードパスが同一かも確認していません。示せるのは、ラベルが一致するという位置的な共起だけです。
その上で、仮にこの前提が確認項目として手元にあれば、気づけた可能性はあります。これは因果の証明ではなく、問題設定を支える動機付けの一例です。

---

<p class="section-tag">まとめ</p>

## まとめ：Leanの前提の多くは、仕様に明示されていなかった

<div class="grid three">
<div class="panel blue"><h3>分かったこと</h3><p>10概念中7概念が、仕様の文章に非明示と判定された（自動判定）。</p></div>
<div class="panel"><h3>言えること</h3><p>実装者は仕様書だけでなく、論文も読んで、前提を知っておきたい。</p></div>
<div class="panel orange"><h3>まだ言えないこと</h3><p>SPECAでの効果（発見数の比較）は今後の課題。判定が正解と一致するか。</p></div>
</div>
<p class="message">前提が仕様に書かれていれば、Leanは要らない。<br>書かれていないから、証明から取り出した。</p>

Note:
このスライドで話すこと：分かったことと、まだ言えないこと。
分かったのは、Leanの定理から取り出した前提のうち、10概念中7概念が、仕様の文章に安全性要件として明示されていないと自動判定されたことです。
ここから言えるのは、実装者は仕様書を読むだけでなく、論文も読んで、どんな前提で作られているかを理解しておく必要がある、というところまでです。
前提が仕様に書かれていれば、Leanは要りません。書かれていなかったので、証明から取り出しました。
まだ言えないのは、確認候補が実際の監査でバグを拾えるか、判定が正解と一致するか、他のシステムでも同じかです。
今後は、人手の正解ラベルによる検証と、実バグを参照せずに作った項目で、修正前のバグを再検出できるかを試します。ご清聴ありがとうございました。

---

<p class="section-tag">補足</p>

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
<p class="message" style="font-size: 26px; margin: 8px 0 0;">人には<strong>確認一覧</strong>、監査ツールには<strong>JSON</strong>。条件・定理・仕様の参照先はどちらもつながる。</p>

Note:
このスライドで話すこと：取り出した前提を、仕様・コード・担当に結びつける。
機械抽出して終わりではなく、その条件が仕様や実装のどこに対応するかを示します。右のJSONは監査ツールへ渡すデータ形式で、現場のエンジニアが確認するのは左の日本語一覧表だけで十分です。
重要度は仕様書の記述量ではなく安全性定理の構造に由来するため、仕様に書かれていない前提でも優先度が落ちません。
こうした項目が全部で27あり、そのうち17項目が前提条件を持ちます。この候補が、仕様の文章だけから得る項目とどれだけ異なるかを調べました。

---

<p class="section-tag">補足</p>

## 前提ごとに「誰が何を確認するか」を決める

<p>取り出した前提を、仕様・コードへ対応付け、<strong>担当と確認方法を割り当てる</strong>。</p>
<div class="grid">
<div class="panel blue"><h3>実装で確認する</h3><p>票の出所と集計対象の対応。<br>総重み・支持重みの計算。<br>状態の表現範囲。</p><p class="small">コード・テスト・レビューへ。</p></div>
<div class="panel purple"><h3>モデル・環境として確認する</h3><p>参加者の入れ替わり。<br>想定する違反者の規模。<br>どの条件下の保証を使うか。</p><p class="small">設計・運用・証明の適用範囲へ。</p></div>
</div>
<p class="message"><strong>すべての前提を単一のassertに変換するわけではない。</strong><br>条件の意味に応じて、確認の責任と手法を正しく割り当てる。</p>

Note:
このスライドで話すこと：前提を、誰がどう確認するかを決める。
取り出した前提には、実装で保つ条件と、モデルや環境についての仮定が含まれます。すべてをassertに置き換えるのではありません。
票と集計対象の対応や計算、状態の表現範囲はコードに結び付けられます。一方、攻撃者がどれだけの重みを持つかは関数のassertで確立するものではありません。
前提一覧を受け取ったら、意味と担当、確認方法を決める。この分担が、証明から得た条件を実務で使うために必要です。同じ考え方は、Raftなど共通仕様と独立した複数実装を持つ他のシステムにも当てはまる可能性があります。ただし、他のシステムでの効果は検証していません。

---

<p class="section-tag">補足</p>

## 安全性の核心：クォーラム交差の前提

<p style="margin: 6px 0 10px;">「仕様どおり」なのに結果が分かれる理由：合意仕様は<strong>数学的な安全性定理（クォーラム交差）</strong>に依存している。</p>
<img class="diagram votes-visual" style="height: 230px; margin: 6px auto; display: block;" src="figs/illustration-votes.svg" alt="同じ参加者集合と同じ票の重みなら、2つの3分の2の支持集合は少なくとも3分の1重なる">
<p class="takeaway" style="margin-top: 10px; padding: 10px 18px; font-size: 24px;">定理は「同じ参加者集合・同じ重み」を前提に安全を保証。<br><strong>その前提が仕様の文章に書かれていなければ、各実装で解釈が分かれる。</strong></p>

Note:
このスライドで話すこと：この安全性の定理は、仕様に書かれていない前提の上に立つ。
合意仕様の安全性を支えるのはクォーラム交差という数学的定理です。2/3以上の支持を集めた決定が2つあれば、少なくとも1/3は重なり、「同時に2つの履歴は確定しない」が保証されます。
ただしそれには「同じ参加者集合を分母に、同じ重みで計算する」という前提が必要です。この前提が仕様の文章に書かれているかは、のちの分析で確かめます。
前提が共有されなければ、各実装が仕様どおりに2/3を計算しても保証は崩れます。

---

<p class="section-tag">補足</p>

## なぜ、仕様を読むだけでは見えないのか

<img class="pipeline-visual" src="figs/diagram-spec-pipeline.svg" alt="3者の会話。理論家「前提Pなら、この動きで安全」（証明 P⇒Q）。仕様書「こう動いてね」（手順Sのみ）。実装者・監査者「前提がない。いつ正しいの？」（基準はSだけ）。前提Pを持つのは上流だけで、届く道は2つとも閉ざされている。仕様経由は転記で落ち、直接読むにも証明はLeanで下流は読めない">
<p class="message">安全が成り立つ<strong>前提条件</strong>は証明の側にあり、<br>実装者・監査者からは<strong>読みにくい</strong>。</p>
<p class="small">「証明」＝「この条件を満たせば保証が必ず成り立つ」を<strong>機械が検算</strong>した文書（Lean）。<br><strong>機械が受理した時点で、仮説に抜け漏れはない</strong>——書くべき前提の確かな一覧は証明の中にだけある。</p>

Note:
このスライドで話すこと：証明の前提は上流にあり、実装者と監査者の手元には届きにくい。
クォーラム交差のような安全性の前提が、なぜ仕様書に書かれないのか。
これは仕様書の欠陥というより、仕様書と証明の役割分担に起因します。
先に理論家による研究と設計があり、そこに安全性の証明、つまり「この前提が満たされるときに安全が成り立つ」という議論があります。
その設計を、実行できる手順に書き下したのが仕様書です。
実装者は手順に従ってコードを書き、監査者は手順を基準に確認します。
しかし、安全が成り立つための前提は証明の側にあり、仕様書の手順には現れにくいと考えられます。実際にどうかは、のちの分析で確かめます。
証明はLeanなどの形式言語で書かれており、現場が直接読むのも難しい。

---

<p class="section-tag">補足</p>

## 仕様どおりの実装は、証明の前提まで満たさない

<p>証明は<mark>保証書</mark>と同じ構造。条件内は保証、<strong>条件外は対象外</strong>。</p>
<img class="scope-visual" src="figs/diagram-guarantee-scope.svg" alt="証明は保証書。「前提Pを満たすなら安全Qを保証」とあるが、届くのはPを満たす実装だけ。満たさない実装は保証対象外">
<div class="route"><span>問題</span><strong>同じ「仕様どおり」でも、前提が満たされるかは仕様を読むだけでは区別がつかない</strong></div>
<div class="route"><span>仮説</span><strong>前提には、仕様に書かれていないものがある</strong></div>
<div class="route"><span>提案</span><strong>証明から取り出して、確認項目として渡す</strong></div>

Note:
このスライドで話すこと：仕様どおりでも、前提を満たしたかは区別できない。
仕様を読んでそのとおり実装するだけでは不十分です。仕様は「こう動け」という手順は教えますが、「証明が要求する前提をあなたの実装が満たしているか」は教えてくれません。
証明は保証書と同じで、条件内は保証、条件外は対象外です。その境界は仕様の手順には書かれていません。
そこで安全性の証明をもう一つの入力にします。提案は、証明が要求する前提を取り出し、実装・監査で使える確認候補へ変換することです。

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

## 補足：「概念」とは何か

<p>延べ57件の前提条件は、文言は違っても同じ安全性の要求を指すものがある。<br>それらをまとめたものが「概念」。10概念中7概念が、全自動判定で非明示。</p>
<table>
<thead><tr><th>概念の例</th><th>延べ件数での表れ方</th></tr></thead>
<tbody>
<tr><td>参加者集合の包含</td><td><code>qL ⊆ vL</code>、<code>qR ⊆ vR</code> など、定理ごとに複数回出現</td></tr>
<tr><td>クォーラムの重み閾値</td><td><code>two_third (wt stake v) ≤ wt stake q</code> など、定理ごとに複数回出現</td></tr>
</tbody>
</table>
<p class="small">同じ概念の反復を1件ずつ数えると延べ57件、重複を除くと10概念になる。延べ件数（57分の48）と概念単位（10分の7）は別の集計であり、取り違えないよう区別する。</p>

Note:
「概念」は、著者らが延べ57件の前提条件を意味のまとまりで分類した単位です。
機械的な抽出では、同じ安全性の要求が複数の定理に別々の変数名・式で現れます。それらをまとめたのが概念で、10個あります。
延べ件数（57分の48、84.2%）と、概念単位（10分の7）は、数え方が違う別の集計です。発表では概念単位の「10分の7」を主に使っています。

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
この三つは、他分野で考えられる確認候補の仮想例です。
Raftでは、メンバーシップ変更の過渡期に、多数派の交差が保たれるかが論点になります。証明側が要求する前提と、実装の手順との間にずれが生じ得る例です。
共通の仕様を複数のチームが独立に実装する構造は、他のシステムにもあります。
ただし、これらの対象で本研究が測定したわけではなく、監査での効果も確かめていません。形式証明がある対象では、その前提を追加の入力にできる、という見通しにとどまります。

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
<div><p class="label">仕様・証明・データ</p><p class="small">gasper-lean4（Nyx Foundation, commit 7650709）／ consensus-specs（commit 2359a5e）／ SPECA（Kamba, Sannai, <a href="https://arxiv.org/abs/2602.07513">arXiv:2602.07513 v2</a>）／ speca-lean4-plugin（tag 20260723-gasper）／ ethereum-vuln-dataset（commit c7c4ccb）</p></div>
<div><p class="label">イラスト・ロゴ</p><p class="small">公式Ethereumロゴ（ethereum.org brand assets）／ クライアント・言語ロゴ（各公式素材、詳細は <code>figs/logo-sources.json</code>）／ イラスト：Katerina Limpitsouni, unDraw</p></div>
</div>

Note:
参照資料と素材の出典です。
