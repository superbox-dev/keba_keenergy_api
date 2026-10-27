#!/usr/bin/env -S uv run python
# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Generate the Markdown pages of the Docusaurus website.

The API reference is rendered from the NumPy-style docstrings with griffe, the sections, enums and models pages
from the modules. The home, donation, contributing and changelog pages are copied from the marked sections of the
Markdown files in the repository root, the hand-written pages from ``website/content``. All pages are written to
``website/docs``, which is not tracked by git.
"""

import annotationlib
import inspect
import re
import shutil
from enum import Enum
from pathlib import Path
from typing import ClassVar
from typing import Final
from typing import TypeAliasType
from typing import get_args

import griffe

from keba_keenergy_api import constants
from keba_keenergy_api import enums
from keba_keenergy_api import exceptions
from keba_keenergy_api import models
from keba_keenergy_api.sections import Section

ROOT: Final[Path] = Path(__file__).resolve().parent.parent
OUTPUT: Final[Path] = ROOT / "website" / "docs"
CONTENT: Final[Path] = ROOT / "website" / "content"
PACKAGE: Final[str] = "keba_keenergy_api"
PAYLOAD_PREFIX: Final[str] = "APPL.CtrlAppl"
SIGNATURE_WIDTH: Final[int] = 100


class DocsGenerator:
    """Render the documentation pages into the Docusaurus docs folder."""

    _ROLE_PATTERN: re.Pattern[str] = re.compile(r":[a-z]+:`~?([^`]+)`")
    _LITERAL_PATTERN: re.Pattern[str] = re.compile(r"``([^`]+)``")
    _WARNING_PREFIX: str = "**Attention!** "

    # Links in the copied Markdown files, mapped to the generated pages, so Docusaurus checks them.
    _LINKS: ClassVar[dict[str, str]] = {
        "(CHANGELOG.md)": "(changelog.md)",
        "(CONTRIBUTING.md)": "(contributing.md)",
        "(https://superbox-dev.github.io/keba_keenergy_api/usage": "(usage.md",
        "(https://superbox-dev.github.io/keba_keenergy_api/migration": "(migration.md",
        "(CLAUDE.md)": "(https://github.com/superbox-dev/keba_keenergy_api/blob/main/CLAUDE.md)",
    }

    def __init__(self, output: Path) -> None:
        """Initialize the generator.

        Parameters
        ----------
        output
            Folder for the generated Markdown pages, replaced on every run.

        """
        self.output: Path = output
        self.package: griffe.Alias | griffe.Object = griffe.load(
            PACKAGE,
            search_paths=[ROOT],
            docstring_parser=griffe.Parser.numpy,
        )

    def run(self) -> None:
        """Write all pages."""
        shutil.rmtree(self.output, ignore_errors=True)
        self.output.mkdir(parents=True)

        for page in sorted(CONTENT.glob("*.md")):
            shutil.copyfile(page, self.output / page.name)

        self._write_page(
            "index.md",
            self._front_matter("Introduction", 0, slug="/"),
            "# KEBA KeEnergy API",
            self._extract("README.md", "home"),
        )
        self._write_page("donation.md", self._front_matter("Donation", 90), self._extract("README.md", "donation"))
        self._write_page("api.md", self._front_matter("API client", 10), self._render_client())
        self._write_page("sections.md", self._front_matter("Sections", 20), self._render_sections())
        self._write_page("enums.md", self._front_matter("Enums", 30), self._render_enums())
        self._write_page("models.md", self._front_matter("Models and errors", 40), self._render_models())
        self._write_page(
            "changelog.md",
            self._front_matter("Changelog", 70, hide_toc=True),
            "# Changelog",
            self._extract("CHANGELOG.md", ""),
        )
        self._write_page(
            "contributing.md",
            self._front_matter("Contributing", 80),
            "# Contributing",
            self._extract("CONTRIBUTING.md", "contributing"),
        )

    def _write_page(self, path: str, *blocks: str) -> None:
        content: str = "\n\n".join(block.strip("\n") for block in blocks if block)
        (self.output / path).write_text(f"{content}\n", encoding="utf-8")

    @staticmethod
    def _front_matter(title: str, position: int, *, slug: str = "", hide_toc: bool = False) -> str:
        lines: list[str] = ["---", f"title: {title}", f"sidebar_position: {position}"]

        if slug:
            lines.append(f"slug: {slug}")

        if hide_toc:
            lines.append("hide_table_of_contents: true")

        lines.append("---")
        return "\n".join(lines)

    def _extract(self, filename: str, marker: str) -> str:
        """Join all sections of a Markdown file between ``<!--start-marker-->`` and ``<!--end-marker-->``."""
        suffix: str = f"-{marker}" if marker else ""
        text: str = (ROOT / filename).read_text(encoding="utf-8")
        pattern: re.Pattern[str] = re.compile(rf"<!--start{suffix}-->(.*?)<!--end{suffix}-->", re.DOTALL)
        content: str = "\n\n".join(part.strip("\n") for part in pattern.findall(text))

        if not content:
            msg: str = f"No <!--start{suffix}--> section in {filename}"
            raise ValueError(msg)

        for link, target in self._LINKS.items():
            content = content.replace(link, target)

        return content

    def _render_client(self) -> str:
        client: griffe.Class = self._get_class("client", "KebaKeEnergyAPI")
        init: griffe.Function = client.functions["__init__"]
        blocks: list[str] = [
            f"# {client.name}",
            self._code(self._signature(client.name, init, prefix="class ")),
            self._render_text(client.docstring),
            self._render_docstring(init.docstring, skip_summary=True),
        ]

        for name, member in client.attributes.items():
            if "property" in member.labels and not name.startswith("_"):
                blocks.extend(
                    [
                        f"## {name}",
                        self._code(f"client.{name}: {member.annotation}"),
                        self._render_docstring(member.docstring),
                    ],
                )

        blocks.extend(self._render_functions(client))
        return "\n\n".join(block for block in blocks if block)

    def _get_class(self, module: str, name: str) -> griffe.Class:
        cls: griffe.Alias | griffe.Object = self.package[module][name]

        if not isinstance(cls, griffe.Class):
            msg: str = f"{module}.{name} is not a class"
            raise TypeError(msg)

        return cls

    @staticmethod
    def _code(code: str) -> str:
        return f"```python\n{code}\n```"

    def _signature(self, name: str, function: griffe.Function, *, prefix: str) -> str:
        parameters: list[str] = []
        keyword_only: bool = False

        for parameter in function.parameters:
            if parameter.name in {"self", "cls"}:
                continue

            if parameter.kind is griffe.ParameterKind.var_positional:
                keyword_only = True
            elif parameter.kind is griffe.ParameterKind.keyword_only and not keyword_only:
                parameters.append("*")
                keyword_only = True

            parameters.append(self._parameter(parameter))

        # A class signature is rendered from its __init__ without the return annotation.
        returns: str = "" if prefix.startswith("class") else f" -> {function.returns}"
        line: str = f"{prefix}{name}({', '.join(parameters)}){returns}"

        if len(line) <= SIGNATURE_WIDTH or not parameters:
            return line

        lines: str = "".join(f"    {parameter},\n" for parameter in parameters)
        return f"{prefix}{name}(\n{lines}){returns}"

    @staticmethod
    def _parameter(parameter: griffe.Parameter) -> str:
        stars: str = {
            griffe.ParameterKind.var_positional: "*",
            griffe.ParameterKind.var_keyword: "**",
        }.get(parameter.kind, "")
        text: str = f"{stars}{parameter.name}"

        if parameter.annotation is not None:
            text = f"{text}: {parameter.annotation}"

        if parameter.default is not None:
            text = f"{text} = {parameter.default}"

        return text

    def _render_text(self, docstring: griffe.Docstring | None) -> str:
        if docstring is None:
            return ""

        return "\n\n".join(
            self._convert(section.value)
            for section in docstring.parsed
            if section.kind is griffe.DocstringSectionKind.text
        )

    def _convert(self, text: str) -> str:
        """Convert reStructuredText markup of a docstring to Markdown."""
        text = self._ROLE_PATTERN.sub(r"`\1`", text)
        text = self._LITERAL_PATTERN.sub(r"`\1`", text)
        paragraphs: list[str] = []

        for paragraph in text.split("\n\n"):
            if paragraph.startswith(self._WARNING_PREFIX):
                body: str = paragraph.removeprefix(self._WARNING_PREFIX)
                paragraphs.append(f":::warning[Attention]\n\n{body}\n\n:::")
            else:
                paragraphs.append(paragraph)

        return "\n\n".join(paragraphs)

    def _render_docstring(self, docstring: griffe.Docstring | None, *, skip_summary: bool = False) -> str:
        if docstring is None:
            return ""

        blocks: list[str] = []

        for section in docstring.parsed:
            if isinstance(section, griffe.DocstringSectionText):
                text: str = section.value

                # The summary of __init__ ("Initialize the ...") repeats the class docstring.
                if skip_summary:
                    text = text.split("\n\n", maxsplit=1)[1] if "\n\n" in text else ""
                    skip_summary = False

                blocks.append(self._convert(text))
            elif isinstance(section, griffe.DocstringSectionParameters):
                blocks.append(self._render_items("Parameters", section.value))
            elif isinstance(section, griffe.DocstringSectionAttributes):
                blocks.append(self._render_items("Attributes", section.value))
            elif isinstance(section, griffe.DocstringSectionReturns):
                blocks.append(self._render_items("Returns", section.value))
            elif isinstance(section, griffe.DocstringSectionRaises):
                blocks.append(self._render_items("Raises", section.value))
            elif isinstance(section, griffe.DocstringSectionExamples):
                blocks.extend(self._render_examples(section))

        return "\n\n".join(block for block in blocks if block)

    def _render_items(
        self,
        title: str,
        items: list[griffe.DocstringAttribute]
        | list[griffe.DocstringParameter]
        | list[griffe.DocstringRaise]
        | list[griffe.DocstringReturn],
    ) -> str:
        lines: list[str] = [f"**{title}**", ""]

        for item in items:
            parts: list[str] = []

            if isinstance(item, griffe.DocstringAttribute | griffe.DocstringParameter):
                parts.append(f"**{item.name}**")

            if item.annotation is not None:
                parts.append(f"`{item.annotation}`")

            if isinstance(item, griffe.DocstringParameter) and item.default is not None:
                parts.append(f"(default: `{item.default}`)")

            description: str = self._convert(item.description).replace("\n", " ")
            lines.append(f"- {' '.join(parts)}" + (f": {description}" if description else ""))

        return "\n".join(lines)

    def _render_examples(self, section: griffe.DocstringSectionExamples) -> list[str]:
        blocks: list[str] = ["**Example**"]

        for kind, text in section.value:
            if kind is griffe.DocstringSectionKind.examples:
                code: str = "\n".join(re.sub(r"^(>>>|\.\.\.) ?", "", line) for line in text.splitlines())
                blocks.append(self._code(code))
            else:
                blocks.append(self._convert(text))

        return blocks

    def _render_functions(self, cls: griffe.Class) -> list[str]:
        blocks: list[str] = []

        for name, function in cls.functions.items():
            if name.startswith("_"):
                continue

            prefix: str = "async def " if "async" in function.labels else "def "
            blocks.extend(
                [
                    f"## {name}",
                    self._code(self._signature(name, function, prefix=prefix)),
                    self._render_docstring(function.docstring),
                ],
            )

        return blocks

    def _render_sections(self) -> str:
        """Render one table per section with the public endpoints."""
        endpoint: griffe.Class = self._get_class("sections", "Endpoint")
        blocks: list[str] = [
            "# Sections",
            (
                f"The module `{PACKAGE}.sections` defines one enum per device type, its members are the sections "
                "for [`read()`](api.md#read), [`filter_supported()`](api.md#filter_supported) and "
                f"[`write()`](api.md#write). Paths are relative to `{PAYLOAD_PREFIX}`, `%s` is replaced by the "
                "zero-based device index. *Message id* is the component node of the message id (`state.msgId`)."
            ),
            "## Endpoint",
            self._render_docstring(endpoint.docstring),
        ]

        for section_class in get_args(Section.__value__):
            rows: list[str] = [
                self._row(
                    f"`{section.name}`",
                    self._type_link(section.value.value_type),
                    section.value.unit or "",
                    "yes" if section.value.writable else "no",
                    f"`{section.value.message_id}`" if section.value.message_id else "",
                    f"`{section.value.path}`",
                )
                for section in section_class
                if not section.name.startswith("_")
            ]
            blocks.extend(
                [
                    f"## {section_class.__name__}",
                    self._render_text(self._get_class("sections", section_class.__name__).docstring),
                    self._table(("Member", "Type", "Unit", "Writable", "Message id", "Path"), rows),
                ],
            )

        return "\n\n".join(block for block in blocks if block)

    @staticmethod
    def _type_link(value_type: type) -> str:
        if issubclass(value_type, Enum):
            return f"[`{value_type.__name__}`](enums.md#{value_type.__name__.lower()})"

        return f"`{value_type.__name__}`"

    @staticmethod
    def _row(*cells: str) -> str:
        return f"| {' | '.join(cells)} |"

    def _table(self, header: tuple[str, ...], rows: list[str]) -> str:
        return "\n".join([self._row(*header), self._row(*("---" for _ in header)), *rows])

    def _render_enums(self) -> str:
        """Render the public enums of the ``enums`` module."""
        blocks: list[str] = [
            "# Enums",
            (
                f"The module `{PACKAGE}.enums` defines the values of the Web HMI. "
                "[`read()`](api.md#read) returns them as enum members, [`write()`](api.md#write) accepts them."
            ),
        ]

        for name, cls in vars(enums).items():
            if inspect.isclass(cls) and issubclass(cls, Enum) and cls.__module__ == enums.__name__ and len(cls):
                if name.startswith("_"):
                    continue

                blocks.extend(
                    [
                        f"## {name}",
                        self._render_text(self._get_class("enums", name).docstring),
                        self._table(
                            ("Member", "Value"),
                            [self._row(f"`{member.name}`", f"`{member.value!r}`") for member in cls],
                        ),
                    ],
                )

        return "\n\n".join(block for block in blocks if block)

    def _render_models(self) -> str:
        """Render the models, the exceptions and the constants."""
        blocks: list[str] = ["# Models and errors", f"## Models (`{PACKAGE}.models`)"]

        for name, cls in vars(models).items():
            if inspect.isclass(cls) and cls.__module__ == models.__name__ and not name.startswith("_"):
                blocks.extend(
                    [
                        f"### {name}",
                        self._code(self._class_fields(cls)),
                        self._render_docstring(self._get_class("models", name).docstring),
                    ],
                )

        blocks.extend(
            [
                "### Type aliases",
                self._code(
                    "\n".join(
                        f"type {name} = {self._type_alias_value(alias)}"
                        for name, alias in vars(models).items()
                        if isinstance(alias, TypeAliasType)
                    ),
                ),
                f"## Errors (`{PACKAGE}.exceptions`)",
            ],
        )

        for name, cls in vars(exceptions).items():
            if inspect.isclass(cls) and cls.__module__ == exceptions.__name__:
                bases: str = ", ".join(base.__name__ for base in cls.__bases__)
                blocks.extend(
                    [
                        f"### {name}",
                        self._code(f"class {name}({bases})"),
                        self._render_text(self._get_class("exceptions", name).docstring),
                    ],
                )

        blocks.extend(
            [
                f"## Constants (`{PACKAGE}.constants`)",
                self._table(
                    ("Name", "Value"),
                    [
                        self._row(f"`{name}`", f"`{value!r}`")
                        for name, value in vars(constants).items()
                        if name.isupper() and not name.startswith("_")
                    ],
                ),
            ],
        )
        return "\n\n".join(block for block in blocks if block)

    @staticmethod
    def _type_alias_value(alias: TypeAliasType) -> str:
        """Return the value of a type alias as written in the source."""
        return str(annotationlib.call_evaluate_function(alias.evaluate_value, annotationlib.Format.STRING))

    @staticmethod
    def _class_fields(model: type) -> str:
        """Return the class with its fields as written in the source, e.g. of a dataclass or a typed dict."""
        annotations: dict[str, str] = annotationlib.get_annotations(model, format=annotationlib.Format.STRING)
        return "\n".join([f"class {model.__name__}:", *(f"    {key}: {value}" for key, value in annotations.items())])


if __name__ == "__main__":
    DocsGenerator(OUTPUT).run()
