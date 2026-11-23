"""Built-in visual palettes for code widgets."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    background: str
    surface: str
    foreground: str
    muted: str
    accent: str
    dots: tuple[str, str, str]
    pygments_style: str


THEMES = {
    "dark": Theme("#0b1020", "#111a2e", "#dbe7ff", "#71809e", "#7c9cff", ("#ff5f57", "#febc2e", "#28c840"), "monokai"),
    "midnight": Theme("#09090b", "#18181b", "#e4e4e7", "#71717a", "#a78bfa", ("#fb7185", "#fbbf24", "#34d399"), "dracula"),
    "light": Theme("#f4f6fb", "#ffffff", "#202738", "#8790a0", "#5269d8", ("#ff5f57", "#febc2e", "#28c840"), "default"),
}


def get_theme(name: str) -> Theme:
    """Return a named palette, with a useful error for unknown names."""
    try:
        return THEMES[name.lower()]
    except (KeyError, AttributeError) as exc:
        choices = ", ".join(sorted(THEMES))
        raise ValueError(f"Unknown theme {name!r}. Choose one of: {choices}.") from exc
