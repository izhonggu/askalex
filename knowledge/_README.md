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
    ├── atoms.jsonl     ├─ ATOM LIBRARY — script-generated, 25,183 atoms
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
# transcripts only:  python3 scripts/atomize.py --sources transcripts
# books only:        python3 scripts/atomize.py --sources books
```

Warning: `atomize.py` **overwrites** `atoms.jsonl`. Back it up first if the
current 25,183 atoms matter.
