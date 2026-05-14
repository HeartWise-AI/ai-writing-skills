---
name: manuscript-writing-tripod
description: Guide for writing AI paper following TRIPOD+AI guidelines, covering objective identification, data sources, model development, evaluation criteria with sensitivity analysis, and presentation best practices. Use when writing or structuring a medical AI manuscript.
---

# How to Write an AI Paper (TRIPOD-AI Guidelines)

Based on the TRIPOD+AI guidelines, here are bullet point guidelines for presenting AI paper results to medical students and bioengineers.

Reusable assets in this skill:

- `scripts/typography_qc.py`: regex-based typography and abbreviation audit for pre-submission drafts
- `templates/label_noise_sensitivity_template.md`: label-noise sensitivity analysis template
- `templates/failure_mode_panel_template.md`: supplementary failure-mode panel template
- `templates/failure_mode_panel_template.ipynb`: executable failure-mode panel notebook skeleton
- `templates/consort_flow_table1_template.md`: CONSORT-style flow and Table 1 denominator template

## Step 0: Identify Primary and Secondary Objectives

Before writing any section, extract and classify the study objectives.

**Primary Objective:** The single main question the study answers. There is exactly one.

**Secondary Objectives:** Additional analyses that support, extend, or contextualize the primary objective.

### Objective-to-Methods Mapping Table

For each objective, define the data source, model development approach, and evaluation criteria before drafting. This table drives the structure of Methods and Results.


| Component                | Primary Objective                                                                                      | Secondary Objective(s)                                                     |
| ------------------------ | ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| **Data Source**          | Which dataset(s), cohort(s), or registry(ies) are used. Specify name, years, sample size, and linkage. | May use the same or different datasets (e.g., external validation cohort). |
| **Data Preprocessing**   | Signal/image processing, feature extraction, missing data handling, inclusion/exclusion applied.       | Any additional preprocessing specific to this objective.                   |
| **Model Development**    | Architecture, training strategy, hyperparameters, cross-validation scheme.                             | May reuse the primary model or develop a separate model. Specify clearly.  |
| **External Validation**  | External cohort source, size, domain adaptation. If absent, justify as limitation.                     | May use a separate external cohort or the same as primary.                 |
| **Model Evaluation**     | Discrimination (AUROC, AUPRC), calibration, threshold selection.                                       | Same or different metrics depending on the secondary question.             |
| **Statistical Analysis** | Hypothesis tests, confidence intervals, comparison to reference standard.                              | Subgroup analyses, interaction tests, etc.                                 |
| **Sensitivity Analysis** | What assumptions are varied and how robustness is assessed (see Evaluation Criteria below).            | Objective-specific sensitivity analyses.                                   |


Every Methods subsection and every Results subsection must trace back to a row in this table.

## Reviewer-Resilience Checklist for Medical-AI Manuscript Drafting

Build these items into the first complete manuscript draft rather than saving them for reviewer response. Keep context general and adapt the wording to the clinical domain, modality, and journal.

