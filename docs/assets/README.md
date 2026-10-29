# Peerboop P2P artwork

Peerboop is the blue waving character in `peerboop-character.png`, approved on 29 October 2026. This raster is the single character source. The layouts scale and position it without redrawing, recolouring or retouching it.

- `peerboop-character.png`: original transparent 1254 × 1254 approved PNG.
- `peerboop-avatar.svg` / `.png`: unchanged character fitted into a 512 × 512 avatar.
- `desk-hero.svg` / `.png`: 1200 × 600 README ticket. Use the PNG in GitHub Markdown.
- `desk-social.svg` / `.png`: 1200 × 630 social still.
- `marketing/`: the four 1080 × 1350 launch images. Each `.html` is the editable layout, `captures/` holds the unedited chat crops and `build.py` renders the PNGs. Provenance is in [Media notes](../launch/MEDIA.md).

The SVG files are editable **layouts containing the approved raster**, not vector versions of the character. Each embeds the PNG, so it is self-contained. Text and geometry remain editable. The retired linked-circle mascot is no longer used.

Marketing images use real captured Grok chat. Artwork contains no invented quote, response or market data. The character is independent artwork, not an official Peer or USDC logo.

Layout colours are blue `#2775CA`, ink `#17212E`, paper `#F4F7FB`, white `#FFFFFF` and rule `#C8D5E5`. The approved character retains its original colours. Type uses Arial/Helvetica with a sans-serif fallback. Layouts are still images with no animation. At 390px wide, the hero's supporting text is about 14px.

To regenerate PNGs, use an existing installation of [Sharp](https://sharp.pixelplumbing.com/) with `node docs/assets/render-art.cjs`. It refreshes embedded image data from `peerboop-character.png` and renders the layouts. Sharp is an optional artwork tool, not a dependency of the bot. Update SVG layouts and PNG exports together.

## Character provenance

Generated with ImageGen and selected by the user after reviewing alternatives. The approved PNG is preserved byte for byte; no vector redraw is claimed. Its SHA-256 is `85be558a6b41ca18dc1b48f7e79949b54d91d0ba6be1d719a0c436eee05c5d33`. An exact generation prompt is not included here; no prompt has been reconstructed.
