#!/usr/bin/env python3
"""
build_embeddings.py — Precompute semantic embeddings for every atom.

Run this once after (re)building knowledge/atoms/atoms.jsonl. search_atoms.py
uses the output to add semantic search on top of its existing keyword/TF
scoring, so queries that don't share vocabulary with an atom (e.g. a user
asking about "customers ghosting me" when the atom says "no-show") can still
match.

This needs the project venv (fastembed + numpy), not system Python:

    python3 -m venv .venv
    .venv/bin/pip install fastembed numpy
    .venv/bin/python3 scripts/build_embeddings.py

Output (both gitignored, same as atoms.jsonl itself — derived from the same
source material):
    knowledge/atoms/embeddings.npy       float32 array, shape (N, 384)
    knowledge/atoms/embeddings_ids.json  list of N atom IDs, same row order

Model: BAAI/bge-small-en-v1.5 (384-dim, ~130MB, English-only — the corpus is
entirely English prose, see skills/README.md's note on non-English queries
for why the *query* side still needs translation to English first).

Takes a few minutes for ~25K atoms on CPU. Safe to re-run; it always
regenerates both output files from the current atoms.jsonl.
"""

from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

try:
    from fastembed import TextEmbedding
except ImportError:
    print(
        "fastembed not found. This script needs the project venv:\n"
        "    python3 -m venv .venv\n"
        "    .venv/bin/pip install fastembed numpy\n"
        "    .venv/bin/python3 scripts/build_embeddings.py",
        file=sys.stderr,
    )
    sys.exit(1)


def find_root() -> str:
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        if os.path.isdir(os.path.join(d, "AskAlex YouTube Scripts")) or \
           os.path.isdir(os.path.join(d, "knowledge")):
            return d
        d = os.path.dirname(d)
    return d


ROOT = find_root()
ATOMS = os.path.join(ROOT, "knowledge", "atoms", "atoms.jsonl")
EMB_OUT = os.path.join(ROOT, "knowledge", "atoms", "embeddings.npy")
IDS_OUT = os.path.join(ROOT, "knowledge", "atoms", "embeddings_ids.json")

MODEL_NAME = "BAAI/bge-small-en-v1.5"
BATCH_SIZE = 16  # kept small deliberately — this machine has 16GB RAM shared with a
                  # full desktop workload; a larger batch (256 was the first attempt)
                  # pushed the system into heavy swapping and never finished in 45+ min
PROGRESS_EVERY = 500


def main() -> int:
    if not os.path.isfile(ATOMS):
        print(f"No atoms file at {ATOMS} — run atomize.py first.", file=sys.stderr)
        return 1

    ids: list[str] = []
    texts: list[str] = []
    with open(ATOMS, encoding="utf-8") as fh:
        for line in fh:
            a = json.loads(line)
            ids.append(a["id"])
            # same text basis as the lexical scorer: title + content
            texts.append(a["title"] + " " + a["content"])

    print(f"Loaded {len(ids)} atoms. Loading {MODEL_NAME}...", flush=True)
    t0 = time.time()
    model = TextEmbedding(model_name=MODEL_NAME)
    print(f"Model ready in {time.time() - t0:.1f}s. Embedding in batches of {BATCH_SIZE}...", flush=True)

    # Preallocate and fill incrementally rather than materializing a giant list of
    # vectors first — keeps peak memory flat regardless of corpus size, and lets us
    # print real progress instead of blocking silently until everything is done.
    t0 = time.time()
    vectors = np.zeros((len(texts), 384), dtype=np.float32)
    done = 0
    for vec in model.embed(texts, batch_size=BATCH_SIZE):
        vectors[done] = vec
        done += 1
        if done % PROGRESS_EVERY == 0 or done == len(texts):
            elapsed = time.time() - t0
            rate = done / elapsed if elapsed > 0 else 0
            eta = (len(texts) - done) / rate if rate > 0 else float("inf")
            print(f"  {done}/{len(texts)} ({rate:.1f}/s, ETA {eta/60:.1f} min)", flush=True)
    print(f"Embedded {len(ids)} atoms in {time.time() - t0:.1f}s -> shape {vectors.shape}")

    # bge models are trained for cosine similarity via normalized dot product —
    # normalize once here so search_atoms.py can just do a dot product at query time.
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    vectors = vectors / norms

    np.save(EMB_OUT, vectors)
    with open(IDS_OUT, "w", encoding="utf-8") as fh:
        json.dump(ids, fh)

    print(f"Wrote {EMB_OUT} ({vectors.nbytes / 1e6:.1f} MB) and {IDS_OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
