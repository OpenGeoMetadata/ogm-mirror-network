#!/usr/bin/env python3
"""Build the circulation-ready OpenGeoMetadata API Mirror Network brief."""

from pathlib import Path
import subprocess

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
SVG_PATH = ROOT / "proposal" / "opengeometadata-mirror-network-architecture.svg"
PNG_PATH = ROOT / "tmp" / "pdfs" / "opengeometadata-mirror-network-architecture.png"
PDF_PATH = ROOT / "output" / "pdf" / "opengeometadata-mirror-network-executive-brief.pdf"

PAGE_W, PAGE_H = landscape(letter)

NAVY = HexColor("#073B4C")
TEAL = HexColor("#087F8C")
GREEN = HexColor("#2A9D68")
GOLD = HexColor("#D18B24")
INK = HexColor("#16363E")
MUTED = HexColor("#536E74")
PALE = HexColor("#F4F8F7")
PALE_TEAL = HexColor("#E5F3F2")
PALE_GREEN = HexColor("#E5F5EC")
PALE_GOLD = HexColor("#FFF0D8")
WHITE = HexColor("#FFFFFF")
BORDER = HexColor("#D6E2E0")
DRAFT_RED = HexColor("#7A271A")
DRAFT_GOLD = HexColor("#F6C56F")
DRAFT_NOTICE = (
    "DRAFT FOR COMMUNITY DISCUSSION - This proposal is under consideration by the "
    "OpenGeoMetadata community. It is not an approved OGM roadmap."
)


def style(size=10, leading=None, color=INK, font="Helvetica", alignment=TA_LEFT):
    return ParagraphStyle(
        name=f"p-{size}-{leading}-{font}-{alignment}",
        fontName=font,
        fontSize=size,
        leading=leading or size * 1.35,
        textColor=color,
        alignment=alignment,
        spaceAfter=0,
        spaceBefore=0,
    )


BODY = style(9.6, 13.2)
BODY_SMALL = style(8.4, 11.3)
BODY_TINY = style(6.7, 8.6, MUTED)
SECTION = style(10.2, 12.5, NAVY, "Helvetica-Bold")
CARD_TITLE = style(12, 14.5, NAVY, "Helvetica-Bold")
WHITE_BODY = style(10.2, 13.5, WHITE)


def paragraph(c, html, x, y_top, width, pstyle=BODY, max_height=1000):
    p = Paragraph(html, pstyle)
    used_w, used_h = p.wrap(width, max_height)
    p.drawOn(c, x, y_top - used_h)
    return used_h


def rounded_card(c, x, y, w, h, fill, stroke=BORDER, radius=12):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(0.7)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)


def page_header(c, section, page_number):
    c.setFillColor(DRAFT_RED)
    c.rect(0, PAGE_H - 26, PAGE_W, 26, fill=1, stroke=0)
    c.setFillColor(DRAFT_GOLD)
    c.rect(0, PAGE_H - 28, PAGE_W, 2, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 7.7)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 17, DRAFT_NOTICE)
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(36, PAGE_H - 43, section.upper())
    c.setFont("Helvetica", 7.5)
    c.drawRightString(PAGE_W - 36, PAGE_H - 43, f"AUGUST 2026  |  {page_number} / 2")


def footer(c):
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.line(36, 27, PAGE_W - 36, 27)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.8)
    c.drawString(36, 16, "OPEN GEOSPATIAL DISCOVERY INFRASTRUCTURE  |  OPEN SOURCE  |  COMMUNITY OPERATED")
    c.drawRightString(PAGE_W - 36, 16, "opengeometadata.org")


def draw_page_one(c):
    page_header(c, "Foundational proposal", 1)

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 27)
    c.drawString(36, 523, "OpenGeoMetadata API Mirror Network")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 14)
    c.drawString(36, 498, "Shared infrastructure that becomes stronger with every new member")

    left_x, left_w = 36, 235
    paragraph(c, "EXECUTIVE SUMMARY", left_x, 466, left_w, SECTION)
    summary = (
        "OpenGeoMetadata already has the essential building blocks: the OGM "
        "Aardvark schema, public GitHub metadata repositories, a proven API, and "
        "the configurable <b>OGM Discovery</b> (<b>ogm-discovery</b>) frontend for GitHub Pages.<br/><br/>"
        "The proposed mirror network adds a protected global endpoint in front "
        "of compatible institutional OGM API nodes. Mirror hosts contribute an "
        "ordinary Linux VM; the OGM operator deploys and updates the application "
        "with Kamal, synchronizes the corpus, monitors readiness, and routes "
        "traffic by health and capacity.<br/><br/>"
        "Capacity is pooled, not an admission requirement. Smaller libraries can "
        "publish metadata and launch a customizable, institution-branded discovery "
        "site against the shared API <i>without operating a local backend</i>. Mirror "
        "hosts add resilience for everyone; service-only adopters add collections, "
        "expertise, and public value."
    )
    paragraph(c, summary, left_x, 447, left_w, BODY, 330)

    rounded_card(c, 291, 151, 465, 315, WHITE)
    image = ImageReader(str(PNG_PATH))
    c.drawImage(image, 303, 164, width=441, height=287, preserveAspectRatio=True, mask="auto")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.4)
    c.drawRightString(744, 157, "Public read path, metadata synchronization, and shared operations")

    c.setFillColor(NAVY)
    c.roundRect(36, 53, 720, 76, 14, fill=1, stroke=0)
    paragraph(
        c,
        "<b>One contributed mirror becomes a community multiplier: it supports "
        "its host, strengthens the shared service, and opens a no-backend path for "
        "smaller institutions to join OpenGeoMetadata discovery.</b>",
        58,
        112,
        676,
        WHITE_BODY,
        54,
    )

    footer(c)
    c.showPage()


