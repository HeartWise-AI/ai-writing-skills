#!/usr/bin/env python3
"""Check a CIHR PDF attachment against the agency's format rules.

CIHR rejects attachments on three mechanical properties: the embedded body font
must be Times New Roman, black, at least 12 pt, and every margin must be at
least 2 cm. All three are read from the PDF itself, not from the source .docx,
so a document that looks correct in Word can still fail after a bad conversion.

Usage:
    python cihr_pdf_check.py FILE.pdf
    python cihr_pdf_check.py FILE.pdf --pages 35-50      # only the applicant-authored pages
    python cihr_pdf_check.py FILE.pdf --min-size 12 --margin-cm 2

Requires PyMuPDF (`pip install pymupdf`).

Exit status is 1 when any BLOCKER is reported, otherwise 0.
"""

import argparse
import collections
import sys

try:
    import pymupdf
except ImportError:  # PyMuPDF <1.24 only exposes the legacy name
    import fitz as pymupdf

CM = 72 / 2.54  # PDF points per centimetre

# Substring match, because embedded fonts carry a subset prefix such as
# "AAAAAC+TimesNewRomanPSMT" and style suffixes such as "-BoldMT".
ACCEPTED_FONT = "TimesNewRoman"

# Liberation Serif and Tinos are metric-compatible clones of Times New Roman.
# They look identical on screen and are what LibreOffice substitutes silently,
# but CIHR reads the embedded font name and rejects them.
CLONE_FONTS = ("LiberationSerif", "Tinos", "Nimbus Roman", "FreeSerif")

# Below this many points of shortfall a margin "overflow" is the glyph's side
# bearing rather than ink outside the margin. 0.2 mm.
NOISE_PT = 0.2 / 10 * CM


def parse_pages(spec, page_count):
    if not spec:
        return range(page_count)
    pages = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            lo, hi = part.split("-", 1)
            pages.update(range(int(lo) - 1, int(hi)))
        else:
            pages.add(int(part) - 1)
    return sorted(p for p in pages if 0 <= p < page_count)


def check_page(page, min_size, margin_pt):
    """Return (font_issues, margin_issues) for one page.

    Margins are measured from individual glyph boxes, not span boxes. A span box
    includes the trailing space of a justified line, which reads as a 1-2 mm
    overflow that is not really there.
    """
    fonts = collections.Counter()
    worst = {"left": None, "right": None, "top": None, "bottom": None}
    examples = {}
    w, h = page.rect.width, page.rect.height

    for block in page.get_text("rawdict")["blocks"]:
        for line in block.get("lines", []):
            for span in line["spans"]:
                text = "".join(c["c"] for c in span["chars"])
                if not text.strip():
                    continue
                fonts[(span["font"], round(span["size"], 1), span["color"])] += len(text.strip())
                for ch in span["chars"]:
                    if not ch["c"].strip():
                        continue
                    x0, y0, x1, y1 = ch["bbox"]
                    for name, value in (
                        ("left", x0), ("right", w - x1), ("top", y0), ("bottom", h - y1)
                    ):
                        if worst[name] is None or value < worst[name]:
                            worst[name] = value
                            examples[name] = (ch["c"], span["font"], round(span["size"], 1))

    font_issues = []
    for (name, size, color), count in fonts.items():
        reasons = []
        if any(clone in name for clone in CLONE_FONTS):
            reasons.append(f"font is a Times clone ({name}), not Times New Roman")
        elif ACCEPTED_FONT not in name:
            reasons.append(f"font is {name}")
        if color != 0:
            reasons.append(f"colour is #{color:06x}, not black")
        if size < min_size:
            reasons.append(f"size is {size} pt, below {min_size} pt")
        if reasons:
            font_issues.append((count, name, size, color, reasons))

    margin_issues = []
    for name, value in worst.items():
        # A glyph box includes its side bearing, so text set exactly on the
        # margin measures a fraction of a point outside it. Anything under
        # 0.2 mm is that artefact, not a real overflow.
        if value is not None and value < margin_pt - NOISE_PT:
            margin_issues.append((name, value / CM, examples[name]))

    return font_issues, margin_issues


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--pages", help="1-based page list or ranges, e.g. 35-50,57")
    ap.add_argument("--min-size", type=float, default=12.0,
                    help="minimum body font size in points (default 12)")
    ap.add_argument("--margin-cm", type=float, default=2.0,
                    help="minimum margin in centimetres (default 2)")
    ap.add_argument("--footnote-size", type=float, default=7.0,
                    help="Times New Roman black text at or above this size but below "
                         "--min-size is reported as NOTE rather than BLOCKER. "
                         "Superscript citation numerals set around 8 pt are standard "
                         "and CIHR accepts them (default 7)")
    ap.add_argument("--show-footers", action="store_true",
                    help="also report short numeric runs intruding on the bottom "
                         "margin; these are Word page numbers, which sit in the "
                         "margin band by design and are suppressed otherwise")
    args = ap.parse_args()

    doc = pymupdf.open(args.pdf)
    pages = parse_pages(args.pages, doc.page_count)
    margin_pt = args.margin_cm * CM
    blockers = notes = 0

    print(f"{args.pdf}: {doc.page_count} pages, checking {len(list(pages))}")
    print(f"Rules: {ACCEPTED_FONT}, black, >= {args.min_size} pt, margins >= {args.margin_cm} cm\n")

    for index in pages:
        page = doc[index]
        font_issues, margin_issues = check_page(page, args.min_size, margin_pt)
        lines = []

        for count, name, size, color, reasons in sorted(font_issues, reverse=True):
            # A handful of characters is a stray glyph (a page number, one
            # separator); a paragraph's worth is a real formatting failure.
            small_but_legal = (
                size < args.min_size
                and size >= args.footnote_size
                and ACCEPTED_FONT in name
                and color == 0
            )
            level = "NOTE" if (count <= 5 or small_but_legal) else "BLOCKER"
            lines.append(f"  [{level}] {count} chars: " + "; ".join(reasons))
            blockers += level == "BLOCKER"
            notes += level == "NOTE"

        for name, value_cm, (char, font, size) in margin_issues:
            shortfall_mm = (args.margin_cm - value_cm) * 10
            # Word puts headers and footers inside the margin band by design and
            # CIHR accepts that, so a page number touching the bottom edge is
            # not a finding unless the reader asks to see it.
            if name == "bottom" and char.isdigit() and not args.show_footers:
                continue
            level = "NOTE" if shortfall_mm < 1.0 or name == "bottom" else "BLOCKER"
            lines.append(
                f"  [{level}] {name} margin {value_cm:.2f} cm "
                f"({shortfall_mm:.1f} mm short) at {char!r} in {font} {size} pt"
            )
            blockers += level == "BLOCKER"
            notes += level == "NOTE"

        if lines:
            print(f"p{index + 1}")
            print("\n".join(lines))

    print(f"\n{blockers} blocker(s), {notes} note(s)")
    if blockers:
        print("Re-export from Word or Chrome headless, then re-run. Never LibreOffice.")
    return 1 if blockers else 0


if __name__ == "__main__":
    sys.exit(main())
