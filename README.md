# MarkItDown Pro Skill

Enhanced file-to-Markdown conversion skill with production-ready plugin development support.

## What's New in Pro

| Feature | Standard | Pro |
|---------|----------|-----|
| Plugin template | `setup.py` + flat layout | `pyproject.toml` + `src/` layout |
| Type hints | ❌ | ✅ Full annotations + `py.typed` |
| Plugin scaffolding | Manual | `plugin_template.py` generator |
| Plugin development guide | ❌ | ✅ `references/plugin_development.md` |
| Sample plugin tests | ❌ | ✅ 14 pytest cases |
| `accepts()` pattern | ❌ | ✅ Early-return filter |
| Error handling | bare `except` | Specific exceptions |
| Logging | `print()` | `logging` module |
| Version management | hardcoded | `importlib.metadata` |

## Contents

### Main Skill File
- **SKILL.md** — Complete guide with Pro enhancements

### References
- **api_reference.md** — Detailed API documentation
- **file_formats.md** — Format-specific guides
- **plugin_development.md** — **NEW** — Full plugin development guide

### Scripts
- **batch_convert.py** — Parallel batch conversion
- **convert_with_ai.py** — AI-enhanced conversion via OpenRouter
- **convert_literature.py** — Scientific literature conversion
- **plugin_template.py** — **NEW** — Scaffold new plugins

### Sample Plugin
- **sample-plugin/** — **NEW** — Production-ready example with `src/` layout and tests

### Assets
- **example_usage.md** — Practical examples

## Quick Start

```bash
# Install MarkItDown
pip install 'markitdown[all]'

# Scaffold a new plugin
python scripts/plugin_template.py my-format --extensions .foo .bar

# Or use the sample plugin
cd sample-plugin
pip install -e '.[dev]'
pytest
```

## Plugin Development

```bash
# Generate plugin scaffold
python scripts/plugin_template.py geojson --extensions .geojson --author "Your Name"

# Created structure:
# geojson/
# ├── pyproject.toml
# ├── src/geojson/
# │   ├── __init__.py
# │   ├── converter.py
# │   └── py.typed
# └── tests/
#     ├── conftest.py
#     └── test_converter.py

# Install and test
cd geojson
pip install -e '.[dev]'
pytest
mypy src/
```

