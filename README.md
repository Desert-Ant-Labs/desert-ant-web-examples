# Desert Ant Web Examples

[![Demo](https://img.shields.io/badge/%E2%96%B6%EF%B8%8E_Demo-open_in_browser-e8a33d?style=for-the-badge)](https://raw.githack.com/Desert-Ant-Labs/desert-ant-web-examples/main/index.html)

A single-page playground demonstrating every [Desert Ant Labs](https://desertant.com)
on-device model that runs in the browser. The web counterpart of
[desert-ant-ios-examples](../desert-ant-ios-examples): each model has its own
hand-written example UI, and models download on demand the first time you run
an example, with progress shown in the card.

Everything is one `index.html` — no build step, no bundler, no backend. The
model SDKs load from [esm.sh](https://esm.sh) via an import map, and inference
runs entirely on-device (WebAssembly + [LiteRT.js](https://www.npmjs.com/package/@litertjs/core)).

## Examples

| Model | Package | Example |
| --- | --- | --- |
| **Emo** | [`@desert-ant-labs/emo`](https://www.npmjs.com/package/@desert-ant-labs/emo) | Suggests emoji for a piece of text, with confidences |
| **Redact** | [`@desert-ant-labs/redact`](https://www.npmjs.com/package/@desert-ant-labs/redact) | Redacts PII (names, phone numbers, emails, …) from text |
| **Gist** | [`@desert-ant-labs/gist`](https://www.npmjs.com/package/@desert-ant-labs/gist) | Classifies text into topics with scores |
| **Tongue** | [`@desert-ant-labs/tongue`](https://www.npmjs.com/package/@desert-ant-labs/tongue) | Language identification for short text, 84 languages (pure JS, web-only) |
| **Shapes** | [`@desert-ant-labs/shapes`](https://www.npmjs.com/package/@desert-ant-labs/shapes) | Draw on a canvas, recognizes and snaps the shape |
| **Clear** | [`@desert-ant-labs/clear`](https://www.npmjs.com/package/@desert-ant-labs/clear) | Records mic audio, enhances it, and plays original vs. enhanced |

Not on the web: **Clips**, **Uhm**, and **Title** ship as Swift/native packages
only (see the iOS examples).

The last card, **Downloaded files**, is the web counterpart of the iOS
“Show all downloaded models” browser: a live file tree of everything fetched
this session (model files, weights, the LiteRT wasm runtime, SDK modules) with
per-file and per-folder sizes, plus the origin's storage estimate. Unlike iOS
there is no on-disk model directory — the browser SDKs keep model bytes in
memory and re-fetches are served by the browser's HTTP cache — so this shows
the session's download log rather than a persistent cache.

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
