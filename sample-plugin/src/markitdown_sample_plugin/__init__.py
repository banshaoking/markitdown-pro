"""
markitdown-sample-plugin — A production-ready sample plugin for MarkItDown.

Demonstrates:
- src/ layout for clean imports
- Type hints throughout
- Proper error handling
- Logging (not print)
- Modern packaging with pyproject.toml
"""

from importlib.metadata import version, PackageNotFoundError

from markitdown_sample_plugin.converter import SamplePlugin

__all__ = ["SamplePlugin"]

try:
    __version__ = version("markitdown-sample-plugin")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"
