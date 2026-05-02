# Export Workflow

Use markdown as the single editable source of truth. Generate DOCX and HTML from `tutorial.md`. Generate PDF via the Kami skill.

Read `references/editorial-production.md` before exporting. The export phase is not just format conversion; it is where the tutorial becomes a polished reading artifact.

## Folder Convention

Inside `outputs/tutorials/<topic-slug>/`:

```text
brief.json
research/source-register.md
research/evidence-map.md
outline.md
visuals/visual-spec.json
visuals/index.html
visuals/*.mmd
visuals/*.svg
assets/screenshots/*.png
tutorial.md
exports/
exports/tutorial-reference.docx
```

## Export: HTML And DOCX

Run from the tutorial output folder:

```bash
python3 /path/to/tutorial/scripts/export_tutorial.py tutorial.md exports/ --css /path/to/tutorial/templates/tutorial-style.css
```

This generates `exports/tutorial.html` and `exports/tutorial.docx`.

Optional title, basename, date, and reference document:

```bash
python3 /path/to/tutorial/scripts/export_tutorial.py tutorial.md exports/ --title "Beginner Guide To <Topic>" --basename tutorial --date "2026年5月2日" --css /path/to/tutorial/templates/tutorial-style.css
python3 /path/to/tutorial/scripts/export_tutorial.py tutorial.md exports/ --reference-doc custom-reference.docx --css /path/to/tutorial/templates/tutorial-style.css
```

## Export: PDF Via Kami

PDF output uses the Kami skill for professional typesetting. After generating the tutorial content, invoke the Kami skill to produce the final PDF:

1. Prepare the tutorial content: `tutorial.md` with all chapter visuals embedded as images.
2. Use the Kami skill's **long-doc** template to typeset the tutorial as a multi-chapter PDF document.
3. Pass the full tutorial text, chapter structure, and embedded images to Kami.
4. Kami will apply its design system: warm parchment background, TsangerJinKai02 Chinese serif headings, Newsreader English serif, ink-blue accent, and WeasyPrint PDF generation.
5. Save the output as `exports/tutorial.pdf`.

The Kami skill handles:

- `@page` rules for A4 sizing and margins
- `@font-face` embedding for Chinese and English fonts
- Warm parchment `#f5f4ed` page background
- Ink-blue `#1B365D` accent for headings and borders
- Clean PDF with no headers, footers, or browser artifacts
- High-resolution image embedding
- Table styling with warm borders and alternating row colors

## Dependencies

The HTML/DOCX export script uses:

- `pandoc` for DOCX and HTML conversion
- `python-docx` for generating the default Word reference document when available

PDF export requires the Kami skill to be available.

If the environment lacks these tools:

- still deliver `tutorial.md` and `visuals/index.html`
- report exactly which export target could not be produced

## Formatting Rules

- Keep headings short and hierarchical.
- Do not show internal source IDs in public text. Keep `[U1]`, `[X1]`, `[A2]`, `[P3]`, `[G4]`, and similar audit IDs inside `research/` files only.
- If references are useful to readers, use a human-readable `参考资料` or `延伸阅读` section with names and links, not bracket IDs.
- Public outputs should not say they are based on user notes, pasted source material, a supplied article, or the original text.
- When a source is a local file, use a human-readable label in final deliverables and keep absolute audit paths only in internal research notes.
- Keep image paths relative to `tutorial.md`.
- Use captions directly below images.
- Chapter headings must stay visible in all formats as `第1章 标题`; chapter subheadings must stay visible as `1.1 标题`, `1.2 标题`.
- In HTML, wrap tables in a scroll-safe table container so wide or dense tables stay readable.
- HTML must include a plain sticky `nav#TOC` anchor menu. The exporter wraps `nav#TOC` and the article in a centered `report-shell`.
- Put a compact document date directly below the visible H1 title.
- Do not create duplicate visible title blocks.
- PDF should read like a clean document with no sticky UI chrome.
- Word output must not include document headers or footers unless the user explicitly asks.
- DOCX should use a reference document for heading, body, table, and caption styles.

## Export Quality Gate

Run the package validator before final delivery:

```bash
python3 /path/to/tutorial/scripts/validate_package.py . --formats docx html pdf --check-deps
```

- DOCX opens and contains images.
- PDF opens and images are visible.
- PDF has no visible header, footer, local file URL, or browser page counter.
- DOCX has no header/footer parts or section header/footer references.
- HTML is standalone with correctly linked local assets.
- HTML has a sticky anchor-text table of contents.
- No chapter is missing its visual.
- No absolute local filesystem paths appear in final outputs.
- No public output contains bracket source markers or internal provenance wording.
