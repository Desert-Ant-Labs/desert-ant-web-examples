# Vendored design system

A verbatim copy of [`Desert-Ant-Labs/design-system`](https://github.com/Desert-Ant-Labs/design-system)
(`styles.css`, `tokens/`, `swarm.js`), plus `../assets/` for the mark and favicons.

It is vendored rather than linked because the design-system repo is **private** and this
repo is **public** — a GitHub Pages visitor cannot fetch it. Copying also keeps the "no
build step" promise: the page links `lib/ds/styles.css` directly.

**Do not edit these files.** They are the design system's source of truth; changes belong
upstream. Page-specific styling lives in the `<style>` block in `index.html` and only ever
consumes the tokens.

## Re-syncing

```sh
./lib/ds/sync.sh
```

Clones the design system to a temp dir and overwrites the copies here. Review the diff and
commit. The dark palette is used as-is: `index.html` sets `data-theme` from the OS
`prefers-color-scheme`, so the design system's own `[data-theme="dark"]` block applies and
no colors are duplicated here.

Synced from design-system `1fb1449` (2026-08-21).
