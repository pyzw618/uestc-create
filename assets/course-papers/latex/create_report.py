#!/usr/bin/env python
"""Create a UESTC course report template from bundled skill assets."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def template_root() -> Path:
    return skill_root() / "assets" / "template"


def iter_template_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*") if path.is_file())


def relative_template_files(root: Path) -> list[Path]:
    return [path.relative_to(root) for path in iter_template_files(root)]


def find_conflicts(src_root: Path, dst_root: Path) -> list[Path]:
    conflicts: list[Path] = []
    for rel_path in relative_template_files(src_root):
        dst_path = dst_root / rel_path
        if dst_path.exists():
            conflicts.append(rel_path)
            continue
        parent = dst_path.parent
        while parent != dst_root.parent:
            if parent.exists() and not parent.is_dir():
                conflicts.append(rel_path)
                break
            if parent == dst_root:
                break
            parent = parent.parent
    return conflicts


def copy_template(src_root: Path, dst_root: Path, force: bool) -> None:
    if not src_root.is_dir():
        raise FileNotFoundError(f"Template assets not found: {src_root}")

    dst_root.mkdir(parents=True, exist_ok=True)

    conflicts = find_conflicts(src_root, dst_root)
    if conflicts and not force:
        print("Refusing to overwrite existing files:", file=sys.stderr)
        for rel_path in conflicts:
            print(f"  {rel_path}", file=sys.stderr)
        print("Use --force to overwrite these files.", file=sys.stderr)
        raise SystemExit(2)

    for src_path in iter_template_files(src_root):
        rel_path = src_path.relative_to(src_root)
        dst_path = dst_root / rel_path
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dst_path)


def compile_report(dst_root: Path) -> int:
    if shutil.which("latexmk") is None:
        print("latexmk was not found on PATH. Install TeX Live/MiKTeX or run with --no-compile.", file=sys.stderr)
        return 127

    command = ["latexmk", "-xelatex", "main.tex"]
    print(f"Running: {' '.join(command)}")
    completed = subprocess.run(command, cwd=dst_root)
    if completed.returncode != 0:
        print("Compilation failed. Check main.log in the output directory.", file=sys.stderr)
    elif not (dst_root / "main.pdf").is_file():
        print("Compilation finished but main.pdf was not created.", file=sys.stderr)
        return 1
    else:
        print(f"Created PDF: {dst_root / 'main.pdf'}")
    return completed.returncode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create and optionally compile a UESTC course report template.")
    parser.add_argument(
        "--output",
        default=".",
        help="Target directory. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing template files in the target directory.",
    )
    parser.add_argument(
        "--no-compile",
        action="store_true",
        help="Copy the template but do not run latexmk.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    src_root = template_root()
    dst_root = Path(args.output).expanduser().resolve()

    copy_template(src_root, dst_root, args.force)
    print(f"Template copied to: {dst_root}")

    if args.no_compile:
        return 0
    return compile_report(dst_root)


if __name__ == "__main__":
    raise SystemExit(main())
