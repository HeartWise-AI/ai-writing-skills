#!/usr/bin/env python3
"""Length, information-density, and redundancy QC for medical-AI manuscript drafts.

Implements the Step 0.5 gate of the manuscript-review skill:

  1. Word budget per section, subsection, and paragraph.
  2. Negative-space sentences that justify an absence instead of reporting a result.
  3. Material repeated between Introduction, Methods, and Discussion.

Usage:
    python length_budget_qc.py draft.docx
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

# Budgets are word counts for the whole unit. See SKILL.md Step 0.5.
SECTION_BUDGETS = {
    "abstract": 300,
    "introduction": 500,
    "background": 500,
    "methods": 1000,
    "results": 750,
    "discussion": 900,
    "limitations": 200,
    "conclusion": 250,
}

SUBSECTION_BUDGET = 130  # 10 lines, any Methods subsection, no exemption

PARAGRAPH_BUDGETS = {
    "results": 65,  # 5 lines
    "discussion": 50,  # 4 lines
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

SECTION_RE = re.compile(
    r"^\s*(?:#{1,6}\s*)?(" + "|".join(SECTION_NAMES) + r")\s*$",
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
    (r"\bwhich\s+(?:varies|depends|suits|conflates|ignores)\b", "rationale for a standard method"),
    (r"\bis\s+interpreted\s+against\b", "metric pedagogy"),
    (r"\brather\s+than\s+(?:intervention|inferring|by\b)", "meta-commentary on approach"),
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
    out: list[tuple[str, str]] = []
    for raw in text.split("\n"):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("### "):
            out.append(("h2", line[4:].strip()))
        elif line.startswith("#"):
            out.append(("h1", line.lstrip("#").strip()))
        else:
            out.append(("", line))
    return out


def read_docx(path: Path) -> list[tuple[str, str]]:
    with zipfile.ZipFile(path) as archive:
        try:
            xml_bytes = archive.read("word/document.xml")
        except KeyError as exc:
            raise SystemExit(f"{path}: not a valid docx file") from exc
    root = ElementTree.fromstring(xml_bytes)
    out: list[tuple[str, str]] = []
    for p in root.iter(W + "p"):
        # Skip text marked as deleted so tracked-change drafts measure the accepted state.
        text = "".join(node.text or "" for node in p.iter(W + "t")).strip()
        if not text:
            continue
        style_node = p.find(f"{W}pPr/{W}pStyle")
        style = style_node.get(W + "val") if style_node is not None else ""
        if style.startswith("Heading1") or style == "Heading1":
            out.append(("h1", text))
        elif style.startswith("Heading2") or style == "Heading2":
            out.append(("h2", text))
        else:
            out.append(("", text))
    return out


def normalize_section(name: str) -> str | None:
    match = SECTION_RE.match(name)
    return match.group(1).lower() if match else None


def build_units(paragraphs: list[tuple[str, str]]) -> list[Unit]:
    units: list[Unit] = []
    section = "front matter"
    current: Unit | None = None

    for style, text in paragraphs:
        as_section = normalize_section(text)
        if as_section or style == "h1":
            section = as_section or text.lower()
            current = Unit("section", section, section)
            units.append(current)
            continue
        if style == "h2":
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


def report_budgets(units: list[Unit]) -> int:
    failures = 0
    section_totals: dict[str, int] = {}
    for unit in units:
        if unit.section in ("references", "front matter"):
            continue
        section_totals[unit.section] = section_totals.get(unit.section, 0) + unit.words

    print("== Section budgets ==")
    for section, words in section_totals.items():
        budget = SECTION_BUDGETS.get(section)
        if budget is None:
            continue
        status = "OVER" if words > budget else "ok"
        if words > budget:
            failures += 1
        print(
            f"  [{status:4s}] {section:14s} {words:6d} w "
            f"(~{words / WORDS_PER_PAGE:.1f} pages)  budget {budget} w  "
            f"ratio {words / budget:.1f}x"
        )

    print("\n== Subsection budgets (10 lines / 130 words) ==")
    any_sub = False
    for unit in units:
        if unit.kind != "subsection" or not unit.words:
            continue
        any_sub = True
        over = unit.words > SUBSECTION_BUDGET
        if over:
            failures += 1
        print(
            f"  [{'OVER' if over else 'ok':4s}] {unit.name[:44]:44s} {unit.words:5d} w "
            f"(~{unit.words / WORDS_PER_LINE:.0f} lines)  ratio {unit.words / SUBSECTION_BUDGET:.1f}x"
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


ENTITY_RE = re.compile(r"\b(?:[A-Z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)+|[A-Z]{3,})\b")

STOP_ENTITIES = {"AUROC", "AUPRC", "ECG", "ECGS", "AND", "THE", "FOR", "WITH", "NOT", "ALL"}


def report_redundancy(units: list[Unit]) -> int:
    """Verbatim repetition plus entities described in more than one section.

    Exact n-gram overlap catches copy-paste. The entity pass catches the more common
    case: the same model or dataset introduced from scratch in two places.
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
        print(f"  {left} <-> {right}: {len(shared)} shared spans")
        for span in sorted(shared)[:5]:
            print(f"      \"{span}\"")
    if not total:
        print("  no verbatim overlap")

    print("\n== Entities introduced in more than one section ==")
    narrative = ("introduction", "background", "methods", "discussion")
    counts: dict[str, dict[str, int]] = {}
    for section in narrative:
        for paragraph in text_by_section.get(section, []):
            for entity in ENTITY_RE.findall(paragraph):
                if entity.upper() in STOP_ENTITIES or len(entity) < 4:
                    continue
                counts.setdefault(entity, {})
                counts[entity][section] = counts[entity].get(section, 0) + 1

    flagged = 0
    for entity, per_section in sorted(counts.items(), key=lambda kv: -sum(kv[1].values())):
        sections = [s for s, n in per_section.items() if n >= 2]
        if len(sections) >= 2:
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
    parser.add_argument("--no-fail", action="store_true", help="Always exit 0.")
    args = parser.parse_args()

    units = build_units(read_paragraphs(args.path))
    label = str(args.path) if args.path else "<stdin>"
    print(f"{label}\n")

    failures = report_budgets(units)
    failures += report_negative_space(units)
    report_redundancy(units)

    print(f"\n== Summary ==\n  {failures} unit(s) over budget or carrying deletable negative space")
    if failures:
        print("  Compress before content review (SKILL.md Step 0.5).")
    return 0 if args.no_fail else (1 if failures else 0)


if __name__ == "__main__":
    raise SystemExit(main())
