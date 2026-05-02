# Visual Board Benchmarks

Use this guide before writing Mermaid diagrams in `visuals/visual-spec.json`.

The visual board should look like a cohesive teaching canvas, not a random collection of generated diagrams.

## Mermaid Diagram Grammar

Before writing Mermaid code, decide the grammar:

| Grammar | Mermaid | Good for |
| --- | --- | --- |
| `flow` | `flowchart LR` or `flowchart TB` | ordered transformation, pipeline |
| `layer` | `flowchart TD` with sequential nodes | stacked abstraction or maturity levels |
| `comparison` | `flowchart LR` with `subgraph` blocks | two-sided contrast |
| `cycle` | `flowchart` with circular edges | feedback or iteration |
| `mindmap` | `mindmap` | concept dependencies around a center |
| `matrix` | `quadrantChart` | two-dimensional decision model |
| `network` | `graph` | nodes and relationships |
| `timeline` | `timeline` | chronological change |

If the chapter cannot be mapped to one grammar, rewrite the visual idea before drawing.

## Layout Rules

- Keep 6 or fewer primary nodes per diagram. Use subgraphs for grouping when more detail is needed.
- Keep node labels under 12 Chinese characters or 4 English words.
- Keep edge labels under 8 Chinese characters or 3 English words.
- For `comparison` visuals, use exactly two `subgraph` blocks to enforce the two-column contrast.
- For `cycle` visuals, connect the last node back to the first to close the loop.
- For `layer` visuals, use `flowchart TD` so the hierarchy reads top-to-bottom.
- Prefer `flowchart LR` (left-to-right) for process flows; use `flowchart TD` (top-down) only for hierarchies.

## Theming

All Mermaid diagrams share one config file (`templates/mermaid-config.json`) that enforces:

- Warm ivory node backgrounds (`#faf9f5`) instead of pure white
- Warm border colors (`#d9d6cc`)
- Ink-dark text (`#111827`)
- Muted edge colors (`#5e5d59`)
- Subtle cluster backgrounds (`#f5f4ed`)

Do not add `%%{init: ...}%%` theme overrides in individual Mermaid files. The config is applied globally by `mmdc`.

## Quality Constraints

- One diagram = one idea. If you need two ideas, use two diagrams (split the chapter visual).
- Vary the diagram grammar across chapters. Avoid using `flowchart LR` for every chapter.
- Use meaningful node IDs that describe the concept, not single letters.
- Avoid deeply nested subgraphs (max 2 levels).
- Avoid edges that create unreadable tangles; simplify the topology first.

## Board HTML Rules

The `visuals/index.html` page is a working board for inspection:

- Left sticky text rail for chapter navigation.
- Right workspace with one diagram per chapter.
- Show chapter label, title, summary, rendered diagram, and caption.
- No helper copy, placeholder text, or generator labels.

## Export Rules

The board is not finished until:

- Every SVG opens directly in a browser.
- Every PNG screenshot is at `2×` scale and readable at A4 page width.
- Labels do not clip or overlap.
- The HTML board is readable at desktop and mobile widths.
