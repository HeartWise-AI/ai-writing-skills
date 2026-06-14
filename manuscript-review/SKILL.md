---
name: manuscript-review
description: Comprehensive checklist for reviewing academic medical AI manuscripts, covering objective identification, Background, Methods, Results, Tables, Discussion, and Abstract sections with success criteria for each. Use when reviewing or evaluating a manuscript draft.
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

Reusable assets in this skill:

- `scripts/typography_qc.py`: regex-based typography and abbreviation audit for pre-submission drafts
- `templates/label_noise_sensitivity_template.md`: reviewer-ready label-noise sensitivity analysis template
- `templates/failure_mode_panel_template.md`: supplementary failure-mode panel template
- `templates/failure_mode_panel_template.ipynb`: executable failure-mode panel notebook skeleton
- `templates/consort_flow_table1_template.md`: CONSORT-style flow and Table 1 denominator template

---

## Step 0: Objective Identification

Before reviewing any section, identify and classify the study objectives.

**Iteration Logic:**

```
EXTRACT objectives from manuscript:
  IDENTIFY primary objective (exactly one)
  IDENTIFY secondary objective(s)
  FOR each objective:
    CHECK that data source is specified
    CHECK that model development approach is described (if applicable)
    CHECK that evaluation criteria are defined
    CHECK that sensitivity analysis is planned
  BUILD objective-to-methods mapping
  VERIFY that Methods and Results trace back to this mapping
```

**Success Checklist:**

- **Single Primary Objective**: Exactly one primary objective stated
- **Secondary Objectives Listed**: Each secondary objective is distinct and measurable
- **Data Source Mapped per Objective**: Each objective specifies which dataset(s), cohort(s), or registry(ies) it uses
- **Model Development Mapped per Objective**: Each objective that involves a model specifies architecture, training strategy, and validation approach
- **Evaluation Criteria Mapped per Objective**: Each objective has discrimination, calibration, and threshold metrics defined
- **Sensitivity Analysis Mapped per Objective**: Each objective specifies which assumptions are varied and how robustness is assessed
- **Objectives Traceable Through Manuscript**: Every Methods subsection and Results subsection maps to an objective

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

- **Clinical Importance Present**: Core problem is defined with quantified scale (e.g., annual volume, error rates, time delays)
- **Unmet Need Articulated**: Clear statement of what current practice lacks
- **AI Evolution Traced**: Historical progression from traditional ML to deep learning with key citations
- **State-of-the-Art Benchmarked**: Current best performance cited with metrics
- **Gaps Are Specific**: Each gap is actionable, not vague ("more work needed" = FAIL)
- **Gaps Map to Contributions**: Every gap directly motivates a contribution
- **Paper Roadmap Included**: Reader knows what to expect in subsequent sections
- **No Overclaiming**: Novelty stated relative to prior work without exaggeration

---

### 2. Methods Section

**Purpose:** Describe ethics, data, modeling, and statistical analysis in reproducible detail.

**Iteration Logic:**

```
FOR each subsection in Methods:
  CHECK presence and order:
    1. Ethics & LLM disclosure (MUST be first)
    2. Data Source for Model Development
    3. Data Preprocessing
    4. Model Development
    5. External Validation (optional)
    6. Model Evaluation and Statistical Methods
  VERIFY each subsection maps to primary or secondary objective
  CHECK that all other methodological detail is routed to Supplement
  EVALUATE against criteria below
  OUTPUT pass/fail for each criterion
```

**Success Checklist:**

