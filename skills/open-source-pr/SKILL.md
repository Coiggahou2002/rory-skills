---
name: open-source-pr
description: "Guide the full workflow of contributing a pull request to an open source project: from discovering a bug or improvement opportunity, through deduplication search, root cause investigation, fork/branch setup, implementation, testing, and PR submission with a well-structured title and body. Trigger this skill whenever the user wants to contribute to an open source project, fix a bug in someone else's repo, submit a PR to upstream, or says things like 'I found a bug in X, let me fix it', 'let's submit a PR', 'I want to contribute', 'help me open a PR', '提PR', '给这个项目修一下', '提个修复', '发现了一个bug想提PR'. Also trigger when the user is working in a forked repo and mentions sending changes upstream, or when they ask about open source contribution best practices."
---

# Open Source PR Contribution Workflow

This skill defines a structured, sequential workflow for contributing pull requests to open source projects. Each phase has a clear gate — do not skip ahead.

The workflow exists because open source maintainers are volunteers reviewing dozens of PRs. A PR that duplicates existing work, ignores contribution guidelines, or has a vague description wastes their time and gets closed. Following this process respects their time and maximizes the chance of getting merged.

## Phase 1: Deduplication — Search Before You Build

Before writing a single line of code, confirm that nobody has already reported or fixed the same issue.

**Actions:**
```bash
# Search issues (open AND closed) with multiple keyword angles
gh issue list -R <owner/repo> --state all --search "<keyword1>" --json number,title,state
gh issue list -R <owner/repo> --state all --search "<keyword2>" --json number,title,state

# Search PRs too — someone might have a fix in review or already merged
gh pr list -R <owner/repo> --state all --search "<keyword>" --json number,title,state
```

**Decision gate:**
- Found an open issue describing the same problem? **Link to it in your PR later, don't file a duplicate.**
- Found a closed issue with a merged fix? **Verify the fix actually works on current main.** If it regressed, your PR fixes the regression (reference the original issue).
- Found an open PR addressing the same thing? **Don't duplicate the work.** Consider reviewing or building on their PR instead.
- Nothing found? Proceed to Phase 2.

Search with at least 2-3 different keyword angles. Bugs are often described in terms of symptoms ("bar doesn't update") rather than causes ("cache restore"), so search both.

## Phase 2: Read the Rules — CONTRIBUTING.md and Project Conventions

Every serious open source project has contribution norms. Violating them gets your PR closed on sight.

**Actions:**
```bash
# Check for contribution docs
cat CONTRIBUTING.md 2>/dev/null
cat .github/CONTRIBUTING.md 2>/dev/null
cat .github/PULL_REQUEST_TEMPLATE.md 2>/dev/null

# Check for lint/format/build requirements
cat Makefile 2>/dev/null | head -30
cat package.json 2>/dev/null | grep -A5 '"scripts"'

# Look at recent merged PRs for style conventions
gh pr list -R <owner/repo> --state merged --limit 5 --json title,body
git log --oneline -10
```

**What to extract:**
- **Build/test commands** — `npm test`, `make check`, `cargo test`, etc.
- **File scope rules** — e.g. "don't commit dist/", "don't modify generated files"
- **Commit message format** — conventional commits (`fix(scope): message`), signed-off-by, etc.
- **PR process** — does the project require an issue first? A CLA signature? Specific labels?
- **Code style** — tabs vs spaces, line length, import order. Match the existing code, don't impose your style.

**Decision gate:** Internalize the rules before proceeding. If the project requires filing an issue before a PR, do that first.

## Phase 3: Investigate — Understand the Problem Before Touching Code

The most common junior mistake is jumping to code changes before understanding the system. Resist this.

### 3a. Map the data flow

For any bug, trace the data from source to symptom:

```
Input → Processing Step 1 → Processing Step 2 → ... → Output (where bug is visible)
```

Read the code along this path. At each step, ask: "What does this step receive? What does it produce? Where could it go wrong?"

### 3b. Form a hypothesis

After tracing the flow, you should be able to state: "The bug occurs because [specific mechanism], which causes [observable symptom]."

A good hypothesis is falsifiable — you can write a test or script that proves it right or wrong.

### 3c. Reproduce the bug

Write a minimal reproduction script **before** writing any fix:

```bash
# Create a standalone script that demonstrates the bug
# Run it and confirm the bug manifests
# This script becomes evidence in your PR
```

Why this matters:
- If your hypothesis is wrong, the repro script saves you from writing a useless fix
- The repro script becomes a "before/after" proof in your PR body
- It often becomes the basis for a regression test

### 3d. Investigate closed-source dependencies

When the bug involves a system you don't have source code for, you can still learn its behavior:

- **`strings <binary> | grep <keyword>`** — JS/TS binaries often contain readable string literals, JSON schemas, error messages, and even inline documentation
- **Observe inputs and outputs** — log or dump what goes in and what comes out
- **Read the transcript/log files** — many systems leave structured traces
- **Check public docs and schemas** — API docs, config file formats, changelog entries

You don't need source code to understand behavior. You need observable inputs and outputs.

**Decision gate:** You can explain the root cause in plain language, you have a repro script that demonstrates the bug, and you know which files need to change. Only then proceed to implementation.

## Phase 4: Fork, Branch, and Implement

### 4a. Set up your fork

