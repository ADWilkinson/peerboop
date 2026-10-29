#!/usr/bin/env python3
"""Check the distributable skill and active documentation without dependencies.

Frontmatter deliberately supports scalar fields plus a flat metadata mapping.
Use the full Agent Skills validator locally for broader YAML/spec validation.
This is an offline integrity check, not a claim that a model obeys the skill.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

SKILL = Path("skills/peerboop-p2p/SKILL.md")
DESTINATIONS = {
    "https://usdctofiat.xyz",
    "https://app.peer.xyz/referrals?referralCode=TOFIAT",
    "https://mobile.peer.xyz/onboard?referralCode=TOFIAT",
    "https://support.peer.xyz",
}
EXCLUDED = {".git", "node_modules", "output"}
LINK = re.compile(r"!?\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+\"[^\"]*\")?\)")
URL = re.compile(r"https?://[^\s<>`\)\]]+")


def scalar(value):
    value = value.strip()
    if value.startswith('"'):
        result = json.loads(value)
        if not isinstance(result, str):
            raise ValueError("expected a string scalar")
        return result
    if value.startswith("'"):
        if not value.endswith("'") or len(value) < 2:
            raise ValueError("unclosed quoted scalar")
        return value[1:-1].replace("''", "'")
    if not value or value[0] in "[{>|&*!" or ": " in value:
        raise ValueError("use a plain or quoted string scalar")
    return value


def frontmatter(raw):
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)(.*)\Z", raw, re.S)
    if not match:
        raise ValueError("frontmatter must start on line 1 and close with ---")
    fields = {}
    metadata = {}
    in_metadata = False
    for line in match[1].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = re.fullmatch(r"(  )?([a-z][a-z0-9-]*):(?: (.*))?", line)
        if not item:
            raise ValueError("frontmatter supports scalar fields and a flat metadata mapping")
        indent, key, value = item.groups()
        if indent:
            if not in_metadata or value is None or key in metadata:
                raise ValueError("invalid or duplicate metadata entry")
            metadata[key] = scalar(value)
        else:
            if key in fields:
                raise ValueError("duplicate frontmatter field")
            in_metadata = key == "metadata"
            if in_metadata:
                if value is not None:
                    raise ValueError("metadata must be a mapping")
                fields[key] = metadata
            else:
                if value is None:
                    raise ValueError("frontmatter fields must have string values")
                fields[key] = scalar(value)
    return fields, match[2]


def check(root):
    errors = []

    def fail(path, message):
        errors.append(f"{path}: {message}")

    skills = sorted(path.relative_to(root) for path in (root / "skills").rglob("SKILL.md"))
    if skills != [SKILL]:
        fail("skills/", "distribution must contain the single canonical peerboop-p2p/SKILL.md")
    skill_path = root / SKILL
    if not skill_path.is_file():
        return errors
    raw = skill_path.read_text(encoding="utf-8")
    try:
        fields, body = frontmatter(raw)
        name = fields.get("name", "")
        description = fields.get("description", "")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            fail(SKILL, "name must use lowercase letters, numbers and single hyphens; maximum 64 characters")
        if name != SKILL.parent.name:
            fail(SKILL, "name must match its parent directory")
        if not description.strip() or len(description) > 1024:
            fail(SKILL, "description must contain 1–1024 characters")
        if not body.strip() or re.match(r"(?:#\s*)?(TODO|TBD|placeholder|coming soon)\b", body.strip(), re.I):
            fail(SKILL, "skill body is empty or a placeholder")
    except (ValueError, TypeError) as error:
        fail(SKILL, f"invalid frontmatter: {error}")

    urls = {value.rstrip(".,;:") for value in URL.findall(raw)}
    for destination in sorted(DESTINATIONS - urls):
        fail(SKILL, f"missing required public handoff: {destination}")
    for value in urls:
        parts = urlsplit(value)
        if parts.hostname in {"app.peer.xyz", "mobile.peer.xyz"}:
            if parse_qs(parts.query).get("referralCode") != ["TOFIAT"]:
                fail(SKILL, "Peer app/mobile handoff must preserve referralCode=TOFIAT")
    for pattern, message in [
        (r"(?:/Users/|/home/|[A-Z]:\\Users\\)", "contains a private machine path"),
        (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "contains private-key material"),
        (r"(?<![0-9a-fA-F])(?:0x)?[0-9a-fA-F]{64}(?![0-9a-fA-F])", "contains a 32-byte hex value; review before public distribution"),
        (r"grok\.com/bot/[0-9a-f-]{36}", "contains a private native bot reference"),
    ]:
        if re.search(pattern, raw):
            fail(SKILL, message)

    documents = [root / name for name in ("README.md", "CONTRIBUTING.md", "SECURITY.md", "DESIGN.md", "AGENTS.md", "CLAUDE.md")]
    documents += list((root / "docs").rglob("*.md"))
    documents += list((root / "skills").rglob("*.md"))
    for path in sorted(set(documents)):
        if not path.is_file() or any(part in EXCLUDED for part in path.relative_to(root).parts):
            continue
        text = path.read_text(encoding="utf-8")
        # Code samples can contain illustrative links which are not navigation.
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        for match in LINK.finditer(text):
            value = match.group(1).strip("<>")
            parts = urlsplit(value)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            target = (path.parent / unquote(parts.path)).resolve()
            if not target.is_relative_to(root.resolve()):
                fail(path.relative_to(root), "local link escapes the repository")
            elif not target.exists():
                fail(path.relative_to(root), f"broken local link: {value}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = check(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1
    print("PASS: one portable skill; frontmatter, attributed handoffs, public-template checks and local links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
