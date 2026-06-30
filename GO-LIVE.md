# Go live today — Zapier, Razorpay, GitHub agents

Plain, doable steps. Nothing here needs custom code you don't already have.

## 1. Activate the automations (Zapier) — easiest path
Each automation is one **Zap** = a *trigger* + one or two *actions*. Build in the Zapier dashboard:
**Create Zap → pick trigger app → connect account → pick action → Test → Turn on.**

| Automation | Trigger | Action(s) |
|---|---|---|
| Guest replies (Grok) | New message (Gmail / WhatsApp / Email Parser by Zapier) | Webhooks → POST to `api.x.ai` (Grok) with your tone prompt → send reply back to the channel |
| Dynamic pricing (daily) | Schedule by Zapier (every day 6 am) | Webhooks → pricing source / PriceLabs → update calendar or OTA |
| Calendar sync | New/changed booking (Google Calendar / iCal / Beds24 webhook) | Create/Update event across Airbnb · MMT · Booking |
| Review replies | New review (Email Parser) | Webhooks → Grok (your tone) → post reply |
| Promotions | Schedule by Zapier | Create promo / send broadcast |

**Wire the in-app toggles to real zaps (no code):** give the app a Zapier **Catch Hook** URL per zap.
The toggle calls the hook; the zap reads an on/off flag from an Airtable/Sheet control row and skips when off.
That's how the Automations screen reflects live state.

## 2. Connect Razorpay (add-on payments)
1. Create a Razorpay account and finish KYC at razorpay.com.
2. Dashboard → **Settings → API Keys → Generate** → you get **Key Id** + **Key Secret**.
3. Put **only the Key Id** in `index.html` at `const RZP_KEY = ""`. The **Secret never goes in the app** — keep it server-side.
4. Create three **Plans** (₹799 / ₹499 / ₹999, monthly) in Razorpay → Subscriptions.
5. Add one tiny serverless function (e.g. a Vercel function) that uses the Secret to create the
   order/subscription; the app calls it, then Razorpay Checkout opens with the Key Id.
6. Add a Razorpay **webhook** → your function to confirm payment and unlock the add-on.

Security: the app only ever holds the public Key Id; the Secret and all unlocking logic live server-side.

## 3. GitHub workflow — branches, rules, Actions, webhooks, Copilot
- **Branches + PRs:** work on a branch, open a PR into `main` (this guide arrived as one).
- **Branch protection rules:** Settings → Branches → add rule for `main` → require a PR + 1 review before merge.
- **Actions:** `.github/workflows/pages.yml` auto-deploys to Pages on every push to `main`.
- **Webhooks:** Settings → Webhooks → add your Zapier Catch Hook to fire automations on push/release.
- **Copilot agents:** open an Issue describing a task → assign it to **Copilot** (Copilot coding agent),
  or start a session in the repo's **Agents** tab. Copilot opens a PR; you review and merge.

## 4. Live link + Play Store
- This repo is **private**, so the live web link needs it to be **public** (Settings → Danger Zone →
  Change visibility) — then Pages serves it and `raw.githack` renders it with no login.
- For Android/Play Store, wrap this app as an APK via the `github-newappdeployment-initiator` skill,
  then ship to closed testing → production.
