# Residio Automations — build-ready blueprint

Every automation Aria/Autopilot runs, with the exact trigger → action recipe. Build each as a
Zapier Zap (or n8n flow). Where Beds24 is the source, use **Beds24 → Zapier Webhook (Catch Hook)**
or the existing **Beds24 ↔ n8n** flow (Beds24 has no native Zapier app).

**Connections needed (your account actions):** reconnect **Grok by xAI** in Zapier · connect
**Hostaway** (or Beds24 webhook). Already connected: Gmail, WhatsApp Business, Google Sheets, LinkedIn.

## Guest engine
| Automation | Trigger | Actions |
|---|---|---|
| Guest replies | New guest message (Hostaway / WhatsApp / Email Parser) | Grok "Ask Grok" (your tone) → send via same channel |
| Welcome + check-in | Reservation confirmed; T-1d; noon day-of | Grok drafts → send; issue smart-lock code at noon |
| Review replies | New review (Hostaway) | Grok tone-matched reply → respond_to_review |
| Negative-review warning | New guest message | Grok categorize_text sentiment → if negative, alert you (WhatsApp) |
| Smart-lock codes | T-3h check-in / checkout | Issue code; revoke at checkout |
| Maintenance routing | Guest reports issue | Create ticket (Sheet) → alert manager (WhatsApp) |

## Revenue
| Automation | Trigger | Actions |
|---|---|---|
| Dynamic pricing | Daily 6am (Schedule) | Pull demand (web/PriceLabs) → update calendar/OTA |
| Competitor price watch | Daily (Schedule) | Grok live_search comparable listings → pricing nudge |
| Upsells (Razorpay) | Booking confirmed / mid-stay | Offer add-on → Razorpay payment link → unlock on paid |
| Win-back | 60 days after checkout (Schedule + Sheet) | Tailored return offer via WhatsApp/Email |
| Promotions | Schedule | Apply promo across channels |

## Operations
| Automation | Trigger | Actions |
|---|---|---|
| Calendar / iCal sync | New/changed booking | Sync Airbnb · MMT · Booking calendars |
| Double-booking guard | Overlapping reservation | Alert + auto-block the conflicting date |
| Cleaning dispatch | Checkout | Auto-WhatsApp cleaner: property + time |
| Daily owner digest | Daily 8am (Schedule) | Occupancy + payouts due + today's check-ins/outs → WhatsApp + Email + Sheet |

## Upsell pricing (Mumbai STR market reference — tune per property tier)
| Add-on | Price (₹) | Notes |
|---|---|---|
| Early check-in | 600 | from 12pm instead of 3pm |
| Late checkout | 700 | until 2pm instead of 11am |
| Airport pickup | 1,500 | sedan, one way |
| Breakfast / grocery stock | 800 | stocked before arrival |
| Mid-stay cleaning | 1,000 | stays of 4+ nights |

All prices charged via **Razorpay** payment links; the add-on unlocks on `payment.captured` webhook.
Secrets stay server-side; the app only holds the public Razorpay key id.
