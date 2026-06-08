"""Tests for the SamplePlugin MarkItDown converter."""

from __future__ import annotations

import io
from pathlib import Path

import pytest

from markitdown_sample_plugin import SamplePlugin
from markitdown_sample_plugin.converter import SUPPORTED_EXTENSIONS


# ── accepts() ──────────────────────────────────────────────────────────


class TestAccepts:
    """Verify that accepts() correctly identifies supported extensions."""

    @pytest.mark.parametrize("ext", [".custom", ".sample", ".CUSTOM", ".SAMPLE"])
    def test_supported_extensions(self, plugin: SamplePlugin, ext: str) -> None:
        assert plugin.accepts(ext) is True

    @pytest.mark.parametrize("ext", [".pdf", ".docx", ".txt", ".md", ""])
    def test_unsupported_extensions(self, plugin: SamplePlugin, ext: str) -> None:
        assert plugin.accepts(ext) is False


# ── convert() ──────────────────────────────────────────────────────────


class TestConvert:
    """Verify conversion behaviour."""

    def test_basic_conversion(self, plugin: SamplePlugin, sample_stream: io.BytesIO) -> None:
        result = plugin.convert(sample_stream, ".custom")
        assert "```custom" in result.text_content
        assert "Hello, MarkItDown!" in result.text_content

    def test_sample_extension(self, plugin: SamplePlugin, sample_stream: io.BytesIO) -> None:
        result = plugin.convert(sample_stream, ".sample")
        assert "```sample" in result.text_content

    def test_title_extraction(self, plugin: SamplePlugin, sample_stream: io.BytesIO) -> None:
        result = plugin.convert(sample_stream, ".custom")
        assert result.title == "Hello, MarkItDown!"

    def test_empty_file(self, plugin: SamplePlugin, empty_stream: io.BytesIO) -> None:
        result = plugin.convert(empty_stream, ".custom")
        assert result.text_content == "```custom\n\n```"
        assert result.title is None

    def test_binary_content_fallback(self, plugin: SamplePlugin, binary_stream: io.BytesIO) -> None:
        """Non-UTF-8 bytes should still produce output (latin-1 / replace)."""
        result = plugin.convert(binary_stream, ".custom")
        assert "```custom" in result.text_content

    def test_unsupported_extension_raises(self, plugin: SamplePlugin, sample_stream: io.BytesIO) -> None:
        with pytest.raises(ValueError, match="does not support"):
            plugin.convert(sample_stream, ".pdf")

    def test_fixture_file(self, plugin: SamplePlugin, fixture_file: Path) -> None:
        """Consume the on-disk fixture file end-to-end."""
        with open(fixture_file, "rb") as f:
            result = plugin.convert(f, ".custom")
        assert "MarkItDown sample plugin" in result.text_content


# ── Edge cases ─────────────────────────────────────────────────────────


class TestEdgeCases:
    """Stress-test boundary conditions."""

    def test_large_file(self, plugin: SamplePlugin) -> None:
        """A 1 MB file should convert without errors."""
        big = b"A" * 1_000_000
        stream = io.BytesIO(big)
        result = plugin.convert(stream, ".custom")
        assert len(result.text_content) > 1_000_000

    def test_multibyte_utf8(self, plugin: SamplePlugin) -> None:
        """CJK and emoji should survive round-trip."""
        text = "你好世界 🚀 MarkItDown"
        stream = io.BytesIO(text.encode("utf-8"))
        result = plugin.convert(stream, ".custom")
        assert "你好世界" in result.text_content
        assert "🚀" in result.text_content

    def test_title_truncation(self, plugin: SamplePlugin) -> None:
        """Titles longer than 120 chars should be truncated."""
        long_title = "X" * 200
        stream = io.BytesIO(long_title.encode("utf-8"))
        result = plugin.convert(stream, ".custom")
        assert result.title is not None
        assert len(result.title) <= 120

    def test_only_whitespace(self, plugin: SamplePlugin) -> None:
        stream = io.BytesIO(b"   \n\n  \t  ")
        result = plugin.convert(stream, ".custom")
        assert result.title is None
