# AskAlex skills

Ten skills. Nine specialists share one knowledge base (25,101 atoms) and one
set of rules, each owning a distinct question — plus `askalex`, the front
door, which reads a situation and routes to the right one (or diagnoses
first, then continues straight into the specialist, in one pass).

**Unsure which one applies? Start with `askalex`.** It does the classification
below for you and chains the diagnosis into the specialist's actual answer
instead of just naming which skill to go ask next. Everything past this point
is what `askalex` is routing against — read on if you're adding a skill,
calling a specialist directly, or want to know why a boundary is drawn where
it is.

## Pick one

| Skill | Use when the question is about | Core framework |
|---|---|---|
| `askalex` | **you don't know which of these nine to pick** | routes to one, or diagnoses then chains into one — see [`askalex/SKILL.md`](askalex/SKILL.md) |
| `askalex-diagnosis` | **the business as a whole**, and the user cannot say where it hurts | three growth levers → locate the constraint, then hand off |
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
the sentence.** The knowledge base is English prose and `search_atoms.py` does
keyword/TF scoring, not cross-lingual embedding matching — querying it with the
user's original non-English text will silently return weak or empty results, which
looks like "the knowledge base has nothing on this" when really the search just never
had a chance to match. Convert what they're actually asking into idiomatic English
search terms first (e.g. a Chinese question about customers not returning becomes
something like `"customer churn repeat purchase"`, not a transliteration), then query
normally. Answer the user in whatever language they wrote in — this only affects the
search string, not the response.
