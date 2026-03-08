---
name: manuscript-writing
description: Full guide for writing a medical AI manuscript from scratch, covering all sections (Introduction, Methods, Results, Discussion, Abstract) with structure, style, and reporting standards. Use when drafting a new AI manuscript or when you need section-by-section writing instructions beyond TRIPOD-AI results reporting.
---

# AI Manuscript Writing Guide

A section-by-section guide for writing medical AI manuscripts, from blank page to submission-ready draft.

---

## General Style Rules

- **No em dashes** — use commas, parentheses, or separate sentences
- Write Results in **past tense**, Discussion in **present tense**
- Report all metrics with **95% confidence intervals**
- **No interpretation in Results** — keep interpretation in Discussion only
- Maximum one acronym introduced per paragraph; spell out on first use
- Never use F1-score, recall, or accuracy as primary performance metrics

---

## 1. Title & Authors

**Title formula:** `[Model/Approach] for [Task] using [Data Source]: [Design]`

Example: *"Deep Learning Detection of Left Ventricular Dysfunction from 12-Lead ECG: A Multicenter Validation Study"*

- Keep under 15 words
- Avoid starting with "A" or "The"
- Include study design (Prospective, Multicenter, Randomized)

**Authorship order:**
1. First author: primary contributor to experiments + writing
2. Middle authors: data, methods, clinical input
3. Penultimate: senior statistician or domain expert
4. Last: senior/corresponding author (lab PI)

---

## 2. Abstract

> Write this **last**, after all sections are complete.

**Structured format (250–300 words):**

| Subsection | Content | Sentences |
|---|---|---|
| Background | Clinical problem + gap | 2 |
| Objective | What this study does | 1 |
| Methods | Design, cohort, model, metrics | 3–4 |
| Results | Primary outcome with metric + CI | 2–3 |
| Conclusion | Key clinical implication | 1–2 |

**Rules:**
- No citations in abstract
- Include primary metric with 95% CI (e.g., AUROC 0.91, 95% CI 0.88–0.94)
- For classification models: include sensitivity and specificity at reported threshold
- State the threshold used (e.g., Youden Index, prespecified operating point)

---

## 3. Introduction / Background

**Structure (4–5 paragraphs):**

### Paragraph 1 — Clinical Problem
- Open with the disease burden (incidence, mortality, cost)
- Quantify the diagnostic challenge (missed diagnoses, diagnostic delay, resource burden)
- No AI mention yet

### Paragraph 2 — Current Standard of Care & Limitations
- Describe existing diagnostic approach and its limitations
- Cite reproducibility, access, cost, or inter-observer variability data

### Paragraph 3 — AI in This Space (Literature)
- Trace AI approaches from traditional ML → deep learning
- Cite key prior works with their best-reported metrics
- Identify specific gaps: external validation, prospective design, subgroup fairness, real-world deployment

### Paragraph 4 — What This Study Does
- State your contribution directly: "In this study, we developed and externally validated..."
- Each gap from paragraph 3 maps to one contribution here

### Paragraph 5 — Roadmap (optional but recommended)
- "This paper is organized as follows..."
- Only include if journal allows or paper is complex

**Forbidden in Introduction:**
- Presenting results
- Vague gaps ("more work is needed")
- Overclaiming novelty without citation support

---

## 4. Methods

**Required subsections, in this order:**

### 4.1 Ethics Statement (FIRST, always)
```
This study was approved by [Institution] Institutional Review Board (IRB #XXXX).
Informed consent was [obtained / waived] given the [prospective/retrospective] design.
If large language models were used in manuscript preparation, disclose here.
```

### 4.2 Study Design & Data Sources
- Study type: retrospective / prospective / randomized
- Institutions involved, years of data collection
- Internal vs. external validation datasets

**Flowchart:** Include a CONSORT/PRISMA-style flowchart as Figure 1 showing:
- Total records screened
- Exclusions with reasons
- Final training / validation / test set sizes
- Event counts in each split

### 4.3 Inclusion / Exclusion Criteria
- List all criteria as bullet points
- Include age ranges, diagnostic codes, date ranges
- State who made eligibility decisions (automated vs. adjudicated)

### 4.4 Outcome Definition
- Primary outcome: exact definition, ICD codes, or measurement method
- Secondary outcomes if applicable
- Adjudication process

### 4.5 Model Development

**For deep learning models:**
```
Architecture: [name, version, input dimensions]
Pre-training: [ImageNet / ECG foundation model / from scratch]
Training: [optimizer, learning rate, batch size, epochs, early stopping criterion]
Augmentation: [list augmentations used]
Loss function: [cross-entropy, focal loss, etc.]
Hardware: [GPU model, memory, training time]
```

**For traditional ML:**
```
Features: [list or reference feature table]
Preprocessing: [normalization, imputation, scaling]
Model: [name, hyperparameter search strategy, CV folds]
Feature selection: [method used]
```

**Threshold selection — REQUIRED for binary classification:**

State explicitly how the operating threshold is chosen:
- **Youden Index** (maximizes sensitivity + specificity): recommended default
- **Prespecified clinical threshold** (e.g., sensitivity ≥ 90%): when clinical constraints drive the operating point
- **Cost-sensitive threshold**: when FP/FN costs differ clinically

> Example: *"The operating threshold was selected using the Youden Index (J = sensitivity + specificity − 1) on the internal validation set and applied without modification to all external validation cohorts."*

