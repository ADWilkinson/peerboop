#!/usr/bin/env python3
"""Crop real Grok Bot chat bubbles out of a window capture without altering pixels.

Usage: crop_bubbles.py CAPTURE.png OUT_PREFIX X,Y [X,Y ...]

Each X,Y is any point inside one bubble or native card. The bubble is found by
walking out to the page background and cropped with a small margin of that
background, so rounded corners stay intact. Pixels are copied unchanged; the
marketing layout scales them. Requires Pillow.
"""

import sys
from PIL import Image

PAGE = (19, 19, 19)
MARGIN = 3


def is_page(pixel):
    return all(abs(a - b) <= 3 for a, b in zip(pixel[:3], PAGE))


def bubble_box(image, x, y):
    width, height = image.size
    px = image.load()
    left = x
    while left > 0 and not all(is_page(px[left - k, y]) for k in range(1, 4)):
        left -= 1
    right = x
    while right < width - 1 and not all(is_page(px[right + k, y]) for k in range(1, 4) if right + k < width):
        right += 1
    probe = min(left + 16, right)
    top = y
    while top > 0 and not all(is_page(px[probe, top - k]) for k in range(1, 3)):
        top -= 1
    bottom = y
    while bottom < height - 1 and not all(is_page(px[probe, bottom + k]) for k in range(1, 3) if bottom + k < height):
        bottom += 1
    # Rounded corners: widen to the widest row inside the bubble.
    for row in range(top, bottom + 1, 2):
        while left > 0 and not is_page(px[left - 1, row]):
            left -= 1
        while right < width - 1 and not is_page(px[right + 1, row]):
            right += 1
    return (max(left - MARGIN, 0), max(top - MARGIN, 0), min(right + MARGIN + 1, width), min(bottom + MARGIN + 1, height))


def main():
    capture, prefix, *points = sys.argv[1:]
    image = Image.open(capture).convert("RGB")
    for index, point in enumerate(points, 1):
        x, y = (int(value) for value in point.split(","))
        box = bubble_box(image, x, y)
        out = f"{prefix}-{index}.png"
        image.crop(box).save(out)
        print(out, box)


if __name__ == "__main__":
    main()
