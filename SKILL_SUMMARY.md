# MarkItDown Pro — Skill Summary

## Overview

An enhanced MarkItDown skill with production-ready plugin development support. Built on Microsoft's MarkItDown tool with significant upgrades to the plugin ecosystem.

## What's New in Pro (vs. Standard)

### 1. Production-Ready Plugin Template

The upstream sample plugin uses `setup.py` and a flat layout. Pro upgrades to:
- `pyproject.toml` (PEP 621) — modern, declarative packaging
- `src/` layout — prevents accidental source imports
- Full type annotations + `py.typed` marker
- `importlib.metadata` for dynamic versioning
- `logging` instead of `print()`
- Specific exception handling

### 2. Plugin Template Generator

`scripts/plugin_template.py` scaffolds a new plugin in seconds:

```bash
python scripts/plugin_template.py my-format --extensions .foo .bar --author "Your Name"
```

Creates a complete project with `pyproject.toml`, `src/` layout, tests, and fixtures.

### 3. Plugin Development Guide

`references/plugin_development.md` covers:
- Architecture overview (entry_points mechanism)
- Step-by-step plugin creation
- DocumentConverter interface reference
- Best practices and anti-patterns
- Testing checklist
- Publishing workflow

### 4. Sample Plugin with Tests

`sample-plugin/` is a fully working example with:
- 14 pytest test cases
- Shared fixtures (`conftest.py`)
- Edge case coverage (empty files, binary content, CJK, large files)
- `accepts()` pattern for early filtering

### 5. All Standard Features Retained

- 15+ file format support
- AI-enhanced image descriptions via OpenRouter
- Azure Document Intelligence integration
- Batch processing scripts
- Scientific literature conversion
- YouTube transcript extraction

## Structure

```
markitdown-pro/
├── SKILL.md                              # Main documentation (Pro)
├── README.md                             # Overview
├── QUICK_REFERENCE.md                    # Cheat sheet
├── INSTALLATION_GUIDE.md                 # Installation
├── OPENROUTER_INTEGRATION.md             # OpenRouter setup
├── SKILL_SUMMARY.md                      # This file
├── LICENSE.txt                           # MIT License
├── references/
│   ├── api_reference.md                  # API docs
│   ├── file_formats.md                   # Format guides
│   └── plugin_development.md             # NEW: Plugin guide
├── scripts/
│   ├── batch_convert.py                  # Batch conversion
│   ├── convert_with_ai.py                # AI conversion
│   ├── convert_literature.py             # Literature conversion
│   └── plugin_template.py                # NEW: Plugin scaffold
├── assets/
│   └── example_usage.md                  # Examples
└── sample-plugin/                        # NEW: Sample plugin
    ├── pyproject.toml
    ├── README.md
    ├── src/markitdown_sample_plugin/
    │   ├── __init__.py
    │   ├── converter.py
    │   └── py.typed
    └── tests/
        ├── conftest.py
        ├── test_converter.py
        └── fixtures/sample.custom
```

## Quick Start

```bash
# Install MarkItDown
pip install 'markitdown[all]'

# Try the sample plugin
cd sample-plugin
pip install -e '.[dev]'
pytest

# Scaffold your own plugin
python scripts/plugin_template.py my-plugin --extensions .foo .bar
```

## Capabilities

- **15+ file formats**: PDF, DOCX, PPTX, XLSX, images, audio, HTML, CSV, JSON, XML, ZIP, EPUB, YouTube
- **AI enhancement**: Image descriptions via OpenRouter (100+ models)
- **Plugin ecosystem**: Modern, testable, type-safe plugins
- **Batch processing**: Parallel conversion with progress tracking
- **Scientific workflows**: Literature conversion with metadata extraction

## Status

**Status**: ✅ Complete and Ready to Use
