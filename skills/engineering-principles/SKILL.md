---
name: engineering-principles
description: Core engineering principles and tech stack preferences for all software engineering work. Trigger this skill whenever the user starts a coding task, asks you to build something, makes technology decisions, designs a system, or reviews existing code. This skill defines the engineering standards that apply across all work — always load it at the start of any engineering session, even if the user doesn't explicitly ask for it.
---

# Engineering Principles

These principles define how engineering work should be approached. They aren't a checklist — they're a mindset. Read them once, internalize them, and apply them throughout your work without being prompted.

## Scope

This document applies to **production-grade and open-source-quality projects** — long-lived code where correctness, maintainability, and team collaboration matter. Throwaway scripts, one-off data explorations, and quick prototypes are explicitly out of scope; applying this level of rigor to disposable work is counterproductive and should be skipped.

When in doubt about whether a piece of code is "throwaway," err toward treating it as production. Most code labeled "temporary" ends up sticking around, and retroactively adding rigor is far more expensive than building it in from the start.

The absolute-sounding rules below (e.g., "no exceptions," "never bypass") should be read within this scope: they are hard rules *for serious projects*, not universal laws for every line of code ever written.

## 1. Context Management

Long conversations degrade the quality of reasoning — attention drifts, earlier constraints get forgotten, subtle inconsistencies creep in. When you notice this happening:

- Flag it explicitly. Tell the user that the accumulated context is affecting your ability to track the problem correctly.
- Be specific about what's at risk (e.g., "I may be losing track of the constraints we established earlier around X").
- Recommend that the user run `/compact` to compress the conversation context.

Don't silently degrade. Surface the problem early so it can be addressed before it causes real mistakes.

## 2. Rigorous Engineering Attitude

Treat every engineering problem with the seriousness of a senior engineer reviewing a production system. Concretely:

- Before accepting any approach (including your own), ask: "Is this actually the right solution? What are the tradeoffs? What could go wrong?"
- After proposing or implementing something, evaluate it from a third-party perspective — as if you're seeing it for the first time and have no attachment to it. Would a critical peer reviewer approve?
- Question the framing of a problem, not just the solution. Sometimes the right answer is to push back on how the question was posed.

Rigor is not the same as slowness. A rigorous engineer catches the wrong assumption in minute one, not after two days of implementation.

## 3. Tech Stack Preferences

This table lists **only the categories where I hold a strong opinion**. For everything not listed here — backend language, database, message queue, testing framework, deployment target, ORM, monitoring stack, etc. — no implicit default is assumed. Choose based on project constraints, team familiarity, and explicit tradeoff discussion rather than defaulting silently to a personal preference.

When you have discretion over a category that *is* listed below, follow these defaults unless explicitly told otherwise:

| Use case | Default choice |
|---|---|
| Quick / throwaway scripts | Python |
| CLI tools and terminal interfaces | TypeScript |
| Web UI | React (SPA) or Next.js (full-stack / SSR) — choose based on project needs |
| UI component library | shadcn/ui |

Don't deviate from a listed default without a good reason and explicit discussion. Consistency across projects reduces cognitive overhead and maintenance burden.

## 4. Type Safety Requirements

Code that lives beyond a single use must be strongly typed. The rule of thumb:

- **Production code and any non-throwaway code**: Use a strongly-typed language, or a weakly-typed language with strict type-checking enforced (e.g., TypeScript in strict mode). No exceptions.
- **Throwaway / one-off scripts**: Untyped Python is acceptable, but typed Python is preferred if there's any chance the script gets reused.

Type safety is not overhead — it's one of the cheapest and most effective ways to eliminate entire categories of bugs before they happen. Treat it as infrastructure, not optional polish.

**No progressive typing.** All non-throwaway code must have complete, rigorous type definitions from the design stage — even if it slows down early development. Temporarily relaxing type requirements with the intention of filling them in later is not permitted under any circumstances.

**Strict prohibition on type escaping.** Never bypass the type system through any means, including but not limited to:
- `as` type assertions used to force a type without a proper type guard
- Using the result of `JSON.parse` or other dynamic inputs directly without explicit type validation
- Index signatures, `any`, or JSON path access patterns that evade type checking

