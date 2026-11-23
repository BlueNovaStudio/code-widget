# CodeWidget

**Create polished, resolution-independent code visuals for video and design.** CodeWidget turns source files into SVG widgets with syntax highlighting, line numbers, and a ready-made editor frame. SVG stays sharp when resized in editors such as Premiere, DaVinci Resolve, CapCut, OBS, or a video-generation workflow.

## Install

```bash
pip install codewidget
```

For development from this repository:

```bash
python -m pip install -e .
```

## Python API

```python
from codewidget import CodeWidget

widget = CodeWidget(
    language="cpp",
    theme="midnight",
    title="main.cpp",
    font_size=20,
)
widget.set_code('''#include <iostream>
int main() {
    std::cout << "Hello, video!";
}''')
widget.render("output/code.svg")
```

You can also initialize with code and get the SVG string directly:

```python
widget = CodeWidget("print('Hello, video!')", language="python")
svg = widget.to_svg()
html = widget.to_html()
widget.render("code.html")
```

Themes included: `dark`, `midnight`, and `light`. Language names are Pygments lexer aliases, such as `python`, `javascript`, `typescript`, `cpp`, `rust`, `html`, and `bash`.

## Command line

```bash
codewidget example.py output/code.svg --language python --theme dark
```

The output directory is created when needed. The current release writes SVG and standalone HTML; raster and video export can be added as optional integrations later.

## Development

```bash
python -m pip install -e .
```

CodeWidget requires Python 3.11 or newer and uses Pygments for syntax highlighting. SVG rendering has no browser, Node.js, or video-library requirement.

## License

MIT. See [LICENSE](LICENSE).
