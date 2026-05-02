# Visual HTML Workflow

Every chapter needs one visual artifact. Use visuals to make structure visible, not to decorate.

Read `references/visual-board-benchmarks.md` before choosing the diagram style.

## Visual Types And Mermaid Mapping

Choose the simplest visual that explains the chapter. Write all visuals in Mermaid syntax.

| Skill type | Mermaid syntax | When to use |
| --- | --- | --- |
| `flow` | `flowchart LR` | process, sequence, pipeline, lifecycle |
| `layer` | `flowchart TD` | stack, architecture, abstraction levels |
| `comparison` | `flowchart LR` with two `subgraph` blocks | before/after, option A vs option B |
| `cycle` | `flowchart` with circular edges | feedback loop, iteration, reinforcement |
| `mindmap` | `mindmap` | concept map, vocabulary map, dependency map |
| `matrix` | `quadrantChart` | tradeoff grid, decision map, 2×2 model |
| `network` | `graph` | nodes and relationships |
| `timeline` | `timeline` | chronological change |

If a chapter genuinely cannot be expressed in Mermaid, create a bespoke SVG. This should be rare.

## Visual Spec

Create `visuals/visual-spec.json` before generating graphics. Use `templates/visual-spec-template.json` as a starting point.

Each chapter entry should include:

- `id`: stable ID such as `chapter-01`
- `title`
- `diagram_type`: one of the 8 types above
- `summary`: what this visual teaches
- `mermaid`: the full Mermaid source code for this diagram
- `caption`
- optional `layout_note`: internal note explaining the grammar choice; not rendered

### Writing Mermaid Code

- Keep node labels short: under 12 Chinese characters or 4 English words.
- Keep 6 or fewer primary nodes per diagram. If more are needed, use subgraphs to group.
- Use descriptive node IDs: `A["Raw topic"]` not just `A`.
- For `comparison` diagrams, use two `subgraph` blocks side by side.
- For `cycle` diagrams, connect the last node back to the first.
- For `layer` diagrams, use `flowchart TD` (top-down) to show hierarchy.
- Avoid complex styling directives in Mermaid source; theming is handled by the config file.

## Generate The Visual Pack

From the tutorial output folder, run:

```bash
python3 /path/to/tutorial/scripts/build_visual_pack.py visuals/visual-spec.json visuals/
```

This creates:

- one `.mmd` file per chapter
- one SVG file per chapter (compiled via `mmdc`)
- `visuals/index.html` (board for inspection)

The build script uses `templates/mermaid-config.json` for consistent theming. If `mmdc` is not installed, install it with `npm install -g @mermaid-js/mermaid-cli`.

## Screenshot And Embedding

Capture each visual as a high-resolution PNG for embedding in the tutorial:

```bash
python3 /path/to/tutorial/scripts/capture_visuals.py visuals/ assets/screenshots/
```

This uses `mmdc` to render each `.mmd` file to PNG at 2× scale.

Embed the screenshot in `tutorial.md`:

```markdown
![第1章：Chapter title](assets/screenshots/chapter-01.png)
```

Fallback: if `mmdc` PNG output fails, embed the SVG path directly and keep `visuals/index.html` as the visual deliverable.

## Visual Quality Gate

- Each visual explains one idea.
- The diagram has 6 or fewer primary nodes.
- Labels fit inside shapes and are readable.
- The caption tells the learner what to notice.
- The visual can stand alone in PDF and Word exports.
- The visual is referenced in the chapter text.
- PNG screenshots are generated at `2×` scale.
- Repeated visual types are intentional; avoid using the same flowchart layout for every chapter.
