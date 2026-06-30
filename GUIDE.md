# Residio — complete guide book

Everything in this package, what it does, and how to connect each piece. Plain language.

## 1. What you have
- **Live web app (PWA):** https://theempirestayys.github.io/residio-owners-op/ — installs on Android/iOS home screen.
- **Android APK:** https://github.com/theempirestayys/residio-owners-op/releases/download/android-latest/app-debug.apk
- **Repo (public):** https://github.com/theempirestayys/residio-owners-op
- **Self-running data pipeline:** `automation/ical_fetch.py` + the `ical-refresh` Action.
- **Automation blueprint:** `AUTOMATIONS.md` (15 automations, recipes + pricing).

## 2. The channel-manager config (put it in, it runs)
File: **`automation/ical_sources.json`**. This is the one place you set your data source — no channel-manager account needed:
```json
{ "sources": [
  { "property": "Bandra 2BHK", "channel": "Airbnb", "url": "PASTE_AIRBNB_ICAL_URL_HERE" }
] }
```
Get each `url` from **Airbnb → Listing → Availability → Export calendar** (a public link, not a login).
Add one line per property, commit, and the `ical-refresh` Action pulls your real bookings automatically.

## 3. Connecting the services (each one, step by step)
| Service | How |
|---|---|
| **iCal (Airbnb availability)** | Paste export URLs into `ical_sources.json` (above). No account. |
| **Beds24 → Zapier** | Beds24 has no native Zapier app. In Beds24: Settings → Apps/API → **Webhooks** → POST booking events to a **Zapier "Catch Hook"** URL. Then build the Zap from that trigger. (Or keep Beds24 ↔ n8n, already running.) |
| **Grok (Aria)** | Reconnect the **Grok by xAI** app inside the **Zapier MCP server** that Claude uses (re-add via Claude's connector settings if the config page is account-gated). |
| **Gmail / Google Sheets / WhatsApp** | Already connected in Zapier. |
| **Razorpay (add-ons)** | Put your **Key Id** in `index.html` (`RZP_KEY`); keep the Secret server-side. |

## 4. The "every 3 minutes" reality
GitHub Actions scheduled jobs have a **5-minute minimum** and are best-effort (often 5–15 min late) — they are **not** guaranteed every 3 minutes. For true 3-minute refresh you need a real always-on runner. You already have one: your **n8n on Hostinger** — set a 3-minute schedule node there to run the fetch and push, and it will hit 3 minutes reliably. The GitHub Action is the free, zero-maintenance fallback (every ~5–15 min).

## 5. Daily use
1. Open the app (home screen icon) → sign in (`master` / `residio@master`, or `staff` / `residio@staff`).
2. Home shows revenue, occupancy, by-channel split. Bookings → tap any for full detail.
3. Guests tab = the lifecycle hub (reservations, check-in/out, IDs, timeline, reviews).
4. Settings → toggle staff access + your preferences.

## 6. Rebuild / redeploy
- Edit `index.html` → push to `main` → Pages auto-deploys in ~10s.
- Edit `android/` → push → the APK rebuilds and republishes to the same Release link.
