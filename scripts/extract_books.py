#!/usr/bin/env python3
"""Extract Alex Hormozi's books (PDF + EPUB) into clean plain text.

Why this script exists
----------------------
The 373 YouTube transcripts are *spoken* language: fragmentary, full of filler,
and heavily skewed toward mindset/general chatter. The books are the opposite:
dense, deliberately structured, and each one is *about* a specific pillar.

That last property is the whole point of this extractor. A book called
"$100M Playbook: Lifetime Value" is a pillar label that came free with the
filename. We bake that label into the catalog as `pillar_hint` so the atomizer
can use it as a prior, which is what fixes the LTV (C1) and Money Models (B3)
shortfall that the transcripts alone can never fix.

Outputs
-------
    .workbuddy/extracted_books/<slug>.txt
    .workbuddy/extracted_books/_catalog.json

Usage
-----
    python3 scripts/extract_books.py              # extract everything
    python3 scripts/extract_books.py --limit 3    # smoke test
    python3 scripts/extract_books.py --dry-run    # report only, write nothing

Notes
-----
- PDFs go through the system `pdftotext` (poppler) with -layout; it handles
  these files far better than the pure-Python parsers we tried.
- EPUBs are read with the stdlib only: zipfile + a spine walk through the OPF.
  Reading the spine (rather than globbing xhtml) keeps chapters in order.
- The $100M Money Models .mp3 audiobook is skipped: transcribing 200MB of audio
  is out of scope here, and the same content exists as PDF + EPUB.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from xml.etree import ElementTree as ET

# ---------------------------------------------------------------- paths


def find_root() -> str:
    """Walk up until we find a directory that looks like the project root."""
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        if os.path.isdir(os.path.join(d, "knowledge")) or os.path.isdir(
            os.path.join(d, "AskAlex YouTube Scripts")
        ):
            return d
        d = os.path.dirname(d)
    raise RuntimeError("could not locate project root")


HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = find_root()
SRC_DIR = os.path.join(ROOT, "Alex Hormozi Books")
OUT_DIR = os.path.join(ROOT, ".workbuddy", "extracted_books")

# ------------------------------------------------------- pillar priors

# Maps a regex on the (normalised) filename -> (primary, [secondary...]).
# Order matters: first match wins, so put specific titles before generic ones.
#
# These are Hormozi's own Acquisition.com model:
#   A1 Branding / A2 Marketing & Ads / A3 Lead Generation
#   B1 Offer / B2 Sales & Closing / B3 Money Models
#   C1 LTV / C2 Retention & Churn
#   D Business General / E Mindset
BOOK_PILLARS: list[tuple[str, str, list[str]]] = [
    # --- the two pillars we are explicitly trying to fix -------------------
    (r"money.?models", "B3", ["C1", "B2"]),          # Money Models book
    (r"lifetime.?value", "C1", ["B3", "C2"]),        # LTV playbook
    (r"retention", "C2", ["C1"]),
    (r"pricing.?value.?checklist", "C1", ["B2"]),
    (r"price.?raise", "B2", ["C1"]),
    (r"pricing", "B2", ["C1", "B1"]),
    (r"fast.?cash", "B3", ["A3"]),
    # --- monetization ------------------------------------------------------
    (r"offers", "B1", ["B2", "B3"]),                 # $100M Offers (+ Lost Chapter)
    (r"closing", "B2", ["B1"]),
    (r"proof", "B2", ["B1"]),
    # --- acquisition -------------------------------------------------------
    (r"goated.?ads", "A2", ["A1"]),
    (r"marketing.?machine", "A2", ["A1"]),
    (r"hooks", "A2", ["A1"]),
    (r"branding", "A1", ["A2"]),
    (r"lead.?nurture", "A3", ["C2"]),
    (r"leads", "A3", ["A2"]),
    # --- general -----------------------------------------------------------
    (r"scaling.?roadmap", "D", ["A3"]),
    (r"lost.?chapters", "D", ["E"]),
    (r"playbook", "D", []),                          # the catch-all main playbook
]

SKIP_PATTERNS = (r"\.mp3$",)  # audiobook: see module docstring

# Several titles ship twice (PDF + EPUB of the same book), and one filename is
# mangled ("$100m Offersi"). Feeding both copies through the atomizer would
# double-count every idea. Canonicalise the title, then keep one copy per book.
# Some copies differ too much in wording for the generic key to catch: one is
# named "$100m Offersi" (mangled) and the other carries the full marketing
# subtitle. These regexes are checked against the whole title BEFORE the generic
# key runs, most specific first.
#
# Keep them narrow. "Offers" alone is not a safe key: "$100M Offers - The Lost
# Chapter" is a genuinely separate short book, not a duplicate of "$100M Offers".
DEDUPE_OVERRIDES: list[tuple[str, str]] = [
    (r"offersi", "offers-main"),                    # "Alex Hormozi - $100m Offersi"
    (r"offers.*how to make offers", "offers-main"),
    (r"offers.*lost chapter", "offers-lost-chapter"),
    (r"money.?models", "money-models"),
]
TITLE_ALIASES = {
    "offersi": "offers",          # mangled filename: "Alex Hormozi - $100m Offersi"
    "100m offersi": "offers",
}

# When duplicates survive canonicalisation, prefer this format. EPUB wins
# because it preserves paragraph breaks; pdftotext -layout instead emits
# column artefacts ("com", "c2N") that end up glued onto the first sentence.
FORMAT_PRIORITY = {"epub": 0, "pdf": 1}


def canonical_key(title: str) -> str:
    """Collapse a book title to a dedup key: 'the same book' -> 'same key'."""
    low = title.lower()
    for pat, key in DEDUPE_OVERRIDES:
        if re.search(pat, low):
            return key

    t = re.sub(r"[\$]", " ", low)
    t = re.sub(r"\b(100m|100\s*m|by alex hormozi|private only|libgen li)\b", " ", t)
    t = re.sub(r"[^a-z0-9]+", " ", t).strip()
    if t in TITLE_ALIASES:
        return TITLE_ALIASES[t]
    # longest-prefix alias, for keys like "offers how to make offers so good..."
    for src, dst in TITLE_ALIASES.items():
        if t.startswith(src + " ") or t.startswith(src):
            return dst
    return t


def pillar_for(filename: str) -> tuple[str, list[str]]:
    low = filename.lower()
    for pat, primary, secondary in BOOK_PILLARS:
        if re.search(pat, low):
            return primary, secondary
    return "D", []


def clean_title(filename: str) -> str:
    """Turn a messy download filename into a readable book title."""
    t = re.sub(r"\.(pdf|epub|mp3)$", "", filename, flags=re.I)
    t = re.sub(r"-private-only", "", t, flags=re.I)
    t = re.sub(r"\(Acquisition\.com.*?\)", "", t, flags=re.I)
    t = re.sub(r"\(2021,\s*Acquisition\.com Publishing\)", "", t, flags=re.I)
    t = re.sub(r"\s*-\s*libgen\.li", "", t, flags=re.I)
    t = re.sub(r"Alex Hormozi\s*-\s*", "", t, flags=re.I)
    t = re.sub(r"\s+", " ", t).strip(" -_")
    return t


def slugify(name: str, idx: int) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_")
    return f"{idx:03d}_{s[:70]}"


# ------------------------------------------------------------- cleaning

BOILERPLATE = re.compile(
    r"all rights reserved|"
    r"no part of this publication|"
    r"permission requests, write to the publisher|"
    r"7710 N FM 620|"
    r"LEGAL DISCLAIMER|"
    r"NOT FOR DISTRIBUTION|"          # running footer on every playbook page
    r"Copyright\s*©\s*\d{4}\s*by|"    # merges with page numbers, so drop wholesale
    r"ISBN|"
    r"Acquisition\.com\s*$|"
    r"without the prior written permission|"
    r"Here.s a generic legal disclaimer|"
    r"sold with the understanding that the author",
    re.I,
)


# Several of these PDFs use a font whose ligature glyphs have no Unicode
# mapping, so poppler emits "!" for them. It shows up two ways:
#   word-initial  !is -> This, !ey -> They, !at -> That, !e -> The
#   word-internal !rst -> first (fi), o!er -> offer (ff), in!uence -> influence (fl)
# A trailing "!" is usually a real exclamation mark (Hormozi writes emphatically)
# so it is left alone.
#
# The internal cases are ambiguous - the same "!" means fi in "first" and ff in
# "offer" - so they are listed explicitly. Multi-character keys matter: "!rst"
# must be replaced before the word-initial rule runs, or it would become "Thrst".
LIGATURE_FIXES = {
    "!rst": "first", "!nd": "find", "!ve": "five", "!rm": "firm",
    "!gure": "figure", "!owers": "flowers", "!uence": "fluence",
    "speci!c": "specific", "pro!t": "profit", "pro!le": "profile",
    "di!erent": "different", "o!er": "offer", "stu!": "stuff",
}
WORD_INITIAL_TH = re.compile(r"(?<![A-Za-z])!([a-z])")


def _repair_ligatures(text: str) -> str:
    for bad, good in LIGATURE_FIXES.items():
        text = text.replace(bad, good)
    return WORD_INITIAL_TH.sub(r"Th\1", text)


def _is_toc_line(s: str) -> bool:
    """True for table-of-contents rows like 'What Is LTV? . . . . . . 3'.

    Poppler renders dot leaders as spaced dots. A real sentence never contains
    five-plus consecutive ' . ' groups, so this is safe.
    """
    if re.search(r"(\.\s+){4,}\.", s):
        return True
    if re.search(r"\.{5,}", s):
        return True
    # "...  .  .  .  42"  -> trailing page number behind a run of dots
    if re.search(r"\.\s+\d{1,4}\s*$", s) and s.count(".") >= 5:
        return True
    return False


def _strip_leading_toc(text: str) -> str:
    """Drop a table-of-contents block that has no dot leaders to detect it.

    Poppler renders most TOCs with dot leaders, but EPUB-derived books often
    emit a bare list of short chapter names ("Start Here", "Section I: ...",
    "The Classic Upsell", ...). Left in, that block becomes an atom that scores
    absurdly high on keyword repetition and outranks the actual prose.

    A TOC run looks like: many consecutive short lines, none ending in a
    sentence terminator. Real prose breaks that pattern within a line or two.
    """
    lines = text.split("\n")
    run: list[int] = []
    for i, ln in enumerate(lines[:200]):
        s = ln.strip()
        if not s:
            continue
        short = len(s) < 60
        # Only "." and "!" count as prose. Contents entries routinely end in
        # "?" ("Section I: What's A Money Model?") or ":" - treating those as
        # prose made the run stop after one line and the TOC survived.
        prose = bool(re.search(r"[.!][\"')\]]?$", s))
        if short and not prose:
            run.append(i)
            continue
        # first line that reads like real prose ends the candidate run
        break
    # GUARD: not every run of short lines is a TOC. The Hooks book is literally
    # a list of one-line hooks, and the GOATed Ads book is mostly short lines
    # too - stripping those would delete the actual content. Require structural
    # outline markers before we believe it is a contents page.
    structural = sum(
        1
        for i in run
        if re.match(
            r"^(section|chapter|part|appendix|introduction|conclusion|prologue|"
            r"start here|summary|final thoughts|bonus)\b",
            lines[i].strip(),
            re.I,
        )
    )
    if len(run) >= 12 and structural >= 2:
        # keep from just after the last TOC line
        return "\n".join(lines[run[-1] + 1 :]).strip()
    return text


def clean_text(raw: str) -> str:
    """Strip boilerplate, page furniture and layout debris from extracted text."""
    # 1. Front matter. Everything before the contents page is title page,
    #    copyright and the legal disclaimer - none of it is knowledge. Cutting
    #    here is what removes the multi-page liability waiver, which no
    #    line-level filter can catch because it reads as ordinary prose.
    m = re.search(r"^\s*(table\s+of\s+)?contents\s*$", raw, re.I | re.M)
    if m:
        raw = raw[m.end() :]

    lines = raw.split("\n")
    kept: list[str] = []
    for ln in lines:
        s = ln.strip()
        if not s:
            kept.append("")  # preserve paragraph breaks
            continue
        if BOILERPLATE.search(s):
            continue
        if _is_toc_line(s):
            continue
        # bare page numbers, and lonely "1" / "Chapter 1" footer artefacts
        if re.fullmatch(r"[\d\sivxlc]{1,6}", s, re.I):
            continue
        if len(s) <= 2 and not s.isalnum():
            continue
        kept.append(s)

    text = "\n".join(kept)
    # collapse the blank-line runs that removing boilerplate leaves behind
    text = re.sub(r"\n{3,}", "\n\n", text)
    # de-hyphenate words broken across a line break
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    # bare, dot-leader-free contents list (EPUB books) - after de-hyphenating so
    # line lengths are final
    text = _strip_leading_toc(text)
    text = _repair_ligatures(text)
    # unify the smart punctuation poppler emits so downstream tokenising is sane
    text = (
        text.replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u2014", " - ")
        .replace("\u2013", "-")
        .replace("\u00a0", " ")
    )
    return text.strip()


# ------------------------------------------------------------- PDF path


def extract_pdf(path: str) -> str:
    """Text from a PDF via poppler's pdftotext.

    We shell out rather than use a Python library because -layout preserves
    Hormozi's many tables and bulleted frameworks, which pure-Python parsers
    flatten into unreadable mush.
    """
    if not shutil.which("pdftotext"):
        raise RuntimeError(
            "pdftotext not found. Install poppler:  brew install poppler"
        )
    out = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", path, "-"],
        capture_output=True,
        text=True,
        timeout=300,
    )
    if out.returncode != 0:
        raise RuntimeError(f"pdftotext failed: {out.stderr.strip()[:200]}")
    return out.stdout


# ------------------------------------------------------------ EPUB path

_NS = {
    "opf": "http://www.idpf.org/2007/opf",
    "dc": "http://purl.org/dc/elements/1.1/",
    "container": "urn:oasis:names:tc:opendocument:xmlns:container",
}


def _strip_html(fragment: str) -> str:
    """HTML -> text. Blocks become newlines so paragraphs survive."""
    fragment = re.sub(r"(?is)<(script|style).*?</\1>", " ", fragment)
    fragment = re.sub(r"(?i)<br\s*/?>", "\n", fragment)
    fragment = re.sub(r"(?i)</(p|div|h[1-6]|li|tr)>", "\n", fragment)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    fragment = html.unescape(fragment)
    fragment = re.sub(r"[ \t]+", " ", fragment)
    return fragment


def extract_epub(path: str) -> str:
    """Text from an EPUB, following the OPF spine so chapters stay in order."""
    with zipfile.ZipFile(path) as z:
        names = z.namelist()

        # 1. locate the OPF package document via the container
        opf_path = "content.opf"
        try:
            container = z.read("META-INF/container.xml").decode("utf-8", "ignore")
            root = ET.fromstring(container)
            node = root.find(".//container:rootfile", _NS)
            if node is not None and node.get("full-path"):
                opf_path = node.get("full-path")
        except Exception:
            pass  # fall back to the conventional name

        # 2. read the spine to get reading order
        base = os.path.dirname(opf_path)
        order: list[str] = []
        try:
            opf = ET.fromstring(z.read(opf_path))
            manifest = {
                m.get("id"): m.get("href")
                for m in opf.findall(".//opf:manifest/opf:item", _NS)
                if m.get("id") and m.get("href")
            }
            for itemref in opf.findall(".//opf:spine/opf:itemref", _NS):
                href = manifest.get(itemref.get("idref"))
                if href:
                    order.append(os.path.normpath(os.path.join(base, href)) if base else href)
        except Exception:
            order = []

        # 3. fall back to a natural sort of every content file if the spine broke
        if not order:
            order = sorted(
                n for n in names if n.lower().endswith((".xhtml", ".html", ".htm"))
            )

        chunks: list[str] = []
        for member in order:
            if member not in names:
                continue
            try:
                raw = z.read(member).decode("utf-8", "ignore")
            except Exception:
                continue
            text = _strip_html(raw).strip()
            if len(text.split()) >= 15:  # drop TOC / nav / cover stubs
                chunks.append(text)
        return "\n\n".join(chunks)


# ----------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="only process first N files")
    ap.add_argument("--dry-run", action="store_true", help="report, write nothing")
    args = ap.parse_args()

    if not os.path.isdir(SRC_DIR):
        print(f"ERROR: source dir not found: {SRC_DIR}", file=sys.stderr)
        return 1

    files = sorted(
        f
        for f in os.listdir(SRC_DIR)
        if not f.startswith(".")
        and not any(re.search(p, f, re.I) for p in SKIP_PATTERNS)
    )
    if args.limit:
        files = files[: args.limit]

    if not args.dry_run:
        os.makedirs(OUT_DIR, exist_ok=True)

    catalog: list[dict] = []
    failed: list[tuple[str, str]] = []
    total_words = 0
    dropped_dupes: list[tuple[str, str]] = []

    print(f"Extracting {len(files)} books from: {os.path.basename(SRC_DIR)}\n")
    print(f"{'words':>8}  {'pillar':6}  title")
    print("-" * 78)

    # Pass 1: extract everything, remembering each candidate by canonical title.
    # We cannot dedup up front because the decision needs the word count, which
    # we only learn after extraction (image-only PDFs collapse to ~0 words).
    candidates: dict[str, dict] = {}

    for i, fname in enumerate(files, start=1):
        path = os.path.join(SRC_DIR, fname)
        ext = os.path.splitext(fname)[1].lower()
        primary, secondary = pillar_for(fname)
        title = clean_title(fname)

        try:
            if ext == ".pdf":
                raw = extract_pdf(path)
            elif ext == ".epub":
                raw = extract_epub(path)
            else:
                raise RuntimeError(f"unsupported extension {ext}")
        except Exception as e:
            failed.append((fname, str(e)[:120]))
            print(f"{'FAIL':>8}  {primary:6}  {title[:50]}  <- {str(e)[:60]}")
            continue

        text = clean_text(raw)
        words = len(text.split())
        if words < 200:
            failed.append((fname, f"image-only, no text layer ({words} words)"))
            print(f"{'SKIP':>8}  {primary:6}  {title[:50]}  <- only {words} words")
            continue

        cand = {
            "idx": i,
            "slug": slugify(title, i),
            "title": title,
            "source_file": os.path.relpath(path, ROOT),
            "source_type": "book",
            "format": ext.lstrip("."),
            "pillar_hint": primary,
            "pillar_secondary": secondary,
            "words": words,
            "text": text,
        }

        key = canonical_key(title)
        prev = candidates.get(key)
        if prev is None:
            candidates[key] = cand
            print(f"{words:8,}  {primary:6}  {title[:52]}")
        else:
            # keep the better copy: EPUB over PDF, then more words
            better = (
                FORMAT_PRIORITY.get(ext.lstrip("."), 9)
                < FORMAT_PRIORITY.get(prev["format"], 9)
            ) or (words > prev["words"] * 1.2)
            if better:
                candidates[key] = cand
                dropped_dupes.append((prev["title"], title))
                print(f"{words:8,}  {primary:6}  {title[:52]}  (dup: replaced)")
            else:
                dropped_dupes.append((title, prev["title"]))
                print(f"{words:8,}  {primary:6}  {title[:52]}  (dup: skipped)")

    # Pass 2: write the survivors, renumbered so ids stay contiguous.
    for n, (key, c) in enumerate(
        sorted(candidates.items(), key=lambda kv: kv[1]["idx"]), start=1
    ):
        total_words += c["words"]
        slug = slugify(c["title"], n)
        entry = {
            "id": n,
            "slug": slug,
            "title": c["title"],
            "source_file": c["source_file"],
            "extracted_file": os.path.relpath(
                os.path.join(OUT_DIR, f"{slug}.txt"), ROOT
            ),
            "source_type": "book",
            "format": c["format"],
            "pillar_hint": c["pillar_hint"],
            "pillar_secondary": c["pillar_secondary"],
            "words": c["words"],
        }
        catalog.append(entry)
        if not args.dry_run:
            with open(os.path.join(OUT_DIR, f"{slug}.txt"), "w", encoding="utf-8") as fh:
                fh.write(c["text"])

    print("-" * 78)
    print(f"books extracted : {len(catalog)}")
    if dropped_dupes:
        print(f"duplicates dropped: {len(dropped_dupes)}")
        for gone, kept in dropped_dupes:
            print(f"  - '{gone[:44]}' -> kept '{kept[:44]}'")
    print(f"total words     : {total_words:,}")
    if failed:
        print(f"\nskipped/failed ({len(failed)}):")
        for f, why in failed:
            print(f"  - {f}: {why}")

    if not args.dry_run:
        cat_path = os.path.join(OUT_DIR, "_catalog.json")
        with open(cat_path, "w", encoding="utf-8") as fh:
            json.dump(catalog, fh, ensure_ascii=False, indent=2)
        print(f"\ncatalog         : {os.path.relpath(cat_path, ROOT)}")

        from collections import Counter

        counts = Counter(e["pillar_hint"] for e in catalog)
        print("\nbooks by pillar hint:")
        for p, c in sorted(counts.items()):
            print(f"  {p}: {c}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