- **Ethics Approval First**: Institutional Review Board (IRB)/ethics statement appears before any data description
- **LLM Use Disclosed**: If Large Language Models (LLMs) used in writing/analysis, disclosed upfront
- **Data Source Described**: Dataset(s) named with full expansion at first mention (e.g., "The Canadian Longitudinal Study on Aging (CLSA)"), years spanned, geographic scope, sample size, inclusion/exclusion criteria
- **Data Source Mapped to Objectives**: Clear which dataset serves the primary vs. secondary objectives
- **Flowchart Present**: CONSORT-style diagram showing patient/sample flow (Figure 1)
- **Data Preprocessing Described**: Signal/image processing, feature extraction, missing data handling, train/validation/test split
- **Model Development Complete**: Architecture, training details, hyperparameters documented; each model mapped to its objective
- **External Validation Described (if applicable)**: External cohort source, size, and any domain adaptation; if absent, justified and acknowledged as limitation
- **Evaluation Criteria Defined per Objective**: Discrimination, calibration, threshold selection, and clinical utility metrics specified for each objective
- **Sensitivity Analysis Specified**: Assumptions to be varied are listed for both primary and secondary objectives
- **Statistical Methods Specified**: Tests, Confidence Intervals (CI), significance thresholds defined
- **Supplement Routing Correct**: Extended preprocessing, hyperparameter search, ablation experiments, heterogeneity assessment, model updating, and extended sensitivity analyses are in Supplement, not main text
- **TRIPOD-AI Compliant**: Cross-reference with Transparent Reporting of a Multivariable Prediction Model for Individual Prognosis or Diagnosis (TRIPOD)-AI checklist items

---

### 3. Results Section

**Purpose:** Present findings factually without interpretation.

**Iteration Logic:**

```
FOR each paragraph in Results:
  CHECK that:
    - No interpretation or "why" statements present
    - Order matches Methods subsections exactly
    - Primary objective results come first
    - Secondary objective results follow in separate subsections
    - Sensitivity analysis results have a dedicated subsection
  FOR each table/figure reference:
    - Verify sequential order
  OUTPUT pass/fail for each criterion
```

**Success Checklist:**

- Leads with cohort description
- **Table 1 = Baseline Characteristics**: Demographics, splits, clinical variables appear first
- **Results Mirror Methods Order**: 1:1 subsection correspondence maintained
- **Primary Objective Results First**: Model performance on the primary objective presented before secondary
- **Secondary Objective Results Separated**: Each secondary objective in its own subsection with its data source and model referenced
- **Sensitivity Analysis Results Present**: Dedicated subsection showing robustness of primary and secondary findings
- **No Interpretation Present**: Zero sentences explaining "why" or comparing to literature
- **Tables/Figures in Order**: Referenced sequentially as they appear
- **No Em Dashes**: Use commas, parentheses, or separate sentences instead
- **Statistics Complete**: Point estimates with 95% CI or p-values included

---

### 4. Tables Section

**Purpose:** Present data in standardized, journal-compliant format.

**Iteration Logic:**

```
FOR each table in manuscript:
  EXTRACT metrics and formatting
  VALIDATE against numerical rules
  CHECK structural requirements
  CHECK abbreviation format
  OUTPUT pass/fail for each criterion
```

**Numerical Formatting Rules:**

| Value Type | Decimals | Example |
|------------|----------|---------|
| AUROC, AUPRC, Sensitivity, Specificity | 2 | 0.85 |
| Values < 0.1 | 2 or 3 | 0.024 |
| Percentages | 1 | 7.6% |
| 95% CI | Match point estimate | 0.85 (0.79 to 0.91) |

**Success Checklist:**

- **Correct Metrics Used**: AUROC, AUPRC, Sensitivity, Specificity, PPV, NPV only (NO F1, recall, accuracy)
- **Classification Threshold Reported**: For binary classification models, the decision threshold used to derive Sensitivity/Specificity/PPV/NPV is explicitly stated in the table footnote (e.g., "threshold selected at Youden Index" or "threshold = 0.XX"). FAIL if threshold is missing or ambiguous.
- **Threshold Selection Method Stated**: The method for selecting the threshold is named: Youden Index, prespecified clinical sensitivity target, or cost-sensitive criterion. FAIL if Sensitivity/Specificity are reported without specifying how the operating point was chosen.
- **Cited Before Appearance**: Table referenced in text before it appears
- **Title Present**: Descriptive title above table, no period at end
- **Abbreviations Defined**: Listed below table in a single paragraph, using colon after abbreviation and semicolons between entries. Format: `Abbreviations: LVEF: Left Ventricular Ejection Fraction; AUROC: Area Under the Receiver Operating Characteristic Curve; PPV: Positive Predictive Value`
- **Abbreviations Expanded at First Use in Text**: Every abbreviation expanded with full name and abbreviation in parentheses at first occurrence in the manuscript body
- **95% CI in Parentheses**: Uses "to" for ranges unless the journal explicitly requires another style: (0.79 to 0.91)
- **Two Decimals Standard**: 0.85, not 0.850 or 0.8
- **Three Decimals for Small Values**: Values < 0.1 use three decimals
- **Sample Sizes Complete**: Format: events/total (X.X%)
- **Consistent CI Spacing**: 0.85 (0.79 to 0.91) with space before parenthesis
- **No Vertical Lines**: Horizontal rules only

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

