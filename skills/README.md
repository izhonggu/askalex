# AskAlex skills

Twelve skills. Nine specialists share one knowledge base (25,101 atoms) and
one set of rules, each owning a distinct question — plus `askalex`, the
front door that routes to one of them (or diagnoses first, then chains
straight into the specialist, in one pass); `askalex-plan`, which sequences
multiple things once there's more than one on the table; and
`askalex-retro`, which interprets the result once something on that
sequence has actually been tried. Diagnosis and plan run *before* evidence
exists; retro is the only one that runs *after* — think Plan → Do (in the
real world, not in AskAlex) → Check, with retro owning Check and feeding
back into diagnosis or plan for the next round.

**Unsure which one applies? Start with `askalex`.** It does the classification
below for you and chains the diagnosis into the specialist's actual answer
instead of just naming which skill to go ask next. Everything past this point
is what `askalex` is routing against — read on if you're adding a skill,
calling a specialist directly, or want to know why a boundary is drawn where
it is.

## Pick one

| Skill | Use when the question is about | Core framework |
|---|---|---|
| `askalex` | **you don't know which of these to pick** | routes to one, or diagnoses then chains into one — see [`askalex/SKILL.md`](askalex/SKILL.md) |
| `askalex-diagnosis` | **the business as a whole**, and the user cannot say where it hurts | three growth levers → locate the constraint, then hand off |
| `askalex-plan` | **more than one thing is already on the table** — from a diagnosis, from several specialists, or the user's own list — and the question is what order to run them in | Ten-Stage Scaling Roadmap + one-constraint-at-a-time — see [`askalex-plan/SKILL.md`](askalex-plan/SKILL.md) |
| `askalex-retro` | **something was already tried and a result came in** — was the bet right, what does the number actually mean | clean-test check + falsifier scoring + "shaking the three" — see [`askalex-retro/SKILL.md`](askalex-retro/SKILL.md) |
| `askalex-offer` | **one offer** — building it, or why it isn't converting | Value Equation (4 variables) + Grand Slam Offer (9 steps) |
| `askalex-pricing` | **the number and the terms** — what to charge, whether to raise, how to bill | three pricing models + 10 pricing plays + price/value/churn |
| `askalex-businessmodel` | **the shape** — no back end, CAC never pays back, always cash-poor | Money Model: attraction → upsell/downsell → continuity |
| `askalex-ltv` | **total value per customer** — make them worth more over the whole relationship | LTGP calculation + the Crazy Eight |
| `askalex-retention` | **why customers leave** — churn, activation, first 30 days | churn checklist + activation points |
| `askalex-sales` | **people already in conversation** — close rate, objections, pitch | three buckets + onion of blame + named closes |
| `askalex-leadgen` | **nobody is talking to you** — not enough leads, one channel | Core Four (warm/cold × 1-to-1/1-to-many) |
| `askalex-entrepreneurship` | **the person** — fear, beliefs, discipline, burnout, consistency | pain / beliefs / fear / identity / agency / patience |

## The boundaries that get confused

- **diagnosis vs everything else.** Diagnosis locates, it does not treat. If the
  user already knows the object of work, skip it and go straight to the specialist.
- **offer vs pricing.** Offer prices *relative to value delivered*. Pricing owns the
  number, the model, the billing terms, and the raise path. "Customers say I'm too
  expensive" is usually an offer problem in a pricing costume — run diagnosis first.
- **businessmodel vs ltv.** Businessmodel asks *which offers exist and in what order*
  (structural; usually "you're missing a whole stage"). LTV assumes the structure and
  asks *how to extract more from each one* (arithmetic).
- **ltv vs retention.** Retention is one input into LTV — it sets the lifespan. If
  customers leave unhappy, fix that before applying any LTV lever.
- **leadgen vs sales.** The dividing line is whether anyone is available to talk to.
- **entrepreneurship vs all of the above.** Sometimes "I'm scared to raise prices" is
  an accurate fear, because the offer really is thin. Check for a business problem
  before coaching through it.
- **plan vs everything else.** Plan doesn't diagnose and doesn't produce a domain fix —
  it only orders things that already exist. It's deliberately **not** auto-chained by
  `askalex`: a single diagnosis handing off to a single specialist is already a
  complete answer most of the time, and bolting a sequencing step onto every response
  would bloat the common case for the sake of the occasional one. Call it directly when
  there are genuinely 2+ things on the table, or when the question is really "what
  stage am I at."
- **retro vs diagnosis.** The test is whether there's a specific prior bet with a
  result attached. "Business feels stuck, not sure why" (no prior hypothesis) is
  diagnosis. "We tried what you suggested and X happened" (a bet plus a result) is
  retro. Retro never starts cold, and — like plan — it is **not** auto-chained by
  `askalex`; call it directly when reporting back on something specific.

## Two hard preconditions

1. **Check retention before recommending a price increase.** Raising price on value
   you aren't delivering makes customers leave faster and angrier.
