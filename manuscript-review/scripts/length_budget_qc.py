#!/usr/bin/env python3
"""Length, information-density, and redundancy QC for medical-AI manuscript drafts.

Implements the Step 0.5 gate of the manuscript-review skill:

  1. Word budget per section, subsection, and paragraph, plus the Introduction
     paragraph cap.
  2. Negative-space sentences that justify an absence instead of reporting a result.
  3. Material repeated between Introduction, Methods, and Discussion.

Tables and figure legends are excluded from the counts, matching the budgets in
SKILL.md, which are main-text only.

Usage:
    python length_budget_qc.py draft.docx
    python length_budget_qc.py draft.md --abstract-limit 250
    python length_budget_qc.py draft.md --no-fail
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from xml.etree import ElementTree

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

WORDS_PER_LINE = 13
WORDS_PER_PAGE = 500

# Whole-section word budgets. See SKILL.md Step 0.5. The Abstract is deliberately
# absent: its budget is the target journal's limit, supplied with --abstract-limit.
SECTION_BUDGETS = {
    "introduction": 500,
    "background": 500,
    "methods": 1000,
    "results": 750,
    "discussion": 900,
    "limitations": 200,
    "conclusion": 250,
}

# 10 lines. SKILL.md applies this to Methods subsections only; subsections elsewhere
# are governed by their section and paragraph budgets, so they are reported for
# information and do not fail the gate.
SUBSECTION_BUDGET = 130
SUBSECTION_BUDGET_SECTIONS = ("methods",)

PARAGRAPH_BUDGETS = {
    "results": 65,  # 5 lines
    "discussion": 50,  # 4 lines
}

PARAGRAPH_COUNT_BUDGETS = {
    "introduction": 4,
    "background": 4,
}

SECTION_NAMES = (
    "abstract",
    "background",
    "introduction",
    "methods",
    "results",
    "discussion",
    "limitations",
    "conclusion",
    "references",
)

# A bare section name resolves anywhere, including an unstyled all-caps paragraph,
# which is how many Word manuscripts mark RESULTS and DISCUSSION. A trailing colon
# is excluded on purpose: "BACKGROUND:" on its own line is a structured abstract's
# run-in label, not a section heading.
SECTION_EXACT_RE = re.compile(
    r"^\s*(?:#{1,6}\s*)?(" + "|".join(SECTION_NAMES) + r")\s*$",
    re.IGNORECASE,
)

# Trailing descriptive text ("METHODS AND MATERIALS") resolves only for a real
# heading. Applying this to unstyled paragraphs breaks structured abstracts, whose
# "Background: ..." and "Results: ..." run-in labels would each open a new section.
SECTION_HEADING_RE = re.compile(
    r"^\s*(?:#{1,6}\s*)?(" + "|".join(SECTION_NAMES) + r")\b[\s:.,;-]+(?:.*)$",
    re.IGNORECASE,
)
MAX_HEADING_WORDS = 8

CAPTION_RE = re.compile(
    r"^\s*(?:supplementary\s+|extended\s+data\s+|online\s+)?"
    r"(?:table|figure|fig\.?|chart|panel|box|appendix|e?table|e?figure)\s*"
    r"(?:[0-9ivxIVX]+|S[0-9]+)\b",
    re.IGNORECASE,
)

# Sentences whose only function is to justify an absence.
NEGATIVE_SPACE = [
    (r"\bno\s+(?:formal\s+)?(?:sample[- ]size|power)\s+calculation\b", "sample-size non-calculation"),
    (r"\bwe\s+(?:do|did)\s+not\s+report\b", "metric non-reporting rationale"),
    (r"\b(?:was|were|is|are)\s+not\s+(?:required|obtained|sought|requested|necessary)\b", "approval or consent non-action"),
    (r"\bis\s+not\s+applicable\b", "not-applicable filler"),
    (r"\bno\s+waiver\s+(?:was\s+)?sought\b", "waiver non-action"),
    (r"\bdoes\s+not\s+constitute\s+human[- ]subjects\s+research\b", "pre-emptive ethics defence"),
    # Anchored to a metric. Unanchored, this matched any clause of the form
    # "the effect, which varies by age, was largest", which is a substantive result.
    (
        r"\b(?:AUROC|AUPRC|AUC|F1|accuracy|sensitivity|specificity|precision|recall|"
        r"prevalence|the\s+metric|this\s+metric)\b[^.]{0,60}?,?\s*which\s+"
        r"(?:varies|depends|suits|conflates|ignores)\b",
        "rationale for a standard method",
    ),
    (r"\bis\s+interpreted\s+against\s+its\b", "metric pedagogy"),
    (r"\brather\s+than\s+(?:intervention|inferring)\b", "meta-commentary on approach"),
    (r"\bare\s+computed\s+from\s+the\s+analy[sz]ed\s+cohort\s+itself\b", "self-evident provenance"),
]

# A negative that is a required reporting element keeps its place.
REQUIRED_NEGATIVE = re.compile(
    r"multipl(?:e\s+compar|icity)|missing\s+data|fairness\s+constraint|reweighting"
    r"|de-?biasing|group-specific\s+threshold|prospective|censor",
    re.IGNORECASE,
)

REDUNDANCY_N = 5
REDUNDANCY_PAIRS = [
    ("introduction", "methods"),
    ("introduction", "discussion"),
    ("methods", "discussion"),
]

NARRATIVE_SECTIONS = ("introduction", "background", "methods", "discussion")

ENTITY_RE = re.compile(r"\b(?:[A-Z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)+|[A-Z]{3,})\b")
STOP_ENTITIES = {"AUROC", "AUPRC", "ECG", "ECGS", "AND", "THE", "FOR", "WITH", "NOT", "ALL"}


@dataclass
class Unit:
    kind: str  # section | subsection
    name: str
    section: str
    paragraphs: list[str] = field(default_factory=list)

    @property
    def words(self) -> int:
        return sum(len(p.split()) for p in self.paragraphs)


def read_paragraphs(path: Path | None) -> list[tuple[str, str]]:
    """Return [(style, text)] where style is 'h1', 'h2' or ''."""
    if path is not None and path.suffix.lower() == ".docx":
        return read_docx(path)
    text = path.read_text(encoding="utf-8") if path else sys.stdin.read()
    return parse_markdown(text)


def parse_markdown(text: str) -> list[tuple[str, str]]:
    """Parse Markdown, honouring heading levels and blank-line paragraph breaks.

    Conventionally wrapped prose must be joined: treating each physical line as a
    paragraph lets a 100-word paragraph slip under a 65-word budget.
    """
    out: list[tuple[str, str]] = []
    buffer: list[str] = []

    def flush() -> None:
        if buffer:
            out.append(("", " ".join(buffer).strip()))
            buffer.clear()

    for raw in text.split("\n"):
        line = raw.strip()
        if not line:
            flush()
            continue
        if line.startswith("#"):
            flush()
            level = len(line) - len(line.lstrip("#"))
            heading = line[level:].strip()
            # A canonical section name is a section at any heading level, so that
            # "# Methods" then "## Statistical analysis" nests correctly.
            out.append(("h1" if normalize_section(heading, styled=True) else "h2", heading))
            continue
        if CAPTION_RE.match(line):
            flush()
            continue
        buffer.append(line)
    flush()
    return out


def iter_body_paragraphs(root: ElementTree.Element) -> list[ElementTree.Element]:
    """Yield w:p elements outside of tables, in document order."""
    found: list[ElementTree.Element] = []

    def walk(node: ElementTree.Element) -> None:
        for child in node:
            if child.tag == W + "tbl":
                continue  # table content is excluded from main-text budgets
            if child.tag == W + "p":
                found.append(child)
            else:
                walk(child)

    body = root.find(W + "body")
    walk(body if body is not None else root)
    return found


def read_docx(path: Path) -> list[tuple[str, str]]:
    with zipfile.ZipFile(path) as archive:
        try:
            xml_bytes = archive.read("word/document.xml")
        except KeyError as exc:
            raise SystemExit(f"{path}: not a valid docx file") from exc
    root = ElementTree.fromstring(xml_bytes)
    out: list[tuple[str, str]] = []
    for p in iter_body_paragraphs(root):
        # w:t only, so text marked deleted (w:delText) is excluded and a
        # tracked-change draft measures its accepted state.
        text = "".join(node.text or "" for node in p.iter(W + "t")).strip()
        if not text:
            continue
        style_node = p.find(f"{W}pPr/{W}pStyle")
        style = style_node.get(W + "val") if style_node is not None else ""
        if "caption" in style.lower() or CAPTION_RE.match(text):
            continue  # figure legends and table titles are not main text
        if style.startswith("Heading1"):
            out.append(("h1", text))
        elif style.startswith("Heading") and style != "Heading1":
            out.append(("h2", text))
        else:
            out.append(("", text))
    return out


def normalize_section(name: str, styled: bool = False) -> str | None:
    """Resolve a heading to a canonical section name.

    `styled` means the source marked this as a heading (a Markdown `#` line or a
    Word Heading style). Only then is trailing descriptive text allowed.
    """
    match = SECTION_EXACT_RE.match(name)
    if match:
        return match.group(1).lower()
    if styled and len(name.split()) <= MAX_HEADING_WORDS:
        match = SECTION_HEADING_RE.match(name)
        if match:
            return match.group(1).lower()
    return None


def build_units(paragraphs: list[tuple[str, str]]) -> list[Unit]:
    units: list[Unit] = []
    section = "front matter"
    current: Unit | None = None

    for style, text in paragraphs:
        styled = style in ("h1", "h2")
        as_section = normalize_section(text, styled=styled)
        # Inside an Abstract, an unstyled "Methods"/"Results" line is a run-in label
        # for the abstract's own structure, not the start of the real section.
        if as_section and section == "abstract" and not styled and as_section != "abstract":
            as_section = None
        if as_section:
            section = as_section
            current = Unit("section", section, section)
            units.append(current)
            continue
        if style in ("h1", "h2"):
            current = Unit("subsection", text, section)
            units.append(current)
            continue
        if current is None:
            current = Unit("section", section, section)
            units.append(current)
        current.paragraphs.append(text)
    return units


def sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def shingles(text: str, n: int = REDUNDANCY_N) -> set[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {" ".join(words[i : i + n]) for i in range(max(0, len(words) - n + 1))}


def report_budgets(units: list[Unit], abstract_limit: int | None) -> int:
    failures = 0
    budgets = dict(SECTION_BUDGETS)
    if abstract_limit is not None:
        budgets["abstract"] = abstract_limit

    section_totals: dict[str, int] = {}
    section_paragraphs: dict[str, int] = {}
    for unit in units:
        if unit.section in ("references", "front matter"):
            continue
        section_totals[unit.section] = section_totals.get(unit.section, 0) + unit.words
        section_paragraphs[unit.section] = section_paragraphs.get(unit.section, 0) + len(unit.paragraphs)

    print("== Section budgets ==")
    for section, words in section_totals.items():
        budget = budgets.get(section)
        if budget is None:
            if section == "abstract":
                print(
                    f"  [info] abstract       {words:6d} w  "
                    f"budget is the journal limit; pass --abstract-limit N to enforce"
                )
            continue
        over = words > budget
        failures += over
        print(
            f"  [{'OVER' if over else 'ok':4s}] {section:14s} {words:6d} w "
            f"(~{words / WORDS_PER_PAGE:.1f} pages)  budget {budget} w  "
            f"ratio {words / budget:.1f}x"
        )

    print("\n== Paragraph-count budgets ==")
    any_count = False
    for section, limit in PARAGRAPH_COUNT_BUDGETS.items():
        if section not in section_paragraphs:
            continue
        any_count = True
        count = section_paragraphs[section]
        over = count > limit
        failures += over
        print(f"  [{'OVER' if over else 'ok':4s}] {section:14s} {count} paragraphs  budget {limit}")
    if not any_count:
        print("  (no budgeted sections found)")

    print(f"\n== Subsection budgets ({SUBSECTION_BUDGET} words, enforced in Methods) ==")
    any_sub = False
    for unit in units:
        if unit.kind != "subsection" or not unit.words:
            continue
        any_sub = True
        enforced = unit.section in SUBSECTION_BUDGET_SECTIONS
        over = unit.words > SUBSECTION_BUDGET
        if over and enforced:
            failures += 1
            status = "OVER"
        elif over:
            status = "info"
        else:
            status = "ok"
        print(
            f"  [{status:4s}] {unit.name[:40]:40s} ({unit.section[:10]:10s}) {unit.words:5d} w "
            f"(~{unit.words / WORDS_PER_LINE:.0f} lines)"
        )
    if not any_sub:
        print("  (no subsection headings detected)")

    print("\n== Over-budget paragraphs ==")
    any_para = False
    for unit in units:
        budget = PARAGRAPH_BUDGETS.get(unit.section)
        if budget is None:
            continue
        for paragraph in unit.paragraphs:
            words = len(paragraph.split())
            if words > budget:
                any_para = True
                failures += 1
                print(
                    f"  [OVER] {unit.section:10s} {words:4d} w (budget {budget}): "
                    f"{' '.join(paragraph.split()[:14])}..."
                )
    if not any_para:
        print("  none")
    return failures


def report_negative_space(units: list[Unit]) -> int:
    print("\n== Negative-space sentences (report what you did, not what you did not) ==")
    hits = 0
    for unit in units:
        for paragraph in unit.paragraphs:
            for sentence in sentences(paragraph):
                for pattern, label in NEGATIVE_SPACE:
                    if re.search(pattern, sentence, re.IGNORECASE):
                        required = bool(REQUIRED_NEGATIVE.search(sentence))
                        tag = "KEEP?" if required else "CUT"
                        if not required:
                            hits += 1
                        print(f"  [{tag:5s}] {unit.section:12s} {label}")
                        print(f"          {' '.join(sentence.split())[:150]}")
                        break
    if not hits:
        print("  none requiring deletion")
    return hits


def report_redundancy(units: list[Unit]) -> int:
    """Verbatim repetition plus entities described in more than one section.

    Verbatim overlap is a defect and counts toward the gate. The entity pass is a
    weaker signal (a model must be named in Results as well as Methods), so it is
    advisory and reported for human judgement.
    """
    print(f"\n== Cross-section repetition ({REDUNDANCY_N}-word spans) ==")
    text_by_section: dict[str, list[str]] = {}
    for unit in units:
        text_by_section.setdefault(unit.section, []).extend(unit.paragraphs)

    total = 0
    for left, right in REDUNDANCY_PAIRS:
        if left not in text_by_section or right not in text_by_section:
            continue
        shared = shingles(" ".join(text_by_section[left])) & shingles(
            " ".join(text_by_section[right])
        )
        if not shared:
            continue
        total += len(shared)
        print(f"  [OVER] {left} <-> {right}: {len(shared)} shared spans")
        for span in sorted(shared)[:5]:
            print(f"      \"{span}\"")
    if not total:
        print("  no verbatim overlap")

    print("\n== Entities introduced in more than one section (advisory) ==")
    counts: dict[str, dict[str, int]] = {}
    for section in NARRATIVE_SECTIONS:
        for paragraph in text_by_section.get(section, []):
            for entity in ENTITY_RE.findall(paragraph):
                if entity.upper() in STOP_ENTITIES or len(entity) < 4:
                    continue
                counts.setdefault(entity, {})
                counts[entity][section] = counts[entity].get(section, 0) + 1

    flagged = 0
    for entity, per_section in sorted(counts.items(), key=lambda kv: -sum(kv[1].values())):
        if len(per_section) >= 2:
            flagged += 1
            spread = ", ".join(f"{s}={per_section[s]}" for s in sorted(per_section))
            print(f"  {entity:38s} {spread}")
    if not flagged:
        print("  none")
    else:
        print("  Describe each once and cite it from the other location (Step 0.5).")
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, help="Draft docx, Markdown, or text. Reads stdin when omitted.")
    parser.add_argument(
        "--abstract-limit",
        type=int,
        default=None,
        metavar="N",
        help="Target journal's abstract word limit. Omitted, the Abstract is reported but not enforced.",
    )
    parser.add_argument("--no-fail", action="store_true", help="Always exit 0.")
    args = parser.parse_args()

    units = build_units(read_paragraphs(args.path))
    label = str(args.path) if args.path else "<stdin>"
    print(f"{label}\n")

    failures = report_budgets(units, args.abstract_limit)
    failures += report_negative_space(units)
    failures += report_redundancy(units)

    print(f"\n== Summary ==\n  {failures} finding(s): over budget, deletable negative space, or verbatim repetition")
    if failures:
        print("  Compress before content review (SKILL.md Step 0.5).")
    return 0 if args.no_fail else (1 if failures else 0)


if __name__ == "__main__":
    raise SystemExit(main())
