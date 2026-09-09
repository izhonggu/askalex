#!/usr/bin/env python3
"""
search_atoms.py — Retrieve knowledge atoms for the AskAlex skills.

The atom file is ~19 MB / 21,700 rows, so a skill must NEVER read it whole.
This is the retrieval layer: hybrid keyword+semantic scoring with pillar and
signal filters, returning only the top matches in a compact, LLM-friendly
shape.

Lexical scoring
    relevance = sum(tf(query_term)) / sqrt(len(atom))      # length-normalised
    final     = relevance * (1 + signal / 20)              # boost topical atoms
    Weak-signal atoms (signal < MIN_SIGNAL) are dropped by default because
    71% of this spoken corpus is general chat with no pillar topic; letting
    them through buries the useful atoms.

Semantic scoring (optional — needs the project venv, see below)
    Pure keyword matching misses atoms that discuss the same idea in
    different words (a user asking about "customers ghosting me" won't
    lexically match an atom about "no-shows"). If knowledge/atoms/embeddings.npy
    exists (built by scripts/build_embeddings.py), each query is also scored
    by cosine similarity against precomputed atom embeddings, and the two
    rankings are combined with Reciprocal Rank Fusion (RRF) — a rank-based
    fusion that needs no score normalization between the two very
    differently-scaled methods. If the embeddings file doesn't exist, or
    fastembed isn't installed, retrieval silently falls back to lexical-only
    (same behavior as before this feature existed) — semantic search is
    additive, never required.

    To enable it once:
        python3 -m venv .venv
        .venv/bin/pip install fastembed numpy
        .venv/bin/python3 scripts/build_embeddings.py
    After that, just keep calling this script with plain `python3` as usual —
    it re-execs itself under .venv's interpreter automatically when needed.

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
    python3 search_atoms.py "churn" --no-dedup           # show duplicates too
    python3 search_atoms.py "churn" --lexical-only       # skip semantic scoring
"""

from __future__ import annotations

import argparse
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
ROOT = find_root()
ATOMS = os.path.join(ROOT, "knowledge", "atoms", "atoms.jsonl")
EMB_FILE = os.path.join(ROOT, "knowledge", "atoms", "embeddings.npy")
EMB_IDS_FILE = os.path.join(ROOT, "knowledge", "atoms", "embeddings_ids.json")
VENV_PYTHON = os.path.join(ROOT, ".venv", "bin", "python3")

MODEL_NAME = "BAAI/bge-small-en-v1.5"
RRF_K = 60  # standard default for reciprocal rank fusion

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


def maybe_reexec_into_venv(want_semantic: bool) -> None:
    """If semantic search is wanted but this interpreter can't do it, and the
    project venv can, re-exec under the venv's python. No-op otherwise —
    lexical-only search never needed numpy/fastembed and still doesn't."""
    if not want_semantic:
        return
    try:
        import fastembed  # noqa: F401
        import numpy  # noqa: F401
        return  # already usable, nothing to do
    except ImportError:
        pass
    if os.path.isfile(VENV_PYTHON) and os.path.abspath(sys.executable) != os.path.abspath(VENV_PYTHON):
        os.execv(VENV_PYTHON, [VENV_PYTHON] + sys.argv)
    # no venv available — fall through and run lexical-only below


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


def load_semantic_index():
    """Returns (embeddings ndarray, id->row dict) or (None, None) if unavailable."""
    if not (os.path.isfile(EMB_FILE) and os.path.isfile(EMB_IDS_FILE)):
        return None, None
    try:
        import numpy as np
    except ImportError:
        return None, None
    vectors = np.load(EMB_FILE)
    with open(EMB_IDS_FILE, encoding="utf-8") as fh:
        ids = json.load(fh)
    id_to_row = {aid: i for i, aid in enumerate(ids)}
    return vectors, id_to_row


_MODEL_CACHE = None


def embed_query(query: str):
    global _MODEL_CACHE
    from fastembed import TextEmbedding
    import numpy as np
    if _MODEL_CACHE is None:
        _MODEL_CACHE = TextEmbedding(model_name=MODEL_NAME)
    vec = next(_MODEL_CACHE.embed([query]))
    norm = np.linalg.norm(vec)
    return vec / norm if norm else vec


