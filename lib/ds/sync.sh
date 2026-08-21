#!/usr/bin/env sh
# Re-copy the vendored design system from the (private) upstream repo.
# Requires `gh` to be authenticated. Run from anywhere; paths are repo-relative.
set -eu

repo=$(cd "$(dirname "$0")/../.." && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

gh repo clone Desert-Ant-Labs/design-system "$tmp/ds" -- --depth 1 --quiet

cp "$tmp/ds/styles.css"      "$repo/lib/ds/styles.css"
cp "$tmp/ds/swarm.js"        "$repo/lib/ds/swarm.js"
cp "$tmp/ds"/tokens/*.css    "$repo/lib/ds/tokens/"
cp "$tmp/ds/assets/favicon.svg" "$tmp/ds/assets/mark.svg" \
   "$tmp/ds/assets/apple-touch-icon.png" "$repo/assets/"

echo "synced from design-system $(git -C "$tmp/ds" rev-parse --short HEAD)"
echo "note: index.html inlines the mark as SVG — re-check it if assets/mark.svg changed."
