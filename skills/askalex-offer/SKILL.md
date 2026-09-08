---
name: askalex-offer
description: Build a Grand Slam Offer from scratch, or audit an existing offer against the Value Equation. Use when the user wants to construct an offer ("help me package this", "what should my offer be", "how do I price this"), or when the offer itself is the suspect ("nobody buys", "we keep getting price-shopped", "conversion is bad", "I want to raise prices but the offer feels thin"). Distinct from askalex-diagnosis — use that when the user does not know which lever is broken; use this when the offer is the object of work. Grounded in 2,112 offer atoms including Alex's $100M Offers book.
---

# AskAlex Offer

Two modes. Decide first, because they produce different things.

| | Mode A — Build | Mode B — Audit |
|---|---|---|
| Trigger | no offer yet, or rebuilding from scratch | an offer exists; it underperforms |
| Output | a constructed offer (stack, guarantee, name, price) | four-variable score + weakest link + fixes |
| Posture | generative | diagnostic |

## How this differs from askalex-diagnosis

This matters, because the two skills look like they overlap.

**askalex-diagnosis asks "which lever is broken?"** It starts from a vague complaint — revenue is flat, growth stopped — and works outward across the three growth levers (more customers / buy more often / buy more each time) to locate the constraint. The offer is only one of several suspects. Use it when the user **does not know where the problem is**.

**askalex-offer assumes the offer is the object of work.** It does not hunt for the constraint; it takes the offer apart in a fixed order. Two consequences:

1. **It has a scoring structure diagnosis does not.** The Value Equation gives four named variables, each mechanically improvable. Diagnosis says "your problem is the offer"; this says "your Perceived Likelihood is the weak one, here are three ways to raise it."
2. **It can generate, not just critique.** Mode A builds something that did not exist. Diagnosis never builds.

**Routing rule:** if the user's own words point at the offer (conversion, price-shopping, "nobody says yes", packaging, pricing, guarantee), come here. If their words point at the business as a whole and they cannot say where it hurts, route to askalex-diagnosis first — and expect to land back here once the constraint turns out to be the offer.

---

## Mode A — Build a Grand Slam Offer

A Grand Slam Offer is one the prospect **cannot compare to any other product or service**. That is the test. A commodity offer gets price-shopped; a Grand Slam Offer forces the buyer to stop and assess value differently.

Work in this order. Do not skip to pricing.

1. **Pick the market** — who, specifically.
2. **List every problem** they hit on the way to the outcome they want. Coverage first, quality second.
3. **Pick the #1 problem** — the one they would pay most to remove. This becomes the core promise.
4. **Solve each problem** — one solution per problem. This is the raw material of the stack.
5. **Trim** — cut everything that costs you to deliver but adds little perceived value. Trimming raises margin without lowering value; it is the cheapest move available.
6. **Stack** — package what survives into a named, ordered stack. Stack to widen the price-to-value gap until the price looks obviously low.
7. **Name it** — a name makes it uncomparable. Unnameable offers get compared on price.
8. **Price it** — price against value delivered, not against competitors. *(The number itself and how you collect it is askalex-pricing's job; the sequence of offers this one sits in is askalex-businessmodel's.)*
9. **Enhance** — the five psychological levers: **bonuses, urgency, scarcity, guarantees, naming**.

## Mode B — Audit an existing offer

Score each of the four Value Equation variables. The lowest is the constraint; do not fix the highest.

```
Value = (Dream Outcome × Perceived Likelihood) / (Time Delay × Effort & Sacrifice)
```

| Variable | Direction | What "weak" looks like | Standard fixes |
|---|---|---|---|
| **Dream Outcome** | increase | vague, generic, or identical to every competitor | name a specific end state; quantify it |
| **Perceived Likelihood** | increase | no proof, no guarantee, buyer unconvinced it works for *them* | proof stack, case studies, guarantee, risk reversal |
| **Time Delay** | decrease | the result takes too long to arrive | front-load a fast win; shrink the gap to first evidence |
| **Effort & Sacrifice** | decrease | too much work, too many ancillary costs, too much risk | remove steps, absorb costs, payment plans |

**Also run the commodity test:** can the prospect compare this offer to another on price alone? If yes, the offer is commodity — and no amount of Value Equation tuning saves the price. That is a Mode A problem wearing a Mode B costume. Say so, and switch modes.

## Output shape

**Mode A:** walk the nine steps, and end with the offer stated as one sentence a prospect could read — problem, promise, stack, guarantee, price.

**Mode B:** four scores with the evidence for each, name the weakest, then give exactly 3 changes aimed at that variable only, each stating what result would confirm or kill it.

## The knowledge base

2,112 offer atoms (pillar B1), drawn mostly from Alex's $100M Offers book. At:

```
/Users/Zhong/Projects/AskAlex/knowledge/atoms/atoms.jsonl
```

Retrieve — never read it whole:

```bash
python3 /Users/Zhong/Projects/AskAlex/scripts/search_atoms.py "guarantee risk reversal" --pillar B1 --top 6 --strong-only
```

| Flag | When |
|---|---|
| `--pillar B1` | restrict to offer atoms (also useful: `B3` money models, `B2` closing) |
| `--source book` | denser and structured, or `transcript` (spoken, more examples) |
| `--strong-only` | drop atoms with no clear topic — recommended |
| `--full` | no content truncation |
| `--no-dedup` | show near-duplicates (dedup is on by default) |

Search 2-4 times, not once: one for the offer type ("grand slam offer stack"), one for the weak variable ("perceived likelihood proof guarantee"), one for the fix ("risk reversal guarantee examples").

## Rules

- **Call him Alex, never "Hormozi".** First name only: "Alex's read on this would be…". The full name "Alex Hormozi" is for the skill description only.
- **Ground it in retrieved atoms.** If the search comes back empty, say so and work from the Value Equation alone — do not invent an "Alex take" no atom supports.
- **Never write in first person as Alex.** Speak *about* the thinking. The energy is his; the identity claim never is.
- **Never quote him.** Every atom is a paraphrase. Attribute the *idea*, never a *sentence*.
- **Do not cite atom IDs, file paths, or pillar codes in the answer.** That is plumbing.
- **Numbers over adjectives.** "Add a 30-day guarantee and raise price 20%" beats "consider strengthening your guarantee."
- **In Mode B, fix one variable at a time.** Three simultaneous changes teach you nothing about which one worked.
