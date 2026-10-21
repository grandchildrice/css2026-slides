"""配信用の dist/ を組み立てる。

    python build_site.py

リポジトリ直下には発表準備の原稿（materials/）や生成・検証スクリプトも置いてあるため、
配信するのは描画に必要なファイルだけに絞る。index.html と slides.md が参照する
figs/ の資産を実際に走査して集めるので、図を足しても本スクリプトの変更は要らない。
出典の記録（*-sources.json・ライセンス）は、図と離れないよう常に同梱する。
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
PAGES = ["index.html", "slides.md"]
PROVENANCE = ["figs/logo-sources.json", "figs/illustration-sources.json",
              "figs/ethereum-illustration-LICENSE.txt"]


def referenced_assets():
    found = set()
    for page in PAGES:
        text = (ROOT / page).read_text(encoding="utf-8")
        found |= set(re.findall(r"figs/[A-Za-z0-9._-]+", text))
    return found | set(PROVENANCE)


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    files = sorted(set(PAGES) | referenced_assets())
    for name in files:
        source = ROOT / name
        if not source.exists():
            raise SystemExit(f"参照先が見つからない: {name}")
        target = DIST / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    print(f"{len(files)} ファイルを {DIST} に配置した")
    for name in files:
        print(f"  {name}")


if __name__ == "__main__":
    main()
