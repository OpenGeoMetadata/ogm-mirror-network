#!/usr/bin/env python3
"""Shared helpers for building self-contained OpenGeoMetadata HTML documents."""

from __future__ import annotations

from base64 import b64encode
from hashlib import sha256
from html import escape
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "assets" / "technical-implementation.css"
FAVICON = ROOT / "assets" / "favicon.svg"
PANDOC_READER = (
    "markdown+yaml_metadata_block+pipe_tables+fenced_code_blocks+backtick_code_blocks"
)
LEGACY_HTML5_SHIM = (
    '  <!--[if lt IE 9]>\n'
    '    <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>\n'
    '  <![endif]-->\n'
)
DRAFT_NOTICE = (
    "DRAFT/DISCUSSION — This is an OpenGeoMetadata Community discussion topic of interest. "
    "This is not a OGM approved roadmap."
)


def _site_navigation(active: str) -> str:
    executive_class = ' class="active" aria-current="page"' if active == "executive" else ""
    technical_class = ' class="active" aria-current="page"' if active == "technical" else ""
    banner_label, banner_detail = DRAFT_NOTICE.split(" — ", 1)
    return (
        '<a class="skip-link" href="#main-content">Skip to content</a>\n'
        '<div class="draft-banner" role="note" aria-label="Draft status">\n'
        f'  <strong>{escape(banner_label)}</strong> — {escape(banner_detail)}\n'
        '</div>\n'
        '<header class="site-nav" aria-label="Site header">\n'
        '  <a class="site-brand" href="../../index.html">OpenGeoMetadata</a>\n'
        '  <nav aria-label="Primary navigation">\n'
        f'    <a{executive_class} href="opengeometadata-mirror-network-executive-summary.html">Executive summary</a>\n'
        f'    <a{technical_class} href="opengeometadata-api-mirror-network-technical-implementation.html">Technical guide</a>\n'
        '  </nav>\n'
        '</header>\n'
        '<main id="main-content">\n'
    )


def _site_footer(source_href: str) -> str:
    return (
        '</main>\n'
        '<footer class="site-footer">\n'
        '  <p><strong>OpenGeoMetadata API Mirror Network</strong></p>\n'
        f'  <p><a href="{escape(source_href, quote=True)}">View Markdown source</a> · '
        '<a href="https://opengeometadata.org/">OpenGeoMetadata</a> · '
        '<a href="https://github.com/OpenGeoMetadata">GitHub repositories</a></p>\n'
        '</footer>\n'
    )


def build_document(
    *,
    source: Path,
    output: Path,
    title: str,
    description: str,
    active: str,
    source_href: str,
    replacements: dict[str, str] | None = None,
) -> Path:
    """Render Markdown to a self-contained, navigable HTML document."""
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "pandoc",
            str(source),
            f"--from={PANDOC_READER}",
            "--to=html5",
            "--standalone",
            "--self-contained",
            "--css",
            str(CSS),
            "--metadata",
            f"pagetitle={title}",
            "--output",
            str(output),
        ],
        check=True,
        cwd=source.parent,
    )

    source_digest = sha256(source.read_bytes()).hexdigest()
    favicon_data = b64encode(FAVICON.read_bytes()).decode("ascii")
    html = output.read_text(encoding="utf-8").replace(LEGACY_HTML5_SHIM, "")
    for old, new in (replacements or {}).items():
        html = html.replace(old, new)

    metadata = (
        f'  <meta name="description" content="{escape(description, quote=True)}">\n'
        f'  <meta name="ogm-source-sha256" content="{source_digest}">\n'
        f'  <meta property="og:title" content="{escape(title, quote=True)}">\n'
        f'  <meta property="og:description" content="{escape(description, quote=True)}">\n'
        f'  <link rel="icon" href="data:image/svg+xml;base64,{favicon_data}" type="image/svg+xml">\n'
    )
    html = html.replace("</head>", f"{metadata}</head>", 1)
    html = html.replace(
        "<body>\n",
        f'<body class="document-page">\n{_site_navigation(active)}',
        1,
    )
    html = html.replace("\n</body>", f"\n{_site_footer(source_href)}</body>", 1)
    output.write_text(html, encoding="utf-8")
    return output
