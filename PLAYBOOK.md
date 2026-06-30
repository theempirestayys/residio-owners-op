# Residio — operations playbook

How the whole system runs itself, who (which "digital employee") owns what, and the exact
sequence to go fully live. Pair this with `GUIDE.md` (setup) and `AUTOMATIONS.md` (recipes).

## The digital team (who does what)
| Role | Powered by | Owns |
|---|---|---|
| **Aria** (guest concierge) | Grok via Zapier | Guest replies, review responses, sentiment watch — all in your tone |
| **Autopilot** (ops engine) | GitHub Actions + Zapier | Runs every automation on schedule, posts to one Zapier hook |
| **Sync** (data) | `ical_fetch.py` + iCal | Pulls live bookings every 5 min — no channel-manager account |
| **Ledger** (money) | App + Razorpay | Payouts view, add-on upsells, daily revenue digest |
| **Concierge desk** (you / staff) | The app | Approve sensitive sends, handle exceptions Aria escalates |

## Architecture (one line)
**Beds24 / Airbnb iCal → `ical_fetch.py` (GitHub, every 5 min) → app shows live data, and
`run_automations.py` POSTs drafts to one Zapier Catch Hook → Zapier sends to WhatsApp / Gmail.**

## Go-live sequence (in order)
1. **Beds24:** Import from Airbnb + Booking.com (gives you properties). Then copy each room's
   **iCal export URL** (Settings → calendar sync) into `automation/ical_sources.json`.
2. **GitHub:** add secret `ZAPIER_HOOK` = a Zapier Catch Hook URL.
3. **Zapier:** one Zap — Webhooks Catch Hook (trigger) → branch by `action` → send via
   WhatsApp / Gmail / Hostaway. Reconnect **Grok** so Aria's drafts are real.
4. Done — the engine runs every 5 min; the app is live at the Pages URL + APK.

## Daily rhythm (automated)
- **6:00** pricing refresh · **8:00** owner digest (WhatsApp + Email + Sheet) ·
  **per check-in** smart-lock code + welcome · **per checkout** cleaning dispatch ·
  **per review** tone-matched reply · **continuous** double-booking guard + sentiment watch.

## Escalation rules (what Aria holds for you)
Auto-sends: welcomes, codes, check-in info, routine FAQs, review thanks.
Holds for your approval: refunds, complaints, price changes, anything flagged negative by Grok.

## Controls
- App → Settings → Staff access toggles (what staff can open) + Preferences.
- Pause any automation from the Automations screen (writes to the live flow).
- Everything is in GitHub — edit, push, it redeploys in ~10s.

## Honest limits (so nothing surprises you)
- GitHub schedules are best-effort (~5–15 min), not exactly every 3–5. For tighter timing use
  your **n8n on Hostinger**.
- Sending requires the `ZAPIER_HOOK` + a Zap; Aria requires Grok reconnected. Data (iCal) needs
  your export links. None are mine to authorize — everything else is built and running.
