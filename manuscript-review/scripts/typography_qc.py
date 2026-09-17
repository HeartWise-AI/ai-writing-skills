#!/usr/bin/env python3
"""Pre-submission typography and abbreviation QC for medical-AI drafts."""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from xml.etree import ElementTree


@dataclass(frozen=True)
class Rule:
    code: str
    pattern: str
    message: str
    suggestion: str
    flags: int = 0
    # Optional second stage: the regex over-matches on purpose and this decides
    # whether a given match is actually a violation. Needed where the contract
    # depends on the numeric value, not on the text shape.
    validator: Optional[Callable[[str], bool]] = None


def excess_decimals(text: str) -> bool:
    """True when a number carries more decimals than SKILL.md permits.

    Percentages get 1 decimal, values at or above 0.1 get 2, values below 0.1 get 3.
    Covers 1.000, 12.345 and 12.345% as well as 0.945, and 0.0123 below the
    0.1 boundary, none of which a 0.xxx-shaped pattern can reach.
    """
    is_percent = text.rstrip().endswith("%")
    number = text.rstrip().rstrip("%")
    try:
        value = float(number)
    except ValueError:
        return False
    decimals = len(number.partition(".")[2])
    if is_percent:
        return decimals > 1
    return decimals > 2 if value >= 0.1 else decimals > 3


@dataclass(frozen=True)
class Finding:
    code: str
    line: int
    column: int
    excerpt: str
    message: str
    suggestion: str


RULES = [
    Rule(
        "EM_DASH",
        "\u2014",
        "Em dash found.",
        "Use a comma, parentheses, colon, or a separate sentence.",
    ),
    Rule(
        "DASHED_NUMERIC_RANGE",
        r"\b\d+(?:\.\d+)?\s*[\u2013\u2014-]\s*\d+(?:\.\d+)?\b",
        "Numeric range uses a dash.",
        'Use "to" for ranges unless journal style requires otherwise.',
    ),
    Rule(
        "VS_PERIOD",
        r"\bvs\.",
        "Found vs. with period.",
        'Use "versus" or "compared with".',
        re.IGNORECASE,
    ),
    Rule(
        "IE_EG",
        r"\b(?:i\.e\.|e\.g\.)",
        "Found Latin abbreviation.",
        'Use "that is", "for example", or direct wording.',
        re.IGNORECASE,
    ),
    Rule(
        "APPROX_SYMBOL",
        r"[~\u2248]",
        "Approximation symbol found.",
        'Use "approximately" or provide the exact value.',
    ),
    Rule(
        "MEAN_PM_SD",
        r"\bmean\s*(?:\+/-|\u00b1)\s*SD\b|\u00b1",
        "Mean plus-minus SD notation found.",
        'Use "mean (SD)".',
        re.IGNORECASE,
    ),
    Rule(
        "COMPARED_TO",
        r"\bcompared to\b",
        "Found compared to.",
        'Use "compared with" for statistical comparisons.',
        re.IGNORECASE,
    ),
    Rule(
        "N_SPACING",
        r"\bn=\s*\d+|\bn\s*=\d+",
        "Sample-size spacing is inconsistent.",
        'Use "n = X" with spaces around equals.',
    ),
    Rule(
        "UPPERCASE_P",
        r"\bP\s*(?:[<=>])",
        "Uppercase P value marker found.",
        "Use lowercase italic p in formatted text.",
    ),
    Rule(
        "P_VALUE_SPACING",
        r"\bp(?:[<=>])",
        "P value lacks spacing.",
        'Use "p < 0.05", "p = 0.04", or journal style equivalent.',
    ),
    # Supersedes the earlier name-anchored METRIC_PRECISION rule, which only fired
    # when a metric name sat next to the number and so missed table cells and
    # confidence-interval bounds. The regex over-matches; excess_decimals decides.
    Rule(
        "DECIMAL_PRECISION",
        r"\b\d+\.\d{2,}\s*%?",
        "Number carries more decimals than the style permits.",
        "Percentages take 1 decimal, values at or above 0.1 take 2, values below 0.1 "
        "take 3. This applies everywhere a reader can see them: text, abstract, tables, "
        "figure annotations, and both confidence-interval bounds. If two arms are "
        "identical at two decimals, report the paired difference instead of adding a "
        "decimal. For very small p values use scientific notation.",
        0,
        excess_decimals,
    ),
]

# Cap per-rule output so one table-wide violation does not bury every other finding.
MAX_PER_RULE = 10


SECTION_RE = re.compile(
    r"(?im)^\s*(?:#{1,6}\s*)?(abstract|introduction|methods|results|discussion|conclusion)\b.*$"
)
ABBREV_RE = re.compile(r"\b[A-Z][A-Z0-9]{1,4}\b")