- **First Line = Main Finding**: Opening sentence states the key interpretation. **Leads with Accomplishment**: First sentence states what was achieved
- **Differences from Prior Work Addressed**: Explicitly states what is novel or contradictory vs. existing literature
- **Similarities to Prior Work Addressed**: Acknowledges concordant findings that reinforce validity
- **Results Sections Correlated**: Synthesizes how different analyses (e.g., subgroups, sensitivity analyses) relate to each other
- **Practitioner Implications Stated**: Clear guidance on how findings affect clinical practice or workflow
- **Researcher Implications Stated**: Identifies future research directions or methodological contributions
- **Limitations Clearly Present**: Dedicated section acknowledging study weaknesses and threats to validity
- **Final Paragraph = Conclusion**: Last paragraph summarizes implications
- **No New Results Introduced**: All data presented in Results section only

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

- **Written Last**: Abstract drafted after all other sections complete
- **Background Present**: 1-2 sentences on clinical problem and gap
- **Methods Summarized**: Study design, cohort, key methods in brief
- **Results Highlighted**: Primary outcome with key metric and CI
- **Conclusion Stated**: Clinical implication in 1-2 sentences
- **Word Count Compliant**: Within journal's abstract limit
- **No Citations in Abstract**: References belong in main text only

---

## Reviewer-Pattern Pre-Submission Checklist for Medical-AI Papers

Use this checklist after the section-level review. Keep it generic and apply it to any clinical AI manuscript, regardless of modality or disease area. The goal is to remove predictable reviewer objections before submission.

### 1. Foundation-model and novelty framing

- If the manuscript uses "foundation model", "general-purpose", or "universal", require operational evidence.
- Acceptable evidence includes zero-shot or few-shot generalization on at least one held-out task without supervised fine-tuning, a self-supervised retrieval probe, or pre-training across more than one institution or domain.
- If this evidence is absent, reframe the claim as a domain-specific multi-task model, contrastive model, or task-specific model.
- Require a glossary or Discussion paragraph defining the term exactly as used by the authors.

### 2. Reference-standard symmetry between internal and external cohorts

- Verify that internal and external performance are compared against similar label quality.
- If internal validation uses a gold standard and external validation uses report-derived, billing-code, single-reader, or NLP-derived labels, require a like-for-like internal metric using the noisier label.
- Require an expert audit of a random sample from the noisier label source.
- Propagate estimated label error as a sensitivity bound around the external metric.

### 3. Prognostic and survival sub-studies

- Flag prognostic claims as fragile when patient count is under 500, event count is under 100, median follow-up is under 12 months, or patients without follow-up are excluded rather than censored.
- Require patient count, event count, median follow-up, maximum follow-up, and censoring approach in the main manuscript.
- Decompose composite endpoints. Report hard endpoints such as death and myocardial infarction separately from softer endpoints such as revascularization.
- Require inverse-probability-of-follow-up sensitivity analysis or worst-case imputation when follow-up is incomplete.

### 4. Clinical positioning of automated interpretation

