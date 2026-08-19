# OpenGeoMetadata API Mirror Network

This repository contains a foundational proposal for a federated network of
OpenGeoMetadata API mirrors. The model pairs a shared, protected API endpoint
with independently hosted institutional mirrors and configurable `abcdefgeo`
frontends on GitHub Pages.

Open [the site landing page](index.html) to browse the complete proposal as a
static website.

## Director-ready materials

- [Executive summary](proposal/opengeometadata-mirror-network-executive-summary.md)
- [Executive summary - HTML](output/html/opengeometadata-mirror-network-executive-summary.html)
- [Architecture diagram](proposal/opengeometadata-mirror-network-architecture.svg)
- [Circulation-ready PDF](output/pdf/opengeometadata-mirror-network-executive-brief.pdf)

## Technical implementation materials

- [Technical implementation guide](proposal/opengeometadata-api-mirror-network-technical-implementation.md)
- [Standalone HTML preview](output/html/opengeometadata-api-mirror-network-technical-implementation.html)
- [Technical architecture diagram](proposal/opengeometadata-api-mirror-technical-flow.svg)
- [Cache strategy diagram](proposal/opengeometadata-api-mirror-cache-strategy.svg)

The PDF can be regenerated with:

```bash
python3 scripts/build_executive_brief.py
```

Both standalone HTML documents can be regenerated with:

```bash
python3 scripts/build_site.py
```

This requires Pandoc. The generated documents are self-contained: their CSS and
SVG diagrams are embedded so they remain portable outside the Pages site.

## GitHub Pages hosting

The repository includes a project-path-safe `index.html`, relative links, a
dependency-free site validator, and a GitHub Actions deployment workflow.

1. In the GitHub repository, open **Settings > Pages**.
2. Set **Source** to **GitHub Actions**.
3. Push to `main`, or run **Deploy GitHub Pages** manually from the Actions tab.

The workflow validates the committed HTML against its Markdown source, stages
only the public materials, and deploys them. Run the same validation locally:

```bash
python3 scripts/check_pages_site.py
```
