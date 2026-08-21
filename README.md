# Desert Ant Web Examples

[![Demo](https://img.shields.io/badge/%E2%96%B6%EF%B8%8E_Demo-open_in_browser-2D52C8?style=for-the-badge)](https://desert-ant-labs.github.io/desert-ant-web-examples/)

A single-page playground demonstrating every [Desert Ant Labs](https://desertant.com)
on-device model that runs in the browser. The web counterpart of
[desert-ant-ios-examples](../desert-ant-ios-examples): each model has its own
hand-written example UI, and models download on demand the first time you run
an example, with progress shown in the card.

No build step, no bundler, no backend: `index.html` is the whole app, and
`lib/ds/` is the design system it links. The model SDKs load from
[esm.sh](https://esm.sh) via an import map, and inference runs entirely
on-device (WebAssembly + [LiteRT.js](https://www.npmjs.com/package/@litertjs/core)).

## Examples

These tables are generated from [`lib/manifest.json`](lib/manifest.json), a
vendored copy of the model manifest in
[desert-ant-core](https://github.com/Desert-Ant-Labs/desert-ant-core) — the
source of truth for which models exist and which SDKs they ship. Run
[`lib/sync-manifest.py`](lib/sync-manifest.py) to re-pull it and rebuild them,
`--no-fetch` to rebuild offline, or `--check` to fail when they have drifted.
The example descriptions are read back out of `index.html`, so the cards and
the table cannot disagree.

<!-- BEGIN generated: lib/sync-manifest.py -->

| Model | Package | Example |
| --- | --- | --- |
| **Clear** | [`@desert-ant-labs/clear`](https://www.npmjs.com/package/@desert-ant-labs/clear) | Records mic audio, enhances it, and plays original against enhanced |
| **Emo** | [`@desert-ant-labs/emo`](https://www.npmjs.com/package/@desert-ant-labs/emo) | Suggests emoji for a piece of text, with confidences |
| **Gist** | [`@desert-ant-labs/gist`](https://www.npmjs.com/package/@desert-ant-labs/gist) | Classifies text into topics with scores |
| **Redact** | [`@desert-ant-labs/redact`](https://www.npmjs.com/package/@desert-ant-labs/redact) | Redacts PII (names, phone numbers, emails, and more) from text |
| **Shapes** | [`@desert-ant-labs/shapes`](https://www.npmjs.com/package/@desert-ant-labs/shapes) | Draw on a canvas, recognizes and snaps the shape |
| **Tongue** | [`@desert-ant-labs/tongue`](https://www.npmjs.com/package/@desert-ant-labs/tongue) | Language identification for short text, 84 languages. Pure JS, no wasm |

### Not on the web yet

Other public models in the manifest have no JavaScript SDK, so they cannot
run in a browser. Uhm is the next one planned for the web.

| Model | Category | JS | Ships as |
| --- | --- | --- | --- |
| **Align** | Word timestamps | — | Swift |
| **Clips** | Clip selection | — | Swift |
| **Moderator** | Content moderation | — | not released |
| **Schemer** | Structured extraction | — | not released |
| **Title** | Titles and descriptions | — | Swift |
| **Toxic** | Hate speech triage | — | not released |
| **Uhm** | Filler-word detection | planned | Swift |

The manifest also carries 3 internal models, not shown here.

<sub>Generated from `lib/manifest.json` (schema 1, SDK 3.0.0) by `lib/sync-manifest.py`. Do not edit by hand.</sub>

<!-- END generated -->

Below the examples, the **session log** panel is the web counterpart of the iOS
“Show all downloaded models” browser: a live file tree of everything fetched
this session (model files, weights, the LiteRT wasm runtime, SDK modules) with
per-file and per-folder sizes, plus the origin's storage estimate. It is styled
deliberately unlike the model cards, sunken and dashed with a mono header, so it
reads as instrumentation rather than another example to try. Unlike iOS there is
no on-disk model directory (the browser SDKs keep model bytes in memory and
re-fetches are served by the browser's HTTP cache), so this shows the session's
download log rather than a persistent cache.

## Design

The page is styled with the [Desert Ant Labs design system](https://github.com/Desert-Ant-Labs/design-system):
cool silver and obsidian neutrals, the polarized-sky cobalt accent, Instrument
Serif for display, Hanken Grotesk for UI, and JetBrains Mono for data. It
defaults to light like desertant.com and follows the OS into dark.

The design system is vendored under [`lib/ds/`](lib/ds) rather than linked,
because that repo is private and this one is public. `index.html` links
`lib/ds/styles.css` and builds only layout and component recipes on top of the
tokens. The one exception is the status badge, which carries the same literal
hex pairs the design system's own `Badge.jsx` hardcodes for its success and
danger tones, plus dark-mode values for them (`Badge.jsx` is light-mode only).

Run [`lib/ds/sync.sh`](lib/ds/sync.sh) to pull a newer copy of the design
system; see [`lib/ds/README.md`](lib/ds/README.md) for the details.

## Running

Serve the directory over HTTP (module scripts and mic access don't work from
`file://`):

```sh
python3 -m http.server 8080
# or: npx serve
```

Then open <http://localhost:8080>.

## Requirements

- A modern browser with import-map and WebAssembly support (any current
  Chrome, Firefox, Safari, Edge)
- Network access on first run of each example (models download from the
  Hugging Face Hub and are cached)
- Microphone access for the Clear example
