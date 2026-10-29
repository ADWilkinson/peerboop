#!/usr/bin/env python3
"""Write skills/peerboop-p2p/manifest.json from SKILL.md.

Installed bots read this manifest at the start of every turn and replace their
skill when the version is newer, so a merge to main is the release. Bump
metadata.version in SKILL.md, run this script, commit both files.
Use --check to fail if the manifest is out of date (CI does this).
"""

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/peerboop-p2p/SKILL.md"
MANIFEST = SKILL.with_name("manifest.json")
RAW = "https://raw.githubusercontent.com/ADWilkinson/peerboop/main/skills/peerboop-p2p/SKILL.md"


def expected():
    raw = SKILL.read_bytes()
    version = re.search(r'^  version: "([0-9]+\.[0-9]+\.[0-9]+)"$', raw.decode("utf-8"), re.M)
    if not version:
        raise SystemExit("SKILL.md needs metadata.version as a quoted x.y.z string")
    return {"version": version[1], "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "skill_url": RAW}


def main():
    want = expected()
    if "--check" in sys.argv:
        have = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else None
        if have != want:
            print("ERROR manifest.json does not match SKILL.md; run python3 scripts/release-manifest.py", file=sys.stderr)
            return 1
        print(f"PASS: manifest matches SKILL.md {want['version']}")
        return 0
    MANIFEST.write_text(json.dumps(want, indent=2) + "\n")
    print(f"wrote {MANIFEST.relative_to(ROOT)} for {want['version']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
