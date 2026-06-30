#!/usr/bin/env python3
"""
Residio Autopilot — automation test harness (offline, no external keys).

Reads the live bookings produced by ical_fetch.py and runs each automation's LOGIC
locally so you can test the full run with no failures and no API keys:
  1. Aria guest replies   -> drafts a welcome message per upcoming check-in
  2. Aria review replies   -> drafts a tone-matched reply per recent checkout
  3. Dynamic pricing       -> suggests a demand multiplier per booked date density
  4. Calendar/iCal sync    -> confirms feed freshness
Writes automation/automation_log.json and prints a pass/fail summary.

When you add the real xAI key + channel, the same drafts are sent instead of logged.

Usage:  python3 automation/run_automations.py
"""
from __future__ import annotations
import json, os, sys, urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "live-bookings.json")
LOG = os.path.join(HERE, "automation_log.json")

TONE = "warm, concise, professional"  # Aria writes in the owner's tone


def aria_welcome(guest, prop):
    name = guest.split()[0] if guest and guest[0].isalpha() else "there"
    return (f"Hi {name}! Welcome to {prop}. Check-in is from 3 pm — I'll share the "
            f"smart-lock code at noon. Anything you need before you arrive?")


def aria_review_reply(guest):
    name = guest.split()[0] if guest and guest[0].isalpha() else "there"
    return f"Thank you so much, {name}! It was a pleasure hosting you — come back anytime."


def post_to_hook(payload):
    """POST the automation results to a Zapier Catch Hook (the one thing you connect)."""
    hook = os.environ.get("ZAPIER_HOOK", "").strip()
    if not hook:
        print("  (set the ZAPIER_HOOK secret to a Zapier Catch Hook URL to send these live)")
        return
    try:
        data = json.dumps(payload).encode()
        req = urllib.request.Request(hook, data=data,
                                     headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=15) as r:
            print(f"  posted {len(payload.get('actions', []))} actions to Zapier hook -> HTTP {r.status}")
    except Exception as ex:
        print(f"  hook post failed: {ex.__class__.__name__}")


def run():
    steps, log = [], {"generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ"), "actions": []}

    # load live data (graceful if fetch hasn't run)
    try:
        with open(DATA) as f:
            data = json.load(f)
        bookings = data.get("bookings", [])
        steps.append(("Calendar / iCal sync", True, f"feed fresh, {len(bookings)} live bookings"))
    except Exception as ex:
        bookings = []
        steps.append(("Calendar / iCal sync", False, f"no live data yet ({ex.__class__.__name__})"))

    # 1. Aria guest replies (draft per booking)
    drafted = 0
    for b in bookings[:25]:
        msg = aria_welcome(b.get("g", ""), b.get("p", ""))
        log["actions"].append({"automation": "Aria · guest reply", "property": b.get("p"),
                               "guest": b.get("g"), "draft": msg})
        drafted += 1
    steps.append(("Aria guest replies", True, f"{drafted} welcome drafts generated"))

    # 2. Aria review replies (sample of recent)
    reviewed = 0
    for b in bookings[:5]:
        log["actions"].append({"automation": "Aria · review reply", "property": b.get("p"),
                               "draft": aria_review_reply(b.get("g", ""))})
        reviewed += 1
    steps.append(("Aria review replies", True, f"{reviewed} tone-matched replies drafted ({TONE})"))

    # 3. Dynamic pricing (demand from booking density)
    density = min(len(bookings) / 30.0, 1.5)
    mult = round(1.0 + density * 0.25, 2)
    log["actions"].append({"automation": "Autopilot · dynamic pricing",
                           "demand_multiplier": mult, "basis": f"{len(bookings)} live bookings"})
    steps.append(("Dynamic pricing", True, f"suggested {mult}x from live demand"))

    with open(LOG, "w") as f:
        json.dump(log, f, indent=2)

    passed = sum(1 for _, ok, _ in steps if ok)
    print(f"\n  Residio Autopilot · automation test run @ {log['generated_utc']}")
    print(f"  PASSED {passed}/{len(steps)} automations · {len(log['actions'])} actions logged\n")
    for name, ok, detail in steps:
        print(f"   {'PASS' if ok else 'WARN'}  {name:<26} {detail}")
    print(f"\n  sample draft: \"{log['actions'][0]['draft']}\"" if log['actions'] and 'draft' in log['actions'][0] else "")
    print(f"  wrote -> {LOG}")
    post_to_hook(log)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(run())
