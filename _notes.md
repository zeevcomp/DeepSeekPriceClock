**v1.7.0 — the price table now shows every price, in a cleaner card design.**

### What's new
- 💰 **All prices visible** — the table previously showed only the currently active price; now each model shows **both off-peak and peak prices** side by side:
  - a row per state (`off-peak` / `peak`) × the three metrics (cache-hit input, cache-miss input, output)
  - the row matching the **current** state is highlighted in the state color (green off-peak / amber peak); the inactive row stays dim
- 🎨 **Prettier card design** — the table sits in its own panel with a subtle border, per-model groups with hairline dividers, and monospaced aligned numbers
- ✨ The smooth color-morph transition now also animates the table highlighting (every row's color eases over ~0.6 s on each state flip)

### Still included
- Analog clock by default with the thin frame that shows the current price state
- Silky ~30 fps hands, live local time zone, Hebrew + English UI
- Automatic price updates from the official DeepSeek pricing page (every 30 min + on demand)
- Single portable `.exe` — 64-bit Windows 10/11, no install

### Download
**DeepSeekPriceClock.exe** (~11 MB). SmartScreen warning? → **More info → Run anyway**.

### SHA-256
`d17adc8f8cc29288d537c05c51f28fb1550b914c337b4b319396d63e1d000148`

> Not affiliated with DeepSeek. Prices and peak hours fetched from DeepSeek's official docs.