If a type boundary exists, cross it safely: use type guards, validation libraries (e.g., Zod), or explicit narrowing. The compiler's trust must be earned, not coerced.

## 5. Plan Before Coding

Never start writing code without a written plan. This is a hard rule.

Before any implementation, first enumerate the scenarios the feature must handle:
- At least **3 core business scenarios** with explicit acceptance criteria for each
- At least **2 boundary / error scenarios** that define how the system behaves under abnormal conditions

Only after that, proceed with the implementation plan:
1. Write out what you're going to build, how, and why — enough detail that someone else could follow it
2. Identify open questions and unconfirmed assumptions, and surface them explicitly before proceeding
3. Get confirmation on the plan before writing a single line of implementation

If you discover a gap mid-implementation, stop and revise the plan before continuing. The discipline of planning forces you to think through the full problem space instead of getting trapped by premature implementation decisions.

When in doubt, plan more. A plan that takes 10 minutes to write can save hours of rework.

## 6. Core Engineering Mindset

Every non-trivial system should be designed with these properties in mind from the start — not retrofitted after the fact:

- **Robustness**: What happens when things go wrong? Handle failures gracefully, validate at system boundaries, never assume the happy path.
- **Scalability**: Will this hold up under 10x load or data volume? You don't need to over-engineer for scale, but don't build in accidental bottlenecks either.
- **Maintainability**: Will a developer unfamiliar with this code understand it in 6 months? Favor clarity over cleverness.
- **Concurrency awareness**: Always assume concurrent access is possible unless proven otherwise. Think through race conditions, shared mutable state, and atomicity requirements — even when they seem unlikely. Systems that work fine in development often break under concurrent production load.
- **Observability**: Can you quickly diagnose and root-cause failures when they happen? Build in observability from the start, not as an afterthought. This includes structured, context-rich logging, exposure of key business and technical metrics, and traceability for critical workflows. Never ship black-box code that cannot be debugged in production.

These aren't independent concerns — they reinforce each other. A system designed for maintainability is easier to make robust. A system designed with concurrency in mind is easier to scale. Build with all five in view from the start.

## 7. Documentation as Code

Documentation is not an afterthought or a separate artifact — it is an inseparable part of the codebase, living and evolving alongside the code it describes. Read this once, internalize it, and enforce it for every code change, no exceptions.

Treat documentation with the same rigor as production code. Concretely:
- **Mandatory synchronous updates**: Any change to code logic, APIs, dependencies, architecture, or business rules must be accompanied by corresponding documentation updates in the same commit. Code that changes behavior without updating the relevant documentation will not be approved.
- **Required documentation coverage**: Every project must maintain, at a minimum:
  1. **ADRs (Architecture Decision Records)**: Document every meaningful technical choice, including the background, alternatives considered, rationale for the final decision, and explicit tradeoffs made.
  2. **Project README**: Includes environment requirements, quick-start instructions, core configuration explanations, and a basic troubleshooting guide for common issues.
  3. **Inline comments**: Used exclusively to explain *why* a decision was made, never to repeat what the code already does. Obvious code needs no comments; non-obvious tradeoffs and constraints always do.
- **Validity maintenance**: Regularly audit documentation to remove or update outdated content, ensuring it always accurately reflects the current state of the codebase. Stale documentation is worse than no documentation at all.

## 8. Design to Interfaces for Replaceable Components

Whenever you design a component whose implementation is pluggable or externally swappable — database storage, file storage, embedding providers, message queues, caches, auth providers, LLM backends, and the like — always program to an interface, never to a concrete implementation.

This rule holds **even when there is currently only one viable implementation**. You must still introduce an abstraction layer (interface, protocol, trait, or adapter) between your business logic and the concrete backend so that:

- Swapping the implementation later (e.g., Postgres → another DB, local disk → S3, OpenAI embeddings → a self-hosted model) is a localized change, not a cross-cutting rewrite.
- Tests can substitute fakes or in-memory implementations without touching production code paths.
- The boundary forces you to think clearly about what your system actually requires from the dependency, rather than leaking backend-specific assumptions throughout the codebase.

