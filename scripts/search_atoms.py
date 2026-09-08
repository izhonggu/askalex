#!/usr/bin/env python3
"""
search_atoms.py — Retrieve knowledge atoms for the AskAlex skills.

The atom file is ~19 MB / 21,700 rows, so a skill must NEVER read it whole.
This is the retrieval layer: keyword + TF scoring with pillar and signal
filters, returning only the top matches in a compact, LLM-friendly shape.

Scoring
    relevance = sum(tf(query_term)) / sqrt(len(atom))      # length-normalised
    final     = relevance * (1 + signal / 20)              # boost topical atoms
    Weak-signal atoms (signal < MIN_SIGNAL) are dropped by default because
    71% of this spoken corpus is general chat with no pillar topic; letting
    them through buries the useful atoms.

Near-duplicate removal
    Hormozi repeats the same frameworks across many videos, and several of
    his books duplicate passages, so the raw corpus has clusters of
    near-identical atoms. Retrieval dedupes them by default (off with
    --no-dedup): atoms are prefix-bucketed by their first 12 words, then any
    pair with Jaccard >= 0.8 is treated as a duplicate and only the
    highest-signal copy survives. This is deliberately conservative — an atom
    that merely shares an opening ("so the first thing is...") but diverges
    is kept, because the spoken vs written versions of the same idea often
    differ enough that Jaccard stays well under the threshold.

Usage
    python3 search_atoms.py "raise prices churn" --top 8
    python3 search_atoms.py "objection handling" --pillar B2 --top 5
    python3 search_atoms.py "guarantee" --source book --top 5
    python3 search_atoms.py "guarantee" --min-signal 6 --json
    python3 search_atoms.py "lead magnet" --full        # no content truncation
    python3 search_atoms.py "churn" --no-dedup          # show duplicates too
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict


def find_root() -> str:
    """Walk up from this file to the project root.

    Resolved by marker directory instead of a fixed number of parent hops, so
    the script keeps working if it is moved elsewhere in the project.
    """
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        if os.path.isdir(os.path.join(d, "AskAlex YouTube Scripts")) or \
           os.path.isdir(os.path.join(d, "knowledge")):
            return d
        d = os.path.dirname(d)
    return d


HERE = os.path.dirname(os.path.abspath(__file__))
ATOMS = os.path.join(find_root(), "knowledge", "atoms", "atoms.jsonl")

STOP = set("""
a an the and or but if then than that this these those is are was were be been being
do does did doing have has had having i you he she we they it its his her their our
your my me him them us of in on at to for from with without into over under about
as by so very can could will would should may might must not no yes what which who
whom when where why how all any both each few more most other some such only own
same too just also get got make made take took go going gone come came want need
""".split())

DEFAULT_MIN_SIGNAL = 3

DEDUP_PREFIX_WORDS = 12   # atoms sharing fewer leading words are never compared
DEDUP_JACCARD = 0.8       # >= this similarity -> duplicate


def terms(q: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9']+", q.lower()) if w not in STOP and len(w) > 1]


def load(min_signal: int, pillar: str | None, strong_only: bool, source: str):
    out = []
    with open(ATOMS, encoding="utf-8") as fh:
        for line in fh:
            a = json.loads(line)
            if source != "all" and a.get("source_type") != source:
                continue
            if pillar and a["pillar"] != pillar and pillar not in a.get("secondary", []):
                continue
            if strong_only and a.get("weak"):
                continue
            if a.get("signal", 0) < min_signal:
                continue
            out.append(a)
    return out


def _norm_words(t: str) -> list[str]:
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).split()


def _shingles(ws: list[str], k: int = 4) -> set[tuple]:
    return {tuple(ws[i:i + k]) for i in range(len(ws) - k + 1)}


def _jaccard(a: str, b: str) -> float:
    A = _shingles(_norm_words(a))
    B = _shingles(_norm_words(b))
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)


def dedup(atoms: list[dict], jaccard: float = DEDUP_JACCARD) -> list[dict]:
    """Drop near-duplicate atoms, keeping the highest-signal copy.

    Sorting by signal desc first makes the survivor the most topical copy,
    then prefix-bucketing keeps the pairwise Jaccard check cheap: only atoms
    that already share their first 12 words are ever compared.
    """
    if not atoms:
        return atoms
    atoms = sorted(atoms, key=lambda a: (-a.get("signal", 0), -a.get("words", 0)))
    buckets: dict[str, list[dict]] = defaultdict(list)
    for a in atoms:
        prefix = " ".join(_norm_words(a["content"])[:DEDUP_PREFIX_WORDS])
        buckets[prefix].append(a)
    kept: list[dict] = []
    for grp in buckets.values():
        reps: list[dict] = []
        for a in grp:
            if any(_jaccard(a["content"], r["content"]) >= jaccard for r in reps):
                continue
            reps.append(a)
        kept.extend(reps)
    return kept


def score_atom(a: dict, qt: list[str]) -> float:
    blob = (a["title"] + " " + a["content"]).lower()
    words = re.findall(r"[a-z0-9']+", blob)
    if not words:
        return 0.0
    tf = Counter(words)
    hits = sum(tf[t] for t in qt)
    if not hits:
        return 0.0
    # title hits are worth more — the title is the atom's distilled topic
    title_hits = sum(t in a["title"].lower() for t in qt) * 2
    relevance = (hits + title_hits) / math.sqrt(len(words))
    return relevance * (1 + a.get("signal", 0) / 20)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("query", help="search terms, e.g. 'raise prices churn'")
    ap.add_argument("--pillar", default=None,
                    help="A1 A2 A3 B1 B2 B3 C1 C2 D E — restrict to one pillar")
    ap.add_argument("--source", default="all", choices=["all", "transcript", "book"],
                    help="restrict to a source type (transcript or book)")
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--min-signal", type=int, default=DEFAULT_MIN_SIGNAL)
    ap.add_argument("--strong-only", action="store_true",
                    help="only atoms with a clear topical signal (drops ~71%% chatter)")
    ap.add_argument("--no-dedup", action="store_true",
                    help="disable near-duplicate removal (show all matches)")
    ap.add_argument("--json", action="store_true", help="emit raw JSON lines")
    ap.add_argument("--full", action="store_true", help="do not truncate content")
    ap.add_argument("--chars", type=int, default=420, help="content truncation length")
    args = ap.parse_args()

    qt = terms(args.query)
    if not qt:
        print("No usable query terms.", file=sys.stderr)
        return 1

    atoms = load(args.min_signal, args.pillar, args.strong_only, args.source)
    if not args.no_dedup:
        atoms = dedup(atoms)
    scored = [(score_atom(a, qt), a) for a in atoms]
    scored = [(s, a) for s, a in scored if s > 0]
    scored.sort(key=lambda x: -x[0])

    if not scored:
        print(f"No atoms matched {qt!r} "
              f"(pillar={args.pillar}, min_signal={args.min_signal}, "
              f"strong_only={args.strong_only}).", file=sys.stderr)
        return 1

    for s, a in scored[: args.top]:
        if args.json:
            print(json.dumps(a, ensure_ascii=False))
            continue
        content = a["content"] if args.full or len(a["content"]) <= args.chars \
            else a["content"][: args.chars] + "..."
        print(f"[{a['id']}] {a['pillar']} {a['pillar_name']} | signal={a['signal']} "
              f"| score={s:.2f} | {a['title']}")
        print(f"    {content}")
        print(f"    — source: {a['source']}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
