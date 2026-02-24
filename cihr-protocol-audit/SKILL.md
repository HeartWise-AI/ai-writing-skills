---
name: cihr-protocol-audit
description: Audit CIHR Project Grant clinical trial protocols for internal consistency, objective-endpoint-analysis traceability, cross-reference integrity, CIHR section compliance, budget-protocol alignment, and terminology consistency. Use when the user asks to audit, review, QC, or check a CIHR grant protocol, or when they want to verify that objectives map to endpoints and analysis plans, that cross-references are accurate, or that the budget matches the protocol. Also trigger when user mentions checking a grant for inconsistencies, garbled text, missing analyses, or section compliance.
---

# CIHR Protocol Audit Skill

## Overview

Systematic audit of a CIHR Project Grant clinical trial protocol. Produces a structured checklist (markdown), applies tracked changes for fixable issues, and adds comments for items requiring investigator judgment.

The audit has five parts plus a consistency check pass. Each part can surface issues that require either tracked changes (fixable problems) or comments (judgment calls).

## Prerequisites

Before starting the audit:

1. Unpack the .docx to access `word/document.xml` and related files
2. Extract plain text for analysis (use `python-docx` or direct XML parsing)
3. If a budget file is provided, extract its text as well
4. Read the `references/cihr-rct-headings.md` file for the mandatory CIHR RCT heading structure

## Part A: Objective-Endpoint-Analysis Traceability Matrix

Every objective in the protocol must have three components:
1. A clearly stated objective (usually in Section 1.2)
2. A defined endpoint or measurement (usually in Section 2.12)
3. A specified analysis plan (usually in Section 2.16)

### Procedure

1. Extract all objectives from Section 1.2 (primary, secondary, exploratory)
2. For each objective:
   - Find the corresponding endpoint definition in 2.12 (2.12.1 for primary, 2.12.2 for secondary/exploratory)
   - Find the corresponding analysis plan in 2.16 (2.16.1 for primary, 2.16.2 for secondary, 2.16.3 for sensitivity)
   - Verify the endpoint measurement method is specified (instrument name, timing, data source)
   - Verify the analysis plan specifies: statistical test, model structure, covariates/adjustments

3. Flag gaps:
   - **GAP**: No analysis plan for this objective
   - **PARTIAL**: Analysis mentioned but lacks specifics (e.g., "descriptive statistics" without specifying which tests, stratification, or comparison methods)
   - **OK**: All three components present and specific

### Output Format

| Objective | Statement | Endpoint (Section) | Analysis Plan (Section) | Status | Notes |
|-----------|-----------|-------------------|------------------------|--------|-------|

### Common Issues

- Exploratory objectives often have endpoints defined but analysis plans that say only "descriptive statistics" without specifying comparison methods
- Provider/patient experience objectives frequently lack between-arm comparison methods for ordinal outcomes (Mann-Whitney U, Wilcoxon)
- Economic/cost-effectiveness objectives may reference a framework section (e.g., 2.15) without a dedicated analysis subsection in 2.16
- Fairness/equity analyses may list metrics (equalized odds, Brier score) without specifying the statistical framework for testing differences

## Part B: Cross-Reference Verification

Every time the document says "Section X.Y" or "see Section X", verify the referenced section contains the promised information.

### Procedure

1. Use regex to find all cross-references: patterns like `Section \d+\.\d+`, `Sec \d+\.\d+`, `(Section \d+)`, `described in \d+\.\d+`
2. For each reference:
   - Note the source location (which section makes the reference)
   - Note the target section
   - Read the target section content
   - Verify the specific information claimed to be there actually exists

3. Flag issues:
   - **OK**: Referenced information is present in the target section
   - **PARTIAL**: Target section exists but the specific referenced information is missing or different from what's claimed
   - **MISSING**: Target section does not exist

### Common Issues

- Interim analysis sections (e.g., 2.17) often describe blinded pooled analyses but get referenced for unblinded arm-specific monitoring (e.g., concordance thresholds). These are conceptually different operations that may need separate procedures.
- Sensitivity analysis sections may be referenced before they are defined
- Budget-related cross-references to protocol sections may not align with actual site counts or resource allocations

### Output Format

| Reference | Source Location | Target Section | Content Present? | Notes |
|-----------|----------------|---------------|------------------|-------|

## Part C: CIHR RCT Section Compliance

Compare protocol headings against CIHR mandatory RCT section structure. Read `references/cihr-rct-headings.md` for the required headings.

### Procedure

1. Extract all section headings from the document (with numbering)
2. Map each heading to the corresponding CIHR required heading
3. Flag missing required headings
4. Flag extra headings that don't map (not an error, just note them)
5. Verify subsection numbering is consistent (1.1, 1.2, etc.)

### Common Issues

- Section numbering in the document may not match CIHR numbering (e.g., document starts with "1. Condition and Burden" instead of "1.1")
- DSMB section (3.3) may exist but with minimal justification for not having a DSMB
- "Duration of treatment period" (2.8) may say "not applicable" for AI/decision-support trials -- this is acceptable but should be explicitly stated

## Part D: Budget-Protocol Alignment

If a budget file is provided, check that every budgeted item aligns with the protocol and every protocol commitment has budget support.

### Procedure

1. Extract budget line items with amounts and justifications
2. For each budget item, verify it maps to a protocol commitment:
   - Personnel: role described in protocol sections 3.1-3.2
   - Equipment/consumables: needed for procedures described in protocol
   - Data linkages: required for endpoints described in protocol
   - Verification studies: sample sizes match protocol
