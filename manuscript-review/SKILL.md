---
name: manuscript-review
description: Comprehensive checklist for reviewing academic medical AI manuscripts, covering Background, Methods, Results, Tables, Discussion, and Abstract sections with success criteria for each. Use when reviewing or evaluating a manuscript draft.
---

# Claude Code Skill: AI Manuscript Section Reviewer

This skill iterates through each section of a medical AI manuscript and outputs a success checklist based on predefined criteria.

---

## Usage

```
Review my manuscript for [SECTION_NAME] compliance
```

or

```
Run full manuscript checklist
```

---

## Section Definitions & Success Checklists

### 1. Background Section

**Purpose:** Establish clinical importance, trace AI evolution, identify gaps, and state contributions.

**Iteration Logic:**

```
FOR each paragraph in Background:
  IDENTIFY which subsection it belongs to:
    - Clinical importance
    - AI evolution
    - Current gaps
    - Contribution statement
  EVALUATE against criteria below
  OUTPUT pass/fail for each criterion
```

**Success Checklist:**

- [ ]  **Clinical Importance Present** — Core problem is defined with quantified scale (e.g., annual volume, error rates, time delays)
- [ ]  **Unmet Need Articulated** — Clear statement of what current practice lacks
- [ ]  **AI Evolution Traced** — Historical progression from traditional ML → deep learning with key citations
- [ ]  **State-of-the-Art Benchmarked** — Current best performance cited with metrics
- [ ]  **Gaps Are Specific** — Each gap is actionable, not vague ("more work needed" = FAIL)
- [ ]  **Gaps Map to Contributions** — Every gap directly motivates a contribution
- [ ]  **Paper Roadmap Included** — Reader knows what to expect in subsequent sections
- [ ]  **No Overclaiming** — Novelty stated relative to prior work without exaggeration

---

### 2. Methods Section

**Purpose:** Describe ethics, data, modeling, and statistical analysis in reproducible detail.

**Iteration Logic:**

```
FOR each subsection in Methods:
  CHECK presence and order:
    1. Ethics & LLM disclosure (MUST be first)
    2. Dataset description
    3. Modeling approach
    4. Statistical analysis
  EVALUATE against criteria below
  OUTPUT pass/fail for each criterion
```

**Success Checklist:**

- [ ]  **Ethics Approval First** — IRB/ethics statement appears before any data description
- [ ]  **LLM Use Disclosed** — If LLMs used in writing/analysis, disclosed upfront
- [ ]  **Internal Dataset Described** — Years spanned, inclusion/exclusion criteria stated
- [ ]  **Flowchart Present** — CONSORT-style diagram showing patient/sample flow
- [ ]  **External Dataset Described** — Validation cohort with source, years, criteria
- [ ]  **Modeling Section Complete** — Architecture, training details, hyperparameters documented
- [ ]  **Statistical Analysis Specified** — Tests, confidence intervals, significance thresholds defined
- [ ]  **TRIPOD-AI Compliant** — Cross-reference with TRIPOD-AI checklist items

---

### 3. Results Section

**Purpose:** Present findings factually without interpretation.

**Iteration Logic:**

```
FOR each paragraph in Results:
  CHECK that:
    - No interpretation or "why" statements present
    - Order matches Methods subsections exactly
  FOR each table/figure reference:
    - Verify sequential order
  OUTPUT pass/fail for each criterion
```

**Success Checklist:**

- [ ]  Leads with cohort description
- [ ]  **Table 1 = Baseline Characteristics** — Demographics, splits, clinical variables appear first
- [ ]  **Results Mirror Methods Order** — 1:1 subsection correspondence maintained
- [ ]  **No Interpretation Present** — Zero sentences explaining "why" or comparing to literature
- [ ]  **Tables/Figures in Order** — Referenced sequentially as they appear
- [ ]  **No Em Dashes** — Use commas, parentheses, or separate sentences instead
- [ ]  **Statistics Complete** — Point estimates with 95% CI or p-values included

---

### 4. Tables Section

**Purpose:** Present data in standardized, journal-compliant format.

**Iteration Logic:**

```
FOR each table in manuscript:
  EXTRACT metrics and formatting
  VALIDATE against numerical rules
  CHECK structural requirements
  OUTPUT pass/fail for each criterion
```

**Numerical Formatting Rules:**

| Value Type | Decimals | Example |
| --- | --- | --- |
| AUROC, AUPRC, Sensitivity, Specificity | 2 | 0.85 |
| Values < 0.1 | 2 or 3 | 0.024 |
| Percentages | 1 | 7.6% |
| 95% CI | Match point estimate | 0.85 (0.79–0.91) |

**Success Checklist:**

