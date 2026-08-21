#!/usr/bin/env python3
"""Re-pull the model manifest and regenerate the README model tables.

The manifest lives in Desert-Ant-Labs/desert-ant-core and is the source of
truth for which models exist and which SDKs they ship. It is vendored here as
lib/manifest.json so the tables can be rebuilt without network access.

The per-example descriptions are NOT in the manifest — they describe this
repo's hand-written example UIs — so they are read back out of index.html,
where they already live. Nothing is duplicated: the manifest owns the model
facts, index.html owns the example blurbs.

    ./lib/sync-manifest.py              # re-fetch, then regenerate
    ./lib/sync-manifest.py --no-fetch   # regenerate from the vendored copy
    ./lib/sync-manifest.py --check      # exit 1 if README is out of date (CI)
"""

import argparse
import json
import pathlib
import re
import sys
import urllib.request

MANIFEST_URL = (
    "https://raw.githubusercontent.com/Desert-Ant-Labs/desert-ant-core/main/manifest.json"
)
REPO = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = REPO / "lib" / "manifest.json"
README = REPO / "README.md"
INDEX = REPO / "index.html"

BEGIN = "<!-- BEGIN generated: lib/sync-manifest.py -->"
END = "<!-- END generated -->"


def fetch() -> None:
    with urllib.request.urlopen(MANIFEST_URL, timeout=30) as r:
        data = r.read()
    json.loads(data)  # fail loudly rather than writing a broken manifest
    MANIFEST.write_bytes(data)
    print(f"fetched {MANIFEST_URL} -> {MANIFEST.relative_to(REPO)}")


def example_descriptions() -> dict[str, str]:
    """Map model id -> the description shown on its card in index.html."""
    html = INDEX.read_text()
    out = {}
    for card in re.finditer(
        r'<details class="card" id="card-([a-z]+)".*?</summary>', html, re.S
    ):
        desc = re.search(r'<span class="desc">(.*?)</span>', card.group(0), re.S)
        if desc:
            out[card.group(1)] = " ".join(desc.group(1).split())
    return out


def render(manifest: dict, descriptions: dict[str, str]) -> str:
    models = manifest["models"]
    public = [m for m in models if m["visibility"] == "public"]
    web = [m for m in public if m["sdks"].get("js", {}).get("status") == "live"]
    rest = [m for m in public if m["sdks"].get("js", {}).get("status") != "live"]

    lines = [BEGIN, ""]
    lines += ["| Model | Package | Example |", "| --- | --- | --- |"]
    for m in sorted(web, key=lambda m: m["name"]):
        pkg = m["sdks"]["js"]["package"]
        npm = f"[`{pkg}`](https://www.npmjs.com/package/{pkg})"
        desc = descriptions.get(m["id"], m["summary"])
        lines.append(f"| **{m['name']}** | {npm} | {desc} |")

    missing = sorted(set(descriptions) - {m["id"] for m in web})
    if missing:
        lines += ["", f"<!-- cards with no live js SDK in the manifest: {', '.join(missing)} -->"]

    lines += ["", "### Not on the web yet", ""]
    lines += [
        "Other public models in the manifest have no JavaScript SDK, so they cannot",
        "run in a browser. Uhm is the next one planned for the web.",
        "",
    ]
    lines += ["| Model | Category | JS | Ships as |", "| --- | --- | --- | --- |"]
    for m in sorted(rest, key=lambda m: m["name"]):
        ships = [
            lang.capitalize() if lang != "js" else "JS"
            for lang in ("swift", "kotlin")
            if m["sdks"].get(lang, {}).get("status") == "live"
        ]
        js = m["sdks"].get("js", {}).get("status", "none")
        js = "planned" if js == "planned" else "—"
        lines.append(
            f"| **{m['name']}** | {m['category']} | {js} | {', '.join(ships) or 'not released'} |"
        )

    # Count only. The names are in the (public) desert-ant-core manifest, but
    # there is no reason for this README to advertise unreleased work.
    internal = [m for m in models if m["visibility"] != "public"]
    if internal:
        lines += ["", f"The manifest also carries {len(internal)} internal models, not shown here."]

    lines += [
        "",
        f"<sub>Generated from `lib/manifest.json` (schema {manifest['schemaVersion']}, "
        f"SDK {manifest['sdkVersion']}) by `lib/sync-manifest.py`. Do not edit by hand.</sub>",
        "",
        END,
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--no-fetch", action="store_true", help="use the vendored manifest as-is")
    ap.add_argument("--check", action="store_true", help="fail if README is out of date")
    args = ap.parse_args()

    if not args.no_fetch and not args.check:
        fetch()

    manifest = json.loads(MANIFEST.read_text())
    block = render(manifest, example_descriptions())

    readme = README.read_text()
    if BEGIN not in readme or END not in readme:
        print(f"error: {README.name} is missing the {BEGIN} / {END} markers", file=sys.stderr)
        return 2
    updated = re.sub(
        re.escape(BEGIN) + r".*?" + re.escape(END), lambda _: block, readme, flags=re.S
    )

    if args.check:
        if updated != readme:
            print("README.md model tables are out of date; run ./lib/sync-manifest.py", file=sys.stderr)
            return 1
        print("README.md model tables are up to date")
        return 0

    if updated == readme:
        print("README.md model tables already up to date")
    else:
        README.write_text(updated)
        print(f"regenerated the model tables in {README.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