def semantic_rank_ids(query: str, candidate_ids: list[str], vectors, id_to_row) -> list[str]:
    """Return candidate_ids sorted by semantic similarity to query, best first."""
    import numpy as np
    rows = [id_to_row[i] for i in candidate_ids if i in id_to_row]
    ids_here = [i for i in candidate_ids if i in id_to_row]
    if not ids_here:
        return []
    qvec = embed_query(query)
    sims = vectors[rows] @ qvec
    order = np.argsort(-sims)
    return [ids_here[i] for i in order]


def rrf_combine(*ranked_id_lists: list[str], k: int = RRF_K) -> dict[str, float]:
    """Reciprocal Rank Fusion: sum of 1/(k + rank) across every ranking an id
    appears in. Robust to the two methods' scores living on incomparable
    scales — only relative order within each list matters."""
    scores: dict[str, float] = defaultdict(float)
    for ranked in ranked_id_lists:
        for rank, aid in enumerate(ranked):
            scores[aid] += 1.0 / (k + rank + 1)
    return scores


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
    ap.add_argument("--lexical-only", action="store_true",
                    help="skip semantic scoring even if embeddings are available")
    ap.add_argument("--json", action="store_true", help="emit raw JSON lines")
    ap.add_argument("--full", action="store_true", help="do not truncate content")
    ap.add_argument("--chars", type=int, default=420, help="content truncation length")
    args = ap.parse_args()

    maybe_reexec_into_venv(want_semantic=not args.lexical_only)

    qt = terms(args.query)
    if not qt:
        print("No usable query terms.", file=sys.stderr)
        return 1

    atoms = load(args.min_signal, args.pillar, args.strong_only, args.source)
    if not args.no_dedup:
        atoms = dedup(atoms)
    by_id = {a["id"]: a for a in atoms}

    # lexical ranking over the whole filtered candidate pool (zero-score atoms
    # excluded from this ranking, same as before this feature existed)
    lex_scored = sorted(
        ((score_atom(a, qt), a["id"]) for a in atoms),
        key=lambda x: -x[0],
    )
    lexical_ranked_ids = [aid for s, aid in lex_scored if s > 0]
    lex_score_by_id = {aid: s for s, aid in lex_scored}

    semantic_used = False
    semantic_ranked_ids: list[str] = []
    if not args.lexical_only:
        vectors, id_to_row = load_semantic_index()
        if vectors is not None:
            try:
                semantic_ranked_ids = semantic_rank_ids(
                    args.query, list(by_id.keys()), vectors, id_to_row
                )
                semantic_used = True
            except Exception as e:  # model/runtime issue — degrade, don't crash a skill's turn
                print(f"(semantic scoring unavailable this run: {e})", file=sys.stderr)

    if semantic_used:
        combined = rrf_combine(lexical_ranked_ids, semantic_ranked_ids)
        ranked_ids = sorted(combined.keys(), key=lambda aid: -combined[aid])
    else:
        ranked_ids = lexical_ranked_ids

    if not ranked_ids:
        print(f"No atoms matched {qt!r} "
              f"(pillar={args.pillar}, min_signal={args.min_signal}, "
              f"strong_only={args.strong_only}).", file=sys.stderr)
        return 1

    shown = ranked_ids[: args.top]
    semantic_only_ids = set(semantic_ranked_ids[:50]) - set(lexical_ranked_ids) if semantic_used else set()

    for aid in shown:
        a = by_id[aid]
        if args.json:
            print(json.dumps(a, ensure_ascii=False))
            continue
        content = a["content"] if args.full or len(a["content"]) <= args.chars \
            else a["content"][: args.chars] + "..."
        # --pillar matches on primary OR secondary tags by design (a secondary-
        # tagged atom is still relevant) — but that means the atom's own
        # a["pillar"] can print as a *different* code than the one just
        # filtered on, which reads like the filter is broken if left silent.
        # Make the secondary-tag match explicit instead.
        pillar_note = ""
        if args.pillar and a["pillar"] != args.pillar:
            pillar_note = f" [secondary match for --pillar {args.pillar}]"
        match_note = " [semantic match — no keyword overlap]" if aid in semantic_only_ids else ""
        score_display = lex_score_by_id.get(aid, 0.0)
        print(f"[{a['id']}] {a['pillar']} {a['pillar_name']}{pillar_note} | signal={a['signal']} "
              f"| score={score_display:.2f}{match_note} | {a['title']}")
        print(f"    {content}")
        print(f"    — source: {a['source']}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