- [ ]  **Correct Metrics Used** — AUROC, AUPRC, Sensitivity, Specificity, PPV, NPV only (NO F1, recall, accuracy)
- [ ]  **Classification Threshold Reported** — For binary classification models, the decision threshold used to derive Sensitivity/Specificity/PPV/NPV is explicitly stated in the table footnote (e.g., "threshold selected at Youden Index" or "threshold = 0.XX"). FAIL if threshold is missing or ambiguous.
- [ ]  **Threshold Selection Method Stated** — The method for selecting the threshold is named: Youden Index, prespecified clinical sensitivity target, or cost-sensitive criterion. FAIL if Sensitivity/Specificity are reported without specifying how the operating point was chosen.
- [ ]  **Cited Before Appearance** — Table referenced in text before it appears
- [ ]  **Title Present** — Descriptive title above table, no period at end
- [ ]  **Abbreviations Defined** — Listed below table in single paragraph
- [ ]  **95% CI in Parentheses** — Uses en-dash, not hyphen: (0.79–0.91)
- [ ]  **Two Decimals Standard** — 0.85, not 0.850 or 0.8
- [ ]  **Three Decimals for Small Values** — Values < 0.1 use three decimals
- [ ]  **Sample Sizes Complete** — Format: events/total (X.X%)
- [ ]  **Consistent CI Spacing** — 0.85 (0.79–0.91) with space before parenthesis
- [ ]  **No Vertical Lines** — Horizontal rules only

---

### 5. Discussion Section

**Purpose:** Interpret findings, compare to literature, acknowledge limitations, and conclude. A good discussion section should answer **6 key questions**.

**The 6 Questions Framework:**

1. **What is different in your findings compared to previous research?**
2. **What is similar in your findings compared to previous research?**
3. **How do different sections of your results correlate?**
4. **What are the implications of your findings for practitioners?**
5. **What are the implications of your findings for researchers?**
6. **What are the limitations or threats to the validity of your findings?**

**Iteration Logic:**

```
FOR each paragraph in Discussion:
  IDENTIFY paragraph type:
    - Main finding interpretation (MUST be paragraph 1)
    - Literature comparison: differences (Question 1)
    - Literature comparison: similarities (Question 2)
    - Results correlation/synthesis (Question 3)
    - Clinical implications (Question 4)
    - Research implications (Question 5)
    - Limitations (Question 6, MUST be present)
    - Conclusion (MUST be final paragraph)
  EVALUATE against criteria below
  OUTPUT pass/fail for each criterion
```

**Success Checklist:**

- [ ]  **First Line = Main Finding** — Opening sentence states the key interpretation. **Leads with Accomplishment** — First sentence states what was achieved
- [ ]  **Differences from Prior Work Addressed** — Explicitly states what is novel or contradictory vs. existing literature
- [ ]  **Similarities to Prior Work Addressed** — Acknowledges concordant findings that reinforce validity
- [ ]  **Results Sections Correlated** — Synthesizes how different analyses (e.g., subgroups, sensitivity analyses) relate to each other
- [ ]  **Practitioner Implications Stated** — Clear guidance on how findings affect clinical practice or workflow
- [ ]  **Researcher Implications Stated** — Identifies future research directions or methodological contributions
- [ ]  **Limitations Clearly Present** — Dedicated section acknowledging study weaknesses and threats to validity
- [ ]  **Final Paragraph = Conclusion** — Last paragraph summarizes implications
- [ ]  **No New Results Introduced** — All data presented in Results section only

---

### 6. Abstract Section

**Purpose:** Summarize entire manuscript in structured format.

**Iteration Logic:**

```
VERIFY that abstract is written LAST
FOR each abstract subsection:
  CHECK alignment with corresponding full section
  VERIFY word count compliance
OUTPUT pass/fail for each criterion
```

**Success Checklist:**

- [ ]  **Written Last** — Abstract drafted after all other sections complete
- [ ]  **Background Present** — 1-2 sentences on clinical problem and gap
- [ ]  **Methods Summarized** — Study design, cohort, key methods in brief
- [ ]  **Results Highlighted** — Primary outcome with key metric and CI
- [ ]  **Conclusion Stated** — Clinical implication in 1-2 sentences
- [ ]  **Word Count Compliant** — Within journal's abstract limit
- [ ]  **No Citations in Abstract** — References belong in main text only

---

## Full Manuscript Review Command

```
RUN full_review():
  sections = [Background, Methods, Results, Tables, Discussion, Abstract]
  FOR section in sections:
    PRINT "=== Reviewing {section} ==="
    RUN section_checklist(section)
    PRINT summary(passed, failed, total)
  PRINT "=== MANUSCRIPT REVIEW COMPLETE ==="
  RETURN overall_compliance_score
```

---

## Quick Reference: Forbidden Patterns

| Don't Use | Use Instead |
| --- | --- |
| F1-score | AUROC, AUPRC |
| Recall | Sensitivity |
| Accuracy | Sensitivity + Specificity |
| Em dashes (—) | Commas, parentheses |
| Hyphens in CI | En-dash (–) |
| Interpretation in Results | Move to Discussion |
| Vague gaps | Specific, actionable gaps |
