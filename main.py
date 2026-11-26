#!/usr/bin/env python3
"""Rename the Planet — make.fun entry.

Writes one line (under 200 chars) to /output/entry.txt: a funny new name
for a solar-system planet plus the why, in the same breath.

Tournament winner (specificity / surprise / freshness 5/4/5 = 14):
Neptune becomes "The Overdue Library Book" — one orbit takes 165 years,
so by the time it comes back nobody remembers checking it out. The why
leans on Neptune's own trait (its 165-year orbital period) and fits no
other planet. The line is 120 chars, leaving an 80-char margin under the
200-char gate, so the gate has room to spare.
"""

import argparse
import pathlib
import sys

ENTRY = (
    "Neptune is now 'The Overdue Library Book', because it takes 165 years "
    "to come back and nobody remembers checking it out."
)

CANDIDATES = {
    "neptune-library": (
        "Neptune is now 'The Overdue Library Book', because it takes 165 years "
        "to come back and nobody remembers checking it out."
    ),
    "saturn-hoarder": (
        "Saturn is now 'The Hoarder', because it kept every ring it ever owned "
        "and refuses to throw a single one away."
    ),
    "mercury-intern": (
        "Mercury is now 'The Intern', because it does a full year of work in "
        "88 days and still gets paid nothing."
    ),
    "venus-sauna": (
        "Venus is now 'The Sauna With No Exit', because it is 465 degrees, "
        "raining acid, and the door has been locked since 1970."
    ),
    "jupiter-bouncer": (
        "Jupiter is now 'The Bouncer', because it is 300 years into one storm "
        "and still will not let asteroids into the club."
    ),
    "mars-mall": (
        "Mars is now 'The Empty Mall', because it used to have rivers and "
        "customers and now it just has dust and a food court that closed in 2010."
    ),
    "uranus-nap": (
        "Uranus is now 'The Sideways Nap', because it spins lying down and has "
        "been asleep on the job for four billion years."
    ),
    "neptune-email": (
        "Neptune is now 'The Reply-All Email', because it takes 165 years to "
        "get back to you and by then nobody cares."
    ),
}

# specificity / surprise / freshness, each 1-5
SCORES = {
    "neptune-library": (5, 4, 5),
    "saturn-hoarder": (4, 3, 3),
    "mercury-intern": (5, 4, 4),
    "venus-sauna": (5, 4, 4),
    "jupiter-bouncer": (4, 4, 4),
    "mars-mall": (3, 3, 3),
    "uranus-nap": (5, 4, 5),
    "neptune-email": (4, 4, 4),
}

GATE_MIN = 1
GATE_MAX = 200


def check(text: str) -> tuple[bool, str]:
    """Gate check: UTF-8 text of 1 to 200 characters, not only whitespace."""
    if not text or text.isspace():
        return False, "empty or whitespace only"
    n = len(text)
    if n < GATE_MIN or n > GATE_MAX:
        return False, f"{n} chars, outside 1-200"
    if "\n" in text:
        return False, "more than one line"
    margin = GATE_MAX - n
    return True, f"VALID, {n} chars, {len(text.encode('utf-8'))} bytes, {margin}-char gate margin"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Rename the Planet entry")
    parser.add_argument("--check", action="store_true",
                        help="gate-check the entry line and exit")
    parser.add_argument("--self-test", action="store_true",
                        help="write entry.txt twice and compare bytes")
    parser.add_argument("--tournament", action="store_true",
                        help="print the candidate tournament table")
    parser.add_argument("--out", default="/output/entry.txt",
                        help="output path (default /output/entry.txt)")
    args = parser.parse_args(argv)

    if args.tournament:
        print(f"{'candidate':<18}{'spec':>5}{'surp':>5}{'fresh':>6}{'total':>6}")
        for name, text in CANDIDATES.items():
            s = SCORES[name]
            print(f"{name:<18}{s[0]:>5}{s[1]:>5}{s[2]:>6}{sum(s):>6}  {len(text)} chars")
        winner = max(SCORES, key=lambda k: sum(SCORES[k]))
        print(f"winner: {winner} ({sum(SCORES[winner])})")
        return 0

    ok, msg = check(ENTRY)
    if args.check:
        print(msg)
        return 0 if ok else 1
    if not ok:
        print(f"gate failed: {msg}", file=sys.stderr)
        return 1

    out = pathlib.Path(args.out)
    if args.self_test:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(ENTRY, encoding="utf-8")
        first = out.read_bytes()
        out.write_text(ENTRY, encoding="utf-8")
        second = out.read_bytes()
        print("byte-identical" if first == second else "MISMATCH")
        return 0 if first == second else 1

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(ENTRY, encoding="utf-8")
    print(f"wrote {out} ({len(ENTRY)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
