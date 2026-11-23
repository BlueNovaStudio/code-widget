"""Public CodeWidget API."""

from pathlib import Path

from .renderer import render_html, render_svg
from .themes import get_theme


class CodeWidget:
    """Turn source code into a styled, resolution-independent visual.

    Example::

        widget = CodeWidget(code="print('hello')", language="python")
        widget.render("hello.svg")
    """

    def __init__(
        self,
        code: str = "",
        *,
        language: str = "python",
        theme: str = "dark",
        title: str | None = None,
        show_line_numbers: bool = True,
        font_size: int = 18,
        padding: int = 28,
        line_height: int | None = None,
        radius: int = 14,
    ) -> None:
        if font_size < 8:
            raise ValueError("font_size must be at least 8 pixels")
        if padding < 0 or radius < 0:
            raise ValueError("padding and radius cannot be negative")
        self.code = code
        self.language = language
        self.theme = theme
        self.title = title or language
        self.show_line_numbers = show_line_numbers
        self.font_size = font_size
        self.padding = padding
        self.line_height = line_height or int(font_size * 1.65)
        self.radius = radius

    def set_code(self, code: str) -> "CodeWidget":
        """Replace the source and return this widget for convenient chaining."""
        self.code = code
        return self

    def to_svg(self) -> str:
        """Return the widget as an SVG document string."""
        return render_svg(
            self.code,
            self.language,
            get_theme(self.theme),
            title=self.title,
            show_line_numbers=self.show_line_numbers,
            font_size=self.font_size,
            padding=self.padding,
            line_height=self.line_height,
            radius=self.radius,
        )

    def to_html(self) -> str:
        """Return a standalone HTML page containing the SVG widget."""
        return render_html(self.to_svg(), self.title)

    def render(self, path: str | Path) -> Path:
        """Write an SVG or HTML file and return its path."""
        destination = Path(path)
        suffix = destination.suffix.lower()
        if suffix == ".svg":
            content = self.to_svg()
        elif suffix in {".html", ".htm"}:
            content = self.to_html()
        else:
            raise ValueError("Output must use the .svg, .html, or .htm extension")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
        return destination
