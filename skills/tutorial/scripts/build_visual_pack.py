#!/usr/bin/env python3
"""Build a visual pack from Mermaid diagrams defined in a visual spec."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from html import escape
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = SKILL_ROOT / "templates" / "mermaid-config.json"


def esc(value: Any) -> str:
    return escape(str(value), quote=True)


def slugify(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")


def chapter_label(module_id: str) -> str:
    match = re.search(r"(?:module|chapter)-0*([0-9]+)$", module_id, re.IGNORECASE)
    if not match:
        return module_id.upper() if module_id else "章节"
    return f"第{int(match.group(1))}章"


def require_mmdc() -> str:
    path = shutil.which("mmdc")
    if not path:
        raise SystemExit(
            "Missing mmdc (Mermaid CLI). Install with: npm install -g @mermaid-js/mermaid-cli"
        )
    return path


def compile_mermaid(mmdc: str, mmd_file: Path, output_file: Path, config: Path | None = None) -> None:
    cmd = [mmdc, "-i", str(mmd_file), "-o", str(output_file), "-b", "transparent"]
    if config and config.exists():
        cmd.extend(["-c", str(config)])
    subprocess.run(cmd, check=True)


def build_index(title: str, modules: list[dict[str, str]]) -> str:
    nav_items = []
    sections = []
    for module in modules:
        nav_items.append(
            f'<a href="#{esc(module["id"])}"><span>{esc(chapter_label(module["id"]))}</span>{esc(module["title"])}</a>'
        )
        sections.append(
            f'''<section class="chapter" id="{esc(module["id"])}">
  <p class="summary">{esc(module["summary"])}</p>
  <figure class="artboard">
    <img src="{esc(module["file"])}" alt="{esc(chapter_label(module["id"]))}：{esc(module["title"])}">
  </figure>
  <p class="caption">{esc(module["caption"])}</p>
</section>'''
        )
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <style>
    :root {{
      --ink: #111827;
      --muted: #5e5d59;
      --accent: #1b365d;
      --border: #d9d6cc;
      --surface: #f5f4ed;
      --paper: #faf9f5;
      --canvas: #f2f0ea;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      background: var(--canvas);
      color: var(--ink);
      font-family: "Noto Sans SC", "Source Han Sans SC", "PingFang SC", system-ui, sans-serif;
    }}
    .shell {{
      display: grid;
      grid-template-columns: minmax(260px, 330px) minmax(0, 1fr);
      gap: clamp(24px, 4vw, 56px);
      max-width: 1440px;
      margin: 0 auto;
      padding: clamp(24px, 4vw, 56px);
    }}
    .rail {{
      position: sticky;
      top: 32px;
      align-self: start;
      padding-right: 20px;
      border-right: 1px solid var(--border);
    }}
    .rail h1 {{
      margin: 0;
      padding-bottom: 18px;
      border-bottom: 2px solid var(--accent);
      font-size: clamp(1.45rem, 2.3vw, 2.35rem);
      line-height: 1.12;
    }}
    .rail nav {{
      display: grid;
      gap: 10px;
      margin-top: 24px;
    }}
    .rail a {{
      color: var(--muted);
      text-decoration: none;
      font-size: 0.94rem;
      line-height: 1.35;
    }}
    .rail a:hover {{ color: var(--ink); }}
    .rail span {{
      display: block;
      margin-bottom: 3px;
      color: var(--accent);
      font-family: monospace;
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
    }}
    .workspace {{
      display: grid;
      gap: clamp(34px, 5vw, 72px);
    }}
    .chapter {{ scroll-margin-top: 32px; }}
    .summary {{
      margin: 0 0 12px;
      color: var(--muted);
      font-size: 0.92rem;
      line-height: 1.5;
    }}
    .artboard {{
      margin: 0;
      border: 1px solid var(--border);
      border-radius: 10px;
      background: var(--paper);
      overflow: hidden;
      padding: 24px;
    }}
    img {{
      display: block;
      width: 100%;
      height: auto;
    }}
    .caption {{
      margin: 12px auto 0;
      max-width: 820px;
      color: var(--muted);
      text-align: center;
      font-size: 0.95rem;
    }}
    @media (max-width: 860px) {{
      .shell {{ display: block; padding: 20px; }}
      .rail {{
        position: sticky; top: 0; z-index: 2;
        margin: -20px -20px 28px;
        padding: 18px 20px 16px;
        border-right: 0;
        border-bottom: 1px solid var(--border);
        background: var(--canvas);
      }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <aside class="rail">
      <h1>{esc(title)}</h1>
      <nav>
        {"".join(nav_items)}
      </nav>
    </aside>
    <main class="workspace">
      {"".join(sections)}
    </main>
  </div>
</body>
</html>
'''


def demo_spec() -> dict[str, Any]:
    return {
        "title": "Demo Tutorial Visual Pack",
        "chapters": [
            {
                "id": "chapter-01",
                "title": "From Confusion To Model",
                "diagram_type": "flow",
                "summary": "A beginner path from raw topic to first useful example.",
                "mermaid": 'flowchart LR\n  A["Raw topic"] --> B["Key question"]\n  B --> C["Mental model"]\n  C --> D["First example"]',
                "caption": "A useful tutorial turns confusion into a small successful action.",
            },
            {
                "id": "chapter-02",
                "title": "The Learning Stack",
                "diagram_type": "layer",
                "summary": "A topic can be taught as stacked levels of understanding.",
                "mermaid": 'flowchart TD\n  A["Goal"] --> B["Workflow"]\n  B --> C["Concepts"]\n  C --> D["Tools"]\n  D --> E["Tradeoffs"]',
                "caption": "The learner needs to know where each new idea belongs.",
            },
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build tutorial chapter visuals from Mermaid diagrams."
    )
    parser.add_argument("spec", nargs="?", help="Path to visual-spec.json.")
    parser.add_argument("output_dir", nargs="?", help="Directory for outputs.")
    parser.add_argument("--demo", action="store_true", help="Generate a demo pack.")
    parser.add_argument(
        "--config", default=None,
        help="Path to mermaid config JSON. Defaults to templates/mermaid-config.json.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.demo:
        spec = demo_spec()
        output_dir = Path(args.output_dir or args.spec or "visuals-demo").resolve()
    else:
        if not args.spec or not args.output_dir:
            raise SystemExit("Usage: build_visual_pack.py visual-spec.json output_dir/ or --demo [output_dir/]")
        spec_path = Path(args.spec).resolve()
        if not spec_path.exists():
            raise SystemExit(f"Spec file not found: {spec_path}")
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        output_dir = Path(args.output_dir).resolve()

    output_dir.mkdir(parents=True, exist_ok=True)
    config = Path(args.config) if args.config else DEFAULT_CONFIG
    mmdc = require_mmdc()

    raw_modules = spec.get("chapters") or spec.get("modules") or []
    if not raw_modules:
        raise SystemExit("No chapters found in visual spec.")

    index_modules: list[dict[str, str]] = []
    used_ids: set[str] = set()

    for number, module in enumerate(raw_modules, start=1):
        module = dict(module)
        raw_id = str(module.get("id") or "")
        module_id = slugify(raw_id) or f"chapter-{number:02d}"
        if module_id in used_ids:
            module_id = f"{module_id}-{number:02d}"
        used_ids.add(module_id)

        mermaid_code = str(module.get("mermaid") or "")
        if not mermaid_code:
            print(f"WARNING: {module_id} has no mermaid code, skipping")
            continue

        mmd_file = output_dir / f"{module_id}.mmd"
        svg_file = output_dir / f"{module_id}.svg"

        mmd_file.write_text(mermaid_code, encoding="utf-8")
        compile_mermaid(mmdc, mmd_file, svg_file, config)

        title = str(module.get("title") or module_id.replace("-", " ").title())
        index_modules.append({
            "id": module_id,
            "title": title,
            "summary": str(module.get("summary") or ""),
            "caption": str(module.get("caption") or ""),
            "file": f"{module_id}.svg",
        })

    index_html = build_index(str(spec.get("title", "Tutorial Visual Pack")), index_modules)
    (output_dir / "index.html").write_text(index_html, encoding="utf-8")

    print(f"Visual pack written to {output_dir}")
    for module in index_modules:
        print(f"  - {module['file']}")


if __name__ == "__main__":
    main()
