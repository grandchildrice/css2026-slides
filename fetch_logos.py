from datetime import date
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
from zipfile import ZipFile

from PIL import Image
from playwright.sync_api import sync_playwright


ASSETS = [
    ("ethereum.svg", "https://ethereum.org/en/assets/", "https://ethereum.org/images/assets/svgs/eth-diamond-rainbow.svg"),
    ("lighthouse.png", "https://lighthouse.sigmaprime.io/", "https://lighthouse.sigmaprime.io/favicon.ico"),
    ("nimbus.jpg", "https://nimbus.team/", "https://nimbus.team/community/ethnimbus.jpg"),
    ("teku.svg", "https://docs.teku.consensys.io/", "https://docs.teku.consensys.io/img/logo.svg"),
    ("lodestar.png", "https://lodestar.chainsafe.io/", "https://lodestar.chainsafe.io/favicons/apple-touch-icon.png"),
    ("language-rust.svg", "https://github.com/rust-lang/rust-artwork/", "https://raw.githubusercontent.com/rust-lang/rust-artwork/main/logo/rust-logo.svg"),
    ("language-nim.png", "https://github.com/nim-lang/assets", "https://raw.githubusercontent.com/nim-lang/assets/master/Art/logo-crown.png"),
    ("language-java.png", "https://dev.java/", "https://dev.java/assets/images/java-logo-vector.png"),
]

LANGUAGE_RIGHTS = {
    "language-rust.svg": {"attribution": "Rust Foundation / Rust project", "license": "CC BY 4.0 and Rust trademark policy", "license_reference": "https://creativecommons.org/licenses/by/4.0/", "policy_reference": "https://rustfoundation.org/policy/rust-trademark-policy/"},
    "language-nim.png": {"attribution": "Nim project", "policy_reference": "https://github.com/nim-lang/assets/blob/master/README.md"},
    "language-java.png": {"attribution": "Oracle / Java", "policy_reference": "https://www.oracle.com/legal/trademarks.html"},
}


def main():
    root = Path(__file__).parent / "figs"
    records = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        for name, site, url in ASSETS:
            response = context.request.get(url)
            assert response.ok, f"{response.status}: {url}"
            content = response.body()
            assert content and "image" in response.headers.get("content-type", ""), url
            path = root / name
            if url.endswith(".ico"):
                Image.open(BytesIO(content)).convert("RGBA").save(path)
            else:
                path.write_bytes(content)
            records.append({"file": "figs/" + name, "publisher_site": site, "asset_url": url, "retrieved": str(date.today()), "original_sha256": sha256(content).hexdigest(), "transformation": "ICO to PNG, original colors retained" if url.endswith(".ico") else "none", "usage": "Project identification in an academic presentation; rights retained by the original owners."})
            records[-1].update(LANGUAGE_RIGHTS.get(name, {}))
            print(name, len(content), flush=True)
        url = "https://www.typescriptlang.org/branding/typescript-design-assets.zip"
        response = context.request.get(url)
        assert response.ok
        content = ZipFile(BytesIO(response.body())).read("ts-logo-128.svg")
        (root / "language-typescript.svg").write_bytes(content)
        records.append({"file": "figs/language-typescript.svg", "publisher_site": "https://www.typescriptlang.org/branding/", "asset_url": url, "archive_member": "ts-logo-128.svg", "retrieved": str(date.today()), "original_sha256": sha256(content).hexdigest(), "transformation": "none", "attribution": "Microsoft / TypeScript", "policy_reference": "https://www.typescriptlang.org/branding/", "usage": "Nominative academic identification of the implementation language; no endorsement implied."})
        print("language-typescript.svg", len(content), flush=True)
        browser.close()
    (root / "logo-sources.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
