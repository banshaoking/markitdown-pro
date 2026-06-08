"""Shared fixtures for markitdown-sample-plugin tests."""

from __future__ import annotations

import io
from pathlib import Path
from typing import Generator

import pytest

from markitdown_sample_plugin import SamplePlugin

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture()
def plugin() -> SamplePlugin:
    """Return a fresh SamplePlugin instance."""
    return SamplePlugin()


@pytest.fixture()
def sample_text() -> str:
    """Return sample text content for testing."""
    return "Hello, MarkItDown!\nThis is a custom file.\n"


@pytest.fixture()
def sample_stream(sample_text: str) -> Generator[io.BytesIO, None, None]:
    """Return a binary stream containing sample text."""
    stream = io.BytesIO(sample_text.encode("utf-8"))
    yield stream
    stream.close()


@pytest.fixture()
def empty_stream() -> Generator[io.BytesIO, None, None]:
    """Return an empty binary stream."""
    stream = io.BytesIO(b"")
    yield stream
    stream.close()


@pytest.fixture()
def binary_stream() -> Generator[io.BytesIO, None, None]:
    """Return a stream with non-UTF-8 binary content."""
    stream = io.BytesIO(b"\x80\x81\x82\x83")
    yield stream
    stream.close()


@pytest.fixture()
def fixture_file() -> Path:
    """Return the path to the sample fixture file."""
    return FIXTURES_DIR / "sample.custom"
