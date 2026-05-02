#!/usr/bin/env python3
"""Capture Mermaid diagrams as high-resolution PNG files using mmdc."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = SKILL_ROOT / "templates" / "mermaid-config.json"


def require_mmdc() -> str:
    path = shutil.which("mmdc")
    if not path:
        raise SystemExit(
            "Missing mmdc (Mermaid CLI). Install with: npm install -g @mermaid-js/mermaid-cli"
        )
    return path


def capture_mmd(mmdc: str, mmd_file: Path, png_file: Path, scale: float, width: int, config: Path | None) -> None:
    cmd = [
        mmdc,
        "-i", str(mmd_file),
        "-o", str(png_file),
        "-s", str(scale),
        "-b", "transparent",
    ]
    if width > 0:
        cmd.extend(["-w", str(width)])
    if config and config.exists():
        cmd.extend(["-c", str(config)])
    subprocess.run(cmd, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture Mermaid diagrams to PNG files.")
    parser.add_argument("visuals_dir", help="Directory containing .mmd files.")
    parser.add_argument("output_dir", help="Directory for PNG screenshots.")
    parser.add_argument("--scale", type=float, default=2.0, help="Scale factor for crisp output.")
    parser.add_argument("--width", type=int, default=1600, help="Output width in pixels.")
    parser.add_argument(
        "--config", default=None,
        help="Path to mermaid config JSON. Defaults to templates/mermaid-config.json.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    visuals_dir = Path(args.visuals_dir).resolve()
    if not visuals_dir.exists():
        raise SystemExit(f"Visuals directory not found: {visuals_dir}")

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    mmd_files = sorted(visuals_dir.glob("*.mmd"))
    if not mmd_files:
        raise SystemExit(f"No .mmd files found in: {visuals_dir}")

    mmdc = require_mmdc()
    config = Path(args.config) if args.config else DEFAULT_CONFIG

    for mmd_file in mmd_files:
        png_file = output_dir / f"{mmd_file.stem}.png"
        capture_mmd(mmdc, mmd_file, png_file, args.scale, args.width, config)
        print(f"  - {png_file}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print(f"Command failed with exit code {exc.returncode}: {exc.cmd}")
        raise SystemExit(exc.returncode)
