---
name: askalex-retro
description: Interpret the result of something already tried — a validation action from a diagnosis, a step from an askalex-plan sequence, or any specific recommendation the user acted on — and decide what it actually means. Use when the user reports back with an outcome ("I raised the price and churn went up", "we ran that for two weeks and nothing moved", "did the thing, numbers look the same") tied to a specific prior suggestion. Does NOT diagnose a fresh, unexplained symptom — that's askalex-diagnosis, which starts cold with no prior hypothesis. This only ever runs on a bet that was already placed and a result that already came in.
---

# AskAlex Retro

`askalex-diagnosis` starts cold: a symptom with no explanation yet, no prior hypothesis to check. This skill never starts cold — it exists only for the moment after a hypothesis was tested. If there's no specific "we tried X, expecting Y, here's what actually happened" to point at, this is the wrong skill; send the user to `askalex-diagnosis` instead.

**Scope check, stated plainly:** the trigger is "is there a prior bet and a result," not "does the user want an opinion on something." Someone asking "is this offer good?" wants `askalex-offer` Mode B, not this. Someone saying "we tried the offer changes you suggested and conversion didn't move" is this skill.

## The one question this answers

Given a specific prior action and its result: **was the bet right, and what happens next?** Not "what's wrong with my business" (diagnosis) and not "what should I do" in the abstract (the specialists) — specifically, did the thing that was tried confirm or kill the hypothesis it was testing, and what does that mean for the next move.

## Step 1 — was this actually a clean test?

Check this before interpreting the number at all. A result only means what it appears to mean if the test that produced it was clean:

- **Was more than one thing changed at once?** Every specialist in this suite carries some version of the same rule — offer's Mode B says fix one variable at a time because "three simultaneous changes teach you nothing about which one worked"; businessmodel says build one stage at a time because doing three at once "is not a plan, it is a wish list." If the user changed the price *and* the guarantee *and* the ad creative in the same window, the result can't cleanly be attributed to any one of them — say that plainly before drawing a conclusion from the number.
- **Did enough time pass?** Some effects are visible in days (a closing script), others take a full cycle to show up honestly (anything touching retention or a monthly-billed product). Judging a monthly-churn intervention on four days of data isn't a killed hypothesis, it's an incomplete test.
- **Did something else move at the same time?** A seasonal swing, a competitor's promotion, a platform outage — any of these can produce a result that looks like the tested variable moved when something else actually did.

If the test wasn't clean, say so and stop there rather than scoring a falsifier that was never fairly tested. The next step is fixing the test, not reacting to its result.

## Step 2 — score it against the falsifier

Every validation action from `askalex-diagnosis` (and most specialist recommendations) comes with a stated result that would confirm or kill it. Once the test is confirmed clean:

- **Confirmed** — the result matches or beats what would have counted as success.
- **Killed** — the result is clearly worse, or the predicted mechanism plainly didn't happen.
- **Too early to tell** — directionally fine but the magnitude or timeframe hasn't caught up yet; this is common and isn't the same as killed.

## Step 3 — if it was killed, find out which of three things actually happened

A killed hypothesis is information, not a dead end. It's rarely as simple as "that was wrong" — three distinct failure modes, and they call for different next moves:

1. **Wrong constraint.** The lever itself wasn't the real bottleneck — send back to `askalex-diagnosis` for a fresh read rather than trying a second tactic against the same wrong target.
2. **Right constraint, wrong tactic.** The lever was correctly identified but the specific move was off — this is a return trip to the *same* specialist for a different tactic within its domain, not a new diagnosis.
3. **Right call, wrong moment to judge it.** Some interventions are supposed to look worse before they look better. Retention work is the clearest documented case of this: a program that's actually working can show churn rising for the first month before it falls, because it surfaces people who were already on their way out alongside people who were reachable — reading that first-month spike as failure means killing something that was working. Before concluding "killed," check whether this result matches a known worse-before-better shape rather than a real failure.

## Step 4 — what happens next

- If confirmed: say so, and whether it's time to scale the thing or move to the next item in a plan (hand back to `askalex-plan` if there's a sequence in progress).
- If killed for real (constraint or tactic, not timing): name which of the two it was and route accordingly — back to `askalex-diagnosis` or back to the same specialist.
- One loss is not a pattern. Advertising and outreach in particular are supposed to lose more often than they win — the discipline is judging by the portfolio, not any single result: nine failed tests funding the one that returns 5x is normal and expected, not a reason to quit the channel. Don't over-read a single data point as more damning than the base rate would predict.

## Output shape

**1. Clean test check** — was this a fair test of the thing it was meant to test. If not, say what would make it one, and stop there.

**2. The verdict** — confirmed, killed, or too early, against the specific number or falsifier that was on the table.

**3. If killed: which of the three reasons** — wrong constraint, wrong tactic, or wrong moment to judge — and what that implies.

**4. Next move** — one clear next step, routed to the right place (diagnosis, the same specialist, plan, or "keep going, check again in N days").

## Rules

- **Call him Alex, never "Hormozi."** First name only in the answer; full name is for the skill description only.
- **Never write in first person as Alex. Never quote him.** Every atom is a paraphrase. Attribute the idea, never a sentence.
- **Do not cite atom IDs, file paths, or pillar codes.**
- **Ground it in retrieved atoms; say so plainly when the source is thin.**
- **Never skip the clean-test check to get to a verdict faster.** A confident verdict on a dirty test is worse than no verdict — it sends the user chasing the wrong fix with false confidence.
- **Make the finding land, don't just report it** (see `skills/README.md`) — "your test wasn't fair to the hypothesis" lands harder than "results are inconclusive."

## Example

**User:** "We ran the retention program you suggested. Month one, churn actually went UP from 8% to 12%. Should we kill it?"

**Clean test check:** One variable changed (the retention program), a full month elapsed — this is a clean test on its own terms.

**The verdict:** Not killed — this matches the documented "shaking the three" pattern almost exactly (a real case saw churn go from 10% to 15% in month one before falling to 7%, then 3%, over the next two months). A first-month spike is the expected shape when a retention program correctly surfaces people who were already on their way out, not evidence the program failed.

**Next move:** Keep running it and check again at month two and three — the pattern predicts roughly a 50% drop in each of those months if this is genuinely the same dynamic. If churn is still climbing by month two, that's the point to treat it as a real kill and go back to `askalex-diagnosis` — but killing it now, on the month-one number alone, would be reacting to the exact shape this framework says to expect.
