# MarkItDown Sample Plugin (Pro)

A **production-ready** sample plugin for [MarkItDown](https://github.com/microsoft/markitdown) that demonstrates modern Python packaging best practices.

## Highlights vs. the upstream sample

| Aspect | Upstream sample | This (Pro) |
|--------|----------------|------------|
| Packaging | `setup.py` + flat layout | `pyproject.toml` + `src/` layout |
| Type hints | ❌ | ✅ Full annotations + `py.typed` |
| `accepts()` | ❌ | ✅ Early-return filter |
| Error handling | bare `except` | Specific exceptions + messages |
| Logging | `print()` | `logging` module |
| Tests | ❌ | ✅ pytest suite (14 tests) |
| CI | ❌ | ✅ GitHub Actions ready |
| Version | hardcoded | `importlib.metadata` dynamic |

## Quick start

```bash
# Install in editable mode
pip install -e '.[dev]'

# Run tests
pytest

# Type-check
mypy src/

# Lint
ruff check src/ tests/
```

## How it works

The plugin registers a `SamplePlugin` converter via the `markitdown.plugins` entry point. When MarkItDown encounters a `.custom` or `.sample` file, it delegates to this converter which:

1. Reads the raw bytes from the stream
2. Decodes (UTF-8 → latin-1 → replacement fallback)
3. Wraps the text in a fenced Markdown block
4. Extracts a title from the first non-empty line

## Project structure

```
sample-plugin/
├── pyproject.toml                          # PEP 621 metadata + tool config
├── README.md
├── src/
│   └── markitdown_sample_plugin/
│       ├── __init__.py                     # re-exports + __version__
│       ├── converter.py                    # SamplePlugin class
│       └── py.typed                        # PEP 561 marker
└── tests/
    ├── __init__.py
    ├── conftest.py                         # shared fixtures
    ├── test_converter.py                   # 14 test cases
    └── fixtures/
        └── sample.custom                   # test data
```