- Avoid framing the AI as real-time operator assistance when a trained operator already interprets the input at the same speed.
- Require at least three non-real-time use cases, such as structured reporting, variance reduction, retrospective research at scale, trainee education, audit or quality control, or downstream multimodal integration.
- Frame clinical use as workflow support unless prospective deployment data proves decision support value.

### 5. Label noise and report-derived ground truth

- For labels derived from clinical reports, LLM extraction, or NLP pipelines, require a human-adjudicated audit on a random sample.
- Report per-class precision and recall for the extraction process.
- Add a confusion matrix between report-derived and adjudicated labels when both exist.
- Require a retrain-on-clean-labels or evaluate-on-clean-labels sensitivity analysis when feasible.

### 6. Hardware, vendor, and acquisition variation

- Require counts by scanner, vendor, acquisition protocol, or equivalent modality-specific metadata.
- For DICOM imaging, extract Manufacturer and ManufacturerModelName when available.
- Report per-vendor or per-protocol performance in Extended Material when sample size permits.
- Discuss any single-vendor or single-protocol limitation directly.

### 7. Architecture and hyperparameter sensitivity

- Identify one hyperparameter most likely to affect the headline result and most likely to be challenged by reviewers.
- Require a short-schedule ablation on that parameter when feasible, for example patch size, frame count, stride, learning-rate schedule, augmentation intensity, or encoder freeze ratio.
- Report the ablation as a robustness check, not as a full model search.

### 8. Failure-mode analysis

- Require a failure-mode supplementary panel before submission.
- Include a confusion matrix stratified by clinically meaningful category, such as anatomic region, territory, cohort, scanner, or disease severity.
- Include a calibration plot and 6 to 12 representative false-positive and false-negative cases with image panels when permitted and one-line clinical narratives.
- Add an operator-vs-model concordance heatmap when the manuscript compares model output to clinician decisions.

### 9. Unit of analysis clarity

- Require a Methods paragraph titled "Unit of analysis".
- State the unit for training, validation, evaluation, and reporting, such as pixel, frame, video, lesion, vessel, study, encounter, or patient.
- Tag every Results subsection with the denominator used for the metric.
- Flag any metric where the unit changes between training, evaluation, and reporting without explanation.

### 10. Subgroup performance and fairness

- Require sex-stratified and age-stratified model performance for every classification paper.
- Add race, ethnicity, socioeconomic status, and disease-severity strata when available and appropriate.
- If women represent less than 35% of the cohort, require a limitations sentence addressing underrepresentation and possible implications for non-obstructive disease, microvascular disease, and atypical presentations when clinically relevant.
- Report interaction testing or explicitly state when the study is underpowered for subgroup interaction tests.

### 11. Statistical reporting and typography

- Report AUROC and similar headline metrics to two decimals in the abstract and main text.
- Do not use three-decimal precision in the abstract.
- Use "to" for numeric ranges unless journal style requires otherwise.
- Use lowercase italic *p* for p values.
- Avoid `vs.`, `approx`, `i.e.`, and `e.g.` in polished submission text.
- Use `mean (SD)`, not mean plus/minus SD notation.
- Use Oxford commas, "compared with", and `n =` with spaces.
- Run `python manuscript-review/scripts/typography_qc.py <draft.txt>` before submission.

### 12. Abbreviation discipline

- Define every abbreviation at first mention within each major section: Abstract, Introduction, Methods, Results, and Discussion.
- Treat the abbreviation list as a backstop, not a substitute for in-section definition.
- Regex-audit all all-caps tokens of length 2 to 5 and require the expansion within 80 characters of first occurrence in each section.

### 13. Figure clarity and CONSORT cohort flow

- Require a CONSORT-style flow diagram when more than 20% of available data is excluded.
- Every exclusion branch must include reason and count.
- Confirm all figure labels remain legible at print resolution and 100% scale.
- Flag overlapping labels, missing denominators, and unclear panel references.

### 14. Public code, data, and reproducibility infrastructure

- If code is public, verify the repository is reviewer-readable.
- Require a `dataset_creation/README.md` or equivalent file describing input schema, expected metadata, preprocessing steps, LLM prompts used for label extraction, and validation procedures.
- Include the repository URL in the abstract or data/code availability statement when allowed by journal policy.

