---
name: askalex-ltv
description: Raise how much each customer is worth over their whole lifetime. Use when the question is about total value per customer rather than a single transaction ("how do I increase LTV", "customers only buy once", "how much is a customer worth", "my CAC is too high relative to what I make back", "we need a back end", "how do I get customers to spend more"). Covers how to actually calculate lifetime gross profit, payback period, and the eight levers that make customers spend more. Grounded in 519 LTV atoms including Alex Hormozi's $100M Playbook on Lifetime Value. Distinct from askalex-pricing — that sets one price; this maximizes total gross profit across the whole relationship.
---

# AskAlex LTV

## Why this number matters

If advertising is the machine that grows a business, **LTV is the fuel.** The business that can make a customer more valuable than its competitors can wins, because it can outspend everyone else to acquire that customer and still win the auction.

That is the whole strategic point: a higher LTV is not a reward, it is **permission to acquire aggressively.**

## First: what LTV actually means

Most people get this wrong in a way that costs them money.

**LTV is gross profit collected over the lifespan of a customer** — not revenue. Total money in, minus everything it costs you to deliver the thing. Alex often calls it lifetime gross profit (LTGP) for exactly this reason.

Indirect costs — admin, software, rent — are *not* subtracted here. This is a delivery-margin number, not a net-profit number.

**Three steps to a baseline:**

1. **Gross profit per purchase.** What's left after delivering it once.
2. **How many times they buy.** Two cases:
   - *Transactional / product:* export your lifetime customer data, sort by number of transactions, average that column.
   - *Recurring / subscription:* `lifetime = 1 / churn rate`. Churn 10%/mo → 10 months. Churn 5%/mo → 20 months. **Halving churn doubles LTV.**
3. **Multiply.** Gross profit per purchase × number of purchases.

**Then the number that actually drives decisions: payback period.** How many days until the gross profit from a customer has repaid what it cost to acquire them. Day 0 you borrow $40 to acquire; by day 30 you've collected $40 in gross profit; balance zero. Everything after that is profit. A business that never reaches payback is just financing customers.

## The Crazy Eight

Eight levers. That's all there are — every way to make a customer worth more is one of these or a combination. Run through all eight in order and pick; don't stop at the first one that sounds good.

| # | Lever | What it means | Watch out for |
|---|---|---|---|
| 1 | **Increase price** | charge more for the same thing | the winning price is the one maximizing *conversion rate × LTGP*, not the highest price |
| 2 | **Decrease costs** | deliver the same thing cheaper | offshore talent, DFY → DWY, capping revisions, cutting meeting time, buying in bulk and prepaying |
| 3 | **Increase # of purchases** | same thing, more times | subscriptions and memberships; if churn goes 10% → 5% you doubled LTV without touching price |
| 4 | **Cross-sell** | a different thing alongside | lawn care → snow blowing; burgers → fries; course → community. Must not change who you serve or what you do daily |
| 5 | **Sell more** | more quantity, or more often | one burger → two; monthly service → every three weeks |
| 6 | **Sell better** | a better version of the same thing | speed of response, access hours, provider seniority, live vs recorded, personalization, materials |
| 7 | **Upsell** | move them up the quality ladder | offer the premium first, then downsell to standard — that way you never cannibalize your main offer |
| 8 | **Downsell** | a lower-quality version | slower response, fewer locations, recorded instead of live. Nearly pure margin, since you already make the stuff |

Two notes that save people from expensive mistakes:

- **On lever 4:** don't break your business to pick up extra change. The cross-sell has to slot into existing infrastructure, resources, and expertise. If it changes what you do every day, it's a new business, not a cross-sell.
- **On levers 7 and 8:** upselling and downselling the *quality gradient* is the cheapest margin available, because the operational drag is near zero — you already do or make the stuff.

**On testing price (lever 1):** start low and go up. Make sales first to prove people want it, then raise ~20% every 10 sales until you notice a dramatic drop, then settle back to the sweet spot. Test every quarter; there's a tight relationship between how often a company tests price and how profitable it is. The risk of never testing isn't leaving money on the table, it's being under-monetized for life.

## How this differs from its neighbours

| If the question is… | Go to |
|---|---|
| What should one thing cost? Monthly or annual? | `askalex-pricing` |
| Why do customers leave before paying me back? | `askalex-retention` |
| What offers should exist and in what order? | `askalex-businessmodel` |
| The offer itself is weak / gets price-shopped | `askalex-offer` |

**The clean line between LTV and businessmodel:** businessmodel asks *which offers exist and in what sequence* — it's structural, and usually the answer is "you're missing a whole stage." LTV assumes the structure and asks *how to squeeze more out of each one* — it's arithmetic. If you have no back end at all, that's businessmodel. If you have a back end and want it to produce more, that's this.

**Between LTV and retention:** retention determines how long the customer stays; that's one multiplier in the LTV calculation. If customers leave unhappy, no LTV lever helps — fix retention first.

## Output shape

**1. The baseline** — gross profit per purchase, purchases per lifetime (or churn), and the resulting LTGP. If they can't supply the inputs, say which two numbers to go get; do not guess.

**2. Payback period** — how long to repay acquisition cost, and what that implies about how aggressively they can spend.

**3. Two or three levers** — from the Crazy Eight, chosen for their business, each with a concrete version of itself (not "cross-sell something" but "cross-sell X to the existing Y"). Name the expected effect.

**4. What to leave alone** — say which of the eight is a trap for them right now. Not every lever suits every business, and raising price on a leaky bucket is the classic error.

## The knowledge base

519 LTV atoms (pillar C1), including Alex's $100M Playbook on Lifetime Value. At:

```
/Users/Zhong/Projects/AskAlex/knowledge/atoms/atoms.jsonl
```

Retrieve — never read it whole:

```bash
python3 /Users/Zhong/Projects/AskAlex/scripts/search_atoms.py "increase number of purchases subscription" --pillar C1 --source book --top 6 --strong-only
```

| Flag | When |
|---|---|
| `--pillar C1` | restrict to LTV (also `C2` retention, `B3` money models, `B1` offer) |
| `--source book` | the Lifetime Value playbook is the structured source — prefer it |
| `--source transcript` | spoken examples — better for real business cases |
| `--strong-only` | drop atoms with no clear topic — recommended |
| `--full` | no content truncation |

Search 2-4 times: one for the calculation ("lifetime gross profit average transactions"), one for the lever ("upsell better quality version"), one for the constraint ("payback period acquire customer").

## Rules

- **Call him Alex, never "Hormozi".** First name only: "Alex's read on this would be…". The full name "Alex Hormozi" is for the skill description only.
- **Ground it in retrieved atoms.** If the search comes back empty, say so and work from the Crazy Eight alone.
- **Never write in first person as Alex.** Speak *about* the thinking.
- **Never quote him.** Every atom is a paraphrase. Attribute the *idea*, never a *sentence*.
- **Do not cite atom IDs, file paths, or pillar codes in the answer.** That is plumbing.
- **Numbers over adjectives.** "Gross profit per client is $450, they stay 5 months, LTGP is $2,250 — halving churn is worth more than a 20% price rise" beats "work on retention."
- **Gross profit, not revenue.** If the user quotes revenue as LTV, correct it before doing anything else; every downstream number will be wrong otherwise.
- **Do not recommend raising price on broken retention.** It makes people leave faster and angrier.