### 4.6 Statistical Analysis
- Primary metric: AUROC with 95% CI (DeLong method)
- Secondary metrics: AUPRC, Sensitivity, Specificity, PPV, NPV at reported threshold
- Confidence intervals: bootstrap (1000 iterations) or DeLong
- Subgroup analyses: prespecified groups (age, sex, race, disease severity)
- Calibration: Brier score, calibration curves
- Comparison to baseline: likelihood ratio test or net reclassification improvement (NRI)
- Software: Python [version] / R [version] / SAS [version]

---

## 5. Results

**Paragraph order must mirror Methods subsections exactly.**

### 5.1 Cohort Description
- Total included, excluded (with reasons)
- Demographic breakdown (Table 1)
- Outcome prevalence in each split

### 5.2 Model Performance (Table 2)

**Required metrics for classification models:**
- AUROC (95% CI)
- AUPRC (95% CI)
- Sensitivity, Specificity, PPV, NPV — **all at the reported threshold**
- **State the threshold explicitly in the table footnote**

> Table 2 footnote format: *"Sensitivity, Specificity, PPV, and NPV calculated at the threshold maximizing the Youden Index (threshold = 0.XX on internal validation set)."*

**For regression models:**
- Mean Absolute Error (MAE)
- Root Mean Square Error (RMSE)
- R² / concordance correlation coefficient

### 5.3 External Validation
- Repeat Table 2 metrics for each external cohort
- Note if threshold was re-derived or fixed from development set

### 5.4 Subgroup Analysis (Table 3)
- Performance stratified by key subgroups
- Forest plot recommended for visual summary

### 5.5 Sensitivity / Supplementary Analyses
- If applicable: performance under data augmentation, different thresholds, model ablation

**Results writing rules:**
- Past tense throughout
- No "why" statements — no interpretation
- Every table/figure cited in order
- Point estimate + 95% CI for every metric

---

## 6. Discussion

**Structure: Answer 6 questions in order**

### Paragraph 1 — Main Finding (MANDATORY opening)
State the primary result and its clinical meaning in 2–3 sentences.
> *"We developed and externally validated a deep learning model for [task] achieving AUROC 0.91 (95% CI 0.88–0.94), demonstrating..."*

### Paragraph 2 — What Is Different from Prior Work
- Compare your key metrics to the best-cited prior results
- Explain why your approach differs: more data, prospective design, external validation, fairness

### Paragraph 3 — What Is Similar to Prior Work
- Acknowledges concordant findings to reinforce validity
- Builds credibility rather than dismissing prior literature

### Paragraph 4 — How Results Sections Correlate
- Synthesizes subgroup, calibration, and primary findings
- Draws internal consistency conclusions

### Paragraph 5 — Clinical Implications for Practitioners
- Workflow integration: where does this model fit?
- Which patients benefit most?
- What human oversight is still needed?

### Paragraph 6 — Research Implications
- What should the field study next?
- What methodological gaps remain?

### Paragraph 7 — Limitations (MANDATORY)
Standard limitations to address:
- Retrospective design (if applicable)
- Single-center development (if applicable)
- Missing subgroup data
- Lack of prospective outcome data
- Threshold generalizability

### Paragraph 8 — Conclusion (MANDATORY final paragraph)
- 2–4 sentences
- Restate main finding + clinical implication
- No new data or citations

---

## 7. Tables Reference

### Table 1. Baseline Characteristics

| Variable | Development (n=X) | External Validation (n=X) |
|---|---|---|
| Age, years, mean ± SD | | |
| Female sex, n (%) | | |
| [Primary outcome], n (%) | | |

*Abbreviations: SD = standard deviation.*

### Table 2. Model Performance

| Metric | Internal Validation | External Validation |
|---|---|---|
| AUROC (95% CI) | 0.91 (0.88–0.94) | 0.89 (0.85–0.93) |
| AUPRC (95% CI) | | |
| Sensitivity | | |
| Specificity | | |
| PPV | | |
| NPV | | |

*Abbreviations: AUROC = Area under the receiver operating characteristic curve; AUPRC = Area under the precision-recall curve; PPV = Positive predictive value; NPV = Negative predictive value.*
*Threshold: Sensitivity, Specificity, PPV, and NPV calculated at the Youden Index threshold (threshold = 0.XX on internal validation set).*

### Table 3. Subgroup Analysis

Report AUROC by: Age group, Sex, Disease severity (at minimum).

---

## 8. Figures Reference

| Figure | Content | Required? |
|---|---|---|
| Figure 1 | Patient/data flowchart | Always |
| Figure 2 | ROC curve (with CI band) | Classification models |
| Figure 3 | Calibration curve | Always |
| Figure 4 | Subgroup forest plot | Recommended |
| Figure 5 | Decision curve analysis | Recommended |

---

## 9. Submission Checklist

- [ ] Title ≤ 15 words, includes study design
- [ ] Abstract written last, includes threshold statement for classification
- [ ] Ethics statement is the first Methods subsection
- [ ] LLM use disclosed if applicable
- [ ] Figure 1 is a flowchart with exact exclusion numbers
- [ ] Table 2 footnote explicitly states threshold and how it was selected
- [ ] All metrics reported with 95% CI
- [ ] No F1, recall, or accuracy as primary metrics
- [ ] Results contain no interpretation
- [ ] Discussion addresses all 6 questions
- [ ] Limitations section present
- [ ] Final paragraph is Conclusion only
- [ ] Code/model available on GitHub or HuggingFace
- [ ] TRIPOD+AI checklist completed (attach as supplement)
- [ ] No em dashes anywhere in manuscript