### 15. Prospective evaluation and journal targeting

- At submission time, state whether prospective deployment, prospective reader study, or silent-mode evaluation data exist.
- If none exist, treat absence of prospective evidence as a substantive limitation for top-tier general medical and digital-health journals.
- Align target journal choice with the evidence level: retrospective external validation is baseline, not a differentiator.

### 16. Discordance versus decisions reporting

- When model output is compared with operator or clinician decisions, report discordance rate and characterize discordant cases.
- Use humble framing. Discordance is a signal for review or hypothesis generation, not proof that the model is right.
- Include a table stratifying discordance by decision type, risk group, anatomic region or modality-specific category, and available outcome.

### 17. Agreement and continuous-measurement validation

- For models that estimate a continuous clinical quantity or substitute for a reference device, require Bland-Altman analysis with limits of agreement in the intended clinical population. Pearson r, coefficient of determination, or intraclass correlation alone quantify association, not agreement, and do not establish clinical accuracy.
- Require the limits of agreement to be interpreted against the minimum clinically important difference, the effect size that matters in the domain. A tool with limits of agreement of plus or minus 10 mL/kg/min cannot support a use case built on a 1.5 mL/kg/min treatment effect.
- Flag systematic directional bias in the intended population. Errors that do not average out, shown as a slope or offset in the Bland-Altman residuals within the target disease group, are disqualifying even when overall performance looks acceptable.
- Flag demographic confounding. When model inputs overlap substantially with known clinical determinants such as age, sex, and body mass index, require isolation of the novel signal. Otherwise the reported correlation may be demographic rather than physiological.
- Treat regulatory clearance as context, not validation. United States Food and Drug Administration (FDA) 510(k) clearance means substantial equivalence to a predicate device, not demonstrated clinical utility. Do not accept 510(k), CE mark, or commercial deployment as evidence of clinical readiness.
- Require methodology that is internally consistent and independently verifiable. Flag pipelines described differently between the abstract and Methods, and proprietary or opaque methods that cannot be reproduced or audited.

### Cross-cutting submission discipline

- The manuscript must be readable end-to-end without requiring the supplement for sample sizes, denominators, or headline metric definitions.
- Abstract headline metrics must match the corresponding table values exactly to the second decimal.
- Build the reusable artifacts before submission: typography QC output, label-noise sensitivity table, failure-mode panel, CONSORT flow, and Table 1 denominators.

---

## Full Manuscript Review Command

```
RUN full_review():
  sections = [Objectives, Background, Methods, Results, Tables, Discussion, Abstract, ReviewerPatterns]
  FOR section in sections:
    PRINT "=== Reviewing {section} ==="
    RUN section_checklist(section)
    PRINT summary(passed, failed, total)
  PRINT "=== MANUSCRIPT REVIEW COMPLETE ==="
  RETURN overall_compliance_score
```

---

## Quick Reference: Forbidden Patterns

| Do Not Use | Use Instead |
|------------|-------------|
| F1-score | AUROC, AUPRC |
| Recall | Sensitivity |
| Accuracy | Sensitivity + Specificity |
| Em dash characters | Commas, parentheses |
| Hyphens or dashes in CI ranges | `to`, for example `0.79 to 0.91` |
| Interpretation in Results | Move to Discussion |
| Vague gaps | Specific, actionable gaps |
| Abbreviations with "=" | Use colon: `LVEF: Left Ventricular Ejection Fraction` |
| Abbreviations separated by commas | Use semicolons between entries |
| Unexpanded abbreviations | Expand at first use: Full Name (ABBREVIATION) |
| `vs.` | `versus` or `compared with` |
| `i.e.` or `e.g.` | `that is`, `for example`, or direct wording |
| `mean +/- SD` | `mean (SD)` |
| Pearson r or ICC alone for agreement | Bland-Altman with limits of agreement |
| 510(k) framed as clinical validation | State as substantial equivalence to a predicate device only |
