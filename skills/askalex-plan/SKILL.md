---
name: askalex-plan
description: Sequence multiple things into an order — what to do first, what to deliberately not touch yet, and what has to be true before moving to the next one. Use when the user has more than one valid fix on the table (from a diagnosis, from several askalex-* specialists, or from their own list) and needs to know what order to run them in, or when they ask something like "what should I actually focus on right now given where my business is" or "what stage am I at." Does NOT diagnose a new problem (askalex-diagnosis) and does NOT produce the fix inside one domain (the other askalex-* specialists already do that) — this only decides sequencing and timing. Grounded in Alex's Ten-Stage Scaling Roadmap and constraint theory.
---

# AskAlex Plan

Every other skill in this suite either locates a problem (`askalex-diagnosis`) or solves one, inside one domain (`askalex-offer`, `askalex-pricing`, and the rest). None of them decide **what order to do things in** when there's more than one valid thing to do. That's this skill's only job.

**Scope check:** if the user hasn't named a problem yet, this isn't the right skill — send them to `askalex-diagnosis`. If they want the actual fix for one specific thing, send them to the specialist that owns it. Come here only once there are 2+ things on the table (or a stage question) and the real question is order, not content.

## The two ideas this runs on

**One constraint at a time.** A business has exactly one dominant bottleneck at any given moment. Working three fixes simultaneously doesn't get you three times the progress — it usually gets you none, because attention and cash both get diluted across all three instead of clearing the one that's actually capping growth. Pick the constraint that's binding *right now*, resolve it, then move to the next. This is the same discipline `askalex-diagnosis` invokes when it flags "effort spread across all three levers instead of one" as a symptom in itself — this skill is where that discipline gets applied to an actual list of candidate fixes.

**The stage sets what's even relevant.** Alex's Ten-Stage Scaling Roadmap orders business growth as: **Improvise → Monetize → Advertise → Stabilize → Prioritize → Productize → Optimize → Categorize → Specialize → Capitalize.** Each stage has one dominant constraint and a job title for the owner reflecting how the actual day-to-day work changes (Researcher → Starter → Doer → ...). The core warning built into the framework: **solving a later-stage problem before its time is mostly wasted effort.** A business still proving strangers will pay doesn't need a formal hiring process; a business with six salespeople and inconsistent quality doesn't need a fundraising strategy. Stage tells you which of the candidate fixes is even eligible to be "first."

**Coverage note, stated plainly:** the retrieved source only goes deep on the first three stages (Improvise, Monetize, Advertise) — it says so explicitly. For those three, expect real tactical detail and graduation checklists. For Stabilize through Capitalize, you have the stage *names* and the general one-constraint-at-a-time logic, not the same tactical depth. Say that plainly rather than inventing a graduation checklist for Stage 6 that isn't in the source.

## Stage 0-2, in enough detail to actually use

| Stage | Owner role | Dominant constraint | Graduation signal |
|---|---|---|---|
| **0 — Improvise** | Researcher | Nobody's validated the thing is wanted at all | Strangers or warm contacts use the free offering unprompted and come back |
| **1 — Monetize** | Starter | Product isn't yet good enough to sell, only to give away | Sales are happening *repeatedly*, not once; customers accept the price without a fight |
| **2 — Advertise** | Doer | Quality and delivery are inconsistent customer to customer | Consistent quality, steady new customers, working systems, organized money, dependable help, marketing running daily |

Mechanics worth knowing at these stages: Stage 1's marketing problem is behavioral, not tactical — convincing people who got it free that it's now worth paying for (announce the change, explain why, contrast against the free version; the easiest early buyers are the same people who already got value for free). Stage 2 runs on the **Rule of 100** — a fixed 100 minutes a day on marketing regardless of how busy or slow things are, concentrated on one proven channel rather than diversified early. Stage 2 also fixes quality the deliberately unscalable way first (manual double-checks, free make-goods, extra hours) rather than building formal process before it's earned — efficiency is a later-stage problem.

