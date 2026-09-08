#!/usr/bin/env python3
"""
atomize.py — Turn extracted transcript sentences into PROPOSITION-LEVEL knowledge atoms.

What "one proposition per atom" means here
------------------------------------------
Hormozi speaks in argument units: he states a claim, then supports it with an
example or a consequence, then moves on. A single sentence is usually not a
standalone proposition (it depends on the previous one for context), and a whole
video is far too coarse. The right unit is a *coherent stretch* of roughly
70-150 words that makes one complete point.

How boundaries are found
------------------------
TextTiling-style lexical cohesion:
    1. For every gap between sentence i and i+1, compare the content-word
       vocabulary of the k sentences BEFORE the gap with the k AFTER it.
    2. Low overlap  -> vocabulary shifted -> topic boundary.
    3. Normalise the gap scores, keep local maxima above a threshold,
       and enforce MIN/MAX length windows so no atom is a fragment or a wall.

This is measured, heuristic segmentation — no LLM call — so it runs over
2.7M words in seconds and is fully reproducible.

Pillar tagging
--------------
Each atom gets one primary pillar and 0-2 secondary pillars, scored by a
keyword lexicon derived from knowledge/_taxonomy.md. Ties fall back to D
(Business General).

Outputs
-------
    knowledge/atoms/atoms.jsonl       one JSON object per line
    knowledge/atoms/atoms_report.json summary stats

Usage
-----
    python3 atomize.py                 # all files
    python3 atomize.py --limit 20      # smoke test
    python3 atomize.py --max-words 120
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from collections import Counter


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
EXTRACT_DIR = os.path.join(ROOT, ".workbuddy", "extracted")
BOOKS_DIR = os.path.join(ROOT, ".workbuddy", "extracted_books")
OUT_DIR = os.path.join(ROOT, "knowledge", "atoms")

# ------------------------------------------------------------------- config
MIN_WORDS = 40       # atoms shorter than this get merged into a neighbour
TARGET_WORDS = 70    # ideal atom size
MAX_WORDS = 110      # hard cap
K = 2                # TextTiling window (sentences each side)
BOUNDARY_STRENGTH = 0.20  # how far between mean and max a gap must sit

# Book-level pillar prior. A book's title labels its whole subject, so every
# atom from it inherits that label as a bonus. Tuned against the lexicon: a
# genuinely on-topic atom scores 10+, incidental mentions score 2-4. Six points
# makes the book's own subject win the tie without overriding a chapter that is
# really about something else (e.g. an ad-creative aside inside Money Models).
PRIOR_BONUS = 6

# --------------------------------------------------------------- stopwords
STOP = set("""
a about above after again against all am an and any are aren't as at be because been
before being below between both but by can't cannot could couldn't did didn't do does
doesn't doing don't down during each few for from further had hadn't has hasn't have
haven't having he he'd he'll he's her here here's hers herself him himself his how how's
i i'd i'll i'm i've if in into is isn't it it's its itself let's me more most mustn't my
myself no nor not of off on once only or other ought our ours ourselves out over own
same shan't she she'd she'll she's should shouldn't so some such than that that's the
their theirs them themselves then there there's these they they'd they'll they're
they've this those through to too under until up very was wasn't we we'd we'll we're
we've were weren't what what's when when's where where's which while who who's whom why
why's with won't would wouldn't you you'd you'll you're you've your yours yourself
yourselves
im ive dont thats youre theyre gonna wanna kinda gotta ain't yeah yeahs okay ok
um uh uhuh er ah hmm right well now just really actually basically literally
gonna gonna thing things stuff lot kind sort way ways bit maybe probably
everyone everybody someone somebody anyone nobody thinking thought knows knew
best worst good bad big small little long short say says saying said talk talking
told tell ask asked asking let lets begin begins start starts started starting
keep keeps kept find finds found try tries trying tried use used using useful
work works working worked call calls called turn turns turned mean means meant
get gets getting got given give gives gave take takes taking took see sees seeing
saw look looks looking looked come comes coming came want wants wanted
need needs needed make makes making made put puts putting go goes going went
people guy guys man men woman women kid kids day days year years time times
place places part parts point points end ends lots kinda sorta
think one two three also can cannot like feel feels felt might even much many
still back another around though enough ever never always something anything
everything nothing whatever however therefore instead perhaps almost rather
quite else whose whom among within without upon while whereas
""".split())


def content_words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z']+", text.lower()) if w not in STOP and len(w) > 2}


# ------------------------------------------------------------ pillar lexicon
# Weighted keyword sets derived from knowledge/_taxonomy.md definitions.
PILLARS: dict[str, dict[str, int]] = {
    "A1": {  # Branding
        "brand*": 3, "positioning": 3, "reputation": 3, "differentiat*": 2,
        "identity": 2, "niche": 2, "authority": 2, "trust": 2, "category": 2,
        "perception": 2, "famous": 1, "celebrity": 2, "rebrand*": 3,
        "differentiator": 3, "unfair advantage": 2, "known for": 2,
    },
    "A2": {  # Marketing & Ads
        "ad": 3, "ads": 4, "advertis*": 4, "hook*": 3, "headline*": 3,
        "creative": 2, "facebook": 3, "instagram": 3, "youtube": 2, "tiktok": 3,
        "campaign*": 2, "impression*": 2, "ctr": 3, "cpm": 3, "cpc": 3,
        "marketing": 2, "organic": 2, "algorithm": 2, "thumbnail*": 2,
        "copywriting": 3, "direct response": 3, "media buy*": 3, "funnel ad*": 3,
    },
    "A3": {  # Lead Generation
        "lead": 3, "leads": 4, "lead magnet": 4, "outreach": 3, "cold call*": 3,
        "cold email*": 3, "email list": 3, "funnel": 2, "traffic": 2,
        "core four": 4, "inbound": 3, "prospect*": 2, "audience": 2,
        "follower*": 2, "subscriber*": 2, "nurture": 3, "giveaway": 2,
        "referral*": 2, "word of mouth": 3, "lead gen": 4,
    },
    "B1": {  # Offer
        "offer*": 3, "grand slam": 5, "value equation": 5, "guarantee*": 3,
        "bonus*": 2, "package": 2, "dream outcome": 4, "likelihood": 2,
        "time delay": 2, "effort": 1, "sacrifice": 1, "value stack*": 4,
        "scarcity": 3, "urgency": 3, "unfair advantage": 2, "pricing": 1,
        "stack": 1, "irresistible": 3,
    },
    "B2": {  # Sales & Closing
        "close": 3, "closing": 4, "sales": 3, "objection*": 4, "pitch": 3,
        "negotiat*": 3, "price increase": 3, "raise price*": 3, "proof": 2,
        "testimonial*": 3, "case stud*": 2, "salesman": 3, "salesperson": 3,
        "sales team": 3, "rebuttal*": 3, "trial close": 3, "downsell*": 2,
        "closing rate": 3, "conversion rate": 2,
    },
    "B3": {  # Money Models
        "upsell*": 4, "downsell*": 3, "cross-sell*": 4, "continuity": 3,
        "recurring revenue": 4, "money model*": 5, "cash flow": 3,
        "attraction offer": 4, "backend": 3, "subscription*": 3,
        "installment*": 2, "payment plan*": 3, "revenue model": 3,
        "monetiz*": 3, "profit margin*": 2, "margin": 1,
    },
    "C1": {  # LTV
        "ltv": 5, "lifetime value": 5, "expansion revenue": 4,
        "repeat purchase*": 3, "arpu": 4, "average order value": 4, "aov": 4,
        "per customer": 2, "gross margin*": 2, "contribution margin*": 3,
        "long-term value": 3, "customer value": 3, "ltv cac": 4,
        # Added after reading the LTV playbook. "gross profit" is how Hormozi
        # actually says unit economics (24 hits in that book); the lexicon only
        # had "gross margin" and missed nearly all of them. "worth more" is the
        # book's own framing ("Eight Ways To Make Customers Worth More").
        # Deliberately NOT adding "spend more"/"more money": they appear in
        # every second transcript sentence and are not LTV-specific.
        # "worth more" alone was a trap: it matched "whose word is worth more"
        # (reputation, not LTV). Pin it to the customer. "expansion" alone was
        # the same story - "expansion into new markets" is not LTV.
        "gross profit": 5, "customer worth": 4, "customers worth": 4,
        "worth more over time": 4,
        "buy again": 4, "second purchase*": 4, "recurring revenue": 4,
        "product line*": 3,
    },
    "C2": {  # Retention & Churn
        "retention": 5, "churn": 5, "cancel*": 4, "no-show*": 4, "noshow": 4,
        "win-back": 4, "onboarding": 3, "activation": 3, "renewal*": 3,
        "renew": 2, "refund*": 2, "satisfaction": 2, "customer success": 3,
        "stay longer": 3, "attrition": 4,
    },
    "D": {  # Business General — deliberately de-weighted: words like team,
            # system, process, scale appear in EVERY pillar's discussion, so
            # they are weak signals and must not let D swallow the corpus.
        "hire": 3, "hiring": 4, "employee*": 2, "operations": 3,
        "scaling": 3, "partner*": 1, "finance": 2, "accounting": 3,
        "accountant": 3, "delegat*": 3, "org chart": 4, "sop": 3, "kpi*": 2,
        "fire someone": 3, "management": 1, "cash flow": 1, "taxes": 2,
        "legal": 2, "llc": 2, "equity": 2, "valuation": 3,
    },
    "E": {  # Mindset
        "mindset": 5, "discipline": 4, "fear": 3, "motivation": 3, "habit*": 3,
        "resilience": 4, "belief*": 3, "psychology": 3, "consistency": 3,
        "procrastinat*": 4, "grind*": 3, "suffer*": 2, "pain": 2,
        "self-worth": 3, "confidence": 3, "happiness": 3, "happy": 1,
        "failure": 2, "quit": 2, "excuse*": 3, "identity": 2,
        "imposter": 3, "burnout": 3, "mental": 2,
    },
}

PILLAR_NAMES = {
    "A1": "Branding", "A2": "Marketing & Ads", "A3": "Lead Generation",
    "B1": "Offer", "B2": "Sales & Closing", "B3": "Money Models",
    "C1": "LTV", "C2": "Retention & Churn", "D": "Business General", "E": "Mindset",
}


def score_pillars(
    text: str,
    prior: str | None = None,
    prior_bonus: int = PRIOR_BONUS,
) -> list[tuple[str, int]]:
    """Score each pillar by weighted keyword hits.

    CRITICAL: matching is word-boundary safe. A plain substring match is
    disastrous here — "ad" would hit advice/add/read/instead and swamp A2.
    Convention in the lexicon below:
        "ad"     -> exact word  (\\bad\\b)
        "ad*"    -> stem, allow suffixes (\\bad\\w*  matches ads, advertise)

    `prior` is a pillar the SOURCE already tells us about — for books, the title
    ("$100M Playbook: Lifetime Value" -> C1). It is added as a flat bonus, not a
    hard override: a chapter of the Money Models book that is really about ad
    creative can still score higher on A2, because PRIOR_BONUS is deliberately
    smaller than a genuinely on-topic keyword score.
    """
    low = text.lower()
    scores: dict[str, int] = {}
    for code, lex in PILLARS.items():
        s = 0
        for kw, w in lex.items():
            stem = kw.endswith("*")
            base = kw[:-1] if stem else kw
            if not base:
                continue
            pat = r"\b" + re.escape(base) + (r"\w*" if stem else r"\b")
            c = len(re.findall(pat, low))
            if c:
                s += w * min(c, 4)  # cap repeat hits so one word can't dominate
        if s:
            scores[code] = s
    if prior:
        scores[prior] = scores.get(prior, 0) + prior_bonus
    return sorted(scores.items(), key=lambda kv: -kv[1])


# ------------------------------------------------------------ segmentation
def cohesion_gaps(sents: list[str], k: int = K) -> list[float]:
    """Lexical-cohesion gap score for each internal sentence boundary."""
    vocab = [content_words(s) for s in sents]
    n = len(sents)
    gaps = []
    for i in range(1, n):
        before: Counter = Counter()
        for v in vocab[max(0, i - k): i]:
            before.update(v)
        after: Counter = Counter()
        for v in vocab[i: min(n, i + k)]:
            after.update(v)
        if not before or not after:
            gaps.append(0.0)
            continue
        inter = sum((before & after).values())
        union = sum((before | after).values())
        # jaccard-ish; low overlap => high gap
        gaps.append(1.0 - (inter / union if union else 0.0))
    return gaps


def smooth(xs: list[float], w: int = 2) -> list[float]:
    out = []
    for i in range(len(xs)):
        lo, hi = max(0, i - w), min(len(xs), i + w + 1)
        out.append(sum(xs[lo:hi]) / (hi - lo))
    return out


def find_boundaries(sents: list[str], word_counts: list[int]) -> list[int]:
    """Return sentence indices where a new atom starts (always includes 0)."""
    n = len(sents)
    if n <= 2:
        return [0]
    gaps = smooth(cohesion_gaps(sents))
    if not gaps or max(gaps) == 0:
        return [0]

    mx = max(gaps)
    mean = sum(gaps) / len(gaps)
    thresh = mean + (mx - mean) * BOUNDARY_STRENGTH  # keep strong-ish boundaries only

    bounds = [0]
    acc = 0
    for i, g in enumerate(gaps, start=1):  # gap i sits before sentence i
        acc += word_counts[i - 1]
        too_long = acc >= MAX_WORDS
        long_enough = acc >= MIN_WORDS
        good_boundary = g >= thresh
        local_max = (i == 1 or g >= gaps[i - 2]) and (i == len(gaps) or g >= gaps[i])
        if long_enough and (too_long or (good_boundary and local_max)):
            bounds.append(i)
            acc = 0
    return bounds


def build_atoms(sents: list[str]) -> list[str]:
    if not sents:
        return []
    wc = [len(s.split()) for s in sents]
    bounds = find_boundaries(sents, wc)
    atoms = []
    for j, start in enumerate(bounds):
        end = bounds[j + 1] if j + 1 < len(bounds) else len(sents)
        chunk = " ".join(sents[start:end]).strip()
        if chunk:
            atoms.append(chunk)
    # merge undersized leftovers
    merged: list[str] = []
    for a in atoms:
        if merged and len(a.split()) < MIN_WORDS:
            merged[-1] = merged[-1] + " " + a
        else:
            merged.append(a)
    # final pass: if the very last atom is a stub, fold it back
    if len(merged) > 1 and len(merged[-1].split()) < MIN_WORDS // 2:
        merged[-2] = merged[-2] + " " + merged.pop()
    return merged


# ------------------------------------------------------------ quality gate
FILLER = re.compile(r"\b(um|uh|er|ah|hmm|like|you know|i mean|right\?|okay so|so yeah)\b", re.I)


def is_low_quality(text: str) -> bool:
    words = text.split()
    if len(words) < MIN_WORDS:
        return True
    filler_hits = len(FILLER.findall(text))
    if filler_hits / max(len(words), 1) > 0.06:      # >6% filler = rambling
        return True
    vocab = content_words(text)
    # Thresholds are calibrated against the EXPANDED stopword list above;
    # with spoken filler stripped, 22% content words is unrealistically high
    # and silently discarded ~1/3 of the corpus. 0.15 keeps real content.
    if len(vocab) / max(len(words), 1) < 0.15:
        return True
    if len(vocab) < 8:
        return True
    # spoken transcripts rarely have questions-only stubs worth keeping
    if text.count("?") > 4 and len(words) < 70:
        return True
    return False


def clean(text: str) -> str:
    t = re.sub(r"\s+", " ", text).strip()
    t = re.sub(r"\s+([,.!?;:])", r"\1", t)
    return t


# Words that end in -s but are NOT plurals. Stripping the s yields junk
# ("always"->"alway", "process"->"proces") that surfaces in atom titles.
NO_STEM = {
    "always", "business", "process", "success", "access", "address", "class",
    "less", "press", "cross", "glass", "kindness", "illness", "witness",
    "purpose", "course", "cause", "base", "case", "phase", "phrase", "use",
    "close", "increase", "release", "promise", "purchase", "expense",
    "response", "else", "itself", "this", "vs", "gas", "bias", "canvas",
    "focus", "bonus", "status", "bus", "plus", "miss", "loss", "gross",
}


def _stem(w: str) -> str:
    """Collapse plurals ONLY.

    Deliberately does not strip -ing/-ed: crude suffix stripping turns
    "dancing" into "danc" and "tried" into "tri", which produces non-words in
    titles. Plural collapsing is the safe, high-value case (lesson/lessons).
    """
    if w in NO_STEM or len(w) < 5:
        return w
    for suf, rep in (("ies", "y"), ("es", ""), ("s", "")):
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: -len(suf)] + rep
    return w


def make_title(text: str, max_terms: int = 6) -> str:
    """Title = the atom's top content terms, in order of first appearance.

    Why not the first sentence: spoken transcripts open with filler
    ("what's going on everyone, i think one of the best things...") far more
    often than not, so first-sentence titles are mostly noise. Why not a
    generated summary: this runs over 2.7M words with no LLM call.

    A compact term list is what a retriever and a human skim actually need —
    it exposes the atom's vocabulary directly.
    """
    toks = [w for w in re.findall(r"[a-z']+", text.lower())
            if w not in STOP and len(w) > 2 and not w.isdigit()]
    if not toks:
        return " ".join(text.split()[:8]) + "..."
    freq = Counter(_stem(w) for w in toks)
    if not freq:
        return " ".join(text.split()[:8]) + "..."

    top_stems = {s for s, _ in freq.most_common(max_terms * 3)}
    picked: list[str] = []
    for w in toks:
        s = _stem(w)
        if s in top_stems and s not in picked:
            picked.append(s)
        if len(picked) >= max_terms:
            break
    return " ".join(picked) if picked else " ".join(text.split()[:8]) + "..."


# ------------------------------------------------------------------- main
def load_catalog(sources: str = "all") -> list[dict]:
    """Merge the transcript and book catalogs into one work list.

    Books come second so transcript ids stay stable across reruns. Each entry
    carries `source_type`, and book entries additionally carry `pillar_hint`
    (written by scripts/extract_books.py from the book's title).
    """
    catalog: list[dict] = []

    def load(path: str, source_type: str) -> list[dict]:
        if not os.path.isfile(path):
            return []
        with open(path, encoding="utf-8") as fh:
            entries = json.load(fh)
        for e in entries:
            e.setdefault("source_type", source_type)
        return entries

    if sources in ("all", "transcripts"):
        catalog += load(os.path.join(EXTRACT_DIR, "_catalog.json"), "transcript")
    if sources in ("all", "books"):
        catalog += load(os.path.join(BOOKS_DIR, "_catalog.json"), "book")

    if not catalog:
        raise SystemExit(
            "No catalog found. Run scripts/extract_docx.py and/or "
            "scripts/extract_books.py first."
        )
    return catalog


def main() -> int:
    global MIN_WORDS, MAX_WORDS
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--min-words", type=int, default=MIN_WORDS)
    ap.add_argument("--max-words", type=int, default=MAX_WORDS)
    ap.add_argument(
        "--sources",
        choices=("all", "transcripts", "books"),
        default="all",
        help="which corpus to atomize (default: both)",
    )
    args = ap.parse_args()
    MIN_WORDS, MAX_WORDS = args.min_words, args.max_words

    os.makedirs(OUT_DIR, exist_ok=True)
    catalog = load_catalog(args.sources)
    if args.limit:
        catalog = catalog[: args.limit]

    out_path = os.path.join(OUT_DIR, "atoms.jsonl")
    atom_id = 0
    kept = dropped = 0
    weak_count = 0
    sec_count = 0
    pillar_counter: Counter = Counter()
    source_counter: Counter = Counter()
    # pillar -> source_type -> count, so we can prove the books actually moved
    # the needle on C1/B3 rather than just adding more of the same
    by_source: dict[str, Counter] = {"transcript": Counter(), "book": Counter()}
    words_total = 0
    per_file = []

    with open(out_path, "w", encoding="utf-8") as out:
        for entry in catalog:
            src = os.path.join(ROOT, entry["extracted_file"])
            if not os.path.exists(src):
                continue
            with open(src, encoding="utf-8") as fh:
                sents = [ln.strip() for ln in fh if ln.strip()]
            source_type = entry.get("source_type", "transcript")
            prior = entry.get("pillar_hint")  # books only; None for transcripts
            atoms = build_atoms(sents)
            local_kept = 0
            for a in atoms:
                a = clean(a)
                if is_low_quality(a):
                    dropped += 1
                    continue
                # Two passes: the final pillar uses the book prior (when there is
                # one), but `signal`/`weak` come from the RAW keyword score.
                # Otherwise every book atom inherits the +6 bonus and nothing
                # ever looks weak — which would silently change what the Skill's
                # --strong-only filter means versus the transcript atoms.
                ranked = score_pillars(a, prior=prior)
                raw = score_pillars(a)
                content_signal = raw[0][1] if raw else 0
                if ranked:
                    primary = ranked[0][0]
                    # 25% of the winner's score, floored at 2 — the old 40%/3
                    # floor was so strict that only 1% of atoms got any
                    # secondary tag at all.
                    secondary = [
                        c for c, s in ranked[1:3]
                        if s >= max(2, content_signal * 0.25)
                    ]
                else:
                    primary, secondary = "D", []
                weak = content_signal < 4  # no real topical signal -> general chat
                atom_id += 1
                local_kept += 1
                words_total += len(a.split())
                pillar_counter[primary] += 1
                source_counter[source_type] += 1
                by_source[source_type][primary] += 1
                if weak:
                    weak_count += 1
                if secondary:
                    sec_count += 1
                rec = {
                    "id": f"ATOM-{atom_id:05d}",
                    "pillar": primary,
                    "pillar_name": PILLAR_NAMES[primary],
                    "secondary": secondary,
                    "signal": content_signal,
                    "weak": weak,
                    "source_type": source_type,
                    "prior_applied": bool(prior),
                    "title": make_title(a),
                    "content": a,
                    "words": len(a.split()),
                    "source": entry["title"],
                    "source_file": entry["source_file"],
                }
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            kept += local_kept
            per_file.append({"slug": entry["slug"], "atoms": local_kept})

    report = {
        "total_atoms": atom_id,
        "dropped_chunks": dropped,
        "total_words": words_total,
        "avg_words_per_atom": round(words_total / max(atom_id, 1), 1),
        "files_processed": len(catalog),
        "by_source_type": dict(source_counter),
        "by_pillar": {k: pillar_counter.get(k, 0) for k in PILLAR_NAMES},
        "by_pillar_by_source": {
            st: {k: c.get(k, 0) for k in PILLAR_NAMES} for st, c in by_source.items()
        },
        "weak_signal_atoms": weak_count,
        "weak_signal_pct": round(weak_count / max(atom_id, 1) * 100, 1),
        "atoms_with_secondary": sec_count,
    }
    with open(os.path.join(OUT_DIR, "atoms_report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)

    print(json.dumps(report, indent=2))
    print(f"\nWrote: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
