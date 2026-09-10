**v1.8.0 — auto-update fixed: the app now discovers DeepSeek's models and prices dynamically.**

### What was wrong
DeepSeek **renamed and restructured** their pricing page: the model list changed (now `deepseek-flash` — V4.1 Flash — and `deepseek-v4-pro`; the vision model was merged into flash), the model names in the table are different, and prices changed. The app's parser was looking for the old hard-coded model ids, so the auto-update silently failed and the app kept showing the built-in snapshot.

### What's fixed
- 🔎 **Dynamic discovery** — the parser now reads the model columns straight from the table (any `deepseek-*` id), matches prices per column, and picks up display names from the `MODEL VERSION` row (e.g. `DeepSeek-V4.1-Flash` → "V4.1 Flash")
- 🔄 **The table rebuilds itself** when the model list changes — new, renamed or removed models appear on their own, no app update needed
- 🧮 New prices currently live: V4.1 Flash — off-peak $0.003 / $0.15 / $0.6, peak $0.006 / $0.3 / $1.2 per 1M tokens (cache-hit / cache-miss / output); V4 Pro unchanged at $0.022/$0.66/$1.98 off-peak
- 🐛 Fixed a sitemap-regex bug that produced garbage candidate URLs and wasted fetch attempts
- 📦 Built-in fallback snapshot refreshed to the current official data

### Verified
Live fetch succeeds in ~0.5 s from the official page, prices and peak windows parse correctly, the UI rebuilt itself from 2 → 3 models in a simulated model-set change, and the status row shows green "Prices up to date (official site)".

### Download
**DeepSeekPriceClock.exe** (~11 MB). SmartScreen warning? → **More info → Run anyway**.

### SHA-256
`a27484728a46e15acf5b76240d4280008b487bef9ca13a74f6c879e26866fb6a`

> Not affiliated with DeepSeek. Prices and peak hours fetched from DeepSeek's official docs.
