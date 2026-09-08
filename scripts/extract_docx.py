#!/usr/bin/env python3
"""
extract_docx.py — Extract Alex Hormozi YouTube transcripts (.docx) into clean plain text.

Design context (measured, not assumed):
    The source .docx files are CAPTION-STYLE transcripts. Two problems:

    1. Every paragraph is a 5-8 word fragment broken on speaking cadence,
       not on sentence boundaries.
    2. Punctuation density is wildly inconsistent across files:
           - some files have 0 periods in 11k+ chars (raw auto-captions)
           - some are normal prose (~110 chars per period)
       So a single punctuation-based splitter produces either one giant
       "sentence" or correct sentences, depending on the file.

    Solution: ADAPTIVE splitting.
        - punctuation-rich  -> split on real terminators ( . ? ! )
        - punctuation-poor  -> split on discourse markers + length window
          (spoken language marks new propositions with "so / but / because /
          here's the thing / the point is ...", so those are reliable seams)

Outputs
    .workbuddy/extracted/<slug>.txt      one sentence per line
    .workbuddy/extracted/_catalog.json   index: id, slug, title, words, sentences, mode

Usage
    python3 extract_docx.py              # extract all
    python3 extract_docx.py --limit 5    # smoke test
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

import docx


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
ROOT = find_root()  # /AskAlex
SRC_DIR = os.path.join(ROOT, "AskAlex YouTube Scripts")
OUT_DIR = os.path.join(ROOT, ".workbuddy", "extracted")

# ------------------------------------------------------------------ config
MIN_WORDS = 12      # shorter than this -> merge with neighbour
TARGET_WORDS = 30   # ideal spoken sentence length
MAX_WORDS = 55      # hard cap: force a break even without a marker

# Spoken discourse markers that open a NEW proposition. Used only when the
# current buffer already reached MIN_WORDS, which keeps mid-clause "and/but"
# from shredding sentences.
MARKERS = re.compile(
    r"\b(?:"
    r"so|and so|but|but here's|and but|because|now|okay|ok|alright|right\?|"
    r"well|yeah|yes|no|look|see|here's|there's|that's|what's|which means|"
    r"the thing is|the point is|the reason|here's the thing|and that's|"
    r"let me|let's|i mean|you know|i think|i believe|i would|i'll|i want|"
    r"if you|when you|what you|how you|why you|the way|in other words|"
    r"for example|first|second|third|finally|then|anyways|anyway|"
    r"here's why|and here's|so here's|this is why|that's why"
    r")\b",
    re.I,
)

# False terminators that must not end a sentence.
_PROTECT = [
    (re.compile(r"(\d)\.(\d)"), r"\1<DOT>\2"),
    (re.compile(r"\b(Mr|Mrs|Ms|Dr|Prof|Sr|Jr|St|vs|etc|approx)\.", re.I), r"\1<DOT>"),
    (re.compile(r"\$(\d+)\.(\d+)"), r"$\1<DOT>\2"),
]
_SENT_END = re.compile(r"([.!?]+)[\"'\)\]]*\s+")


def normalise(raw: str) -> str:
    text = raw.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    return re.sub(r"\s+", " ", text).strip()


def _protect(text: str) -> str:
    for pat, rep in _PROTECT:
        text = pat.sub(rep, text)
    return text


def split_punct(text: str) -> list[str]:
    """Punctuation-rich path: split on real terminators."""
    text = _protect(text)
    parts = _SENT_END.split(text)
    out, buf = [], ""
    for chunk in parts:
        buf += chunk
        if re.fullmatch(r"[.!?]+[\"'\)\]]*", chunk.strip()):
            out.append(buf.strip())
            buf = ""
    if buf.strip():
        out.append(buf.strip())
    return [s.replace("<DOT>", ".") for s in out if s.strip()]


def split_spoken(text: str) -> list[str]:
    """Punctuation-poor path: split on discourse markers + length window.

    Any hard terminators that DO exist are honoured first (they are reliable);
    the marker/length heuristic only handles the unpunctuated stretches.
    """
    text = _protect(text)
    # First honour whatever real terminators exist.
    chunks = re.split(r"(?<=[.!?])\s+", text)
    out: list[str] = []
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        out.extend(_split_long(chunk))
    return [s.replace("<DOT>", ".") for s in out if s.strip()]


def _split_long(chunk: str) -> list[str]:
    """Split an unpunctuated stretch using markers + length window."""
    words = chunk.split()
    if len(words) <= MAX_WORDS:
        return [chunk]

    out, buf = [], []
    for i, w in enumerate(words):
        buf.append(w)
        n = len(buf)
        at_end = i == len(words) - 1
        if at_end:
            break
        if n < MIN_WORDS:
            continue
        # Is the NEXT word a discourse marker? -> the current clause is ending
        nxt = words[i + 1]
        nxt2 = " ".join(words[i + 1 : i + 3]).lower()
        is_marker = bool(MARKERS.fullmatch(re.sub(r"[^\w']", "", nxt).lower())) or (
            nxt2 in {"here's the", "the thing", "the point", "and so", "and that's"}
        )
        if (n >= TARGET_WORDS and is_marker) or n >= MAX_WORDS:
            out.append(" ".join(buf))
            buf = []
    if buf:
        out.append(" ".join(buf))

    # merge fragments that ended up too short
    merged: list[str] = []
    for s in out:
        if merged and len(s.split()) < 5:
            merged[-1] = merged[-1] + " " + s
        else:
            merged.append(s)
    return merged


def to_sentences(raw: str) -> tuple[list[str], str]:
    """Return (sentences, mode) where mode is 'punct' or 'spoken'."""
    text = normalise(raw)
    if not text:
        return [], "empty"
    words = max(len(text.split()), 1)
    terminators = text.count(".") + text.count("?") + text.count("!")
    per_1k = terminators / words * 1000

    if per_1k >= 8:  # ~1 terminator per 125 words or better -> real punctuation
        sents = split_punct(text)
        mode = "punct"
    else:
        sents = split_spoken(text)
        mode = "spoken"

    # final cleanup + merge undersized fragments
    cleaned: list[str] = []
    for s in sents:
        s = re.sub(r"\s+", " ", s).strip()
        if len(s.split()) < 3:
            continue
        if cleaned and len(s.split()) < MIN_WORDS // 2:
            cleaned[-1] = cleaned[-1] + " " + s
        else:
            cleaned.append(s)
    return cleaned, mode


def slugify(title: str, idx: int) -> str:
    base = re.sub(r"\.docx$", "", title, flags=re.I)
    base = re.sub(r"[^\w\s-]", "", base, flags=re.UNICODE).strip()
    base = re.sub(r"\s+", "_", base) or "untitled"
    return f"{idx:03d}_{base[:70].rstrip('_')}"


def extract_one(path: str):
    try:
        d = docx.Document(path)
    except Exception as exc:
        print(f"  !! cannot open {os.path.basename(path)}: {exc}", file=sys.stderr)
        return None

    chunks = [p.text.strip() for p in d.paragraphs if (p.text or "").strip()]
    for table in getattr(d, "tables", []):
        for row in table.rows:
            for cell in row.cells:
                t = (cell.text or "").strip()
                if t:
                    chunks.append(t)
    if not chunks:
        return None

    sents, mode = to_sentences(" ".join(chunks))
    if not sents:
        return None
    words = sum(len(s.split()) for s in sents)
    return "\n".join(sents), words, len(sents), mode


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)
    files = sorted(glob.glob(os.path.join(SRC_DIR, "*.docx")))
    if args.limit:
        files = files[: args.limit]
    print(f"Found {len(files)} .docx")

    catalog, failed = [], []
    total_words = total_sents = 0
    modes = {"punct": 0, "spoken": 0}

    for i, path in enumerate(files, start=1):
        title = os.path.basename(path)
        res = extract_one(path)
        if res is None:
            failed.append(title)
            continue
        text, words, sents, mode = res
        slug = slugify(title, i)
        with open(os.path.join(OUT_DIR, slug + ".txt"), "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        catalog.append(
            {
                "id": i,
                "slug": slug,
                "title": title,
                "source_file": f"AskAlex YouTube Scripts/{title}",
                "extracted_file": f".workbuddy/extracted/{slug}.txt",
                "words": words,
                "sentences": sents,
                "mode": mode,
            }
        )
        modes[mode] = modes.get(mode, 0) + 1
        total_words += words
        total_sents += sents
        if i % 50 == 0:
            print(f"  ...{i}/{len(files)}  ({total_words:,} words)")

    with open(os.path.join(OUT_DIR, "_catalog.json"), "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, ensure_ascii=False, indent=2)

    print(f"\nDone. {len(catalog)} extracted, {len(failed)} failed.")
    print(f"Words: {total_words:,}  Sentences: {total_sents:,}  "
          f"Avg words/sentence: {total_words / max(total_sents,1):.1f}")
    print(f"Split mode: punct={modes.get('punct',0)}  spoken={modes.get('spoken',0)}")
    print(f"Catalog: {os.path.join(OUT_DIR, '_catalog.json')}")
    if failed:
        print("Failed:", *failed, sep="\n  - ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
