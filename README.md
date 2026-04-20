# rory-skills

A collection of custom [Claude Code skills](https://docs.anthropic.com/en/docs/claude-code/skills) I've created for my own use. Feel free to use or adapt them.

## Skills

Install individual skills using [`npx skills`](https://github.com/vercel-labs/skills):

| Skill | Install | Description |
|---|---|---|
| [engineering-principles](./skills/engineering-principles/SKILL.md) | `npx skills add Coiggahou2002/rory-skills -s engineering-principles` | Core engineering principles and tech stack preferences: rigorous attitude, type safety, plan-first discipline, concurrency awareness, and default tooling choices (TypeScript, shadcn/ui, etc.). |
| [daily-report-email](./skills/daily-report-email/SKILL.md) | `npx skills add Coiggahou2002/rory-skills -s daily-report-email` | Draft send-ready daily/weekly status report emails (To/Cc/Bcc/Subject/Body) from a dump of what you did, structured as Done / Key Decisions / Blockers / Next. |
| [release-pipeline-patterns](./skills/release-pipeline-patterns/SKILL.md) | `npx skills add Coiggahou2002/rory-skills -s release-pipeline-patterns` | Design and debug GitHub Actions release pipelines for open-source npm packages: label-driven version bumps, concurrency safety, npm publish + provenance, binary builds, CHANGELOG automation, alpha previews, merge queue. |

Add `-g` to install globally, or `-a claude-code` to target a specific agent.
