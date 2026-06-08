#!/usr/bin/env python3
"""
Scaffold a new MarkItDown plugin with modern Python packaging.

Usage:
    python plugin_template.py my-plugin --extensions .foo .bar --author "Your Name"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from textwrap import dedent


def to_package_name(project_name: str) -> str:
    """Convert 'my-plugin' → 'my_plugin'."""
    return project_name.replace("-", "_").replace(" ", "_").lower()


def to_class_name(project_name: str) -> str:
    """Convert 'my-plugin' → 'MyPluginConverter'."""
    parts = project_name.replace("-", " ").replace("_", " ").split()
    return "".join(p.capitalize() for p in parts) + "Converter"


def generate_pyproject_toml(
    project_name: str,
    package_name: str,
    class_name: str,
    extensions: list[str],
    author: str,
) -> str:
    ext_list = ", ".join(f'".{e.lstrip(".")}"' for e in extensions)
    return dedent(f"""\
        [build-system]
        requires = ["hatchling"]
        build-backend = "hatchling.build"

        [project]
        name = "markitdown-{project_name}"
        version = "0.1.0"
        description = "MarkItDown plugin for {', '.join(extensions)} files"
        requires-python = ">=3.10"
        license = "MIT"
        authors = [
            {{ name = "{author}" }},
        ]
        dependencies = [
            "markitdown>=0.1.0",
        ]

        [project.optional-dependencies]
        dev = [
            "pytest>=8.0",
            "pytest-cov>=5.0",
            "mypy>=1.10",
            "ruff>=0.5",
        ]

        [project.entry-points."markitdown.plugins"]
        {package_name} = "{package_name}:{class_name}"

        [tool.hatch.build.targets.wheel]
        packages = ["src/{package_name}"]

        [tool.pytest.ini_options]
        testpaths = ["tests"]
        addopts = "-v --tb=short"

        [tool.mypy]
        python_version = "3.10"
        strict = true
    """)


def generate_init(package_name: str, class_name: str) -> str:
    return dedent(f'''\
        """
        markitdown-{package_name} — MarkItDown plugin.
        """
        from importlib.metadata import version, PackageNotFoundError

        from {package_name}.converter import {class_name}

        __all__ = ["{class_name}"]

        try:
            __version__ = version("markitdown-{package_name}")
        except PackageNotFoundError:
            __version__ = "0.0.0-dev"
    ''')


def generate_converter(
    package_name: str,
    class_name: str,
    extensions: list[str],
) -> str:
    ext_set = ", ".join(f'".{e.lstrip(".")}"' for e in extensions)
    return dedent(f'''\
        """Converter for {', '.join(extensions)} files."""

        from __future__ import annotations

        import logging
        from typing import BinaryIO

        from markitdown import DocumentConverter, DocumentConverterResult

        logger = logging.getLogger(__name__)

        SUPPORTED_EXTENSIONS: frozenset[str] = frozenset({{{ext_set}}})


        class {class_name}(DocumentConverter):
            """Converts {", ".join(extensions)} files to Markdown."""

            def accepts(self, file_extension: str) -> bool:
                return file_extension.lower() in SUPPORTED_EXTENSIONS

            def convert(
                self, stream: BinaryIO, file_extension: str
            ) -> DocumentConverterResult:
                ext = file_extension.lower()
                if ext not in SUPPORTED_EXTENSIONS:
                    raise ValueError(f"Unsupported extension: {{ext}}")

                logger.debug("Converting %s file", ext)

                raw: bytes = stream.read()
                text: str = raw.decode("utf-8", errors="replace")

                lang = ext.lstrip(".") or "text"
                markdown = f"```{{lang}}\\n{{text}}\\n```"

                title: str | None = None
                for line in text.splitlines():
                    stripped = line.strip()
                    if stripped:
                        title = stripped[:120]
                        break

                logger.info("Converted %s file (%d bytes)", ext, len(raw))

                return DocumentConverterResult(
                    text_content=markdown,
                    title=title,
                )
    ''')


def generate_test_converter(
    package_name: str,
    class_name: str,
    extensions: list[str],
) -> str:
    ext_first = extensions[0].lstrip(".")
    return dedent(f'''\
        """Tests for {class_name}."""

        from __future__ import annotations

        import io
        import pytest

        from {package_name} import {class_name}


        @pytest.fixture()
        def converter() -> {class_name}:
            return {class_name}()


        class TestAccepts:
            @pytest.mark.parametrize("ext", [{", ".join(f'".{e.lstrip(".")}"' for e in extensions)}])
            def test_supported(self, converter: {class_name}, ext: str) -> None:
                assert converter.accepts(ext) is True

            @pytest.mark.parametrize("ext", [".pdf", ".docx", ".txt"])
            def test_unsupported(self, converter: {class_name}, ext: str) -> None:
                assert converter.accepts(ext) is False


        class TestConvert:
            def test_basic(self, converter: {class_name}) -> None:
                stream = io.BytesIO(b"Hello, world!")
                result = converter.convert(stream, ".{ext_first}")
                assert "Hello, world!" in result.text_content

            def test_empty(self, converter: {class_name}) -> None:
                stream = io.BytesIO(b"")
                result = converter.convert(stream, ".{ext_first}")
                assert result.title is None

            def test_unsupported_raises(self, converter: {class_name}) -> None:
                stream = io.BytesIO(b"test")
                with pytest.raises(ValueError):
                    converter.convert(stream, ".pdf")
    ''')


def generate_conftest(package_name: str) -> str:
    return dedent(f'''\
        """Shared fixtures."""
        import pytest
    ''')


def create_plugin(
    output_dir: Path,
    project_name: str,
    extensions: list[str],
    author: str,
) -> None:
    package_name = to_package_name(project_name)
    class_name = to_class_name(project_name)

    # Directory structure
    src_dir = output_dir / "src" / package_name
    tests_dir = output_dir / "tests"
    fixtures_dir = tests_dir / "fixtures"

    for d in (src_dir, tests_dir, fixtures_dir):
        d.mkdir(parents=True, exist_ok=True)

    # Files
    files = {
        output_dir / "pyproject.toml": generate_pyproject_toml(
            project_name, package_name, class_name, extensions, author
        ),
        output_dir / "README.md": f"# markitdown-{project_name}\n\nMarkItDown plugin for {', '.join(extensions)} files.\n",
        src_dir / "__init__.py": generate_init(package_name, class_name),
        src_dir / "converter.py": generate_converter(package_name, class_name, extensions),
        src_dir / "py.typed": "",
        tests_dir / "__init__.py": "",
        tests_dir / "conftest.py": generate_conftest(package_name),
        tests_dir / "test_converter.py": generate_test_converter(package_name, class_name, extensions),
        fixtures_dir / f"sample.{extensions[0].lstrip('.')}": "This is a sample file for testing.\n",
    }

    for path, content in files.items():
        path.write_text(content, encoding="utf-8")
        print(f"  ✓ {path.relative_to(output_dir)}")

    print(f"\n✅ Plugin '{project_name}' created at {output_dir}")
    print(f"\nNext steps:")
    print(f"  cd {output_dir}")
    print(f"  pip install -e '.[dev]'")
    print(f"  pytest")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold a new MarkItDown plugin",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent("""\
            Examples:
              python plugin_template.py my-format --extensions .foo .bar
              python plugin_template.py geojson --extensions .geojson --author "Jane Doe"
        """),
    )
    parser.add_argument("name", help="Plugin project name (e.g. my-format)")
    parser.add_argument(
        "--extensions", "-e",
        nargs="+",
        required=True,
        help="File extensions to support (e.g. .foo .bar)",
    )
    parser.add_argument("--author", default="Your Name", help="Author name")
    parser.add_argument("--output-dir", "-o", type=Path, default=None, help="Output directory")

    args = parser.parse_args()

    output_dir = args.output_dir or Path(args.name)
    if output_dir.exists():
        print(f"Error: Directory '{output_dir}' already exists", file=sys.stderr)
        sys.exit(1)

    extensions = [e if e.startswith(".") else f".{e}" for e in args.extensions]
    create_plugin(output_dir, args.name, extensions, args.author)


if __name__ == "__main__":
    main()
