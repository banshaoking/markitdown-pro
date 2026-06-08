---
name: markitdown-pro
description: "MarkItDown Pro — enhanced file-to-Markdown conversion with production-ready plugin development, src/ layout, type hints, test scaffolding, and modern Python packaging."
allowed-tools: [Read, Write, Edit, Bash]
license: MIT
source: https://github.com/microsoft/markitdown
version: 0.2.0
---

# MarkItDown Pro — File to Markdown Conversion

## Overview

MarkItDown Pro is an enhanced skill built on top of Microsoft's MarkItDown tool. It adds:

- **Production-ready plugin template** with `src/` layout, type hints, and tests
- **Plugin development guide** with best practices and anti-patterns
- **Plugin template generator** script for bootstrapping new plugins
- **Modern Python packaging** (`pyproject.toml` + hatchling)
- **15+ file format support** inherited from MarkItDown core

**Key Benefits**:
- Convert documents to clean, structured Markdown
- Token-efficient format for LLM processing
- Extensible plugin system with proper scaffolding
- AI-enhanced image descriptions via OpenRouter
- OCR for images and scanned documents
- Speech transcription for audio files

---

## Supported Formats

| Format | Description | Notes |
|--------|-------------|-------|
| **PDF** | Portable Document Format | Full text extraction |
| **DOCX** | Microsoft Word | Tables, formatting preserved |
| **PPTX** | PowerPoint | Slides with notes |
| **XLSX** | Excel spreadsheets | Tables and data |
| **Images** | JPEG, PNG, GIF, WebP | EXIF metadata + OCR |
| **Audio** | WAV, MP3 | Metadata + transcription |
| **HTML** | Web pages | Clean conversion |
| **CSV** | Comma-separated values | Table format |
| **JSON** | JSON data | Structured representation |
| **XML** | XML documents | Structured format |
| **ZIP** | Archive files | Iterates contents |
| **EPUB** | E-books | Full text extraction |
| **YouTube** | Video URLs | Fetch transcriptions |

---

## Quick Start

### Installation

```bash
# Install with all features
pip install 'markitdown[all]'

# Or from source
git clone https://github.com/microsoft/markitdown.git
cd markitdown
pip install -e 'packages/markitdown[all]'
```

### Command-Line Usage

```bash
# Basic conversion
markitdown document.pdf > output.md

# Specify output file
markitdown document.pdf -o output.md

# Pipe content
cat document.pdf | markitdown > output.md

# Enable plugins
markitdown --list-plugins  # List available plugins
markitdown --use-plugins document.pdf -o output.md
```

### Python API

```python
from markitdown import MarkItDown

# Basic usage
md = MarkItDown()
result = md.convert("document.pdf")
print(result.text_content)

# Convert from stream
with open("document.pdf", "rb") as f:
    result = md.convert_stream(f, file_extension=".pdf")
    print(result.text_content)
```

---

## Plugin System (Pro Enhancements)

### Using Plugins

```python
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=True)
result = md.convert("document.pdf")
```

```bash
markitdown --list-plugins
markitdown --use-plugins file.custom -o output.md
```

### Creating Plugins — The Pro Way

The upstream sample plugin uses `setup.py` and a flat layout. The **Pro** template upgrades to:

| Aspect | Upstream | Pro |
|--------|----------|-----|
| Packaging | `setup.py` | `pyproject.toml` (PEP 621) |
| Layout | Flat `my_plugin/` | `src/` layout |
| Type hints | ❌ | ✅ + `py.typed` |
| `accepts()` | ❌ | ✅ Early-return filter |
| Error handling | bare `except` | Specific exceptions |
| Logging | `print()` | `logging` module |
| Tests | ❌ | ✅ pytest suite |
| Version | hardcoded | `importlib.metadata` |

### Bootstrap a New Plugin

```bash
# Use the built-in template generator
python scripts/plugin_template.py my-converter --extensions .foo .bar

# This creates:
# my-converter/
# ├── pyproject.toml
# ├── README.md
# ├── src/
# │   └── my_converter/
# │       ├── __init__.py
# │       ├── converter.py
# │       └── py.typed
# └── tests/
#     ├── __init__.py
#     ├── conftest.py
#     └── test_converter.py
```