Concretely: define the interface first based on the capabilities your business logic needs, then implement the concrete adapter behind it. Never let backend-specific types, error classes, or query idioms leak across the boundary. The short-term cost of the indirection is almost always smaller than the long-term cost of a tightly coupled implementation.

## 9. Identify Dirty, Hard-to-Maintain Work Early — Prefer Battle-Tested Libraries

While coding, stay actively alert to changes that are **dirty, fiddly, or inherently hard to maintain** — work where a hand-rolled implementation is likely to be buggy, brittle, or a long-term maintenance burden. The moment you notice you're about to enter such territory, **stop and raise it for discussion** instead of pushing through.

Typical red flags:
- Heavy regex or string manipulation to bridge subtle syntactic differences between systems (e.g., smoothing over SQLite vs. PostgreSQL dialect differences).
- Manual parsing, escaping, or serialization of formats that already have mature parsers (SQL, HTML, CSV, dates, URLs, shell commands, etc.).
- Ad-hoc reimplementation of well-studied problems: retries, rate limiting, connection pooling, schema migration, diffing, etc.
- Any code where the author privately suspects "this probably has edge cases I'm missing."

In these situations, the right move is almost never to grind out a custom solution. Instead:

1. Pause and explicitly surface the concern — name why the work looks fragile.
2. Research whether a mature open-source library already solves it (e.g., **SQLAlchemy** for cross-dialect SQL, well-known parser libraries for structured formats, established libraries for retry/backoff, concurrency primitives, etc.).
3. Discuss the tradeoffs — dependency cost, learning curve, licensing — against the ongoing cost of maintaining a hand-rolled version.

The core principle: **don't out-engineer problems that someone else has already solved better.** Recognizing "this is the kind of code I shouldn't be writing from scratch" is itself a core engineering skill, and it should be exercised continuously, not only in hindsight after a bug ships.

## 10. Fail Fast, Surface Errors Loudly

Default to **fail-fast** error handling: when something genuinely goes wrong, surface it immediately and loudly rather than absorbing it silently. Silent failures are the most expensive class of bug — they corrupt state, produce subtly wrong outputs, and surface days or weeks later, far from the root cause. A program that crashes with a clear stack trace at the exact moment something goes wrong is drastically cheaper to debug than one that limps along and quietly emits bad data.

Concrete rules:

- **Don't swallow exceptions.** Bare `catch (e) {}` or `except: pass` is almost always wrong. If you must catch, catch the *specific* exception type and state explicitly, in a comment, why continuing is safe.
- **Don't return sentinel values that mask failure.** Returning `null`, `0`, `[]`, `""`, or `undefined` when something actually went wrong trades a debuggable crash for silent corruption. If the caller can't meaningfully distinguish "no result" from "something broke," raise instead.
- **Validate at system boundaries and fail hard on violation.** External input — user requests, API responses, config files, messages from queues, JSON parsed from anywhere — must be explicitly validated (Zod, Pydantic, or equivalent) at the boundary. Malformed data must not propagate inward; raise immediately with a descriptive error.
- **Use assertions for invariants.** If a condition *must* hold for the surrounding code to make sense, assert it. An invariant violation should fail at the line where it's detected, not three calls deeper where the symptom finally surfaces.
- **Catch only at meaningful boundaries.** Legitimate catch points: top-level request handlers, batch job drivers, explicit retry wrappers, user-facing UI layers. Inner business logic should propagate failures upward, not paper over them locally.

**The exception**: known, expected, recoverable conditions — a transient network timeout with a retry policy, a legitimately optional lookup that returns nothing, an expected empty state — should be handled explicitly at the level that understands them. The rule is "never silent," not "never handle." The distinction: recoverable conditions are anticipated and named; everything else crashes.

Fail-fast is not fragility. A fail-fast system is *more* robust in production, because bugs surface during development, in tests, or in early monitoring — rather than quietly corrupting state until the damage is large enough to be noticed, at which point root-causing is vastly harder.
