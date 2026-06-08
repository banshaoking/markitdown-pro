# MarkItDown Pro — Quick Reference

## Installation

```bash
pip install 'markitdown[all]'
```

## Basic Usage

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("file.pdf")
print(result.text_content)
```

## Command Line

```bash
markitdown input.pdf > output.md
markitdown input.pdf -o output.md
markitdown --use-plugins file.custom -o output.md
markitdown --list-plugins
```

## Plugin System (Pro)

### Scaffold a new plugin

```bash
python scripts/plugin_template.py my-plugin --extensions .foo .bar
cd my-plugin
pip install -e '.[dev]'
pytest
```

### Use plugins

```python
md = MarkItDown(enable_plugins=True)
result = md.convert("file.custom")
```

### Sample plugin structure

```
sample-plugin/
├── pyproject.toml
├── src/markitdown_sample_plugin/
│   ├── __init__.py
│   ├── converter.py        # SamplePlugin class
│   └── py.typed
└── tests/
    ├── conftest.py
    └── test_converter.py   # 14 tests
```

### Key plugin patterns

```python
# Always implement accepts() for early filtering
def accepts(self, file_extension: str) -> bool:
    return file_extension.lower() in SUPPORTED_EXTENSIONS

# Use logging, not print
logger = logging.getLogger(__name__)

# Use type hints
def convert(self, stream: BinaryIO, file_extension: str) -> DocumentConverterResult:
```

## AI-Enhanced Conversion

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-openrouter-api-key",
    base_url="https://openrouter.ai/api/v1"
)

md = MarkItDown(
    llm_client=client,
    llm_model="anthropic/claude-sonnet-4.5"
)
result = md.convert("slides.pptx")
```

## Batch Processing

```bash
python scripts/batch_convert.py input/ output/ --extensions .pdf .docx --workers 4
python scripts/convert_literature.py papers/ markdown/ --organize-by-year --create-index
python scripts/convert_with_ai.py paper.pdf output.md --prompt-type scientific
```

## Supported Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| PDF | `.pdf` | Full text + OCR |
| Word | `.docx` | Tables, formatting |
| PowerPoint | `.pptx` | Slides + notes |
| Excel | `.xlsx`, `.xls` | Tables |
| Images | `.jpg`, `.png`, `.gif`, `.webp` | EXIF + OCR |
| Audio | `.wav`, `.mp3` | Transcription |
| HTML | `.html`, `.htm` | Clean conversion |
| Data | `.csv`, `.json`, `.xml` | Structured |
| Archives | `.zip` | Iterates contents |
| E-books | `.epub` | Full text |
| YouTube | URLs | Transcripts |

## Environment Variables

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
export AZURE_DOCUMENT_INTELLIGENCE_KEY="key..."
export AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT="https://..."
```

## More Information

- **Full Docs**: `SKILL.md`
- **API Reference**: `references/api_reference.md`
- **Plugin Guide**: `references/plugin_development.md`
- **Examples**: `assets/example_usage.md`