### Sample Plugin Structure

See `sample-plugin/` for a complete working example:

```
sample-plugin/
├── pyproject.toml                          # PEP 621 metadata
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

For the full plugin development guide, see `references/plugin_development.md`.

---

## Advanced Features

### 1. AI-Enhanced Image Descriptions

Use LLMs via OpenRouter to generate detailed image descriptions:

```python
from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI(
    api_key="your-openrouter-api-key",
    base_url="https://openrouter.ai/api/v1"
)

md = MarkItDown(
    llm_client=client,
    llm_model="anthropic/claude-sonnet-4.5",
    llm_prompt="Describe this image in detail for scientific documentation"
)

result = md.convert("presentation.pptx")
print(result.text_content)
```

### 2. Azure Document Intelligence

```python
from markitdown import MarkItDown

md = MarkItDown(docintel_endpoint="<document_intelligence_endpoint>")
result = md.convert("complex_document.pdf")
print(result.text_content)
```

### 3. Batch Processing

```python
from markitdown import MarkItDown
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

md = MarkItDown()

def convert_file(filepath):
    result = md.convert(filepath)
    return filepath, result.text_content

with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(convert_file, Path("docs/").glob("*.pdf"))
```

---

## Optional Dependencies

```bash
pip install 'markitdown[all]'                  # All features
pip install 'markitdown[pdf]'                  # PDF support
pip install 'markitdown[docx]'                 # Word documents
pip install 'markitdown[pptx]'                 # PowerPoint
pip install 'markitdown[xlsx]'                 # Excel
pip install 'markitdown[audio-transcription]'  # Audio files
pip install 'markitdown[youtube-transcription]' # YouTube videos
```

---

## Common Use Cases

### 1. Convert Scientific Papers

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("research_paper.pdf")
with open("paper.md", "w") as f:
    f.write(result.text_content)
```

### 2. Extract Tables from Excel

```python
md = MarkItDown()
result = md.convert("data.xlsx")
print(result.text_content)  # Markdown tables
```

### 3. Process Multiple Documents

```python
from markitdown import MarkItDown
from pathlib import Path

md = MarkItDown()

for pdf_file in Path("papers/").glob("*.pdf"):
    result = md.convert(str(pdf_file))
    output = Path("output") / f"{pdf_file.stem}.md"
    output.write_text(result.text_content)
```

### 4. YouTube Transcript Extraction

```python
md = MarkItDown()
result = md.convert("https://www.youtube.com/watch?v=VIDEO_ID")
print(result.text_content)
```

---

## Best Practices

1. **Reuse MarkItDown instance** — create once, use many times
2. **Use streaming for large files** — `convert_stream()` avoids loading entire files
3. **Enable plugins only when needed** — `enable_plugins=True` has a startup cost
4. **Handle errors gracefully** — catch `FileNotFoundError`, `ValueError`, and generic `Exception`
5. **Clean output** — strip excessive whitespace with `re.sub(r'\n{3,}', '\n\n', text)`

---

## Next Steps

- See `references/api_reference.md` for complete API documentation
- See `references/plugin_development.md` for the full plugin guide
- Check `references/file_formats.md` for format-specific details
- Review `scripts/batch_convert.py` for automation examples
- Explore `scripts/convert_with_ai.py` for AI-enhanced conversions
- Run `python scripts/plugin_template.py my-plugin --extensions .foo` to scaffold a new plugin

## Resources

- **MarkItDown GitHub**: https://github.com/microsoft/markitdown
- **PyPI**: https://pypi.org/project/markitdown/
- **OpenRouter**: https://openrouter.ai (for AI-enhanced conversions)
- **OpenRouter API Keys**: https://openrouter.ai/keys
- **OpenRouter Models**: https://openrouter.ai/models
- **Plugin Development**: See `references/plugin_development.md`
- **Sample Plugin**: See `sample-plugin/` directory
