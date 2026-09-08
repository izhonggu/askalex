# AskAlex Knowledge Base — Taxonomy Reference

All knowledge-base content, tags, and filenames in this project are in ENGLISH ONLY.
This file is the single source of truth for how source material (YouTube scripts, book PDFs)
gets classified into the knowledge base. Every extraction agent must read this file first.

## Core rule: paraphrase, never transcribe

Every entry in the knowledge base must be written in the extractor's OWN WORDS — a distilled,
synthesized summary of the idea/framework/lesson, not a transcription or close paraphrase of the
source script. Direct quotes are allowed only for short, distinctive phrases (under 15 words) in
quotation marks, and should be rare (at most one per source item). Do not reproduce long passages,
stories, or numbered lists verbatim from the source — re-derive the structure in new wording.
This is a hard requirement: the output must read as an analyst's notes, not a copy of the transcript.

## Taxonomy (10 pillars, grouped under Hormozi's own "Acquisition.com" mental model)

### A. Acquisition (getting people to know you / come to you)
- **A1 — Branding**: positioning, personal brand, content-as-brand, reputation, differentiation
- **A2 — Marketing & Ads**: paid ads, hooks, headlines, creative strategy, organic content strategy,
  social media growth tactics, "the marketing machine" (brand + ads + content working together)
- **A3 — Lead Generation**: lead magnets, outreach (warm/cold), the "Core Four" channels, lead nurture,
  audience-building tactics that produce inbound demand

### B. Monetization (getting people to buy / buy more)
- **B1 — Offer**: Grand Slam Offer construction, Value Equation (dream outcome, likelihood, time delay,
  effort/sacrifice), guarantees, bonuses, naming/packaging
- **B2 — Sales & Closing**: sales process, objection handling, closing scripts, pricing psychology,
  price increases, proof/social proof systems
- **B3 — Money Models**: offer sequencing across a customer journey, cash-flow structuring, upsell/
  downsell/cross-sell architecture, "fast cash" tactics, how a business's monetization model is built

### C. Retention (getting people to stay / buy again)
- **C1 — LTV (Lifetime Value)**: increasing value per customer over time, expansion revenue, LTV math
- **C2 — Retention & Churn**: keeping customers engaged, reducing cancellations/no-shows, win-back

### Cross-cutting (support the whole system, not tied to one of A/B/C)
- **D — Business General**: operations, hiring/team, systems & processes, scaling, partnerships,
  financials/accounting basics, general "how to run a business" content
- **E — Mindset**: entrepreneurial psychology, discipline, decision-making, resilience, life philosophy,
  personal development (this pillar draws almost entirely on YouTube, not the books)

### Not yet used
- If a source item is really about none of the above (e.g. pure personal-life content, unrelated to
  business or mindset), skip it — do not force a tag.

## Tagging rule

Each source item (one video or one book chapter) gets exactly **one primary tag** and may get
**0–2 secondary tags** if it genuinely spans pillars (e.g. a video that opens with a mindset point
and then teaches a sales technique gets primary=B2, secondary=[E]).

## Knowledge base file layout

One markdown file per pillar in `/Users/Zhong/Projects/AskAlex/knowledge/`:

```
A1_branding.md
A2_marketing_ads.md
A3_lead_generation.md
B1_offer.md
B2_sales_closing.md
B3_money_models.md
C1_ltv.md
C2_retention.md
D_business_general.md
E_mindset.md
```

## Card format (used inside each pillar file)

```markdown
### <Concise English title for the idea, NOT the video title verbatim>
**Source:** <original video/chapter title> — `AskAlex YouTube Scripts/<filename>.docx`
**Tags:** Primary: <CODE> | Secondary: <CODE, CODE or none>

- <Point 1, paraphrased, own words>
- <Point 2, paraphrased, own words>
- <Point 3, paraphrased, own words — 2-6 bullets total, whatever the idea needs>
```

Multiple cards can come from a single long video (e.g. a 90-minute Q&A might yield 4-5 cards across
different pillars). Short videos may yield only 1 card. Skip filler/small-talk content — only extract
substantive frameworks, tactics, or lessons.
