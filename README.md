# AskAlex

English | [简体中文](README.zh-CN.md)

**A 24/7 business coach that thinks the way Alex Hormozi does — living inside your Claude Code.**

![License](https://img.shields.io/badge/license-MIT-blue)
![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-blueviolet)
![Skills](https://img.shields.io/badge/skills-9-orange)
![Status](https://img.shields.io/badge/status-early-lightgrey)

> Bring it a business problem at any hour — pricing, an offer that isn't converting, customers who cancel, leads that go nowhere, or just the fact that you know what to do and aren't doing it — and it doesn't just answer, it diagnoses. Nine specialist skills share one job: locate what's actually broken, name the framework behind the read, and hand you three things to try this week, each with a way to know if it worked.

Not affiliated with or endorsed by Alex Hormozi or Acquisition.com. This is fan-built, educational tooling — see [Disclaimer](#disclaimer).

---

![How AskAlex works](docs/how-it-works.svg)

## The problem this solves

Most "AI business advice" fails in one of two ways: it's generic enough to apply to any business (so it applies to none), or it answers the question you asked instead of the question underneath it. "Should I raise my prices?" is rarely a pricing question — it's usually an offer problem, an activation problem, or a wrong-customer problem wearing a pricing costume.

AskAlex diagnoses before it prescribes. Nine specialist skills, each owning one part of the business (the offer, the price, the sequence of offers, lifetime value, retention, sales, lead flow, or the operator's own head), plus one skill whose only job is figuring out which of the other eight you actually need.

| Real situation | What you get |
|---|---|
| "Customers say I'm too expensive" and you don't know if it's the price, the offer, or the pitch | A located constraint, the mechanism behind it, and three falsifiable actions — not a guess |
| An offer that isn't converting, or no offer yet | A four-variable audit (Value Equation) or a built offer, step by step, ending in one sentence a prospect could read |
| Good sales, thin profit, always short on cash | A map of your offer sequence against the three-stage Money Model, and the one stage that's missing |
| Customers cancel around the same point every time | The activation point, the decay curve, and the specific week to intervene |
| Leads exist but nobody closes, or nobody's calling at all | Routed to the right one of leadgen (nobody's talking to you) or sales (they are, but it's not converting) |
| "I know what to do and I'm not doing it" | The entrepreneurship skill — this is the one time the constraint is the person, not the business |

## Quick start

```bash
git clone https://github.com/izhonggu/askalex.git
cd askalex
```

Read [Knowledge base](#knowledge-base-you-build-your-own) first — the skills need a local `knowledge/atoms/atoms.jsonl` to retrieve from, and this repo doesn't ship one (on purpose; see why below).

Then install the skills into Claude Code:

```bash
# Project-scoped — only active inside this project
mkdir -p /path/to/your/project/.claude/skills
cp -r skills/askalex-* /path/to/your/project/.claude/skills/

# or globally — active in every project
cp -r skills/askalex-* ~/.claude/skills/
```

Once installed, just describe the problem — you don't need to know which skill you want:

```text
/askalex My coaching business is $500/mo and people cancel around month 3.
Should I just raise the price?
```

`askalex` is the front door — it reads the situation, decides whether it's one specialist's job or needs diagnosis first, and answers in one pass (here: it diagnoses, finds the real issue is retention rather than pricing, and continues straight into the retention read — no need to ask twice). See the example inside [`skills/askalex/SKILL.md`](skills/askalex/SKILL.md).

If you already know exactly what you need, skip the front door and say so directly — "audit this offer," "help me raise prices," "why do people cancel" — and Claude will match straight to the relevant specialist.

## The ten skills

One front door, nine specialists behind it:

| Skill | Use when the question is about | Core framework |
|---|---|---|
| `askalex` | **you don't know which of these to pick** — the front door | routes directly, or diagnoses then chains into the right specialist |
| `askalex-diagnosis` | **the business as a whole**, and you can't say where it hurts | three growth levers → locate the constraint, then hand off |
| `askalex-offer` | **one offer** — building it, or why it isn't converting | Value Equation (4 variables) + Grand Slam Offer (9 steps) |
| `askalex-pricing` | **the number and the terms** — what to charge, whether to raise, how to bill | three pricing models + 10 pricing plays + price/value/churn |
| `askalex-businessmodel` | **the shape** — no back end, CAC never pays back, always cash-poor | Money Model: attraction → upsell/downsell → continuity |
| `askalex-ltv` | **total value per customer** — make them worth more over the whole relationship | LTGP calculation + the Crazy Eight |
| `askalex-retention` | **why customers leave** — churn, activation, first 30 days | churn checklist + activation points |
| `askalex-sales` | **people already in conversation** — close rate, objections, pitch | three buckets + onion of blame + named closes |
| `askalex-leadgen` | **nobody is talking to you** — not enough leads, one channel | Core Four (warm/cold × 1-to-1/1-to-many) |
| `askalex-entrepreneurship` | **the person** — fear, beliefs, discipline, burnout, consistency | pain / beliefs / fear / identity / agency / patience |

Full routing table, boundary rules between skills, and shared conventions live in [`skills/README.md`](skills/README.md) — read it before adding a tenth skill, the nine already spent real effort not overlapping.

## How it works

```text
your source material (transcripts, books, notes — yours to provide)
   │
   ▼  scripts/extract_docx.py, scripts/extract_books.py
plain text, cleaned of front matter / TOCs / ligature-encoding bugs
   │
   ▼  scripts/atomize.py  (TextTiling semantic segmentation, no LLM calls)
knowledge/atoms/atoms.jsonl — ~100-word propositional atoms, tagged by pillar
   │
   ▼  scripts/search_atoms.py  (TF + title weighting + signal scoring)
a handful of relevant atoms per query
   │
   ▼
whichever askalex-* skill is answering, grounding its reasoning in what it retrieved
```

Every skill answers the same way: retrieve 2-4 times with different framings (the symptom, the mechanism, the fix), synthesize instead of dumping raw results, name the framework it used, and say plainly when retrieval comes back empty instead of inventing a take. See the shared rules in [`skills/README.md`](skills/README.md#shared-rules).

## Knowledge base — you build your own

This repo ships the **skills and the pipeline**, not a pre-built knowledge base. That's a deliberate line, not a missing feature:

The atomization pipeline (`atomize.py`) works by cutting source text into ~100-word chunks at semantic boundaries — it does **not** paraphrase or summarize. Run against copyrighted source material (books, paid course content), the output is near-verbatim excerpts of that material, just chunked. Distributing that alongside the skills would mean redistributing someone else's paid content, which this project isn't going to do.

To build your own:

```bash
python3 scripts/extract_docx.py      # your .docx transcripts -> plain text
python3 scripts/extract_books.py     # your PDF/EPUB books -> plain text (needs poppler: brew install poppler)
python3 scripts/atomize.py           # both -> knowledge/atoms/atoms.jsonl
```

`atomize.py --sources books` or `--sources transcripts` if you only have one kind. See [`knowledge/_README.md`](knowledge/_README.md) for the file layout, the `--strong-only` filtering flag (spoken transcripts run ~70% filler/small-talk), and the pillar taxonomy in [`knowledge/_taxonomy.md`](knowledge/_taxonomy.md).

If you want to point this whole system at your *own* business's content instead of Hormozi's — your own YouTube channel, your own internal playbooks — the pipeline doesn't care whose material it is. The skills' framework logic (Value Equation, Money Model stages, the Crazy Eight, etc.) stays useful as the diagnostic frame either way; only the retrieved examples change.

## Repo structure

```text
askalex/
├── skills/
│   ├── README.md              routing table + shared rules
│   ├── askalex/SKILL.md       the front door — routes or diagnoses-then-chains
│   └── askalex-*/SKILL.md     the nine specialists
├── scripts/
│   ├── extract_docx.py        transcript -> plain text
│   ├── extract_books.py       PDF/EPUB -> plain text
│   ├── atomize.py             plain text -> knowledge/atoms/atoms.jsonl
│   └── search_atoms.py        the retriever every skill calls
└── knowledge/
    ├── _taxonomy.md           the 10-pillar classification (A1-E)
    ├── _README.md             card library vs. atom library, rebuild instructions
    └── atoms/                 gitignored — build your own, see above
```

## Who this is for

- Founders, coaches, consultants, and agency operators who want a second opinion structured like a real diagnostic, not a pep talk
- Anyone who wants Alex's frameworks as a *thinking tool* inside their own agent, not a course to sit through
- Builders curious about the pipeline itself — TextTiling segmentation, prior-weighted pillar scoring, retrieval without an LLM in the loop — reusable on any corpus, business content or not

## Who this isn't for

- Anyone wanting a pre-packaged Hormozi knowledge base to download — see [above](#knowledge-base-you-build-your-own) for why that's not what ships here
- One-shot content generation (ad copy, social posts, landing pages) — every skill here diagnoses and prescribes, none of them draft publishable copy
- Anything requiring the skills to speak *as* Alex in the first person, or to quote him directly — both are hard rules the skills refuse, by design (see [Disclaimer](#disclaimer))

## Disclaimer

AskAlex is an independent, fan-built project. It is **not affiliated with, endorsed by, or reviewed by** Alex Hormozi or Acquisition.com. The frameworks referenced (Value Equation, Grand Slam Offer, Money Model, the Crazy Eight, and others) are his public teaching, distilled and paraphrased for this project's own use — not licensed or officially sanctioned material.

Every skill enforces the same three rules, and they are load-bearing, not decorative:

1. **First name only.** Body text says "Alex," never "Hormozi" — the full name appears only in skill descriptions, where exact identification is needed for triggering.
2. **Third person, always.** No skill writes in first person as Alex. It reasons *about* his frameworks — "Alex's read on this would be…" — and never claims his identity.
3. **No quotes.** Nothing in this project's knowledge base is presented as something he said verbatim. Every atom is a paraphrase; skills attribute the *idea*, never a *sentence*.

## License

[MIT](LICENSE) — the skills and pipeline code, which is all this repo contains. This license says nothing about, and grants no rights to, Alex Hormozi's underlying books or teaching; if you build your own knowledge base from his (or anyone else's) copyrighted material per the instructions above, that material remains under its own copyright and is yours to use locally, not to redistribute.

## Frameworks

Alex Hormozi's public teaching — YouTube, books, and talks.

## Author & support

Built by Zhong — [X](https://x.com/izhonggu) · [LinkedIn](https://www.linkedin.com/in/guzhong/) · [hardcoremkt.com](https://hardcoremkt.com/)

This ran a genuinely large amount of extraction, review, and iteration to put together — if a diagnosis here saved you a coaching call, a tip is welcome and helps keep it maintained.

<a href="https://www.paypal.com/qrcodes/managed/6048bb04-3f01-4e36-8a8a-77422345af41?utm_source=consweb_more"><img src="docs/paypal-qr.png" width="160" alt="Tip via PayPal"></a>

**[Tip via PayPal](https://www.paypal.com/qrcodes/managed/6048bb04-3f01-4e36-8a8a-77422345af41?utm_source=consweb_more)**
