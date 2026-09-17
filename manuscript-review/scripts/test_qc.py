#!/usr/bin/env python3
"""Contract tests for the manuscript-review QC scripts.

Each test names the contract it protects. No test dependencies: run it with

    python manuscript-review/scripts/test_qc.py
"""

from __future__ import annotations

import importlib.util
import io
import sys
import zipfile
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module  # dataclasses resolve annotations via sys.modules
    spec.loader.exec_module(module)
    return module


lbq = load("length_budget_qc")
tqc = load("typography_qc")

FAILURES: list[str] = []


def check(condition: bool, contract: str, detail: str = "") -> None:
    if condition:
        print(f"  PASS  {contract}")
    else:
        FAILURES.append(contract)
        print(f"  FAIL  {contract}" + (f"\n        {detail}" if detail else ""))


def units_from_markdown(text: str) -> list:
    return lbq.build_units(lbq.parse_markdown(text))


def section_words(units: list, section: str) -> int:
    return sum(u.words for u in units if u.section == section)


def run_gate(text: str, **kwargs) -> tuple[int, str]:
    """Return (failure count, captured output) for a Markdown draft."""
    units = units_from_markdown(text)
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        failures = lbq.report_budgets(units, kwargs.get("abstract_limit"))
        failures += lbq.report_negative_space(units)
        failures += lbq.report_redundancy(units)
    return failures, buffer.getvalue()


def words(n: int, token: str = "word") -> str:
    return " ".join([token] * n)


# --------------------------------------------------------------------------
print("\ntypography_qc: decimal precision contract")
# Contract: percentages take 1 decimal, values >= 0.1 take 2, values < 0.1 take 3.
for sample in ("1.234", "12.345", "12.345%", "1.000", "0.945", "0.0123", "100.123"):
    check(tqc.excess_decimals(sample), f"{sample} is flagged as excess precision")
for sample in ("0.85", "0.024", "7.6%", "0.001", "1.00", "12.34"):
    check(not tqc.excess_decimals(sample), f"{sample} is accepted")

# Contract: the rule fires through the real pipeline, not just the helper.
found = {f.code for f in tqc.regex_findings("AUROC was 1.000 with CI (0.0123 to 1.000).")}
check("DECIMAL_PRECISION" in found, "value-aware precision rule fires end to end", str(found))
clean = {f.code for f in tqc.regex_findings("AUROC was 0.94 (0.92 to 0.96).")}
check("DECIMAL_PRECISION" not in clean, "compliant two-decimal reporting is not flagged", str(clean))

# --------------------------------------------------------------------------
print("\nlength_budget_qc: Markdown heading levels")
# Contract: '## Statistical analysis' under '# Methods' is a Methods subsection,
# and its prose counts toward the Methods total rather than starting a new section.
draft = f"""# Methods

{words(30)}

## Statistical analysis

{words(40)}
"""
units = units_from_markdown(draft)
check(section_words(units, "methods") == 70, "level-2 subsection prose counts toward Methods",
      f"got {section_words(units, 'methods')}")
check(any(u.kind == "subsection" and u.name == "Statistical analysis" and u.section == "methods"
          for u in units), "level-2 heading becomes a subsection of the open section")

# Contract: a section heading with a descriptive suffix still resolves.
check(lbq.normalize_section("METHODS AND MATERIALS", styled=True) == "methods",
      "styled section heading with trailing words resolves")
check(lbq.normalize_section("Statistical analysis", styled=True) is None,
      "a non-section heading does not resolve to a section")
# Contract: a structured abstract's run-in labels are prose, not section headings.
# Matching trailing text on unstyled paragraphs silently emptied the Abstract.
check(lbq.normalize_section(
    "Background: Very few high-performing AI models have been externally validated "
    "at healthcare system scale, despite the size of the task.") is None,
    "a structured-abstract run-in label does not open a section")
check(lbq.normalize_section("RESULTS") == "results",
      "an unstyled all-caps section name still resolves")
check(lbq.normalize_section("BACKGROUND:") is None,
      "a run-in label with a trailing colon is not a section heading")

# Contract: a structured abstract keeps its whole body, and its BACKGROUND:/METHODS:
# labels do not open real sections. This is how Word manuscripts lay out abstracts.
structured = (
    "ABSTRACT\n\nBACKGROUND:\n\n" + words(40)
    + "\n\nMETHODS:\n\n" + words(40)
    + "\n\nRESULTS:\n\n" + words(40)
    + "\n\n# INTRODUCTION\n\n" + words(25)
)
su = units_from_markdown(structured)
check(section_words(su, "abstract") >= 120,
      "structured abstract body is attributed to the Abstract",
      f"abstract={section_words(su, 'abstract')} methods={section_words(su, 'methods')}")
check(section_words(su, "methods") == 0,
      "an abstract METHODS: label does not open the Methods section",
      f"methods={section_words(su, 'methods')}")
check(section_words(su, "introduction") == 25,
      "the first real heading after the abstract opens its section")

# --------------------------------------------------------------------------
print("\nlength_budget_qc: subsection budget is Methods-only")
# Contract: the 130-word subsection budget applies to Methods. A compliant Results
# subsection built from within-budget paragraphs must not fail the gate.
results_draft = f"""# Results

## Subgroup performance

{words(60)}

{words(60)}

{words(60)}
"""
failures, out = run_gate(results_draft)
check(failures == 0, "a 180-word Results subsection of compliant paragraphs passes",
      f"failures={failures}\n{out}")
