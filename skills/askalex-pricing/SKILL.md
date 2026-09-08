---
name: askalex-pricing
description: Set, structure, and raise prices. Use when the question is about the number or the way money is collected ("what should I charge", "should I raise my prices", "how do I raise prices without losing customers", "monthly or annual", "do I add a setup fee", "my margins are too thin", "should I discount"). Covers the three pricing models, staged price increases, and ten concrete pricing plays. Grounded in 2,398 pricing atoms including Alex Hormozi's $100M Playbook on Pricing and Price Raise. Distinct from askalex-offer — that builds and audits the offer; this decides what it costs and how the money is collected.
---

# AskAlex Pricing

## How this differs from askalex-offer

Both touch price, and the confusion is worth killing early.

**askalex-offer works on the offer** — problem coverage, stack, guarantee, name. It prices *relative to value delivered* as step 8 of nine. If the offer itself is weak, no pricing work saves it: a commodity offer gets compared on price no matter how cleverly it is structured.

**askalex-pricing works on the number and the structure** — which pricing model you are using, whether the price is too low, how to raise it without detonating churn, how often you bill, what fees exist, how payment terms shape cash.

**Routing rule:**

| The user says | Go to |
|---|---|
| "nobody buys", "we keep getting price-shopped", "my offer feels thin" | askalex-offer |
| "what should I charge", "should I raise prices", "monthly or annual", "margins are thin" | askalex-pricing |
| "customers say I'm too expensive" | neither yet — that is usually an offer problem in a pricing costume. Run askalex-diagnosis. |

**One hard precondition before any price increase:** raising price on value you are not delivering makes people leave faster and angrier. If retention is already broken, fix that first and say so. Price is a multiplier on delivery, not a substitute for it.

## The three pricing models

Almost everyone prices by looking at what competitors charge. That is the recipe for break-even and burnout — you end up running a nonprofit with none of the benefits.

| Model | How it works | The problem |
|---|---|---|
| **Cost plus** | costs plus an arbitrary margin | you never capture the buyers who would pay more because they need it more |
| **Competitor based** | charge roughly what everyone else charges | you inherit someone else's margins and their blind spots |
| **Value based** | price against the value delivered | the only one that leaves upside on the table in your favour |

The default answer is value based. But the model question is usually not where the money is — the number is.

## Raising prices

The core claim, and it is blunt: **9 times out of 10, when you raise prices you make more profit than you lose in sales.** Most businesses need to raise prices to grow, not lower them. Profit is oxygen.

Five mechanics:

1. **Raise price in stages.** Start cheap, take the early yeses, use the feedback to make the product better, then keep raising until you can no longer make up for the nos with the extra margin.
2. **Pair every increase with a value increase.** The bigger the price increase, the bigger the value increase has to be. You justify the number by making the thing better.
3. **Raise on new customers first**, never on an existing cohort you have not yet fixed.
4. **Annual price increases** as a standing policy, not a crisis response.
5. **More nos is not the same as less money.** On paper you sell fewer units at a higher price; in practice the margin usually wins. Do not read a dip in close rate as failure without checking profit.

**Watch the triangle: price, value, churn.** Price is what they pay; value is what they get. Keep value above price and customers stay. You can do that two ways — deliver more value, or charge less. Raising price while value stays flat is how churn starts.

## Ten pricing plays

Concrete, low-effort, and mostly independent of what you sell:

| # | Play | Effect |
|---|---|---|
| 1 | **Monthly → 28-day billing cycles** | 13 billing periods a year instead of 12 (~8% more) |
| 2 | **Processing fees + a second form of payment** | recovers fees, and cuts involuntary churn from expired cards (1.2–1.7%/mo) |
| 3 | **Sales tax handled explicitly** | menu pricing; stop absorbing it silently |
| 4 | **Annual price increases** | compounding, small enough to be unremarkable |
| 5 | **Annual billing** | cash up front, churn pushed out a year |
| 6 | **Round up** — 7s to 9s, add .99 | tiny per-client, large in aggregate |
| 7 | **Annual renewal fee on top of monthly** | a second, separate line |
| 8 | **Automatic continuity** | price an add-on at 5–20% of the main thing and attach it by default — but do not be a sneak about it |
| 9 | **Ultra high ticket anchor** | one very expensive option makes the middle option look reasonable |
| 10 | **Guarantee and warranty upsells** | ~1 in 20 takes it; nearly pure margin |

Pick by effort, not by greed. Plays 1, 6, and 10 are usually same-week.

## Output shape

**1. Model** — which of the three they are actually using, and whether that is the constraint. Say it plainly; most are on competitor-based and do not know it.

**2. The precondition check** — is retention healthy enough to raise? If not, stop and say what to fix first. Do not hand someone a price increase they will bleed from.

**3. The number** — a specific new price, or a specific staged path to one (e.g. $99 → $129 for new customers this month, $149 after the next value release). Attach the value change that justifies each step.

**4. Plays** — two or three from the ten above, chosen for their situation, with the expected effect quantified where the source supports it.

**5. What would falsify it** — the number that tells you this was wrong (close rate below X, churn above Y), and how fast you would see it.

## The knowledge base

2,398 pricing-related atoms across pillars, including Alex's $100M Playbook volumes on Pricing and Price Raise. At:

```
/Users/Zhong/Projects/AskAlex/knowledge/atoms/atoms.jsonl
```

Retrieve — never read it whole:

```bash
python3 /Users/Zhong/Projects/AskAlex/scripts/search_atoms.py "raise prices existing customers churn" --source book --top 6 --strong-only
```

| Flag | When |
|---|---|
| `--source book` | the two Pricing playbooks are the densest source — prefer it here |
| `--pillar C1` / `C2` | LTV and churn effects of a price change |
| `--pillar B2` | pricing inside the sales conversation |
| `--strong-only` | drop atoms with no clear topic — recommended |
| `--full` | no content truncation |

Search 2-4 times: one for the model ("three models of pricing"), one for the increase mechanics ("raise price in stages"), one for the second-order effect ("price value churn").

## Rules

- **Call him Alex, never "Hormozi".** First name only: "Alex's read on this would be…". The full name "Alex Hormozi" is for the skill description only.
- **Ground it in retrieved atoms.** If the search comes back empty, say so and work from the three models alone — do not invent an "Alex take" no atom supports.
- **Never write in first person as Alex.** Speak *about* the thinking.
- **Never quote him.** Every atom is a paraphrase. Attribute the *idea*, never a *sentence*.
- **Do not cite atom IDs, file paths, or pillar codes in the answer.** That is plumbing.
- **Numbers over adjectives.** "Move new customers to $129 and add a $49 annual renewal fee" beats "consider revisiting your pricing."
- **Do not recommend a discount as the first move.** It is the easiest lever and almost always the wrong one — it trains the buyer to wait. If discounting is genuinely the answer, justify it against the alternative.
- **Check churn before recommending a raise.** This is the one place where the default answer (raise) can do real damage.
