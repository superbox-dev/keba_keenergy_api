#!/usr/bin/env -S uv run python
# Copyright 2023-2026 Michael Hacker
# SPDX-License-Identifier: Apache-2.0

"""Generate the Markdown pages of the Docusaurus website.

The API reference is rendered from the NumPy-style docstrings with griffe. The home, donation,
contributing and changelog pages are copied from the marked sections of the Markdown files in the
repository root, the hand-written pages from ``website/content``. All pages are written to
``website/docs``, which is not tracked by git.
"""

import importlib
import inspect
import re
import shutil
from enum import Enum
from pathlib import Path
from types import ModuleType
from typing import ClassVar
from typing import Final

import griffe

ROOT: Final[Path] = Path(__file__).resolve().parent.parent
OUTPUT: Final[Path] = ROOT / "website" / "docs"
CONTENT: Final[Path] = ROOT / "website" / "content"
PACKAGE: Final[str] = "keba_keenergy_api"
CLIENT: Final[str] = "client"
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
        (self.output / "endpoints").mkdir(parents=True)

        client: griffe.Class = self._get_class("api", "KebaKeEnergyAPI")
        sections: list[tuple[str, griffe.Class]] = [
            (name, self._get_class("endpoints", str(member.annotation)))
            for name, member in client.attributes.items()
            if "property" in member.labels and str(member.annotation).endswith("Endpoints")
        ]

        for page in sorted(CONTENT.glob("*.md")):
            shutil.copyfile(page, self.output / page.name)

        self._write_home()
        self._write_page("donation.md", self._front_matter("Donation", 90), self._extract("README.md", "donation"))
        self._write_page("api.md", self._front_matter("API client", 10), self._render_client(client, sections))
        self._write_page("constants.md", self._front_matter("Constants", 30), self._render_constants())

        for position, (name, section) in enumerate(sections, start=1):
            self._write_page(
                f"endpoints/{self._slug(name)}.md",
                self._front_matter(self._title(name), position),
                self._render_section(name, section),
            )

        self._write_page(
            "endpoints/_category_.json",
            '{\n  "label": "Endpoints",\n  "position": 20,\n  "link": {"type": "generated-index"}\n}',
        )
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

    def _get_class(self, module: str, name: str) -> griffe.Class:
        cls: griffe.Alias | griffe.Object = self.package[module][name]

        if not isinstance(cls, griffe.Class):
            msg: str = f"{module}.{name} is not a class"
            raise TypeError(msg)

        return cls

    def _write_home(self) -> None:
        intro: str = self._extract("README.md", "home")
        self._write_page(
            "index.md",
            self._front_matter("Introduction", 0, slug="/"),
            "# KEBA KeEnergy API",
            intro,
        )

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

    def _write_page(self, path: str, *blocks: str) -> None:
        content: str = "\n\n".join(block.strip("\n") for block in blocks if block)
        (self.output / path).write_text(f"{content}\n", encoding="utf-8")

    def _get_class(self, module: str, name: str) -> griffe.Class:
        cls: griffe.Object | griffe.Alias = self.package[module][name]

        if not isinstance(cls, griffe.Class):
            msg: str = f"{module}.{name} is not a class"
            raise TypeError(msg)

        return cls

    @staticmethod
    def _slug(name: str) -> str:
        return name.replace("_", "-")

    @staticmethod
    def _title(name: str) -> str:
        return name.replace("_", " ").capitalize()

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

    def _render_client(self, client: griffe.Class, sections: list[tuple[str, griffe.Class]]) -> str:
        init: griffe.Function = client.functions["__init__"]
        blocks: list[str] = [
            f"# {client.name}",
            self._code(self._signature(client.name, init, prefix="class ")),
            self._render_text(client.docstring),
            self._render_docstring(init.docstring, skip_summary=True),
            "## Endpoints",
            "Each endpoint group is a property of the client:",
            "\n".join(
                f"- [`{CLIENT}.{name}`](endpoints/{self._slug(name)}.md): {self._summary(section.docstring)}"
                for name, section in sections
            ),
        ]

        for name, member in client.attributes.items():
            if "property" in member.labels and not name.startswith("_") and name not in dict(sections):
                blocks.extend(
                    [
                        f"## {name}",
                        self._code(f"{CLIENT}.{name}: {member.annotation}"),
                        self._render_docstring(member.docstring),
                    ],
                )

        blocks.extend(self._render_functions(client))
        return "\n\n".join(block for block in blocks if block)

    def _render_section(self, name: str, section: griffe.Class) -> str:
        blocks: list[str] = [
            f"# {self._title(name)}",
            f"Endpoint group `{CLIENT}.{name}` ({section.name}).",
            self._render_docstring(section.docstring),
            *self._render_functions(section),
        ]
        return "\n\n".join(block for block in blocks if block)

    def _render_constants(self) -> str:
        """Render the endpoint enums, the value enums and the other public constants."""
        module: ModuleType = importlib.import_module(f"{PACKAGE}.constants")
        classes: list[type] = [
            cls
            for name, cls in vars(module).items()
            if inspect.isclass(cls) and cls.__module__ == module.__name__ and not name.startswith("_")
        ]
        sections: list[type[Enum]] = [
            cls
            for cls in classes
            if issubclass(cls, Enum) and len(cls) and all(isinstance(member.value, module.Endpoint) for member in cls)
        ]
        values: list[type[Enum]] = [
            cls for cls in classes if issubclass(cls, module.BaseEnum) and cls is not module.BaseEnum
        ]
        blocks: list[str] = [
            "# Constants",
            (
                f"The module `{PACKAGE}.constants` defines the endpoints and their values, e.g. for "
                "[`read_data()`](api.md#read_data) and [`write_data()`](api.md#write_data). "
                f"Paths are relative to `PAYLOAD_PREFIX` (`{module.PAYLOAD_PREFIX}`), "
                "`%s` is replaced by the zero-based device index."
            ),
            "## Endpoints",
        ]

        for section in sections:
            rows: list[str] = [
                self._row(
                    f"`{member.name}`",
                    member.value.value_type.__name__,
                    "no" if member.value.read_only else "yes",
                    self._enum_link(member.value.human_readable),
                    f"`{member.value.value.removeprefix(module.PAYLOAD_PREFIX + '.')}`",
                )
                for member in section
                if not member.name.startswith("_")
            ]
            blocks.extend(
                [
                    f"### {section.__name__}",
                    self._render_text(self._get_class("constants", section.__name__).docstring),
                    self._table(("Member", "Type", "Writable", "Values", "Path"), rows),
                ],
            )

        blocks.extend(
            [
                "## Values",
                "Enums of the readable names, returned with `human_readable=True` and accepted by the setters.",
            ],
        )

        for cls in values:
            rows = [self._row(f"`{member.name}`", f"`{member.value}`") for member in cls]
            blocks.extend(
                [
                    f"### {cls.__name__}",
                    self._render_text(self._get_class("constants", cls.__name__).docstring),
                    self._table(("Member", "Value"), rows),
                ],
            )

        blocks.extend(self._render_other_constants(module, [*sections, *values]))
        return "\n\n".join(block for block in blocks if block)

    def _render_other_constants(self, module: ModuleType, documented: list[type[Enum]]) -> list[str]:
        blocks: list[str] = ["## Other constants"]
        rows: list[str] = [
            self._row(f"`{name}`", f"`{value!r}`")
            for name, value in vars(module).items()
            if name.isupper() and not name.startswith("_") and isinstance(value, int | str)
        ]
        blocks.append(self._table(("Name", "Value"), rows))

        for name, cls in vars(module).items():
            if not inspect.isclass(cls) or cls.__module__ != module.__name__ or name.startswith("_"):
                continue

            if cls in documented or cls is module.BaseEnum or issubclass(cls, module.Endpoint):
                continue

            members: dict[str, object] = (
                {member.name: member.value for member in cls}
                if issubclass(cls, Enum)
                else {key: value for key, value in vars(cls).items() if key.isupper()}
            )
            blocks.extend(
                [
                    f"### {name}",
                    self._render_text(self._get_class("constants", name).docstring),
                    self._table(("Member", "Value"), [self._row(f"`{k}`", f"`{v!r}`") for k, v in members.items()]),
                ],
            )

        return blocks

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

    def _summary(self, docstring: griffe.Docstring | None) -> str:
        text: str = self._render_text(docstring)
        return text.split("\n\n", maxsplit=1)[0].replace("\n", " ")

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
        items: list[griffe.DocstringParameter] | list[griffe.DocstringRaise] | list[griffe.DocstringReturn],
    ) -> str:
        lines: list[str] = [f"**{title}**", ""]

        for item in items:
            parts: list[str] = []

            if isinstance(item, griffe.DocstringParameter):
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

    @staticmethod
    def _slug(name: str) -> str:
        return name.replace("_", "-")

    def _summary(self, docstring: griffe.Docstring | None) -> str:
        text: str = self._render_text(docstring)
        return text.split("\n\n", maxsplit=1)[0].replace("\n", " ")

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

    def _render_constants(self) -> str:
        """Render the endpoint enums, the value enums and the other public constants."""
        module: ModuleType = importlib.import_module(f"{PACKAGE}.constants")
        classes: list[type] = [
            cls
            for name, cls in vars(module).items()
            if inspect.isclass(cls) and cls.__module__ == module.__name__ and not name.startswith("_")
        ]
        sections: list[type[Enum]] = [
            cls
            for cls in classes
            if issubclass(cls, Enum) and len(cls) and all(isinstance(member.value, module.Endpoint) for member in cls)
        ]
        values: list[type[Enum]] = [
            cls for cls in classes if issubclass(cls, module.BaseEnum) and cls is not module.BaseEnum
        ]
        blocks: list[str] = [
            "# Constants",
            (
                f"The module `{PACKAGE}.constants` defines the endpoints and their values, e.g. for "
                "[`read_data()`](api.md#read_data) and [`write_data()`](api.md#write_data). "
                f"Paths are relative to `PAYLOAD_PREFIX` (`{module.PAYLOAD_PREFIX}`), "
                "`%s` is replaced by the zero-based device index."
            ),
            "## Endpoints",
        ]

        for section in sections:
            rows: list[str] = [
                self._row(
                    f"`{member.name}`",
                    member.value.value_type.__name__,
                    "no" if member.value.read_only else "yes",
                    self._enum_link(member.value.human_readable),
                    f"`{member.value.value.removeprefix(module.PAYLOAD_PREFIX + '.')}`",
                )
                for member in section
                if not member.name.startswith("_")
            ]
            blocks.extend(
                [
                    f"### {section.__name__}",
                    self._render_text(self._get_class("constants", section.__name__).docstring),
                    self._table(("Member", "Type", "Writable", "Values", "Path"), rows),
                ],
            )

        blocks.extend(
            [
                "## Values",
                "Enums of the readable names, returned with `human_readable=True` and accepted by the setters.",
            ],
        )

        for cls in values:
            rows = [self._row(f"`{member.name}`", f"`{member.value}`") for member in cls]
            blocks.extend(
                [
                    f"### {cls.__name__}",
                    self._render_text(self._get_class("constants", cls.__name__).docstring),
                    self._table(("Member", "Value"), rows),
                ],
            )

        blocks.extend(self._render_other_constants(module, [*sections, *values]))
        return "\n\n".join(block for block in blocks if block)

    @staticmethod
    def _row(*cells: str) -> str:
        return f"| {' | '.join(cells)} |"

    @staticmethod
    def _enum_link(enum: type[Enum] | None) -> str:
        return f"[`{enum.__name__}`](#{enum.__name__.lower()})" if enum else ""

    def _table(self, header: tuple[str, ...], rows: list[str]) -> str:
        return "\n".join([self._row(*header), self._row(*("---" for _ in header)), *rows])

    def _render_other_constants(self, module: ModuleType, documented: list[type[Enum]]) -> list[str]:
        blocks: list[str] = ["## Other constants"]
        rows: list[str] = [
            self._row(f"`{name}`", f"`{value!r}`")
            for name, value in vars(module).items()
            if name.isupper() and not name.startswith("_") and isinstance(value, int | str)
        ]
        blocks.append(self._table(("Name", "Value"), rows))

        for name, cls in vars(module).items():
            if not inspect.isclass(cls) or cls.__module__ != module.__name__ or name.startswith("_"):
                continue

            if cls in documented or cls is module.BaseEnum or issubclass(cls, module.Endpoint):
                continue

            members: dict[str, object] = (
                {member.name: member.value for member in cls}
                if issubclass(cls, Enum)
                else {key: value for key, value in vars(cls).items() if key.isupper()}
            )
            blocks.extend(
                [
                    f"### {name}",
                    self._render_text(self._get_class("constants", name).docstring),
                    self._table(("Member", "Value"), [self._row(f"`{k}`", f"`{v!r}`") for k, v in members.items()]),
                ],
            )

        return blocks

    @staticmethod
    def _title(name: str) -> str:
        return name.replace("_", " ").capitalize()

    def _render_section(self, name: str, section: griffe.Class) -> str:
        blocks: list[str] = [
            f"# {self._title(name)}",
            f"Endpoint group `{CLIENT}.{name}` ({section.name}).",
            self._render_docstring(section.docstring),
            *self._render_functions(section),
        ]
        return "\n\n".join(block for block in blocks if block)


if __name__ == "__main__":
    DocsGenerator(OUTPUT).run()
