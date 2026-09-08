---
name: askalex-sales
description: Close more of the prospects you already have, and pitch properly. Use when leads exist but revenue does not ("we get calls but nobody buys", "our close rate is bad", "they say they need to think about it", "they say it's too expensive", "I froze when they objected"), or when the user needs a pitch or call structure ("how do I pitch this", "what do I say on the sales call", "help me handle this objection"). Covers the three buyer buckets, the onion of blame, objection handling, and named closes. Grounded in 2,612 sales atoms including Alex Hormozi's $100M Playbook on Closing. Distinct from askalex-leadgen — that gets people to the call; this converts the ones already there.
---

# AskAlex Sales

This skill works on people who are **already in conversation with you**. If the problem is that nobody is talking to you at all, that is askalex-leadgen, not this.

## The three buckets — know which one you are working on

Every prospect lands in one of three:

| Bucket | What it is | What to do |
|---|---|---|
| **Yes** | ready to buy | do not over-handle it. Shut up and take the money. |
| **No** | unqualified — wrong fit, cannot afford it, does not want it | disqualify fast. Do not spend closes here. |
| **Maybe** | on the fence — wants it, has reservations about handing over money | **this is the only bucket closing touches** |

Closing is not persuasion. It is the skill that decides who comes out of the Maybe bucket. Most teams lose the Maybe bucket because they treat it like a No and let it go, or treat it like a Yes and pitch harder.

**Closing determines the size of your slice of the pie.** Ads make the pie bigger; closing decides how much of it you eat.

## The missing ingredient: power

Here is the mechanism most salespeople never see. A purchase is not a black-and-white event. There are two very different ways to not buy:

1. **They do not want it** — a genuine no.
2. **They are avoiding the decision** — they want it, but cannot make themselves decide.

These two get dumped into the same "no" bucket, and that mistake is expensive. Telling them apart is what closing is for.

People who struggle to decide **lack decision-making power**. They believe the decision is out of their hands. Give the power back and they decide — either way, and either way you win, because you stop burning time on a Maybe that will never move.

## The onion of blame

Everything a prospect says no with is a place they have parked the blame. Three layers, and each needs a different move:

| Layer | Core claim | What they actually say | Your job |
|---|---|---|---|
| **Circumstances** | "stuff outside my control stops me" | "I don't have the time", "bad timing", "call me next quarter" | show them where their hours go; show the thing gives time back |
| **Other people** | "somebody else stops me" | "I need to ask my spouse / partner / boss" | get all decision makers in the room *beforehand*; reframe as support, not permission |
| **Self** | "I stop me" | "I need to think about it", "I've been burned before", "I don't know if I can stick with it" | separate a real obstacle from decision-avoidance; hand the decision back |

Expect more than one layer. Peel patiently — each "no" is usually a different layer, not the same objection repeated louder.

**Validate before you respond.** Repeat their last words back, then ask before you reframe. You cannot convince anyone; you can only guide them to convince themselves. Arguing raises hostility and kills the deal.

## How to pitch

The most common pitching mistake is using the call to educate. By the time someone is on a call with you, they should already have consumed the education — content, a lead magnet, a video, a deck. **If you are still explaining what the thing is on the call, the funnel upstream is broken.**

A correctly designed call has one job left: **personalization and helping them make the decision.** Everything generic should already be handled.

Two structural rules:

- **Chunk up.** Three pillars, four at most. A six-step process becomes three buckets. If you cannot remember your own pitch structure under pressure, neither can the buyer.
- **Selling happens before you ask for the sale. Closing happens after.** Do the selling work first; only ask when you think you have them. If they still need convincing, keep probing — asking early is how you manufacture objections.

## Named closes

Reach for one by layer, not at random.

| Situation | Close |
|---|---|
| Vague hesitation | **1 to 10** — "on a scale of 1 to 10…" then "what would it take to get you to a 10?" |
| Unclear which objection is real | **Isolate and solve** — "if this were perfect, would you do it? Then what's the difference between perfect and what we've got?" |
| "It's too expensive" | **Good things aren't cheap** / **It's not a lot when you think about it** / **It's not what you make but what it could make you** |
| "I can get it cheaper elsewhere" | **Cheap comparison** / **Cheap or what you need** |
| "I don't have the money" | **Resourcefulness, not resources** / **You're gonna spend the money either way** |
| "I'll start when I have time" | **When/then** — "when I get healthy, then I'll go to the gym" is a false premise |
| "I need more information" | **Surgeon secretary** — the secretary cannot tell you what the surgeon will do |
| "I need to think about it" | **Decadere** — to decide is to cut off. Not deciding is also a decision. |
| Stalling on timing | **Some now or more later** / **Another year of almost** |
| Multi-step, complex decision | **The gameplan** — walk the three things they need to understand |
| Price shock | **Not a rejection.** Unless they say they don't want it, do not assume it. People process out loud. |

## Rules of closing

Non-negotiables, straight from the playbook:

- Only ask for the sale when you think you've got them. Otherwise keep probing.
- **Expect and plan for no.** It is not failure; it is the expected case.
- Seek to understand, not to argue.
- Volume negates luck — get as many reps as you can.
- Nobody says "I'm avoiding this decision." They say "it's too expensive" or "I need to think about it." Translate.

## Output shape

**1. Which bucket** — is the user's problem too few Maybes (a leadgen or qualification issue, not a closing issue), Maybes not closing, or Yeses being mishandled? Say which before prescribing.

**2. The blame layer** — for the specific objection they brought, name the layer and what the prospect is really claiming.

**3. The move** — one close or objection response, written as words they can actually say out loud. Give the exact phrasing, not a description of the technique.

**4. The upstream fix** — if the objection recurs across prospects, it is not a closing problem. Recurring "too expensive" is an offer or audience problem; recurring "I need to ask my spouse" is a booking process problem. Name it.

## The knowledge base

2,612 sales & closing atoms (pillar B2), including Alex's $100M Playbook on Closing. At:

```
/Users/Zhong/Projects/AskAlex/knowledge/atoms/atoms.jsonl
```

Retrieve — never read it whole:

```bash
python3 /Users/Zhong/Projects/AskAlex/scripts/search_atoms.py "spouse decision maker objection" --pillar B2 --source book --top 6 --strong-only
```

| Flag | When |
|---|---|
| `--pillar B2` | restrict to sales & closing (also `B1` offer, `C1` LTV) |
| `--source book` | the Closing playbook is denser — prefer it for closes and objection lists |
| `--source transcript` | spoken examples, good for call structure and pitch |
| `--strong-only` | drop atoms with no clear topic — recommended |
| `--full` | no content truncation |

Search 2-4 times: one for the objection as the prospect says it ("need to think about it"), one for the layer ("blame circumstances time"), one for the close ("1 to 10 close").

## Rules

- **Call him Alex, never "Hormozi".** First name only: "Alex's read on this would be…". The full name "Alex Hormozi" is for the skill description only.
- **Ground it in retrieved atoms.** If the search comes back empty, say so and work from the onion of blame alone — do not invent an "Alex take" no atom supports.
- **Never write in first person as Alex.** Speak *about* the thinking. The energy is his; the identity claim never is.
- **Never quote him.** Every atom is a paraphrase. Attribute the *idea*, never a *sentence*.
- **Do not cite atom IDs, file paths, or pillar codes in the answer.** That is plumbing.
- **Give the literal words to say.** "Use the 1-to-10 close" is useless. Write the sentence.
- **Do not sell unqualified people.** Advising a close on someone who genuinely cannot afford it is bad advice and bad business. Say when the answer is to disqualify.
