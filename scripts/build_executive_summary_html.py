#!/usr/bin/env python3
"""Build the standalone HTML Executive Summary."""

from pathlib import Path

from site_html import build_document


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "proposal" / "opengeometadata-mirror-network-executive-summary.md"
OUTPUT = ROOT / "output" / "html" / "opengeometadata-mirror-network-executive-summary.html"


def main() -> None:
    result = build_document(
        source=SOURCE,
        output=OUTPUT,
        title="OpenGeoMetadata API Mirror Network - Executive Summary",
        description=(
            "A director-ready proposal for a low-cost, health-aware network of "
            "institutional OpenGeoMetadata API mirrors."
        ),
        active="executive",
        source_href="../../proposal/opengeometadata-mirror-network-executive-summary.md",
        replacements={
            'href="opengeometadata-api-mirror-network-technical-implementation.md"':
                'href="opengeometadata-api-mirror-network-technical-implementation.html"',
        },
    )
    print(result)


if __name__ == "__main__":
    main()
