#!/usr/bin/env python3
"""Build every generated HTML document used by the GitHub Pages site."""

from build_executive_summary_html import main as build_executive_summary
from build_technical_implementation_html import main as build_technical_guide


def main() -> None:
    build_executive_summary()
    build_technical_guide()


if __name__ == "__main__":
    main()
