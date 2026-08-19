#!/usr/bin/env python3
"""Build the standalone HTML technical implementation guide."""

from pathlib import Path

from site_html import build_document


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "proposal" / "opengeometadata-api-mirror-network-technical-implementation.md"
OUTPUT = ROOT / "output" / "html" / "opengeometadata-api-mirror-network-technical-implementation.html"


def main() -> None:
    # Pandoc 1.x drops a leading section number when generating heading IDs,
    # while GitHub keeps it. Preserve GitHub-friendly Markdown and make the
    # standalone preview's hand-authored contents links match Pandoc's IDs.
    replacements: dict[str, str] = {}
    for number, section in enumerate((
        "purpose-and-design-principles",
        "runtime-architecture-at-each-institution",
        "metadata-synchronization-and-indexing",
        "public-traffic-failover-and-maintenance",
        "cache-architecture-and-cross-institution-sharing",
        "network-and-security-requirements",
        "monitoring-recovery-and-operating-responsibilities",
        "pilot-implementation-and-acceptance-tests",
        "implementation-decisions-to-ratify",
    ), start=1):
        replacements[f'href="#{number}-{section}"'] = f'href="#{section}"'

    replacements[
        'href="opengeometadata-mirror-network-executive-summary.md"'
    ] = 'href="opengeometadata-mirror-network-executive-summary.html"'
    replacements[
        'href="../output/pdf/opengeometadata-mirror-network-executive-brief.pdf"'
    ] = 'href="../pdf/opengeometadata-mirror-network-executive-brief.pdf"'

    result = build_document(
        source=SOURCE,
        output=OUTPUT,
        title="OpenGeoMetadata API Mirror Network - Technical Implementation Guide",
        description=(
            "Implementation details for institutional OGM API mirrors, GitHub metadata "
            "synchronization, indexing, caching, failover, security, and operations."
        ),
        active="technical",
        source_href="../../proposal/opengeometadata-api-mirror-network-technical-implementation.md",
        replacements=replacements,
    )
    print(result)


if __name__ == "__main__":
    main()