1. **Foundation-model and novelty framing**: Use "foundation model", "general-purpose", or "universal" only when the manuscript includes operational evidence, such as zero-shot or few-shot transfer on a held-out task, a self-supervised retrieval probe, or pre-training across more than one institution or domain. If not, use a narrower term such as domain-specific multi-task model, contrastive model, or task-specific model. Define the term in a glossary or Discussion paragraph.
2. **Reference-standard symmetry**: If external validation uses a noisier label than internal validation, add a like-for-like internal result against the noisier label, audit the external label source, and report a label-noise sensitivity bound.
3. **Prognostic and survival sub-studies**: Report patient count, event count, median follow-up, maximum follow-up, censoring approach, and endpoint decomposition. Add inverse-probability-of-follow-up or worst-case imputation sensitivity when follow-up is incomplete.
4. **Clinical positioning**: Do not rely on real-time operator assistance as the main value proposition when the operator already interprets the input quickly. Name at least three non-real-time use cases, such as structured reporting, variance reduction, retrospective research at scale, trainee education, audit or quality control, or downstream multimodal integration.
5. **Label noise and report-derived labels**: For report-derived, LLM-derived, NLP-derived, billing-code, or single-reader labels, include a human-adjudicated random audit, per-class precision and recall, a confusion matrix against adjudicated labels where available, and a clean-label sensitivity analysis when feasible.
6. **Hardware, vendor, and acquisition variation**: Extract modality-specific acquisition metadata. For DICOM imaging, use Manufacturer and ManufacturerModelName when available. Report vendor or protocol counts in Methods and per-vendor or per-protocol performance in Extended Material when sample size permits.
7. **Architecture and hyperparameter sensitivity**: Preselect one likely reviewer-challenged hyperparameter and run a short-schedule ablation when feasible, such as patch size, frame count, stride, learning-rate schedule, augmentation intensity, or encoder freeze ratio.
8. **Failure-mode analysis**: Prepare a supplementary failure-mode panel with confusion matrices by clinically meaningful strata, calibration, representative false-positive and false-negative cases, and operator-vs-model concordance when relevant.
9. **Unit of analysis clarity**: Add a Methods paragraph titled "Unit of analysis". State the unit for training, validation, evaluation, and reporting, and tag each Results subsection with its denominator.
10. **Subgroup performance and fairness**: Include sex-stratified and age-stratified performance for classification papers. Add race, ethnicity, socioeconomic status, and disease-severity strata when available. If women are under 35% of the cohort, include a limitations sentence addressing underrepresentation and clinically relevant implications.
11. **Statistical reporting and typography**: Use two decimals for AUROC and related headline metrics. Use "to" for ranges unless journal style requires otherwise. Use lowercase italic *p*, `mean (SD)`, Oxford commas, "compared with", and `n =` with spaces. Avoid `vs.`, `approx`, `i.e.`, and `e.g.` in polished text. Run `python manuscript-writing-tripod/scripts/typography_qc.py <draft.txt>` before submission.
12. **Abbreviation discipline**: Define every abbreviation at first mention in each major section. Regex-audit all all-caps tokens of length 2 to 5 and require expansion near first use.
13. **Figure clarity and CONSORT cohort flow**: Add a CONSORT-style flow when more than 20% of available data is excluded. Include reason and count for each exclusion branch. Check figure legibility at print resolution and 100% scale.
14. **Public code, data, and reproducibility**: If a public repository is provided, include a `dataset_creation/README.md` or equivalent with input schema, expected metadata, preprocessing steps, prompts used for label extraction, and validation procedures. Include the repository URL where journal policy allows.
15. **Prospective evaluation and journal targeting**: State whether prospective deployment, prospective reader-study, or silent-mode evaluation data exist. If absent, treat this as a substantive limitation for top-tier general medical and digital-health journals.
16. **Discordance versus decisions**: When comparing model output with clinician or operator decisions, report discordance rate and characterize discordant cases. Frame discordance as a signal for review or hypothesis generation, not proof that the model is right.

Cross-cutting rule: the manuscript must be readable end-to-end without requiring the supplement for sample sizes, denominators, or headline metric definitions. Abstract headline metrics must match the corresponding table values exactly to the second decimal.

## Abbreviation Rules

Expand every abbreviation at first use in the text, with the abbreviation in parentheses. After first use, use the abbreviation only.

**Format:** Full Name (ABBREVIATION)

**Common abbreviations in medical AI manuscripts:**


| Abbreviation | Full Form                                                                                       |
| ------------ | ----------------------------------------------------------------------------------------------- |
| AUROC        | Area Under the Receiver Operating Characteristic Curve                                          |
| AUPRC        | Area Under the Precision-Recall Curve                                                           |
| PPV          | Positive Predictive Value                                                                       |
| NPV          | Negative Predictive Value                                                                       |
| CI           | Confidence Interval                                                                             |
| CLSA         | Canadian Longitudinal Study on Aging                                                            |
| TRIPOD       | Transparent Reporting of a Multivariable Prediction Model for Individual Prognosis or Diagnosis |
| EHR          | Electronic Health Record                                                                        |
| NRI          | Net Reclassification Improvement                                                                |
| PVD          | Peripheral Vascular Disease                                                                     |
| BMI          | Body Mass Index                                                                                 |
| IRB          | Institutional Review Board                                                                      |
| REB          | Research Ethics Board                                                                           |
| DCA          | Decision Curve Analysis                                                                         |
| ROC          | Receiver Operating Characteristic                                                               |


Add study-specific abbreviations to this table as they appear. Define each abbreviation in the text at first use AND in a consolidated abbreviation list in the supplement.

## Methods Section Structure (Main Manuscript)

The main manuscript Methods must contain the following subsections in order. All other methodological details go in the Supplement.

### 1. Data Source for Model Development (Item 20)

- Name and describe each dataset fully at first mention
  - Example: "The Canadian Longitudinal Study on Aging (CLSA) is a national longitudinal study..."
- Specify years of data collection, geographic scope, and sample size
- State inclusion and exclusion criteria with numeric thresholds
- Report the number of participants and outcome events at each stage
- Describe cohort linkage when multiple datasets are merged
- Map which data source serves which objective (primary vs. secondary)
- Add a dedicated "Unit of analysis" paragraph that states the unit for training, validation, evaluation, and reporting
- Report label source and reference standard for each cohort, including whether labels are adjudicated, report-derived, billing-code-derived, single-reader, NLP-derived, or LLM-derived
- Report acquisition metadata availability, including vendor, scanner, protocol, or equivalent modality-specific fields

