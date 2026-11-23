"""Command-line entry point."""

import argparse
from pathlib import Path

from .widget import CodeWidget


def main() -> None:
    parser = argparse.ArgumentParser(description="Render source code as an SVG or HTML widget.")
    parser.add_argument("input", type=Path, help="Source code file")
    parser.add_argument("output", type=Path, help="Destination ending in .svg or .html")
    parser.add_argument("--language", "-l", default="python", help="Pygments language alias")
    parser.add_argument("--theme", default="dark", choices=("dark", "midnight", "light"))
    parser.add_argument("--title", help="Window title shown above the code")
    parser.add_argument("--no-line-numbers", action="store_true")
    parser.add_argument("--font-size", type=int, default=18)
    args = parser.parse_args()

    widget = CodeWidget(
        args.input.read_text(encoding="utf-8"),
        language=args.language,
        theme=args.theme,
        title=args.title or args.input.name,
        show_line_numbers=not args.no_line_numbers,
        font_size=args.font_size,
    )
    widget.render(args.output)
