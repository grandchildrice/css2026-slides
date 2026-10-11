import base64
from html import escape
import json
import math
from pathlib import Path


ROOT = Path(__file__).parent
BLUE = "#006ba6"
NAVY = "#18334c"
PURPLE = "#6541a5"
ORANGE = "#a84c1d"


def text(x, y, value, size=27, color=NAVY, anchor="start", bold=False):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{700 if bold else 400}">{escape(value)}</text>'


def rect(x, y, width, height, fill="#eef6fc", stroke="#cbd8e2", radius=12, extra=""):
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" fill="{fill}" stroke="{stroke}" {extra}/>'


def arrow(points, color=BLUE):
    return f'<path d="{points}" fill="none" stroke="{color}" stroke-width="4" marker-end="url(#arrow)"/>'


def embedded_logo(name, x, y, width=76, height=76):
    mime = "image/svg+xml" if name.endswith(".svg") else "image/jpeg" if name.endswith(".jpg") else "image/png"
    encoded = base64.b64encode((ROOT / name).read_bytes()).decode()
    return f'<image data-logo-file="{escape(name)}" x="{x}" y="{y}" width="{width}" height="{height}" href="data:{mime};base64,{encoded}" preserveAspectRatio="xMidYMid meet"/>'


def save(name, body, description, height=340, attributes=""):
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 {height}" width="1200" height="{height}" role="img" {attributes}>
<title>{escape(description)}</title>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="{BLUE}"/></marker></defs>
<g font-family="Arial, Yu Gothic, Meiryo, sans-serif">{body}</g>
</svg>
'''
    (ROOT / name).write_text(content, encoding="utf-8")
    print(name)


def ledger_scene():
    body = rect(10, 32, 225, 263, "#fff6ee")
    body += '<circle cx="122" cy="93" r="26" fill="#ffbf75" stroke="#a84c1d" stroke-width="3"/><path d="M73 165 Q73 126 122 126 Q171 126 171 165" fill="#ffbf75" stroke="#a84c1d" stroke-width="3"/>'
    body += rect(85, 177, 76, 70, "white", "#a84c1d", 8)
    body += '<path d="M100 193 H145 M100 205 H135 M100 218 H145" stroke="#a84c1d" stroke-width="3"/>'
    body += text(122, 278, "送金を依頼", 27, anchor="middle", bold=True)
    body += arrow("M247 166 H305")
    for index, x in enumerate([335, 625, 915], 1):
        body += rect(x, 32, 263, 263, "#f4f8fc")
        body += rect(x + 53, 70, 157, 92, "white", BLUE, 8)
        body += '<path d="M{0} 165 V183 M{1} 184 H{2}" stroke="{3}" stroke-width="5"/>'.format(x + 132, x + 102, x + 162, BLUE)
        body += rect(x + 95, 92, 78, 48, "#eef6fc", BLUE, 3)
        body += f'<path d="M{x + 108} 107 H{x + 160} M{x + 108} 121 H{x + 150}" stroke="{BLUE}" stroke-width="3"/>'
        body += text(x + 132, 222, f"コンピュータ {index}", 26, anchor="middle", bold=True)
        body += text(x + 132, 266, "同じ履歴を検証・保存", 23, anchor="middle")
    body += '<path d="M598 115 H618 M888 115 H908 M598 202 H618 M888 202 H908" stroke="#8baec7" stroke-width="4"/>'
    save("illustration-ledger.svg", body, "送金の記録を複数のコンピュータが検証し、同じ取引履歴を共有する")


def client_scene():
    body = rect(10, 92, 235, 196, "#eef6fc", BLUE)
    body += rect(77, 116, 88, 101, "white", BLUE, 4)
    body += f'<path d="M95 142 H148 M95 160 H140 M95 178 H148 M95 196 H132" stroke="{BLUE}" stroke-width="4"/>'
    body += text(127, 238, "例：支持×3 ≥ 総重み×2", 15, NAVY, "middle")
    body += text(127, 268, "共通の合意層仕様", 23, anchor="middle", bold=True)
    body += f'<path d="M247 190 H273 V47 H1070" fill="none" stroke="{BLUE}" stroke-width="4"/>'
    clients = [("lighthouse.png", "Lighthouse", "Rust", "language-rust.svg", "Sigma Prime", "#f5f1fc"), ("nimbus.jpg", "Nimbus", "Nim", "language-nim.png", "Nimbus / Status", "#fff7ec"), ("teku.svg", "Teku", "Java", "language-java.png", "Consensys", "#eef8fb"), ("lodestar.png", "Lodestar", "TypeScript", "language-typescript.svg", "ChainSafe", "#fff4f6")]
    for index, (logo, name, language, language_logo, team, color) in enumerate(clients):
        x = 310 + index * 220
        body += arrow(f"M{x + 99} 47 V81")
        body += rect(x, 84, 198, 284, color)
        body += embedded_logo(logo, x + 61, 100)
        body += text(x + 99, 212, name, 29, anchor="middle", bold=True)
        body += text(x + 99, 253, language, 28, BLUE, "middle", True)
        if language == "Java":
            body += rect(x + 44, 264, 110, 64, NAVY, NAVY, 6)
            body += embedded_logo(language_logo, x + 49, 270, 100, 52)
        else:
            body += embedded_logo(language_logo, x + 75, 268, 48, 48)
        body += text(x + 99, 349, team, 19, anchor="middle")
    save("illustration-clients.svg", body, "共通仕様から四つの独立実装へ分岐。実装ロゴに加え、各言語名の下に公式の言語ロゴを表示", height=390)


def vote_scene():
    body = '<defs><clipPath id="right"><circle cx="700" cy="160" r="145"/></clipPath></defs>'
    body += '<circle cx="490" cy="160" r="145" fill="#eef6fc" stroke="#006ba6" stroke-width="4"/><circle cx="700" cy="160" r="145" fill="#f5f1fc" stroke="#6541a5" stroke-width="4"/>'
    body += '<circle cx="490" cy="160" r="145" fill="#ffe49b" clip-path="url(#right)"/>'
    body += text(195, 85, "記録 A を支持", 28, BLUE, "middle", True)
    body += text(195, 125, "重み ≥ 2/3", 29, BLUE, "middle")
    body += text(1000, 85, "記録 B を支持", 28, PURPLE, "middle", True)
    body += text(1000, 125, "重み ≥ 2/3", 29, PURPLE, "middle")
    body += '<path d="M325 100 H350 M846 100 H865" stroke="#8baec7" stroke-width="3"/>'
    for x, color in [(423, BLUE), (594, "#9b6b00"), (767, PURPLE)]:
        body += f'<circle cx="{x}" cy="115" r="15" fill="{color}"/><path d="M{x - 26} 165 Q{x - 26} 139 {x} 139 Q{x + 26} 139 {x + 26} 165" fill="{color}"/>'
    body += text(595, 211, "≥ 1/3", 29, "#805600", "middle", True)
    body += text(595, 260, "両方を支持", 24, "#805600", "middle")
    body += text(195, 246, "同じ参加者集合", 25, anchor="middle")
    body += text(1000, 246, "同じ票の重み", 25, anchor="middle")
    save("illustration-votes.svg", body, "同じ参加者集合と同じ票の重みなら、2つの3分の2の支持集合は少なくとも3分の1重なる。面積比は数量を表さない模式図")


def denominator_scene():
    scenario = json.loads((ROOT.parent / "css2026-slides.json").read_text(encoding="utf-8"))["motivating_scenario"]
    body = ""
    for row, (side, color) in enumerate([("A", BLUE), ("B", ORANGE)]):
        participants = set(scenario[f"participants_{side}"])
        supporters = set(scenario[f"supporters_{side}"])
        assert supporters <= participants
        y = 50 + row * 100
        body += text(15, y + 34, f"実装{side}", 30, color, bold=True)
        lo, hi = min(participants), max(participants)
        body += f'<rect x="{157 + (lo - 1) * 88}" y="{y - 8}" width="{(hi - lo) * 88 + 80}" height="80" fill="none" stroke="{color}" stroke-width="3" stroke-dasharray="9 6" rx="12"/>'
        body += text(157 + (lo - 1) * 88 + 10, y - 14, "有権者（分母）", 18, color, bold=True)
        for index in range(1, 9):
            fill = color if index in supporters else "white" if index in participants else "#e4e9ee"
            body += rect(165 + (index - 1) * 88, y, 72, 66, fill, color if index in participants else "#cbd8e2", 8, f'data-side="{side}" data-person="{index}" data-included="{str(index in participants).lower()}" data-support="{str(index in supporters).lower()}"')
            body += text(201 + (index - 1) * 88, y + 43, str(index), 30, "white" if index in supporters else NAVY, "middle", True)
        body += text(940, y + 44, f"{len(supporters)} / {len(participants)} = 2/3", 35, color, bold=True)
    save("scenario-denominators.svg", body, "仮想例。8人のうち実装Aは1〜6、実装Bは3〜8を分母にする（破線枠）。それぞれ4人が支持し4/6を満たすが、分母も支持者も重ならない。色付きは支持、白は対象内で非支持、灰色は対象外", height=235, attributes='data-scenario="illustrative"')


def pipeline_scene():
    body = rect(30, 55, 310, 190, "#f5f1fc", PURPLE)
    body += text(185, 100, "理論家（研究・設計）", 26, PURPLE, "middle", True)
    body += text(185, 148, "「前提 P なら、この動きで安全」", 20, NAVY, "middle")
    body += text(185, 200, "証明：P ⇒ Q", 24, PURPLE, "middle", True)
    body += arrow("M352 150 H428")
    body += text(390, 136, "翻訳", 22, NAVY, "middle")
    body += rect(440, 55, 320, 190, "#eef6fc", NAVY)
    body += text(600, 100, "仕様書", 29, NAVY, "middle", True)
    body += text(600, 148, "「こう動いてね」", 22, NAVY, "middle")
    body += text(600, 200, "手順 S（文章＋疑似コード）", 23, NAVY, "middle", True)
    body += arrow("M772 150 H848")
    body += text(810, 136, "利用", 22, NAVY, "middle")
    body += rect(860, 55, 310, 190, "#eef6fc", BLUE)
    body += text(1015, 100, "実装者・監査者", 26, BLUE, "middle", True)
    body += text(1015, 148, "「前提がない。いつ正しいの？」", 19, NAVY, "middle")
    body += text(1015, 200, "基準は仕様 S だけ", 24, BLUE, "middle", True)
    body += f'<path d="M185 250 V276" fill="none" stroke="{ORANGE}" stroke-width="3.5" stroke-dasharray="9 7"/>'
    body += f'<path d="M185 276 H1015" fill="none" stroke="{ORANGE}" stroke-width="3.5" stroke-dasharray="9 7"/>'
    body += text(600, 260, "前提 P を持つのは上流だけ", 21, ORANGE, "middle", True)
    body += text(597, 288, "×", 30, ORANGE, "middle", True)
    body += text(1012, 288, "×", 30, ORANGE, "middle", True)
    body += text(600, 318, "仕様経由 → 転記で落ちる", 20, ORANGE, "middle", True)
    body += text(600, 346, "直接読む → 証明は Lean。実装者・監査者は読めない", 20, ORANGE, "middle", True)
    save("diagram-spec-pipeline.svg", body, "理論家は前提Pから保証Qへの証明を持つ。仕様書は実装可能な手順Sを記し、実装者・監査者はSだけを基準にする。前提Pを持つのは上流だけで、下流へ届く道は2つとも閉ざされている。仕様経由は転記で落ち、直接読むにも証明はLeanで実装者・監査者は読めない", height=360)


def scope_scene():
    body = rect(330, 8, 540, 90, "#f5f1fc", PURPLE, 12)
    body += text(600, 46, "証明 ＝ 保証書", 29, PURPLE, "middle", True)
    body += text(600, 82, "「前提 P を満たすなら、安全 Q を保証」", 21, NAVY, "middle")
    body += arrow("M400 98 V142")
    body += text(430, 126, "保証が届く", 20, BLUE, "start", True)
    body += f'<path d="M800 98 V142" fill="none" stroke="{ORANGE}" stroke-width="3.5" stroke-dasharray="8 6"/>'
    body += text(770, 126, "✕ 届かない", 20, ORANGE, "end", True)
    body += rect(40, 148, 540, 178, "#eef6fc", BLUE, 12)
    body += rect(88, 164, 168, 38, "#ffffff", BLUE, 19)
    body += text(172, 190, "仕様どおり", 21, BLUE, "middle", True)
    body += text(310, 246, "前提 P を満たす実装", 25, BLUE, "middle", True)
    body += text(310, 290, "→ 保証が効く（安全）", 27, NAVY, "middle", True)
    body += rect(620, 148, 540, 178, "#fff6ee", ORANGE, 12)
    body += rect(668, 164, 168, 38, "#ffffff", ORANGE, 19)
    body += text(752, 190, "仕様どおり", 21, ORANGE, "middle", True)
    body += text(890, 246, "前提 P を満たさない実装", 25, ORANGE, "middle", True)
    body += text(890, 290, "→ 保証対象外", 27, NAVY, "middle", True)
    body += text(890, 318, "（壊れるとは、言っていない）", 18, "#516575", "middle")
    save("diagram-guarantee-scope.svg", body, "証明は保証書。前提Pを満たすなら安全Qを保証すると書くが、届くのはPを満たす実装だけ。満たさない実装は保証対象外（壊れるとは言っていない）。どちらの実装にも同じ「仕様どおり」の印が押されている", height=335)


def result_chart():
    research = json.loads((ROOT.parent / "css2026-slides.json").read_text(encoding="utf-8"))["research"]
    total = research["conditions_with_repetition"]
    non_explicit = research["unanimously_not_explicit"]
    disputed = research["disputed"]
    assert non_explicit + disputed == total
    fraction = non_explicit / total
    circumference = math.tau * 112
    body = f'<circle cx="225" cy="145" r="112" fill="none" stroke="{ORANGE}" stroke-width="40"/>'
    body += f'<circle class="non-explicit-arc" cx="225" cy="145" r="112" fill="none" stroke="{BLUE}" stroke-width="40" stroke-dasharray="{fraction * circumference:.8f} {circumference:.8f}" transform="rotate(-90 225 145)"/>'
    body += text(225, 139, f"{100 * fraction:.1f}%", 53, BLUE, "middle", True)
    body += text(225, 177, f"{non_explicit} / {total} 件", 28, anchor="middle", bold=True)
    body += text(550, 56, "1マス ＝ 延べ前提1件", 28, bold=True)
    for index in range(total):
        classification = "non-explicit" if index < non_explicit else "disputed"
        body += rect(550 + (index % 19) * 32, 85 + (index // 19) * 48, 26, 36, BLUE if index < non_explicit else ORANGE, "white", 3, f'class="premise {classification}" data-index="{index + 1}"')
    body += text(550, 272, f"青 {non_explicit} 件：全自動判定で非明示", 26, BLUE, bold=True)
    body += text(550, 310, f"橙 {disputed} 件：判定が分かれた", 26, ORANGE, bold=True)
    body += text(225, 306, "安全性要件としての文章の明示", 21, anchor="middle")
    save("chart-premises.svg", body, f"延べ{total}件中{non_explicit}件（{100 * fraction:.1f}%）は全自動判定で非明示、{disputed}件は判定が分かれた。ドーナツと{total}マスで可視化", attributes=f'data-total="{total}" data-non-explicit="{non_explicit}" data-disputed="{disputed}"')


if __name__ == "__main__":
    ledger_scene()
    client_scene()
    vote_scene()
    denominator_scene()
    pipeline_scene()
    scope_scene()
    result_chart()
