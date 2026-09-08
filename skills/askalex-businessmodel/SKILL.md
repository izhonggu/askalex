---
name: askalex-businessmodel
description: Design the sequence of offers that turns a business into a cash machine. Use when the problem is structural rather than per-offer ("we make one sale and that's it", "no backend", "customers buy once and disappear", "CAC takes too long to pay back", "we're always cash poor despite good sales", "what do I sell next", "how do I add recurring revenue"). Covers the three-stage Money Model — attraction offers, upsells and downsells, continuity — and how cash moves through them. Grounded in 929 money-model atoms including Alex Hormozi's $100M Money Models book. Distinct from askalex-offer, which designs a single offer; this arranges many offers into an order.
---

# AskAlex Business Model

## How this differs from askalex-offer

**askalex-offer makes one offer excellent.** It works on problem coverage, stack, guarantee, name. The unit of work is a single offer.

**This skill arranges offers into a sequence.** The unit of work is the *order* and the *cash flow between them*. A business can have a wonderful offer and still be broke, because there is nothing to buy next and no cash collected up front.

**Routing rule:** if the user is describing one offer that underperforms, go to askalex-offer. If they are describing a business where the offers exist but the *shape* is wrong — no backend, no recurring, cash-starved — come here.

## The Money Model

A Money Model is a **deliberate sequence of offers**. Not a menu, not a product line — an order, designed so that each stage does a specific job.

Different offers solve different problems. Once you solve one problem for a customer, the next problem appears, and that problem also needs an offer. Winning is figuring out what to offer next.

**Three stages:**

| Stage | Name | Job |
|---|---|---|
| **I** | **Get Cash** — Attraction Offers | get more customers, for less |
| **II** | **Get More Cash** — Upsells & Downsells | make more money from them, faster |
| **III** | **Get The Most Cash** — Continuity Offers | maximize what they spend in total |

The sequence matters. Attraction first — once it reliably produces customers and cash, add upsells. Then continuity. Building stage III before stage I works is the most common way to waste a year.

### Stage I — Attraction Offers

The job is customer acquisition that does not lose money. Two design notes:

- **Up-front cash.** Structure the front offer so cash lands before you deliver. This is what makes acquisition affordable at scale — you are not financing the customer's first month out of pocket.
- **Decoy offers.** Advertise something free or heavily discounted to get attention, then present the premium offer alongside it once they raise their hand. The decoy is not the product; it is the entry.

### Stage II — Upsells & Downsells

The goal of an upsell: **30-day profits well above the cost of acquiring the customer and delivering the thing.** That single sentence is the test. If your upsell does not clear CAC inside 30 days, it is not doing its stage-II job.

A downsell is **what you offer when they say no**. Most businesses treat a no as the end of the conversation; a money model treats it as a branch. Downselling tweaks the original offer — same outcome, different scope, different payment terms — and can run as a payment-plan ladder rather than a single step.

Recovering the no is usually cheaper than generating a new lead. This is the most underbuilt stage in most businesses.

### Stage III — Continuity

Continuity is what turns a transaction into a relationship: the thing they keep paying for. It is where total spend per customer is actually determined, and it is why two businesses with identical front-end offers can have wildly different enterprise values.

Adding recurring revenue to a business that has none is usually the single largest LTV move available.

## Diagnosing the shape

Find which stage is missing or broken. They fail in distinguishable ways:

| Symptom | Missing / broken | Why |
|---|---|---|
| Acquisition is expensive, growth is slow | **Stage I** | no attraction offer doing the acquisition work; you are paying full price for cold attention |
| Good sales, thin profit, always short on cash | **Stage II** | no upsell clearing CAC in 30 days; you collect once and carry the cost |
| Constantly re-buying the same customer | **Stage III** | no continuity; every month starts from zero |
| Customers buy once and vanish though they're happy | **Stage III** | satisfied but nothing to buy next — a catalogue problem, not a satisfaction problem |

**One important distinction before prescribing:** "customers leave" has two very different causes. If they leave *unhappy*, that is a delivery and retention problem — not a business-model problem, and adding a backend offer will not save it. If they leave *satisfied*, there is simply nothing next for them to buy, and that is squarely this skill. Establish which before you design anything.

## Output shape

**1. Current shape** — map what they sell today onto the three stages. Name which stage is empty or underbuilt. Most businesses have one and a half stages and do not know it.

**2. The constraint** — one sentence on which stage caps them and what the money consequence is (CAC payback, cash timing, LTV).

**3. The next offer** — one offer to add, placed at the stage that is missing, stated concretely: what it is, who it is for, what it costs, and what it does for cash. Do not design all three stages at once; sequencing is the point.

**4. The cash effect** — what changes in 30-day profit or payback period if this works, and the number that would tell you it did not.

## The knowledge base

929 money-model atoms (pillar B3), including Alex's $100M Money Models book and the related lost chapters. At:

```
/Users/Zhong/Projects/AskAlex/knowledge/atoms/atoms.jsonl
```

Retrieve — never read it whole:

```bash
python3 /Users/Zhong/Projects/AskAlex/scripts/search_atoms.py "upsell offer 30 day profit" --pillar B3 --source book --top 6 --strong-only
```

| Flag | When |
|---|---|
| `--pillar B3` | restrict to money models (also `C1` LTV, `B1` offer, `C2` retention) |
| `--source book` | $100M Money Models is structured and dense — prefer it for stage design |
| `--source transcript` | spoken examples — better for real business breakdowns |
| `--strong-only` | drop atoms with no clear topic — recommended |
| `--full` | no content truncation |

Search 2-4 times: one for the stage ("attraction offer up front cash"), one for the mechanism ("downsell payment plan"), one for the constraint ("customer acquisition cost payback").

## Rules

- **Call him Alex, never "Hormozi".** First name only: "Alex's read on this would be…". The full name "Alex Hormozi" is for the skill description only.
- **Ground it in retrieved atoms.** If the search comes back empty, say so and work from the three stages alone — do not invent an "Alex take" no atom supports.
- **Never write in first person as Alex.** Speak *about* the thinking.
- **Never quote him.** Every atom is a paraphrase. Attribute the *idea*, never a *sentence*.
- **Do not cite atom IDs, file paths, or pillar codes in the answer.** That is plumbing.
- **Numbers over adjectives.** "Add a $199/mo continuity tier and CAC pays back in 18 days instead of 90" beats "consider adding recurring revenue."
- **Build one stage at a time.** Recommending attraction + upsell + continuity simultaneously is not a plan, it is a wish list.
- **Check whether customers leave happy or unhappy before prescribing.** Adding backend offers to a broken delivery just makes more people leave.
