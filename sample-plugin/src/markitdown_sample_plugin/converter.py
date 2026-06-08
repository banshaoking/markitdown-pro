"""
Sample MarkItDown plugin — converts .custom files to Markdown.

This module demonstrates best practices for writing a MarkItDown plugin:
- Type-annotated interface
- Early-return via accepts()
- Structured logging
- Graceful error handling
- Encoding detection with UTF-8 fallback
"""

from __future__ import annotations

import logging
from typing import BinaryIO

from markitdown import DocumentConverter, DocumentConverterResult

logger = logging.getLogger(__name__)

# File extensions this plugin handles
SUPPORTED_EXTENSIONS: frozenset[str] = frozenset({".custom", ".sample"})


class SamplePlugin(DocumentConverter):
    """Converts plain-text .custom / .sample files into Markdown.

    The converter reads the raw bytes, decodes them (UTF-8 with fallback),
    and wraps the content in a fenced Markdown block so downstream tools
    can process it uniformly.
    """

    # ------------------------------------------------------------------
    # Interface
    # ------------------------------------------------------------------

    def accepts(self, file_extension: str) -> bool:  # type: ignore[override]
        """Return True when *file_extension* is one we handle."""
        return file_extension.lower() in SUPPORTED_EXTENSIONS

    def convert(self, stream: BinaryIO, file_extension: str) -> DocumentConverterResult:  # type: ignore[override]
        """Read *stream* and return a Markdown representation.

        Parameters
        ----------
        stream:
            A binary file-like object positioned at the start.
        file_extension:
            The detected (or overridden) file extension, e.g. ``".custom"``.

        Returns
        -------
        DocumentConverterResult
            Markdown text plus optional title.

        Raises
        ------
        ValueError
            If the extension is unsupported (should not happen when
            :meth:`accepts` is used for filtering).
        """
        ext = file_extension.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"SamplePlugin does not support '{file_extension}'. "
                f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
            )

        logger.debug("Converting %s file", ext)

        raw: bytes = stream.read()
        text: str = self._decode(raw)
        markdown: str = self._to_markdown(text, ext)

        logger.info("Converted %s file (%d bytes → %d chars)", ext, len(raw), len(markdown))

        return DocumentConverterResult(
            text_content=markdown,
            title=self._extract_title(text),
        )

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    @staticmethod
    def _decode(data: bytes) -> str:
        """Decode *data* to str, trying UTF-8 first then latin-1."""
        for encoding in ("utf-8", "latin-1"):
            try:
                return data.decode(encoding)
            except (UnicodeDecodeError, ValueError):
                continue
        # Last resort — replace undecodable bytes
        return data.decode("utf-8", errors="replace")

    @staticmethod
    def _to_markdown(text: str, ext: str) -> str:
        """Wrap raw *text* in a fenced Markdown block."""
        lang = ext.lstrip(".") or "text"
        return f"```{lang}\n{text}\n```"

    @staticmethod
    def _extract_title(text: str) -> str | None:
        """Heuristically pull a title from the first non-empty line."""
        for line in text.splitlines():
            stripped = line.strip()
            if stripped:
                return stripped[:120]
        return None