def read_text(path: Path | None) -> str:
    if path is None:
        return sys.stdin.read()
    if path.suffix.lower() == ".docx":
        return read_docx(path)
    return path.read_text(encoding="utf-8")


def read_docx(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        try:
            xml_bytes = archive.read("word/document.xml")
        except KeyError as exc:
            raise SystemExit(f"{path}: not a valid docx file") from exc
    root = ElementTree.fromstring(xml_bytes)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraphs: list[str] = []
    for paragraph in root.findall(".//w:p", ns):
        chunks = [node.text or "" for node in paragraph.findall(".//w:t", ns)]
        if chunks:
            paragraphs.append("".join(chunks))
    return "\n".join(paragraphs)


def line_starts(text: str) -> list[int]:
    starts = [0]
    for match in re.finditer("\n", text):
        starts.append(match.end())
    return starts


def line_col(starts: list[int], offset: int) -> tuple[int, int]:
    lo = 0
    hi = len(starts) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if starts[mid] <= offset:
            lo = mid + 1
        else:
            hi = mid - 1
    line_index = max(0, hi)
    return line_index + 1, offset - starts[line_index] + 1


def excerpt(text: str, start: int, end: int) -> str:
    left = max(0, start - 50)
    right = min(len(text), end + 50)
    return " ".join(text[left:right].split())


def regex_findings(text: str) -> list[Finding]:
    starts = line_starts(text)
    findings: list[Finding] = []
    for rule in RULES:
        for match in re.finditer(rule.pattern, text, rule.flags):
            if rule.validator is not None and not rule.validator(match.group(0)):
                continue
            line, column = line_col(starts, match.start())
            findings.append(
                Finding(
                    rule.code,
                    line,
                    column,
                    excerpt(text, match.start(), match.end()),
                    rule.message,
                    rule.suggestion,
                )
            )
    return findings


def split_sections(text: str) -> list[tuple[str, int, int]]:
    matches = list(SECTION_RE.finditer(text))
    if not matches:
        return [("document", 0, len(text))]
    sections: list[tuple[str, int, int]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((match.group(1).lower(), start, end))
    return sections


def abbreviation_findings(text: str) -> list[Finding]:
    starts = line_starts(text)
    findings: list[Finding] = []
    for section_name, start, end in split_sections(text):
        body = text[start:end]
        seen: set[str] = set()
        for match in ABBREV_RE.finditer(body):
            token = match.group(0)
            if token in seen:
                continue
            seen.add(token)
            absolute_start = start + match.start()
            absolute_end = start + match.end()
            window_start = max(0, absolute_start - 80)
            window_end = min(len(text), absolute_end + 20)
            window = text[window_start:window_end]
            if f"({token})" in window:
                continue
            line, column = line_col(starts, absolute_start)
            findings.append(
                Finding(
                    "ABBREVIATION_FIRST_USE",
                    line,
                    column,
                    excerpt(text, absolute_start, absolute_end),
                    f"{token} may be undefined at first use in {section_name}.",
                    "Define abbreviations at first mention within each major section.",
                )
            )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, help="Draft text, Markdown, or docx file. Reads stdin when omitted.")
    parser.add_argument("--no-abbrev", action="store_true", help="Skip abbreviation first-use audit.")
    parser.add_argument("--no-fail", action="store_true", help="Always exit 0.")
    args = parser.parse_args()

    text = read_text(args.path)
    findings = regex_findings(text)
    if not args.no_abbrev:
        findings.extend(abbreviation_findings(text))
    findings.sort(key=lambda item: (item.line, item.column, item.code))

    label = str(args.path) if args.path else "<stdin>"
    if not findings:
        print(f"{label}: OK")
        return 0

    counts: dict[str, int] = {}
    for item in findings:
        counts[item.code] = counts.get(item.code, 0) + 1

    shown: dict[str, int] = {}
    for item in findings:
        shown[item.code] = shown.get(item.code, 0) + 1
        if shown[item.code] > MAX_PER_RULE:
            continue
        print(f"{label}:{item.line}:{item.column}: {item.code}: {item.message}")
        print(f"  text: {item.excerpt}")
        print(f"  suggestion: {item.suggestion}")
        if shown[item.code] == MAX_PER_RULE and counts[item.code] > MAX_PER_RULE:
            print(f"  ... and {counts[item.code] - MAX_PER_RULE} more {item.code} finding(s)")

    print("\n== Totals by rule ==")
    for code, count in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {code:26s} {count}")

    return 0 if args.no_fail else 1


if __name__ == "__main__":
    raise SystemExit(main())
