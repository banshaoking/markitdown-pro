# Plugin Development Guide (Pro)

This guide covers how to write, test, and publish MarkItDown plugins using modern Python best practices.

---

## Architecture

MarkItDown uses Python's `entry_points` mechanism to discover plugins at runtime.

```
┌─────────────────────────────────────────────────┐
│  MarkItDown (enable_plugins=True)               │
│                                                 │
│  1. Scan installed packages for                 │
│     entry_points group "markitdown.plugins"     │
│  2. Load each converter class                   │
│  3. On convert(): iterate converters,           │
│     call accepts(ext) → first True wins         │
│  4. Call convert(stream, ext) on winner         │
└─────────────────────────────────────────────────┘
```

### Entry Point Group

```toml
# pyproject.toml
[project.entry-points."markitdown.plugins"]
my_plugin = "my_package:MyConverter"
```

The key must be `"markitdown.plugins"` (plural). The value is a `module:Class` reference.

---

## Step-by-Step: Creating a Plugin

### 1. Scaffold with the template generator

```bash
python scripts/plugin_template.py my-format --extensions .foo .bar --author "Your Name"
cd my-format
```

### 2. Implement the converter

Edit `src/my_format/converter.py`:

```python
from __future__ import annotations
import logging
from typing import BinaryIO
from markitdown import DocumentConverter, DocumentConverterResult

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS: frozenset[str] = frozenset({".foo", ".bar"})


class MyFormatConverter(DocumentConverter):
    """Converts .foo / .bar files to Markdown."""

    def accepts(self, file_extension: str) -> bool:
        return file_extension.lower() in SUPPORTED_EXTENSIONS

    def convert(self, stream: BinaryIO, file_extension: str) -> DocumentConverterResult:
        ext = file_extension.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported extension: {ext}")

        raw = stream.read()
        text = raw.decode("utf-8", errors="replace")

        # Your conversion logic here
        markdown = f"```{ext.lstrip('.')}\n{text}\n```"

        return DocumentConverterResult(
            text_content=markdown,
            title=text.splitlines()[0][:120] if text.strip() else None,
        )
```

### 3. Write tests

```python
import io
import pytest
from my_format import MyFormatConverter

@pytest.fixture()
def converter():
    return MyFormatConverter()

def test_accepts(converter):
    assert converter.accepts(".foo") is True
    assert converter.accepts(".pdf") is False

def test_convert(converter):
    stream = io.BytesIO(b"Hello, world!")
    result = converter.convert(stream, ".foo")
    assert "Hello, world!" in result.text_content
```

### 4. Install and test locally

```bash
pip install -e '.[dev]'
pytest
mypy src/
```

### 5. Verify in MarkItDown

```python
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=True)
result = md.convert("test.foo")
print(result.text_content)
```

---

## The DocumentConverter Interface

### Required Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `convert()` | `(stream: BinaryIO, file_extension: str) -> DocumentConverterResult` | Main conversion logic |

### Optional Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `accepts()` | `(file_extension: str) -> bool` | Early filter — return True if you handle this extension |

### Why `accepts()` matters

Without `accepts()`, MarkItDown calls `convert()` on every converter until one succeeds. This means:
- Unnecessary I/O (reading streams that will fail)
- Confusing error messages
- Slower startup

With `accepts()`, converters self-report their capabilities and MarkItDown skips non-matching ones entirely.

---

## Best Practices

### ✅ Do

- **Use `src/` layout** — prevents accidental imports of the source directory
- **Add type hints** — enables IDE autocomplete and catches bugs early
- **Add `py.typed`** — signals to mypy that your package supports typing
- **Use `logging`** — not `print()`. Users can control log levels
- **Use `frozenset` for extensions** — immutable, fast lookup
- **Handle encoding gracefully** — `utf-8` → `latin-1` → `errors="replace"`
- **Return early in `accepts()`** — avoid unnecessary work
- **Write tests** — at minimum: `accepts()`, `convert()`, edge cases
- **Use `pyproject.toml`** — PEP 621 standard, replaces `setup.py`

### ❌ Don't

- **Don't use `setup.py`** — deprecated for new projects
- **Don't use flat layout** — `src/` prevents import shadowing
- **Don't use `print()`** — use `logging` instead
- **Don't catch bare `Exception`** — catch specific exceptions
- **Don't hardcode version** — use `importlib.metadata`
- **Don't skip `accepts()`** — it's optional but strongly recommended
- **Don't read the entire stream into memory for huge files** — consider chunked processing

---

## File Structure Reference

```
my-markitdown-plugin/
├── pyproject.toml                          # PEP 621 metadata + tool config
├── README.md                               # User-facing docs
├── LICENSE                                 # MIT / Apache-2.0 / etc.
├── src/
│   └── my_package/
│       ├── __init__.py                     # Re-exports + __version__
│       ├── converter.py                    # DocumentConverter subclass
│       ├── py.typed                        # PEP 561 marker (empty file)
│       └── _helpers.py                     # Optional: internal utilities
└── tests/
    ├── __init__.py
    ├── conftest.py                         # Shared fixtures
    ├── test_converter.py                   # Unit tests
    ├── test_integration.py                 # End-to-end with MarkItDown
    └── fixtures/
        ├── sample.foo                      # Test data
        └── sample.bar
```

---

## pyproject.toml Template

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "markitdown-my-format"
version = "0.1.0"
description = "MarkItDown plugin for .foo files"
requires-python = ">=3.10"
license = "MIT"
dependencies = ["markitdown>=0.1.0"]

[project.optional-dependencies]
dev = ["pytest>=8.0", "pytest-cov>=5.0", "mypy>=1.10", "ruff>=0.5"]

[project.entry-points."markitdown.plugins"]
my_format = "my_package:MyFormatConverter"

[tool.hatch.build.targets.wheel]
packages = ["src/my_package"]
```

---

## Testing Checklist

- [ ] `accepts()` returns `True` for all supported extensions (case-insensitive)
- [ ] `accepts()` returns `False` for unsupported extensions
- [ ] `convert()` produces valid Markdown from normal input
- [ ] `convert()` handles empty files gracefully
- [ ] `convert()` handles non-UTF-8 bytes without crashing
- [ ] `convert()` raises `ValueError` for unsupported extensions
- [ ] `convert()` extracts a reasonable title (or returns `None`)
- [ ] Large files (1 MB+) convert without memory issues
- [ ] CJK / emoji / multibyte characters survive round-trip
- [ ] Integration test: works with `MarkItDown(enable_plugins=True)`

---

## Publishing

1. **Bump version** in `pyproject.toml`
2. **Run tests**: `pytest --cov`
3. **Type-check**: `mypy src/`
4. **Lint**: `ruff check src/ tests/`
5. **Build**: `python -m build`
6. **Upload**: `twine upload dist/*`
7. **Tag**: `git tag v0.1.0 && git push --tags`

Users install with:
```bash
pip install markitdown-my-format
markitdown --use-plugins file.foo
```
