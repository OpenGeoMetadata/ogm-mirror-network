#!/usr/bin/env python3
"""Validate the committed GitHub Pages site without third-party dependencies."""

from __future__ import annotations

from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    ROOT / "index.html",
    ROOT / "output" / "html" / "opengeometadata-mirror-network-executive-summary.html",
    ROOT
    / "output"
    / "html"
    / "opengeometadata-api-mirror-network-technical-implementation.html",
)
SOURCE_BY_PAGE = {
    PAGES[1]: ROOT / "proposal" / "opengeometadata-mirror-network-executive-summary.md",
    PAGES[2]: ROOT
    / "proposal"
    / "opengeometadata-api-mirror-network-technical-implementation.md",
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.references: list[tuple[str, str]] = []
        self.h1_count = 0
        self.source_digest: str | None = None
        self.external_scripts: list[str] = []
        self.draft_banner_count = 0
        self.draft_banner_text: list[str] = []
        self._inside_draft_banner = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value for key, value in attrs if value is not None}
        if element_id := values.get("id"):
            self.ids.add(element_id)
        if tag == "h1":
            self.h1_count += 1
        if tag == "meta" and values.get("name") == "ogm-source-sha256":
            self.source_digest = values.get("content")
        if tag == "script" and (src := values.get("src")):
            self.external_scripts.append(src)
        classes = set(values.get("class", "").split())
        if tag == "div" and "draft-banner" in classes:
            self.draft_banner_count += 1
            self._inside_draft_banner = True
        for attribute in ("href", "src"):
            if reference := values.get(attribute):
                self.references.append((attribute, reference))

    def handle_endtag(self, tag: str) -> None:
        if tag == "div" and self._inside_draft_banner:
            self._inside_draft_banner = False

    def handle_data(self, data: str) -> None:
        if self._inside_draft_banner:
            self.draft_banner_text.append(data)


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def resolve_reference(page: Path, reference: str) -> tuple[Path, str]:
    split = urlsplit(reference)
    target = page if not split.path else (page.parent / unquote(split.path)).resolve()
    return target, unquote(split.fragment)


def main() -> None:
    errors: list[str] = []
    parsed: dict[Path, PageParser] = {}

    for page in PAGES:
        if not page.is_file():
            errors.append(f"missing page: {page.relative_to(ROOT)}")
            continue
        parser = parse_page(page)
        parsed[page] = parser
        if parser.h1_count != 1:
            errors.append(
                f"{page.relative_to(ROOT)}: expected exactly one h1, found {parser.h1_count}"
            )
        if parser.external_scripts:
            errors.append(
                f"{page.relative_to(ROOT)}: external scripts are not allowed: "
                f"{', '.join(parser.external_scripts)}"
            )
        expected_notice = (
            "DRAFT FOR COMMUNITY DISCUSSION — This proposal is under consideration by "
            "the OpenGeoMetadata community. It is not an approved OGM roadmap."
        )
        actual_notice = " ".join("".join(parser.draft_banner_text).split())
        if parser.draft_banner_count != 1 or actual_notice != expected_notice:
            errors.append(
                f"{page.relative_to(ROOT)}: missing or incorrect public draft banner"
            )

    for page, source in SOURCE_BY_PAGE.items():
        parser = parsed.get(page)
        if parser is None:
            continue
        expected_digest = sha256(source.read_bytes()).hexdigest()
        if parser.source_digest != expected_digest:
            errors.append(
                f"{page.relative_to(ROOT)} is stale; run python3 scripts/build_site.py"
            )

    for page, parser in parsed.items():
        for attribute, reference in parser.references:
            split = urlsplit(reference)
            if split.scheme in {"http", "https", "mailto", "data"}:
                continue
            if split.scheme or split.netloc:
                errors.append(f"{page.relative_to(ROOT)}: unsupported URL {reference}")
                continue
            if reference.startswith("/"):
                errors.append(
                    f"{page.relative_to(ROOT)}: root-relative URL breaks project Pages: {reference}"
                )
                continue

            target, fragment = resolve_reference(page, reference)
            try:
                target.relative_to(ROOT)
            except ValueError:
                errors.append(f"{page.relative_to(ROOT)}: URL escapes repository: {reference}")
                continue
            if not target.exists():
                errors.append(f"{page.relative_to(ROOT)}: broken {attribute}: {reference}")
                continue
            if fragment and target.suffix.lower() == ".html":
                target_parser = parsed.get(target) or parse_page(target)
                if fragment not in target_parser.ids:
                    errors.append(
                        f"{page.relative_to(ROOT)}: missing anchor #{fragment} in "
                        f"{target.relative_to(ROOT)}"
                    )

    required_files = (
        ROOT / "assets" / "technical-implementation.css",
        ROOT / "assets" / "favicon.svg",
        ROOT / "output" / "pdf" / "opengeometadata-mirror-network-executive-brief.pdf",
        ROOT / "proposal" / "opengeometadata-mirror-network-architecture.svg",
        ROOT / "proposal" / "opengeometadata-api-mirror-technical-flow.svg",
        ROOT / "proposal" / "opengeometadata-api-mirror-cache-strategy.svg",
    )
    for required in required_files:
        if not required.is_file():
            errors.append(f"missing site asset: {required.relative_to(ROOT)}")

    if errors:
        raise SystemExit("GitHub Pages validation failed:\n- " + "\n- ".join(errors))

    reference_count = sum(len(parser.references) for parser in parsed.values())
    print(f"GitHub Pages site valid: {len(parsed)} pages, {reference_count} references checked")


if __name__ == "__main__":
    main()