### 2. Data Preprocessing

- Signal or image processing (filtering, normalization, resampling)
- Feature extraction and selection
- Missing data handling (imputation method or complete-case justification)
- Train/validation/test split strategy with sizes and stratification
- Label-extraction pipeline if labels are derived from reports or notes, including prompts or rules used
- Human-adjudication workflow for label audits

### 3. Model Development (Items 21 to 22)

- Specify exact sample sizes for each analysis phase:
  - Training set size and outcome events
  - Hyperparameter tuning set size
  - Internal validation set size
- Provide complete model specifications enabling reproduction:
  - Mathematical formulas for regression models
  - Architecture details for neural networks (layers, nodes, activation functions)
  - Hyperparameter values used
- Map each model to its corresponding objective (primary or secondary)
- Include code repositories or supplementary implementation details
- Report computational resources and training time when relevant
- Justify any foundation-model, general-purpose, or universal framing with transfer or retrieval evidence; otherwise use narrower terminology
- Predefine one short-schedule hyperparameter ablation most likely to address reviewer concern

### 4. External Validation (Optional)

- External validation set size and source
- Describe the external cohort (different institution, time period, or population)
- Report any domain adaptation or recalibration applied
- If no external validation, justify and acknowledge as a limitation
- If the external label is noisier than the internal label, report the same noisy-label metric internally and include label-noise sensitivity analysis

### 5. Model Evaluation and Statistical Methods (Item 23a)

**Evaluation Criteria: map to each objective:**


| Criterion           | Primary Objective                                                | Secondary Objective(s)                      |
| ------------------- | ---------------------------------------------------------------- | ------------------------------------------- |
| Discrimination      | AUROC, AUPRC with 95% CI                                         | Specify per objective                       |
| Calibration         | Calibration plot, Hosmer-Lemeshow or calibration slope/intercept | Same or adapted                             |
| Threshold selection | Youden Index, clinical utility threshold                         | Same or adapted                             |
| Clinical utility    | Decision Curve Analysis (DCA), net benefit                       | If applicable                               |
| Comparison          | vs. existing clinical scores or simple models                    | vs. primary model or alternative approaches |


**Sensitivity Analysis (required for both primary and secondary objectives):**

- Vary key assumptions and report impact on primary metric:
  - Alternative outcome definitions (e.g., different diagnostic thresholds)
  - Alternative inclusion/exclusion criteria
  - Alternative imputation strategies for missing data
  - Restricted populations (e.g., excluding borderline cases)
  - Alternative model architectures or hyperparameter ranges
  - Impact of class imbalance correction methods
  - Label-noise bounds for report-derived, NLP-derived, or LLM-derived labels
  - Worst-case or inverse-probability-of-follow-up analysis for incomplete follow-up
- Present sensitivity analysis results in a dedicated table or figure

**Statistical methods:**

- Hypothesis tests, Confidence Intervals (CI) via bootstrap or DeLong, significance thresholds
- Comparison to reference standard
- Multiple comparison correction when applicable
- Survival analysis details when applicable: event definitions, censoring, follow-up distribution, composite endpoint components, and incomplete-follow-up handling

### What Goes in the Supplement

- Extended data preprocessing details (e.g., full signal processing pipeline)
- Full hyperparameter search space and tuning logs
- Additional ablation experiments
- Heterogeneity assessment across centers/datasets (Item 23b)
- Model updating and recalibration results (Item 24)
- Extended sensitivity analysis tables
- Label-noise sensitivity analysis
- Failure-mode panel
- Vendor, scanner, protocol, or acquisition heterogeneity tables
- CONSORT-style flow and full Table 1 denominator audit
- Code and reproducibility details beyond what fits in main text
- Consolidated abbreviation list

## Results Section Structure

Results must mirror the Methods subsections in order.

### Participants and Data Flow

- Report participant flow with clear numbers at each stage (development, validation, exclusion)
- Include demographic characteristics, baseline predictors, and outcome frequencies
- Show missing data patterns and follow-up times
- Report differences across demographic subgroups (Table 1)
- Report denominators in every Results subsection
- If more than 20% of available data is excluded, include a CONSORT-style flow diagram with explicit exclusion counts and reasons

### Figures

**Figure 1** should always be a flow chart showing data flow.

If multiple datasets are merged, include separate branches for each dataset.

### Primary Objective Results

- Present model performance on the primary objective first
- Report all evaluation criteria from the mapping table with 95% CI

### Secondary Objective Results

- Present each secondary objective's results in a separate subsection
- Reference the specific data source and model used for each

