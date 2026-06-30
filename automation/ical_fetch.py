#!/usr/bin/env python3
"""
Residio Autopilot — live iCal fetcher (no API key, no channel manager).

Reads automation/ical_sources.json (your Airbnb iCal export URLs — public links),
fetches each calendar live, parses the VEVENTs, and writes data/live-bookings.json
that the app loads. Run it on the PC on a loop/cron for "live every few minutes".

Zero external dependencies — standard library only. Designed to NOT fail:
every source is fetched in its own try/except and the run reports per-source status.

Usage:
  python3 automation/ical_fetch.py
"""
from __future__ import annotations
import json, os, sys, urllib.request, ssl
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, "ical_sources.json")
OUT = os.path.join(ROOT, "data", "live-bookings.json")
MON = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]


def fetch(url: str, timeout: int = 20) -> str:
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "Residio-Autopilot/1.0"})
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        return r.read().decode("utf-8", "replace")


def unfold(ics: str) -> list[str]:
    out = []
    for line in ics.splitlines():
        if line[:1] in (" ", "\t") and out:
            out[-1] += line[1:]
        else:
            out.append(line)
    return out


def parse_date(val: str):
    v = val.split(":")[-1].strip()
    for f in ("%Y%m%dT%H%M%SZ", "%Y%m%dT%H%M%S", "%Y%m%d"):
        try:
            return datetime.strptime(v, f)
        except ValueError:
            continue
    return None


def fmt(d):
    return f"{d.day} {MON[d.month-1]}" if d else "?"


def parse_events(ics: str):
    events, cur = [], None
    for line in unfold(ics):
        key = line.split(":", 1)[0].split(";", 1)[0].upper()
        if line.startswith("BEGIN:VEVENT"):
            cur = {}
        elif line.startswith("END:VEVENT"):
            if cur is not None:
                events.append(cur); cur = None
        elif cur is not None:
            if key == "DTSTART": cur["start"] = parse_date(line)
            elif key == "DTEND": cur["end"] = parse_date(line)
            elif key == "SUMMARY": cur["summary"] = line.split(":", 1)[-1].strip()
            elif key == "UID": cur["uid"] = line.split(":", 1)[-1].strip()
    return events


def main():
    with open(SRC) as f:
        cfg = json.load(f)
    bookings, report = [], []
    for s in cfg.get("sources", []):
        url, prop, ch = s.get("url", ""), s.get("property", "?"), s.get("channel", "Airbnb")
        if not url or url.startswith("PASTE_"):
            report.append({"property": prop, "status": "skipped (no URL yet)", "events": 0})
            continue
        try:
            ics = fetch(url)
            evs = parse_events(ics)
            kept = 0
            for e in evs:
                if not e.get("start"):
                    continue
                start, end = e["start"], e.get("end") or e["start"]
                # only keep current/future events to mirror a live booking list
                if end.date() < datetime.now(timezone.utc).date():
                    continue
                bookings.append({
                    "g": (e.get("summary") or "Reserved")[:40],
                    "p": prop, "ch": ch,
                    "in": fmt(start), "out": fmt(end),
                    "amt": 0, "st": "Confirmed",
                })
                kept += 1
            report.append({"property": prop, "status": "ok", "events": kept})
        except Exception as ex:  # never let one bad source kill the run
            report.append({"property": prop, "status": f"error: {ex.__class__.__name__}", "events": 0})

    bookings.sort(key=lambda b: b["in"])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    payload = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ"),
        "source": "iCal (no API key)",
        "count": len(bookings),
        "bookings": bookings[:60],
    }
    with open(OUT, "w") as f:
        json.dump(payload, f, indent=2)

    ok = sum(1 for r in report if r["status"] == "ok")
    print(f"\n  Residio Autopilot · iCal fetch @ {payload['generated_utc']}")
    print(f"  sources ok: {ok}/{len(report)}   total live bookings: {len(bookings)}")
    for r in report:
        mark = "OK " if r["status"] == "ok" else "-- "
        print(f"   {mark}{r['property']:<42} {r['status']:<22} {r['events']} events")
    print(f"  wrote -> {OUT}\n")
    # exit 0 always: partial success is still a successful run
    return 0


if __name__ == "__main__":
    sys.exit(main())
