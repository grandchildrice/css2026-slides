import argparse
import base64
import json
import math
from hashlib import sha256
import re
import xml.etree.ElementTree as ET
from pathlib import Path
import tempfile

from playwright.sync_api import sync_playwright


def verify(url, capture):
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.on("pageerror", lambda error: errors.append(str(error)))
        response = page.goto(url, wait_until="networkidle")
        separator = re.search(r'data-separator="([^"]+)"', response.text()).group(1)
        page.wait_for_function("window.Reveal && Reveal.isReady()")
        slides = page.evaluate("Reveal.getSlides().length")
        assert slides == 25, f"Expected 25 slides, got {slides}"
        assert page.locator(".slides aside.notes").count() == slides
        assert page.locator(".slides").inner_text().find("Note:") == -1
        page.wait_for_function("Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)")
        assert page.locator("img.architecture-visual").count() == 1
        assert page.locator("img.scenario-visual").count() == 1
        assert page.locator("img.web-illustration").count() == 2
        assert page.locator("img.scope-visual").count() == 1
        assert page.locator(".slides section:nth-child(2) .takeaway").count() == 0
        assert page.locator(".slides section:nth-child(2) img.ethereum-logo").get_attribute("src") == "figs/ethereum.svg"
        assert "証明から前提" in page.locator(".cover-claim").text_content()
        assert page.locator("img.result-visual").count() == 1
        assert page.locator("pre code").count() == 5
        assert page.locator("code.language-python").count() == 2
        assert page.locator("code.language-json").count() == 1
        sample = page.locator("code.language-python").nth(1).text_content()
        expected = "def unpack(bits):\n    return [(bits >> i) & 1\n            for i in range(4)]\nfor bits in range(16):\n    actual = (bits << 1) & 0b1111\n    expected = [0] + unpack(bits)[:3]\n    assert 0 <= actual < 16\n    assert unpack(actual) == expected"
        assert sample == expected
        exec(compile(expected, "slide-test-example", "exec"), {})
        assert page.locator(".slides h1").text_content() == "仕様どおりに実装すれば安全か"
        inventory = json.loads((Path(__file__).parent / "css2026-slides.json").read_text(encoding="utf-8"))
        titles = page.locator(".slides section > h2, .slides .cover h1").all_text_contents()
        assert titles == [slide["title"] for slide in inventory["slides"]]
        assert inventory["main_slides"] + inventory["appendix_slides"] == slides
        root = Path(__file__).parent
        sources = json.loads((root / inventory["illustration_sources"]).read_text(encoding="utf-8"))
        web_images = page.locator("img.web-illustration").evaluate_all("els => els.map(e => e.getAttribute('src'))")
        assert set(web_images) <= {source["file"] for source in sources}
        for source in sources:
            assert sha256((root / source["file"]).read_bytes()).hexdigest() == source["sha256"]
            assert source["source_page"].startswith(("https://ethereum.org/", "https://undraw.co/"))
            assert source["license_reference"]
        for visual in inventory["visuals"]:
            assert page.locator(f'.slides section:nth-child({visual["slide"]}) img[src="{visual["file"]}"]').count() == 1
        chart = ET.parse(root / "figs/chart-premises.svg").getroot()
        research = inventory["research"]
        assert int(chart.attrib["data-total"]) == research["conditions_with_repetition"]
        assert int(chart.attrib["data-non-explicit"]) == research["unanimously_not_explicit"]
        assert int(chart.attrib["data-disputed"]) == research["disputed"]
        tiles = [element for element in chart.iter() if "premise" in element.attrib.get("class", "").split()]
        assert len(tiles) == 57
        assert sum("non-explicit" in element.attrib["class"].split() for element in tiles) == 48
        assert sum("disputed" in element.attrib["class"].split() for element in tiles) == 9
        arc = next(element for element in chart.iter() if element.attrib.get("class") == "non-explicit-arc")
        arc_length, circumference = map(float, arc.attrib["stroke-dasharray"].split())
        assert math.isclose(circumference, math.tau * float(arc.attrib["r"]), abs_tol=1e-7)
        assert math.isclose(arc_length / circumference, 48 / 57, abs_tol=1e-9)
        clients = ET.parse(root / "figs/illustration-clients.svg").getroot()
        logos = clients.findall(".//{http://www.w3.org/2000/svg}image")
        assert len(logos) == 8
        assert {image.attrib["data-logo-file"] for image in logos} == {"lighthouse.png", "nimbus.jpg", "teku.svg", "lodestar.png", "language-rust.svg", "language-nim.png", "language-java.png", "language-typescript.svg"}
        for image in logos:
            assert base64.b64decode(image.attrib["href"].split(",", 1)[1]) == (root / "figs" / image.attrib["data-logo-file"]).read_bytes()
            if image.attrib["data-logo-file"].startswith("language-"):
                assert float(image.attrib["y"]) > 253
        scenario = inventory["motivating_scenario"]
        diagram = ET.parse(root / "figs/scenario-denominators.svg").getroot()
        assert diagram.attrib["data-scenario"] == "illustrative"
        assert scenario["kind"] == "illustrative_only"
        assert scenario["weight_per_participant"] == 1
        for side in ["A", "B"]:
            included = set(scenario[f"participants_{side}"])
            supported = set(scenario[f"supporters_{side}"])
            assert supported <= included
            assert len(supported) * 3 == len(included) * 2
            boxes = [element for element in diagram.iter() if element.attrib.get("data-side") == side]
            assert len(boxes) == 8
            for box in boxes:
                person = int(box.attrib["data-person"])
                assert (box.attrib["data-included"] == "true") == (person in included)
                assert (box.attrib["data-support"] == "true") == (person in supported)
        assert not set(scenario["supporters_A"]) & set(scenario["supporters_B"])
        assert set(scenario["participants_A"]) | set(scenario["participants_B"]) == set(scenario["all_participants"])
        for newline in ["\n", "\r\n"]:
            regression = page.evaluate("""({newline, separator}) => {
                const input = ['# One', '', 'Note:', 'Private one', '', '---', '', '# Two', '', 'Note:', 'Private two'].join(newline);
                const html = Reveal.getPlugin('markdown').slidify(input, {separator, notesSeparator: '^Note:'});
                return {slides: (html.match(/<section /g) || []).length, notes: (html.match(/<aside class="notes">/g) || []).length};
            }""", {"newline": newline, "separator": separator})
            assert regression == {"slides": 2, "notes": 2}, regression
        output = Path(tempfile.mkdtemp(prefix="css2026-preview-")) if capture else None
        if output:
            print(json.dumps({"screenshots": str(output)}), flush=True)
        for viewport in [{"width": 1280, "height": 720}, {"width": 1920, "height": 1080}, {"width": 1024, "height": 768}, {"width": 390, "height": 844}]:
            page.set_viewport_size(viewport)
            for index in range(slides):
                page.evaluate("i => Reveal.slide(i)", index)
                page.wait_for_timeout(100)
                result = page.evaluate("""() => {
                    const slide = Reveal.getCurrentSlide();
                    const frame = document.querySelector('.slides').getBoundingClientRect();
                    const visible = Array.from(Reveal.getSlides()).filter(s => getComputedStyle(s).display !== 'none' && getComputedStyle(s).visibility !== 'hidden' && Number(getComputedStyle(s).opacity) > 0);
                    const outside = Array.from(slide.querySelectorAll('*')).filter(e => !e.closest('aside.notes') && e.getBoundingClientRect().width > 0 && getComputedStyle(e).visibility !== 'hidden').filter(e => {
                        const b = e.getBoundingClientRect();
                        return b.left < frame.left - 2 || b.right > frame.right + 2 || b.top < frame.top - 2 || b.bottom > frame.bottom + 2;
                    }).map(e => e.tagName + ':' + e.className);
                    const overflowingCode = Array.from(slide.querySelectorAll('pre, pre code')).filter(e => e.scrollWidth > e.clientWidth + 2).map(e => e.tagName);
                    return {visible: visible.length, outside, overflowingCode, notes: getComputedStyle(slide.querySelector('aside.notes')).display, title: slide.querySelector('h1,h2').innerText};
                }""")
                assert result["notes"] == "none", f"Visible notes on slide {index + 1}"
                assert result["visible"] == 1, f"Multiple visible slides: {result}"
                assert not result["outside"], f"Overflow {viewport} slide {index + 1}: {result}"
                assert not result["overflowingCode"], f"Code overflow slide {index + 1}: {result}"
                if output and viewport["width"] == 1280:
                    page.screenshot(path=str(output / f"slide-{index + 1:02}.png"))
            print(f"PASS: {viewport['width']}x{viewport['height']}, {slides} slides")
        page.evaluate("Reveal.slide(0)")
        page.keyboard.press("ArrowRight")
        assert page.evaluate("Reveal.getIndices().h") == 1
        with page.expect_popup() as popup_info:
            page.keyboard.press("s")
        popup = popup_info.value
        popup.wait_for_load_state()
        popup.wait_for_timeout(1500)
        assert "Speaker" in popup.title(), popup.title()
        popup.wait_for_function("document.body.innerText.includes('第三者')")
        assert not errors, errors
        print("PASS: keyboard navigation, notes popup, images, no JavaScript errors")
        if output:
            print(json.dumps({"screenshots": str(output)}))
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", nargs="?", default="http://localhost:8791")
    parser.add_argument("--capture", action="store_true")
    args = parser.parse_args()
    verify(args.url, args.capture)