def draw_page_two(c):
    page_header(c, "Director decision brief", 2)

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 21.5)
    c.drawString(36, 531, "The smallest possible institutional ask; network-wide return")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10.5)
    c.drawString(36, 510, "Mirror hosts supply capacity. Service-only adopters need no backend. Every member benefits.")

    # Cost card
    rounded_card(c, 36, 328, 362, 162, PALE_TEAL)
    paragraph(c, "COST AND EFFORT", 54, 470, 325, SECTION)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(54, 426, "$1,500 / year")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8.8)
    c.drawString(54, 409, "planning target per externally purchased mirror node")
    paragraph(
        c,
        "<b>Reference:</b> 16 vCPU, 64 GB RAM, 500 GB usable SSD/NVMe, 1 Gbps.<br/>"
        "Sized from BTAA production; target 4-8 provisioning hours plus a few host-support hours per quarter.",
        54,
        389,
        325,
        BODY_SMALL,
        52,
    )
    c.setStrokeColor(HexColor("#9FC4C1"))
    c.setLineWidth(0.8)
    c.line(54, 349, 379, 349)
    paragraph(
        c,
        "<b>Campus VM: little or no incremental cost.</b><br/>"
        "<b>Service-only adopter: $0 API hosting.</b>",
        54,
        346,
        325,
        style(7.8, 8.6, NAVY, "Helvetica-Bold"),
        20,
    )

    # Value card
    rounded_card(c, 414, 328, 342, 162, PALE_GOLD)
    paragraph(c, "WHY THIS IS INEXPENSIVE", 432, 470, 306, SECTION)
    paragraph(
        c,
        "No local software project. No institution-specific backend. No frontend server. "
        "No cross-campus database replication. Public Aardvark records in GitHub remain "
        "canonical, so indexes and caches are rebuildable.<br/><br/>"
        "The closest public hardware benchmark is a 16-thread / 64 GB / 2x512 GB NVMe "
        "dedicated server at about $117 per month. Shared edge and monitoring costs are "
        "budgeted once for the network, not once per campus.",
        432,
        448,
        306,
        BODY_SMALL,
        112,
    )

    # Three responsibility / benefit cards
    cards = [
        (
            36,
            "MIRROR HOST PROVIDES",
            PALE,
            "One production VM<br/>Firewall, DNS, SSH, and OS coordination<br/>One service sponsor + one technical contact",
        ),
        (
            280,
            "OGM OPERATES",
            PALE_GREEN,
            "Kamal install, drain, update, and rollback<br/>Harvest, index, cache, and monitor<br/>Health-aware traffic weights + incidents",
        ),
        (
            524,
            "COMMUNITY-WIDE RETURN",
            PALE_TEAL,
            "Service-only adoption with no backend<br/>Customizable, institution-branded discovery<br/>More metadata, capacity, and resilience",
        ),
    ]
    for x, heading, fill, copy in cards:
        rounded_card(c, x, 178, 232, 126, fill)
        paragraph(c, heading, x + 16, 286, 200, SECTION)
        paragraph(c, copy, x + 16, 260, 200, BODY_SMALL, 80)

    # Pilot and decision bar
    c.setFillColor(NAVY)
    c.roundRect(36, 58, 720, 96, 14, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(55, 129, "DECISION REQUESTED")
    paragraph(
        c,
        "Approve a <b>90-day pilot</b>: the current BTAA node plus two additional "
        "institutional mirrors and one service-only adopter. Measure onboarding, "
        "cost, API compatibility, corpus freshness, traffic distribution, bot "
        "protection, failover, and infrastructure-free adoption. Return with a "
        "production governance and service-level proposal.",
        55,
        114,
        680,
        WHITE_BODY,
        62,
    )

    # Source line stays above the standard footer.
    source_text = (
        "Planning sources: opengeometadata.org; github.com/opengeometadata; "
        "github.com/geobtaa/api; github.com/ewlarson/ogm-api; github.com/ewlarson/ogm-discovery; "
        "Hetzner price adjustment (2026-06-15); Cloudflare Load Balancing docs."
    )
    paragraph(c, source_text, 36, 46, 720, BODY_TINY, 18)
    footer(c)
    c.showPage()


def add_metadata(c):
    c.setTitle("OpenGeoMetadata API Mirror Network - Executive Brief")
    c.setAuthor("OpenGeoMetadata community proposal")
    c.setSubject("A federated network of institution-hosted OGM API mirrors")
    c.setKeywords("OpenGeoMetadata, Aardvark, OGM API, OGM Discovery, ogm-discovery, mirror network")


def main():
    PNG_PATH.parent.mkdir(parents=True, exist_ok=True)
    PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "rsvg-convert",
            "--width",
            "2400",
            "--height",
            "1560",
            "--output",
            str(PNG_PATH),
            str(SVG_PATH),
        ],
        check=True,
    )

    c = canvas.Canvas(str(PDF_PATH), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    add_metadata(c)
    draw_page_one(c)
    draw_page_two(c)
    c.save()
    print(PDF_PATH)


if __name__ == "__main__":
    main()
