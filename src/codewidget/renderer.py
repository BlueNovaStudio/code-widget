"""SVG rendering helpers."""

from __future__ import annotations

from html import escape
from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name
from pygments.token import Token

from .themes import Theme


def _token_style(style, token):
    token_style = style.style_for_token(token)
    color = f"#{token_style['color']}" if token_style.get("color") else None
    return color, token_style.get("bold", False), token_style.get("italic", False)


def _lines_with_spans(code: str, language: str, pygments_style: str):
    lexer = get_lexer_by_name(language, stripnl=False, ensurenl=False)
    style = get_style_by_name(pygments_style)
    lines: list[list[tuple[str, str | None, bool, bool]]] = [[]]
    for token, value in lex(code, lexer):
        color, bold, italic = _token_style(style, token)
        pieces = value.expandtabs(4).split("\n")
        for index, piece in enumerate(pieces):
            if piece:
                lines[-1].append((piece, color, bold, italic))
            if index < len(pieces) - 1:
                lines.append([])
    if code.endswith("\n") and len(lines) > 1 and not lines[-1]:
        lines.pop()
    return lines


def render_svg(
    code: str,
    language: str,
    theme: Theme,
    *,
    title: str,
    show_line_numbers: bool,
    font_size: int,
    padding: int,
    line_height: int,
    radius: int,
) -> str:
    lines = _lines_with_spans(code, language, theme.pygments_style)
    columns = max((sum(len(part[0]) for part in line) for line in lines), default=0)
    char_width = font_size * 0.62
    number_width = (len(str(len(lines))) + 1) * char_width if show_line_numbers else 0
    gutter = 16 if show_line_numbers else 0
    header_height = max(48, font_size * 2.7)
    code_width = max(columns, 1) * char_width
    title_width = 68 + len(title or language) * font_size * 0.45
    width = int(padding * 2 + number_width + gutter + max(code_width, title_width))
    height = int(header_height + padding * 2 + max(len(lines), 1) * line_height)
    code_x = padding + number_width + gutter
    header_title = escape(title or language, quote=True)
    chunks = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{header_title} code widget">',
        '<style>text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace}</style>',
        f'<rect width="{width}" height="{height}" rx="{radius}" fill="{theme.background}"/>',
        f'<path d="M0 {header_height}H{width}" stroke="{theme.surface}" stroke-width="1"/>',
    ]
    for index, color in enumerate(theme.dots):
        chunks.append(f'<circle cx="{padding + index * 19 + 6}" cy="{header_height / 2}" r="5" fill="{color}"/>')
    chunks.append(f'<text x="{padding + 68}" y="{header_height / 2 + font_size * 0.35}" font-size="{font_size * 0.78}" fill="{theme.muted}">{header_title}</text>')

    for line_index, spans in enumerate(lines):
        baseline = header_height + padding + font_size + line_index * line_height
        if show_line_numbers:
            chunks.append(f'<text x="{padding + number_width - char_width}" y="{baseline}" text-anchor="end" font-size="{font_size}" fill="{theme.muted}">{line_index + 1}</text>')
        chunks.append(f'<text x="{code_x}" y="{baseline}" font-size="{font_size}" xml:space="preserve">')
        offset = 0
        for value, color, bold, italic in spans:
            attrs = [f'x="{code_x + offset * char_width:.2f}"', f'fill="{color or theme.foreground}"']
            if bold:
                attrs.append('font-weight="700"')
            if italic:
                attrs.append('font-style="italic"')
            chunks.append(f'<tspan {" ".join(attrs)}>{escape(value)}</tspan>')
            offset += len(value)
        chunks.append('</text>')
    chunks.append('</svg>')
    return "\n".join(chunks)


def render_html(svg: str, title: str) -> str:
    safe_title = escape(title or "Code widget", quote=True)
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{safe_title}</title>
  <style>html,body{{margin:0;min-height:100%;background:#09090b}}body{{display:grid;place-items:center;padding:4vw}}svg{{max-width:100%;height:auto;box-shadow:0 24px 80px #0008}}</style>
</head>
<body>{svg}</body>
</html>
'''