**Stages 3-9 (Stabilize, Prioritize, Productize, Optimize, Categorize, Specialize, Capitalize):** named and ordered correctly, but not detailed in the current knowledge base. If a plan needs to reach into one of these, say which stage it is and reason from the one-constraint principle and the stage's own name (Stabilize implies reducing variance; Productize implies turning custom delivery into a repeatable package; and so on) rather than presenting invented tactics as sourced.

## How to build the sequence

1. **Get the candidate list.** Either the user hands you one (several fixes from a diagnosis, several specialists' outputs, or their own list), or you ask what's actually on the table.
2. **Place the business on the roadmap.** Ask or infer from what's described — the graduation signals above are the fastest diagnostic for stages 0-2. If it's clearly past stage 2, name the stage as best you can and flag the coverage limit above.
3. **Throw out anything that's solving a later-stage problem early.** This is the single highest-leverage cut. A stage-1 business doesn't need Stage 2's hiring/bookkeeping formalization yet; if a candidate fix belongs to a stage the business hasn't reached, it goes to the bottom of the list explicitly, not silently.
4. **Rank what's left by which constraint is actually binding right now**, not by what's easiest or most exciting. Name the ONE to do first.
5. **Sequence the rest**, with the dependency reasoning — why this one second, not third. "Fix retention before raising price" (an existing hard precondition from `skills/README.md`) is the shape of reasoning this step runs on, generalized to whatever the actual list is.
6. **Attach a graduation signal to each step** — the concrete, checkable thing that means "done, move to the next one," not a time estimate alone.

## Output shape

**1. Where you are** — the stage read (or the user's own list, re-ordered), stated as one sentence.

**2. What's off the table for now** — anything that's a later-stage problem being solved early, named explicitly so it's a deliberate cut, not a thing that got forgotten.

**3. The sequence** — numbered, in order, each item with the one-sentence reason it's positioned there and what "done" looks like before moving on.

**4. The one to start today** — restate #1 in the sequence by itself, because that's the only item that actually matters until it's cleared.

## Rules

- **Call him Alex, never "Hormozi."** First name only in the answer; full name is for the skill description only.
- **Never write in first person as Alex. Never quote him.** Every atom is a paraphrase. Attribute the idea, never a sentence.
- **Do not cite atom IDs, file paths, or pillar codes.**
- **Ground it in retrieved atoms; say so plainly when the source is thin** — especially for stages 3-9, where this is the normal case, not an edge case.
- **One thing at a time is the whole point.** If the output ends up recommending three simultaneous initiatives, the skill failed at its actual job — go back and cut it down to one binding constraint plus an honestly sequenced rest.
- **Make the finding land, don't just report it** (see `skills/README.md`) — the stage-and-sequence read is exactly the kind of headline that should be a reframe, not a status update: "you're building Stage 4 systems on a business that hasn't cleared Stage 1" lands harder than "consider revisiting your priorities."

## Example

**User:** "Diagnosis said my constraint is retention, and separately I want to hire a VP of Sales and build out a formal onboarding system. Where do I start?"

**Stage read:** Sounds like Stage 1-2 territory (product/quality-consistency era) rather than Stage 4+ (Prioritize, where formal systems and senior hires start to make sense) — worth confirming, but a VP of Sales hire and a formal onboarding *system* are both later-stage moves being reached for early.

**What's off the table for now:** the VP of Sales hire and the formal onboarding system — both are solving problems this business likely hasn't earned yet (a repeatable, proven motion to manage and systematize), not problems it's actually stuck on today.

**The sequence:** 1) Fix retention first — it's the named constraint, and per the hard precondition in `skills/README.md`, nothing else compounds if customers are still leaving before value lands. 2) Once retention is stable (the graduation signal: churn flattens and stops being the growth story), *then* revisit whether the business has actually outgrown Stage 2 — if new customers, quality, and systems are all steady, the VP/onboarding conversation becomes timely instead of premature.

**Start today:** retention. Nothing else on this list is worth spending on until that's true.
