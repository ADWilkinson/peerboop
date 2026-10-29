#!/usr/bin/env python3
"""Lay out the Peerboop marketing images around genuine Grok Bot captures.

Each image places unedited bubble crops from captures/ (see docs/launch/MEDIA.md)
in their original order and scales every crop in an image by the same factor.
Headlines, the character and the capture note sit outside the chat panel.
Writes <name>.html (the editable layout) and renders <name>.png with Chrome.
"""

import subprocess
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PANEL = 1016  # widest crop is scaled to at most this many pixels
CAPTURED = "Real Grok Bot chat · Peerboop P2P 1.6.2 · prices captured 29 Oct 2026, 16:18 UTC"

IMAGES = [
    {
        "name": "01-buy",
        "kicker": "Buy USDC",
        "crops": [("buy-1", "right"), ("buy-2", "left"), ("buy-3", "left")],
        "max_scale": 1.8,
    },
    {
        "name": "02-sell",
        "kicker": "Sell USDC",
        "crops": [("sell-1", "right"), ("sell-2", "left"), ("sell-3", "left")],
        "max_scale": 1.8,
    },
    {
        "name": "03-venmo",
        "kicker": "Every payment app",
        "crops": [("venmo-1", "right"), ("venmo-2", "left"), ("venmo-3", "left")],
        "max_scale": 1.8,
    },
    {
        "name": "04-track",
        "kicker": "Track a deposit",
        "crops": [("trackq-1", "right"), ("trackq-2", "left"), ("trackc-1", "left"), ("trackr-1", "left")],
        "max_scale": 1.8,
        "mascot": False,
        "note": "Real Grok Bot chat · Peerboop P2P 1.6.2 · public deposit read 29 Oct 2026, 16:19 UTC",
    },
]

CSS = """
:root { --blue: #2775CA; --ink: #17212E; --paper: #F4F7FB; --chat: #131313; --muted: #4A5B70; }
* { box-sizing: border-box; margin: 0; }
html, body { width: 1080px; height: 1350px; }
body { background: var(--paper); color: var(--ink); font-family: "Helvetica Neue", Arial, sans-serif; overflow: hidden;
  display: flex; flex-direction: column; padding: 40px 20px 32px; }
.brand { padding-left: 16px; display: flex; align-items: center; gap: 14px; font-weight: 700; font-size: 30px; letter-spacing: -0.01em; }
.brand img { width: 68px; height: 68px; }
.stage { margin-top: 28px; }
.panel { width: 100%; background: var(--chat); border-radius: 32px; padding: 28px 12px; display: flex; flex-direction: column; gap: 14px;
  box-shadow: 0 30px 70px rgba(23, 33, 46, .22); }
.panel img { display: block; }
.panel .right { align-self: flex-end; }
.panel .left { align-self: flex-start; }
.mascot { position: absolute; right: 44px; bottom: 70px; width: 200px; height: 200px; }
.foot { padding-left: 16px; font-size: 22px; color: var(--muted); }
"""


def render(spec):
    sizes = {name: Image.open(HERE / "captures" / f"{name}.png").size for name, _ in spec["crops"]}
    scale = min(spec["max_scale"], PANEL / max(width for width, _ in sizes.values()))
    crops = "\n".join(
        f'    <img class="{side}" src="captures/{name}.png" width="{round(sizes[name][0] * scale)}" '
        f'height="{round(sizes[name][1] * scale)}" alt="">'
        for name, side in spec["crops"]
    )
    mascot = '\n  <img class="mascot" src="../peerboop-character.png" alt="">' if spec.get("mascot", True) else ""
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Peerboop P2P · {spec['kicker']}</title>
<style>{CSS}</style>
</head>
<body>
  <div class="brand"><img src="../peerboop-character.png" alt="">Peerboop P2P</div>
  <div class="stage"><div class="panel">
{crops}
  </div></div>

</body>
</html>
"""
    page = HERE / f"{spec['name']}.html"
    page.write_text(html)
    out = HERE / f"{spec['name']}.png"
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
         "--window-size=1080,1350", f"--screenshot={out}", page.as_uri()],
        check=True, capture_output=True,
    )
    trim(out)
    print(out.name, f"scale {scale:.2f}")


def trim(path, pad=40):
    """Crop the empty paper below the chat panel so the image ends with the chat."""
    image = Image.open(path).convert("RGB")
    paper = image.getpixel((5, image.height - 5))
    px = image.load()
    bottom = image.height - 1
    while bottom > 0 and all(sum(abs(a - b) for a, b in zip(px[x, bottom], paper)) < 60 for x in range(0, image.width, 4)):
        bottom -= 1
    image.crop((0, 0, image.width, min(image.height, bottom + pad))).save(path)


if __name__ == "__main__":
    for spec in IMAGES:
        render(spec)