### Sensitivity Analysis Results

- Dedicated subsection showing robustness of primary and secondary findings
- Reference the specific assumptions varied
- Include label-noise sensitivity results when any label source is report-derived, NLP-derived, LLM-derived, billing-code-derived, or single-reader
- Include follow-up sensitivity results for prognostic or survival analyses with incomplete follow-up

### Failure-Mode and Discordance Results

- Include a confusion matrix by clinically meaningful strata
- Include calibration and representative false-positive and false-negative cases when feasible
- Report operator-vs-model discordance rate when model outputs are compared with clinician or operator decisions
- Characterize discordant cases without implying the model is inherently correct

### Table 1. Baseline characteristics

Expand all abbreviations below the table.

Table 1 must include denominators for every row, missingness for key variables, and representation by sex, age, race or ethnicity when available, and disease severity.

### Table 2. Results on internal dataset

Abbreviations: AUROC: Area Under the Receiver Operating Characteristic Curve; PPV: Positive Predictive Value; NPV: Negative Predictive Value

*Threshold calculated at Youden Index

### Guidelines for Table 2

**For Regression Models (Continuous Outcomes):**

- Report discrimination metrics with 95% confidence intervals
- Comparison to clinically meaningful difference thresholds

**For Classification Models (Binary/Categorical Outcomes):**

- Report discrimination metrics with 95% confidence intervals
- IN ALL CASES: include calibration metrics
- **REQUIRED: Threshold Reporting:** Sensitivity, Specificity, PPV, and NPV must be accompanied by an explicit statement of the decision threshold used and how it was selected. Acceptable methods:
  - **Youden Index** (J = sensitivity + specificity - 1): maximizes combined sensitivity and specificity; use as default
  - **Prespecified sensitivity target** (e.g., >= 90% sensitivity): use when clinical context requires a minimum detection rate
  - **Cost-sensitive threshold**: use when FP and FN carry different clinical consequences
- Table 2 footnote MUST include: *"Sensitivity, Specificity, PPV, and NPV calculated at the threshold maximizing the Youden Index (threshold = 0.XX on internal validation set)."* (or equivalent for other methods)
- **FAIL condition:** Reporting Sensitivity/Specificity without stating the threshold or selection method is non-compliant with TRIPOD+AI Item 23a.

### Subgroup Analysis (Item 23a) - Table 3

- Stratify performance by key demographic groups:
  - Age categories
  - Sex/gender
  - Race/ethnicity
  - Socioeconomic status
  - Disease severity levels
- Test for statistical interactions between subgroups
- Address fairness implications of differential performance
- Include sex-stratified and age-stratified AUROC for every classification paper
- Add a limitations sentence when key groups are underrepresented

### Heterogeneity Assessment (Item 23b) - IF APPLICABLE (Supplement)

- Report between-center/dataset variability when applicable
- Use forest plots to visualize performance across sites
- Calculate I^2 statistics for heterogeneity quantification
- Discuss clinical implications of performance variation

### Model Updating Results (Item 24) - IF APPLICABLE (Supplement)

- Document any recalibration procedures performed
- Report before/after performance comparisons
- Specify populations or settings where updates were needed
- Include updated model parameters and performance metrics

## Presentation Best Practices

### Visual Elements

**For Regression Models:**

- Use calibration plots to show predicted vs. observed continuous values
- Include residual plots to assess model assumptions
- Create scatter plots of predicted vs. actual values with identity line
- Show distribution plots of residuals by predictor variables

**For Classification Models:**

- Use calibration plots to demonstrate agreement between predicted probabilities and observed frequencies
- Include Receiver Operating Characteristic (ROC) curves with confidence intervals and AUROC values
- Create Decision Curve Analysis (DCA) plots for clinical utility
- Show distribution plots of predicted probabilities by outcome status
- Present confusion matrices at optimal thresholds

### Clinical Context - Discussion

**For Regression Models:**

- Interpret prediction accuracy in terms of clinical decision-making relevance
- Compare prediction intervals to clinically meaningful ranges
- Discuss practical implications of prediction uncertainty
- Address generalizability across different patient populations

**For Classification Models:**

- Interpret performance metrics in terms of clinical decision-making
- Compare results to existing clinical standards or simple scoring systems
- Discuss practical implications of false positive/negative rates
- Address cost-benefit considerations of different threshold choices

### Transparency Requirements

- Report all prespecified analyses, including negative results
- Acknowledge any post-hoc analyses performed
- Discuss limitations affecting result interpretation
- Provide sufficient detail for independent validation studies

---

These guidelines ensure comprehensive, transparent reporting that enables critical appraisal and potential clinical implementation of AI prediction models for both regression and classification tasks.
