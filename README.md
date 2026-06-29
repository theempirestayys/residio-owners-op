# Residio Owners — main app

The production owner application for **The Empire Stays** — a calm, classy, Airbnb-grade
panel for managing a short-term-rental portfolio. White + peach theme, smooth motion, a 3D
portfolio hero, live Zapier automations, and Razorpay-powered add-ons.

> The lightweight **wireframe** lives separately in `residio-sample-01` and is intentionally
> left untouched. **This** repo is the main app we build and ship to the Play Store.

## Sections
Dashboard · Properties · Bookings · Payouts · Inbox (Grok) · Reviews · Automations (Zapier) ·
Dynamic pricing · Add-ons (Razorpay) · Settings — with monthly/yearly and per-property filters.

## Run locally
Open `index.html`, or serve it:
```bash
python3 -m http.server 8080   # then visit http://localhost:8080
```

## Live
Auto-deploys to **GitHub Pages** on every push to `main` via `.github/workflows/pages.yml`.

## Connect the real services (see GO-LIVE.md)
- **Zapier** — the automations (Grok replies, daily pricing, calendar sync, reviews) are wired to zaps.
- **Razorpay** — paste your key id where marked in `index.html` (`RZP_KEY`) to enable add-on checkout.
  Secrets stay server-side; the app never stores keys.

## Next: Android / Play Store
Wrap this app as an installable APK via the `github-newappdeployment-initiator` skill, then
ship to the Play Store (closed testing → production).
