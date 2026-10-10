from datetime import date
from hashlib import sha256
import json
from pathlib import Path
import re

from playwright.sync_api import sync_playwright


ETHEREUM_ASSETS = [
    ("web-infrastructure.png", "https://ethereum.org/_next/static/media/infrastructure_transparent.3n6b-a9kiks3t.png", "Infrastructure", "WT"),
    ("web-finance.png", "https://ethereum.org/_next/static/media/finance_transparent.111-t5d0dg_nt.png", "Finance", "WT"),
]
UNDRAW_ASSETS = [
    ("web-connected-world.svg", "https://undraw.co/illustration/connected-world_anke", "Connected world"),
    ("web-agreement.svg", "https://undraw.co/illustration/agreement_ftet", "Agreement"),
    ("web-voting.svg", "https://undraw.co/illustration/voting_3ygx", "Voting"),
]


def main():
    root = Path(__file__).parent / "figs"
    records = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(accept_downloads=True)
        for name, url, title, artist in ETHEREUM_ASSETS:
            response = context.request.get(url)
            assert response.ok and "image" in response.headers.get("content-type", ""), url
            content = response.body()
            (root / name).write_bytes(content)
            records.append({"file": "figs/" + name, "title": title, "artist": artist, "source_page": "https://ethereum.org/en/assets/", "asset_url": url, "license_reference": "https://github.com/ethereum/ethereum-org-website/blob/dev/LICENSE", "license_notice": "figs/ethereum-illustration-LICENSE.txt", "sha256": sha256(content).hexdigest(), "retrieved": str(date.today()), "modification": "none"})
            print(name, len(content), flush=True)
        license_response = context.request.get("https://raw.githubusercontent.com/ethereum/ethereum-org-website/dev/LICENSE")
        assert license_response.ok
        (root / "ethereum-illustration-LICENSE.txt").write_bytes(license_response.body())
        page = context.new_page()
        for name, url, title in UNDRAW_ASSETS:
            page.goto(url, wait_until="networkidle")
            with page.expect_download() as download_info:
                page.get_by_role("button", name=re.compile("Download SVG for your projects")).click()
            download = download_info.value
            assert download.failure() is None
            download.save_as(root / name)
            content = (root / name).read_bytes()
            assert b"<svg" in content
            records.append({"file": "figs/" + name, "title": title, "artist": "Katerina Limpitsouni / unDraw", "source_page": url, "download_method": "Official illustration page SVG download button", "license_reference": "https://undraw.co/license", "license_use": "Illustration in this academic presentation only; not for ML development or redistribution as an illustration pack.", "sha256": sha256(content).hexdigest(), "retrieved": str(date.today()), "modification": "none"})
            print(name, len(content), flush=True)
        browser.close()
    (root / "illustration-sources.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