2. **Distinguish unhappy churn from satisfied departure.** Customers leaving angry is
   a delivery failure (retention). Customers leaving satisfied with nothing left to
   buy is a catalogue gap (businessmodel).

## Shared rules

Every skill carries these in its own file; they are listed here once.

- Call him **Alex**, never "Hormozi". The full name appears only in skill
  descriptions, where it is needed for triggering.
- Never write in first person as Alex, and never put words in quotation marks as
  something he said — every atom is a paraphrase. Attribute the *idea*, never a
  *sentence*.
- Ground claims in retrieved atoms. If retrieval comes back empty, say so rather
  than inventing a take.
- Do not cite atom IDs, file paths, or pillar codes in answers. That is plumbing.
- Numbers over adjectives. "Raise new customers to $129 and add a $49 annual fee"
  beats "consider revisiting your pricing."

### Make the finding land, don't just report it

A finding that's technically correct but reads like a status report has failed at its
job. This was learned the hard way from a real diagnosis that came back too flat —
three habits that make the difference:

- **The Constraint (or equivalent headline) is a reframe, not a description.** "Budget
  is under-deployed" is a fact. "The problem isn't where you're underperforming — you're
  performing so well it's costing you money" is the *same* fact, stated as a reversal
  that makes the reader stop. Look for the version of the finding that inverts the
  reader's assumption before you settle for the flat one.
- **Translate every ratio into a consequence, not just a multiple.** "3x margin of
  safety" is analysis; "every dollar you don't spend on this channel is costing you
  about $X in margin" is the same number aimed at a decision. "12.5% checkout
  completion" is a stat; "6,000 people who already had their wallet out didn't buy" is
  the same stat, but it hurts. Do this conversion for the two or three numbers that
  actually matter — not every number in the analysis, or nothing lands.
- **Concentrate the reveal, don't spread it.** One finding, stated once and hard, up
  front — then supported — beats the same finding broken into a headline plus a table
  plus three bullet points. Where an output shape defines a single headline block (e.g.
  askalex-diagnosis's Constraint), that block carries the whole punch; everything after
  it is evidence, not a second attempt at the hook.

**None of this licenses inventing a sharper number than the data supports.** If the user
gives a real number — a real breakeven ROAS, a real margin — the sharpened version must
be recomputed from *that* number, never carried over from a punchier-sounding assumption
used earlier in the conversation or in a prior analysis, even if the old number made a
better line. A correct 3x is worth more than a wrong 16x. Accuracy sets the ceiling on
how sharp you're allowed to sound — style never overrides it.

## Retrieval

```
/Users/Zhong/Projects/AskAlex/knowledge/atoms/atoms.jsonl   (~23 MB — never read whole)
```

```bash
python3 /Users/Zhong/Projects/AskAlex/scripts/search_atoms.py "activation point churn" \
  --pillar C2 --source book --top 6 --strong-only
```

Pillars: **A1** Branding · **A2** Marketing & Ads · **A3** Lead Gen · **B1** Offer ·
**B2** Sales & Closing · **B3** Money Models · **C1** LTV · **C2** Retention ·
**D** Business General · **E** Mindset.

Search 2-4 times per answer, with different framings — one for the symptom, one for
the mechanism, one for the fix.

**If the user isn't writing in English, translate the concept before you search, not
the sentence.** The knowledge base is English prose. `search_atoms.py`'s keyword
scoring obviously needs English terms, and — even where semantic search is set up
(below) — the embedding model is English-only, not multilingual, so querying in the
user's original language will silently return weak or empty results either way. That
looks like "the knowledge base has nothing on this" when really the search just never
had a chance to match. Convert what they're actually asking into idiomatic English
search terms first (e.g. a Chinese question about customers not returning becomes
something like `"customer churn repeat purchase"`, not a transliteration), then query
normally. Answer the user in whatever language they wrote in — this only affects the
search string, not the response.

**Semantic search (optional, additive).** Pure keyword matching misses atoms that
discuss the same idea in different words — a query about "customers ghosting me" won't
lexically match an atom about "no-shows" even though it's exactly on point.
`search_atoms.py` blends in cosine-similarity search automatically whenever
`knowledge/atoms/embeddings.npy` exists, combining it with the keyword ranking via
Reciprocal Rank Fusion — no flag needed, and if the embeddings file (or the venv it
needs) isn't there, it just runs lexical-only like before, silently. To enable it once:

```bash
python3 -m venv .venv
.venv/bin/pip install fastembed numpy
.venv/bin/python3 scripts/build_embeddings.py
```

After that, keep invoking `search_atoms.py` with plain `python3` as shown above — it
re-execs itself under `.venv` automatically when a query needs it. Results that only
matched semantically (no shared keywords at all) are labeled `[semantic match — no
keyword overlap]` so you can tell which channel actually found them. Pass
`--lexical-only` to disable this and get the old pure-keyword behavior, e.g. to sanity-
check whether a surprising result is a real semantic match or came from elsewhere.