methods_draft = f"""# Methods

## Statistical analysis

{words(200)}
"""
failures, _ = run_gate(methods_draft)
check(failures >= 1, "a 200-word Methods subsection fails")

# --------------------------------------------------------------------------
print("\nlength_budget_qc: abstract limit comes from the journal")
abstract_draft = f"""# Abstract

{words(400)}
"""
failures, out = run_gate(abstract_draft)
check(failures == 0 and "journal limit" in out,
      "abstract is not enforced without --abstract-limit", out)
failures, _ = run_gate(abstract_draft, abstract_limit=250)
check(failures >= 1, "abstract over the supplied journal limit fails")
failures, _ = run_gate(abstract_draft, abstract_limit=500)
check(failures == 0, "abstract under the supplied journal limit passes")

# --------------------------------------------------------------------------
print("\nlength_budget_qc: Introduction paragraph cap is enforced")
# Contract: 4 paragraphs maximum, even when the word count is compliant.
intro_draft = "# Introduction\n\n" + "\n\n".join(words(20) for _ in range(5))
failures, out = run_gate(intro_draft)
check(failures >= 1 and "paragraphs" in out,
      "a 5-paragraph Introduction under 500 words still fails", out)
intro_ok = "# Introduction\n\n" + "\n\n".join(words(20) for _ in range(4))
failures, _ = run_gate(intro_ok)
check(failures == 0, "a 4-paragraph Introduction passes")

# --------------------------------------------------------------------------
print("\nlength_budget_qc: entity repetition detected at one mention per section")
entity_draft = """# Introduction

The DeepECG-SSL model is a self-supervised encoder.

# Methods

We evaluated DeepECG-SSL on the held-out cohort.
"""
_, out = run_gate(entity_draft)
check("DeepECG-SSL" in out, "an entity mentioned once per section is reported", out)

# --------------------------------------------------------------------------
print("\nlength_budget_qc: wrapped Markdown lines form one paragraph")
# Contract: conventionally wrapped prose must not evade the paragraph budget.
wrapped = "# Results\n\n" + "\n".join(words(10) for _ in range(10))
units = units_from_markdown(wrapped)
paragraphs = [p for u in units for p in u.paragraphs]
check(len(paragraphs) == 1 and len(paragraphs[0].split()) == 100,
      "ten wrapped lines join into one 100-word paragraph",
      f"{len(paragraphs)} paragraph(s)")
failures, _ = run_gate(wrapped)
check(failures >= 1, "the wrapped 100-word Results paragraph exceeds its 65-word budget")

# --------------------------------------------------------------------------
print("\nlength_budget_qc: verbatim repetition fails the gate")
shared = "the two models were scored on identical recordings throughout"
repeat_draft = f"""# Introduction

{shared}

# Discussion

{shared}
"""
failures, out = run_gate(repeat_draft)
check(failures >= 1, "cross-section verbatim overlap alone is a failure", out)

# --------------------------------------------------------------------------
print("\nlength_budget_qc: negative-space detection is anchored")
# Contract: a substantive result that happens to contain 'which varies' is kept.
substantive = """# Results

The treatment effect, which varies by age, was largest among older participants.
"""
failures, out = run_gate(substantive)
check(failures == 0, "a substantive 'which varies' result is not flagged", out)

deletable = """# Methods

We do not report F1, which varies with prevalence and has no clinical interpretation.
"""
_, out = run_gate(deletable)
check("CUT" in out, "metric non-reporting rationale is still flagged", out)

required = """# Methods

Strata were prespecified and no multiplicity correction was applied.
"""
_, out = run_gate(required)
check("CUT" not in out, "a required negative is not marked for deletion", out)

# --------------------------------------------------------------------------
print("\nlength_budget_qc: tables and figure legends are excluded (docx)")


def build_docx(path: Path) -> None:
    """Minimal docx: one Methods heading, one body paragraph, a table, a caption."""
    ns = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'

    def para(text: str, style: str | None = None) -> str:
        pr = f"<w:pPr><w:pStyle w:val=\"{style}\"/></w:pPr>" if style else ""
        return f"<w:p>{pr}<w:r><w:t>{text}</w:t></w:r></w:p>"

    document = (
        f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f"<w:document {ns}><w:body>"
        + para("Methods", "Heading1")
        + para(words(20))
        + f"<w:tbl><w:tr><w:tc>{para(words(500))}</w:tc></w:tr></w:tbl>"
        + para("Table 1. " + words(50))
        + para(words(40), "Caption")
        + "</w:body></w:document>"
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", document)


tmp = Path(__file__).resolve().parent / "_test_fixture.docx"
try:
    build_docx(tmp)
    units = lbq.build_units(lbq.read_docx(tmp))
    total = section_words(units, "methods")
    check(total == 20, "table rows, table titles and captions are excluded from the count",
          f"got {total} words, expected 20")
finally:
    tmp.unlink(missing_ok=True)

# --------------------------------------------------------------------------
print()
if FAILURES:
    print(f"{len(FAILURES)} contract(s) violated:")
    for item in FAILURES:
        print(f"  - {item}")
    sys.exit(1)
print("All contracts hold.")
