---
name: askalex-leadgen
description: Diagnose and fix lead flow with the Core Four. Use when the user needs more prospects at the top of the funnel ("not enough leads", "we only have one channel working", "where do I find customers", "our ads died and we have no backup", "should I do cold outreach or content"). Covers the four ways to get leads — warm outreach, posting content, cold outreach, paid ads — how to choose given time vs money, and how to build a lead magnet that converts. Grounded in 2,080 lead-gen atoms including Alex's $100M Leads book.
---

# AskAlex LeadGen

## The Core Four — the whole model

There are exactly four ways to let other people know you exist. Everything else is a variation on these.

|  | **Warm** (they know you) | **Cold** (they don't) |
|---|---|---|
| **1-to-1** | Warm Outreach | Cold Outreach |
| **1-to-many** | Posting Content | Paid Ads |

Most businesses have one working and ignore the other three. That is both the diagnosis and the ceiling: **a single channel is a single point of failure**, and every channel saturates eventually.

**Scope:** this skill gets people to notice you. If leads are arriving and not converting, that is a closing problem — go to askalex-sales, not here.

## Which channel — time vs money

Warm outreach comes first, always: it is free and fastest to cash.

After that the choice is a resource question, not a taste question:

- **More time than money → posting content.** Compounds slowly, costs labour, no cash outlay.
- **More money than time → paid ads.** Fast, costs cash, scales while you sleep.

"Which channel is best" is the wrong question. The right one is which resource you have surplus of.

## The Core Four stacks

Channels are not either/or. The sequence compounds: get leads yourself, then get **lead getters** who bring leads on your behalf, then lead getters who recruit lead getters. Each layer trades your work for leverage.

## Lead magnets

A lead magnet is free value traded for contact details. It lowers acquisition cost because free converts better than paid-to-paid.

Two tests, both from Alex:

1. **It should be valuable enough that you could charge for it.**
2. **After consuming it, they should want more of what you sell** — it moves them one step closer to buying.

Most lead magnets fail one or both: either filler nobody wants, or genuinely useful but unrelated to the paid offer.

Rough economics: customer acquisition cost often lands near **3x the cost to deliver the lead magnet**. If your numbers are far worse, the magnet is wrong — not the channel.

## Output shape

**1. Channel map** — which of the four is working, which are empty. Name the single point of failure.

**2. The constraint** — is this a *volume* problem (too few channels), a *conversion* problem (leads arrive but they are bad), or a *leverage* problem (you personally are the channel)? These have different fixes and get confused constantly. Establish which one before prescribing.

**3. Next channel** — one to add, with the time-vs-money reason attached.

**4. Lead magnet** — one spec that passes both tests, or a concrete fix to the existing one.

## The knowledge base

2,080 lead-gen atoms (pillar A3), drawn mostly from Alex's $100M Leads book. At:

```
/Users/Zhong/Projects/AskAlex/knowledge/atoms/atoms.jsonl
```

Retrieve — never read it whole:

```bash
python3 /Users/Zhong/Projects/AskAlex/scripts/search_atoms.py "cold outreach warm audience" --pillar A3 --top 6 --strong-only
```

| Flag | When |
|---|---|
| `--pillar A3` | restrict to lead-gen atoms (also useful: `A2` ads, `A1` branding) |
| `--source book` | denser and structured, or `transcript` (spoken, more examples) |
| `--strong-only` | drop atoms with no clear topic — recommended |
| `--full` | no content truncation |
| `--no-dedup` | show near-duplicates (dedup is on by default) |

Search 2-4 times: one for the channel ("cold outreach script"), one for the asset ("lead magnet free value"), one for the constraint ("channel saturated second source").

## Rules

- **Call him Alex, never "Hormozi".** First name only: "Alex's read on this would be…". The full name "Alex Hormozi" is for the skill description only.
- **Ground it in retrieved atoms.** If the search comes back empty, say so and work from the Core Four alone.
- **Never write in first person as Alex.** Speak *about* the thinking.
- **Never quote him.** Every atom is a paraphrase. Attribute the *idea*, never a *sentence*.
- **Do not cite atom IDs, file paths, or pillar codes in the answer.** That is plumbing.
- **Numbers over adjectives.** "Send 50 cold DMs a day for two weeks" beats "consider doing outreach."
- **Separate volume from conversion from leverage.** "Not enough leads" is at least three different problems. Diagnose which before prescribing.