3. For each protocol commitment, verify budget support:
   - Number of sites: do personnel/equipment budgets cover all sites?
   - Sample sizes: does the verification substudy budget match the protocol target?
   - Data sources: are all required data linkage fees budgeted?

### Common Issues

- Coordinator coverage at N sites but protocol specifies M sites (M > N) -- needs justification for which sites have existing support
- Equipment/modules budgeted for fewer sites than the protocol describes
- Verification substudy budgets slightly over the protocol target (acceptable buffer) or under (problem)
- Training stipend amounts that don't round cleanly (e.g., $75K rounded to $90K for "benefits and adjustments")

### Output Format

| Category | Amount | Protocol Alignment | Issues |
|----------|--------|-------------------|--------|

## Part E: Content Issues

Scan the full document text for garbled text, missing spaces, duplicate fragments, and formatting errors.

### Procedure

1. **Garbled text detection**: Search for patterns indicating splice errors from tracked-change acceptance:
   - Period immediately followed by lowercase letter with no space: `\.\w` (excluding decimals and abbreviations)
   - Orphan fragments: short phrases that don't connect grammatically to surrounding text
   - Possessive markers without antecedent: `'s advisory` without a noun before the apostrophe

2. **Missing spaces**: Search for:
   - Two capitalized words joined without space: `[a-z][A-Z]` patterns (e.g., "ORsA" should be "ORs. A")
   - "of" followed directly by a proper noun: `of[A-Z]`

3. **Duplicate fragments**: Search for:
   - Near-identical phrases within 100 characters of each other
   - Sentences that end with a period and are immediately followed by a rephrased version of the same content

4. **Section reference format**: Verify consistent formatting of section references (e.g., "Section 2.7" vs "Sec 2.7" vs "section 2.7")

## Part F: Terminology and Naming Consistency

Check that key terms, group names, instrument names, and abbreviations are used consistently throughout.

### Procedure

1. **Arm/group names**: Extract all references to study arms. Flag inconsistencies:
   - "intervention arm" vs "AI arm" vs "EchoNext arm" vs "experimental arm"
   - "control arm" vs "usual care" vs "standard care" vs "comparator"
   - Pick the canonical name used in Section 2.1 (study design) and flag deviations

2. **Survey/instrument names**: Extract all named instruments and check consistency:
   - System Usability Scale (SUS) -- always abbreviated the same way after first use?
   - CAHPS or CAHPS-adapted -- used consistently?
   - Trust-in-automation scale -- same name each time?
   - Likert scale references -- consistent anchoring descriptions?

3. **Abbreviation discipline**:
   - Every abbreviation should be defined at first use
   - After definition, use the abbreviation consistently (don't alternate between spelled-out and abbreviated)
   - Common abbreviations to check: TTE, SHD, ECG, MACE, ICC, OR, CI, FTE, DSMB, SAP, CRF

4. **Endpoint naming**: Verify that endpoint descriptions in 2.12 match the analysis plan descriptions in 2.16 (same names, same definitions)

5. **Site/center naming**: If sites are named, verify consistent naming throughout (e.g., "Montreal Heart Institute" vs "MHI" vs "Institut de cardiologie de Montreal")

6. **Statistical test naming**: Verify consistent naming of statistical methods across sections (e.g., "mixed-effect logistic regression" vs "mixed-effects logistic regression" vs "multilevel logistic model")

### Output Format

| Term Category | Variants Found | Canonical Form | Locations |
|--------------|----------------|---------------|-----------|

## Applying Fixes

After completing the audit:

### Tracked Changes (for fixable issues)

Use the body-swap serialization approach for Word XML manipulation:
1. Parse document.xml with lxml
2. Modify the `<w:body>` element (add `<w:del>` and `<w:ins>` elements)
3. Serialize only the body: `etree.tostring(body, encoding='unicode')`
4. Replace the `<w:body>...</w:body>` region in the original XML string
5. This preserves namespace declarations that lxml would otherwise mangle

For text replacements that span multiple `<w:r>` elements:
- Collect all non-deleted runs, concatenate their text
- Find the match position in the concatenated string
- Map back to affected runs
- Remove affected runs, insert: before-text run + `<w:del>` + `<w:ins>` + after-text run

Use author "Claude (Audit)" and a fixed date for all changes.

### Comments (for judgment calls)

For issues requiring investigator review:
1. Add `<w:commentRangeStart>` before the target paragraph's first run
2. Add `<w:commentRangeEnd>` and `<w:commentReference>` after the last run
3. Add the comment text to `word/comments.xml`
4. Add the author to `word/people.xml` (check namespace prefix -- may be `w15:` not `w:`)
5. Escape any `<` or `>` characters in comment text

### Output Checklist

Save the audit results as a markdown checklist file alongside the document. Structure:
- Part A table
- Part B table
- Part C table
- Part D table (if budget provided)
- Part E issue list with fix status
- Part F consistency table

## Quick Reference: What Gets a Tracked Change vs a Comment

| Issue Type | Action |
|-----------|--------|
| Garbled text / splice error | Tracked change |
| Missing space | Tracked change |
| Duplicate fragment | Tracked change (delete duplicate) |
| Missing analysis detail | Tracked change (add specifics) |
| Cross-reference discrepancy | Comment |
| Budget-protocol mismatch | Comment |
| Missing DSMB justification | Comment |
| Ambiguous methodology | Comment |
| Terminology inconsistency (minor) | Comment noting canonical form |
| Terminology inconsistency (in endpoint/analysis names) | Tracked change to standardize |
