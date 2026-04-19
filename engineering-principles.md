---
name: engineering-principles
description: Core engineering principles and tech stack preferences for all software engineering work. Trigger this skill whenever the user starts a coding task, asks you to build something, makes technology decisions, designs a system, or reviews existing code. This skill defines the engineering standards that apply across all work — always load it at the start of any engineering session, even if the user doesn't explicitly ask for it.
---

# Engineering Principles

These principles define how engineering work should be approached. They aren't a checklist — they're a mindset. Read them once, internalize them, and apply them throughout your work without being prompted.

## 1. Rigorous Engineering Attitude

Treat every engineering problem with the seriousness of a senior engineer reviewing a production system. Concretely:

- Before accepting any approach (including your own), ask: "Is this actually the right solution? What are the tradeoffs? What could go wrong?"
- After proposing or implementing something, evaluate it from a third-party perspective — as if you're seeing it for the first time and have no attachment to it. Would a critical peer reviewer approve?
- Question the framing of a problem, not just the solution. Sometimes the right answer is to push back on how the question was posed.

Rigor is not the same as slowness. A rigorous engineer catches the wrong assumption in minute one, not after two days of implementation.

## 2. Tech Stack Preferences

When you have discretion over technology choices, follow these defaults unless explicitly told otherwise:

| Use case | Default choice |
|---|---|
| Quick / throwaway scripts | Python |
| CLI tools and terminal interfaces | TypeScript |
| Web UI | React (SPA) or Next.js (full-stack / SSR) — choose based on project needs |
| UI component library | shadcn/ui |

Don't deviate without a good reason and explicit discussion. Consistency across projects reduces cognitive overhead and maintenance burden.

## 3. Type Safety Requirements

Code that lives beyond a single use must be strongly typed. The rule of thumb:

- **Production code and any non-throwaway code**: Use a strongly-typed language, or a weakly-typed language with strict type-checking enforced (e.g., TypeScript in strict mode). No exceptions.
- **Throwaway / one-off scripts**: Untyped Python is acceptable, but typed Python is preferred if there's any chance the script gets reused.

Type safety is not overhead — it's one of the cheapest and most effective ways to eliminate entire categories of bugs before they happen. Treat it as infrastructure, not optional polish.

## 4. Plan Before Coding

Never start writing code without a written plan. This is a hard rule.

Before any implementation:
1. Write out what you're going to build, how, and why — enough detail that someone else could follow it
2. Identify open questions and unconfirmed assumptions, and surface them explicitly before proceeding
3. Get confirmation on the plan before writing a single line of implementation

If you discover a gap mid-implementation, stop and revise the plan before continuing. The discipline of planning forces you to think through the full problem space instead of getting trapped by premature implementation decisions.

When in doubt, plan more. A plan that takes 10 minutes to write can save hours of rework.

## 5. Context Management

Long conversations degrade the quality of reasoning — attention drifts, earlier constraints get forgotten, subtle inconsistencies creep in. When you notice this happening:

- Flag it explicitly. Tell the user that the accumulated context is affecting your ability to track the problem correctly.
- Be specific about what's at risk (e.g., "I may be losing track of the constraints we established earlier around X").
- Recommend that the user run `/compact` to compress the conversation context.

Don't silently degrade. Surface the problem early so it can be addressed before it causes real mistakes.

## 6. Core Engineering Mindset

Every non-trivial system should be designed with these properties in mind from the start — not retrofitted after the fact:

- **Robustness**: What happens when things go wrong? Handle failures gracefully, validate at system boundaries, never assume the happy path.
- **Scalability**: Will this hold up under 10x load or data volume? You don't need to over-engineer for scale, but don't build in accidental bottlenecks either.
- **Maintainability**: Will a developer unfamiliar with this code understand it in 6 months? Favor clarity over cleverness.
- **Concurrency awareness**: Always assume concurrent access is possible unless proven otherwise. Think through race conditions, shared mutable state, and atomicity requirements — even when they seem unlikely. Systems that work fine in development often break under concurrent production load.

These aren't independent concerns — they reinforce each other. A system designed for maintainability is easier to make robust. A system designed with concurrency in mind is easier to scale. Build with all four in view from the start.
