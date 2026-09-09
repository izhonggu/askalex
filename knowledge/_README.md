# knowledge/ — what lives here

Two layers of the same source material, at different granularity. They are not
duplicates, and neither is a "newer version" of the other.

```
knowledge/
├── _taxonomy.md        the 10-pillar classification rules (A1-E)
├── A1_branding.md      ┐
├── A2_marketing_ads.md │
├── A3_lead_generation.md
├── B1_offer.md         ├─ CARD LIBRARY  — hand-curated, 2,095 cards
├── B2_sales_closing.md │   ~200-500 words per card, markdown
├── B3_money_models.md  │   built for humans reading top to bottom
├── C1_ltv.md           │
├── C2_retention.md     │
├── D_business_general.md
├── E_mindset.md        ┘
└── atoms/              ┐
    ├── atoms.jsonl     ├─ ATOM LIBRARY — script-generated, 25,101 atoms
    └── atoms_report.json  ~100 words per atom, JSONL
                        ┘  built for machines retrieving by keyword
```

## Card library vs atom library

| | Cards (`.md`) | Atoms (`atoms/atoms.jsonl`) |
|---|---|---|
| Made by | curation | `scripts/atomize.py` |
| Sources | hand notes | 373 YouTube transcripts + 18 books |
| Granularity | one card = a full idea with context | one atom = one proposition |
| Format | markdown, `###` title + bullets | one JSON object per line |
| Read by | humans, and `.claude/skills/ask-alex` | `scripts/search_atoms.py`, and the nine `skills/askalex-*` skills — see `skills/README.md` for the routing table |
| Size | 2.2 MB total | ~23 MB — **never read whole** |

## Pillars

Same 10 codes in both layers, defined in `_taxonomy.md`:

**A** Acquisition — A1 Branding · A2 Marketing & Ads · A3 Lead Generation
**B** Monetization — B1 Offer · B2 Sales & Closing · B3 Money Models
**C** Retention — C1 LTV · C2 Retention & Churn
**Cross-cutting** — D Business General · E Mindset

## Caveat worth knowing

~71% of atoms carry `weak: true` (`signal < 4`) — Alex's spoken transcripts
contain a lot of chat, Q&A filler, and client-specific tangents with no clear
topic. This is a property of the source, not a bug. Retrieve with
`--strong-only` to filter them out.

Book atoms are the exception: each book's title supplies a `pillar_hint`, so a
book atom is tagged by its source's subject even when the passage itself has
weak keyword signal. They carry `source_type: "book"` and `prior_applied: true`
so you can tell them apart from transcript atoms.

## Rebuilding

```bash
python3 scripts/extract_docx.py     # 373 .docx -> .workbuddy/extracted/
python3 scripts/extract_books.py    # 18 books -> .workbuddy/extracted_books/
python3 scripts/atomize.py          # both -> knowledge/atoms/atoms.jsonl
```

Warning: `atomize.py` **overwrites** `atoms.jsonl` — the whole file, not just the
source you asked for. `--sources books` and `--sources transcripts` are filters on
which *input* to read, not a merge into the existing output: running `--sources books`
after a full build replaces atoms.jsonl with *books only*, silently dropping every
transcript atom that was in there. (Hit this firsthand re-extracting one book — the fix
was rerunning with `--sources all`, i.e. no flag, to regenerate the true merged set.)
Back up `atoms.jsonl` before rerunning anything, and if you only changed one source's
input text, still rebuild with both (the default, no `--sources` flag) afterward.

### Semantic search index (optional)

```bash
python3 -m venv .venv
.venv/bin/pip install fastembed numpy
.venv/bin/python3 scripts/build_embeddings.py   # atoms.jsonl -> embeddings.npy + embeddings_ids.json
```

Adds cosine-similarity retrieval on top of `search_atoms.py`'s keyword scoring (see
`skills/README.md`'s Retrieval section for how the two combine). Rerun this after any
`atomize.py` run that changes `atoms.jsonl` — the embeddings are keyed by atom ID, so a
stale index just silently stops matching rows that changed rather than erroring. Both
output files land in `knowledge/atoms/`, gitignored the same as `atoms.jsonl` itself.