```bash
# Fork if you haven't already
gh repo fork <owner/repo> --clone=false

# Add your fork as a remote
git remote add fork https://github.com/<your-username>/<repo>.git

# Create a descriptive branch from up-to-date main
git fetch origin
git checkout -b fix/short-description origin/main
```

Branch naming conventions (adapt to project norms):
- `fix/brief-description` — bug fixes
- `feat/brief-description` — new features
- `docs/brief-description` — documentation only

### 4b. Make minimal, focused changes

- **Change only what's necessary to fix the bug.** No drive-by refactors, no style cleanups, no "while I'm here" additions. Each unrelated change is a reason for the maintainer to delay review.
- **Follow the project's existing patterns.** If they use single quotes, you use single quotes. If they name tests a certain way, follow it.
- **Only modify the files the project expects you to modify.** If CONTRIBUTING.md says "don't touch dist/", don't commit dist/ even if your build generates it.

### 4c. Test thoroughly

```bash
# Run the project's full test suite — it must pass before you push
npm test  # or whatever the project uses

# Add tests for your fix: cover the bug case AND the original behavior
# - "the bug no longer occurs" (your fix works)
# - "the original behavior still works" (your fix doesn't break existing functionality)
```

The dual test pattern is critical: every bug fix needs both a **positive test** (the fix works) and a **negative test** (existing behavior is preserved). If you only test the fix, you might be introducing a regression.

### 4d. Verify with your repro script

Run the reproduction script from Phase 3 again. It should now show the fixed behavior. Include the before/after output in your PR body.

## Phase 5: Write the PR — Title and Body

The PR title and body are what the maintainer reads to decide whether your PR is worth reviewing. A vague title or wall-of-text body gets deprioritized.

### Title format

Follow the project's commit/PR convention. If they use conventional commits:

```
fix(scope): concise description of what changed

# Examples:
fix(context): skip cache restore after /compact so the bar updates
feat(auth): add JWT token refresh on 401 responses
docs(readme): fix broken installation link
```

Rules:
- **Under 70 characters** — it must fit in a single line in GitHub's PR list
- **Start with the type** — `fix`, `feat`, `docs`, `refactor`, `test`, `chore`
- **Describe the effect, not the mechanism** — "so the bar updates" is better than "by checking compact_boundary timestamp"
- **Use imperative mood** — "fix", "add", "remove", not "fixed", "added", "removed"

### Body structure

```markdown
## Summary

One paragraph: what's broken, why, and how this PR fixes it.

## Root cause

Explain the mechanism that causes the bug. Use observable field names,
file paths, and function names from the project — not internal/minified
identifiers from dependencies. Write so that someone who has never seen
the codebase can follow the logic. Include the data flow if relevant.

## Fix

What you changed and why each change is necessary. If the fix involves
a tradeoff or design choice, explain why you chose this approach over
alternatives.

## Test plan

- [ ] Existing test suite passes (N tests)
- [ ] New tests added for the fix
- [ ] New tests added for regression protection
- [ ] Manual verification / repro script results
```

### Body principles

- **Write for someone who hasn't been debugging this for 3 hours.** They need context.
- **Use the project's own vocabulary.** Reference field names, file paths, and function names from the project source — things a reviewer can `grep` for and verify.
- **Never reference minified/obfuscated identifiers** from closed-source dependencies. Describe the behavior you observed, not the internal symbol names.
- **Include reproduction evidence.** A "before/after" section with your repro script's output is the strongest argument that your fix works.
- **Link related issues.** "Fixes #123" or "Builds on the cache fallback introduced in #456" — this gives the maintainer the full history.

### Optional: collapsible details

For long reproduction scripts or verbose output, use GitHub's `<details>` tag:

```markdown
<details><summary>Reproduction script and output</summary>

\`\`\`js
// script here
\`\`\`

Before: `bar = 85%` (stuck)
After: `bar = 4%` (correct)

</details>
```

## Phase 6: Submit and Follow Up

```bash
# Push to your fork
git push -u fork <branch-name>

# Create the PR against upstream
gh pr create \
  --repo <owner/repo> \
  --base main \
  --head <your-username>:<branch-name> \
  --title "fix(scope): description" \
  --body "$(cat <<'EOF'
...your PR body...
EOF
)"
```

After submitting:
- **Respond to review comments promptly and constructively.** If the maintainer asks for changes, make them in new commits (don't force-push unless they ask you to squash).
- **Don't take rejection personally.** Maintainers may prefer a different approach, or the timing may be wrong. A closed PR with good analysis is still a contribution — the maintainer now understands the bug.
- **If CI fails, fix it before pinging for review.** A red CI is an automatic "not ready".

## Checklist

Use this as a pre-submit gate:

- [ ] Searched issues and PRs — no duplicates
- [ ] Read CONTRIBUTING.md — following all rules
- [ ] Root cause understood — can explain in plain language
- [ ] Reproduction script confirms the bug
- [ ] Fix is minimal — no unrelated changes
- [ ] Tests added — both positive (fix works) and negative (existing behavior preserved)
- [ ] Full test suite passes
- [ ] Repro script confirms the fix
- [ ] PR title follows project convention, under 70 chars
- [ ] PR body has Summary, Root cause, Fix, and Test plan sections
- [ ] No minified/obfuscated identifiers in the PR body
- [ ] Only modified files the project expects contributors to change
