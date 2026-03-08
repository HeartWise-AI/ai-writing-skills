---
name: manuscript-writing-tripod
description: Guide for writing AI paper results following TRIPOD+AI guidelines, covering participants, model development, performance metrics, and presentation best practices. Use when writing or structuring a medical AI manuscript results section.
---

# How to Write an AI Paper (TRIPOD-AI Guidelines)

Based on the TRIPOD+AI guidelines, here are bullet point guidelines for presenting AI paper results to medical students and bioengineers:

## Results Section Structure

### Participants and Data Flow (Item 20)

- Report participant flow with clear numbers at each stage (development, validation, exclusion)
- Include demographic characteristics, baseline predictors, and outcome frequencies
- Show missing data patterns and follow-up times
- Create flow diagrams for complex multi-stage studies
- Report differences across demographic subgroups (Table 1)

### Figures

**Figure 1** should always be a flow chart showing data flow.

If multiple datasets are merged, include separate branches for each dataset.

### Model Development Details (Item 21) - Methods

- Specify exact sample sizes for each analysis phase:
  - Training set size and outcome events
  - Hyperparameter tuning set size
  - Internal validation set size
  - External validation set size
- Report computational resources and training time when relevant

### Model Specification (Item 22) - Methods

- Provide complete model specifications enabling reproduction:
  - Mathematical formulas for regression models
  - Architecture details for neural networks (layers, nodes, activation functions)
  - Hyperparameter values used
  - Feature preprocessing steps
- Include code repositories or supplementary implementation details
- Specify any access restrictions or proprietary limitations

### Performance Metrics (Item 23a) - Results and Methods

- In methods: describe the metrics you will report
- In results: present these results

### Table 1. Baseline characteristics

Abbreviations: PVD = Peripheral vascular disease

### Table 2. Results on internal dataset

Abbreviations: AUROC = Area under the receiver operating characteristic curve; PPV = Positive predictive value; NPV = Negative predictive value

*Threshold calculated at Youden Index

### Guidelines for Table 2

**For Regression Models (Continuous Outcomes):**
- Report discrimination metrics with 95% confidence intervals
- Comparison to clinically meaningful difference thresholds

**For Classification Models (Binary/Categorical Outcomes):**
- Report discrimination metrics with 95% confidence intervals
- IN ALL CASES: include calibration metrics
- **REQUIRED — Threshold Reporting:** Sensitivity, Specificity, PPV, and NPV must be accompanied by an explicit statement of the decision threshold used and how it was selected. Acceptable methods:
  - **Youden Index** (J = sensitivity + specificity − 1): maximizes combined sensitivity and specificity; use as default
  - **Prespecified sensitivity target** (e.g., ≥ 90% sensitivity): use when clinical context requires a minimum detection rate
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

### Heterogeneity Assessment (Item 23b) - IF APPLICABLE (Table 4 or Supplement)

- Report between-center/dataset variability when applicable
- Use forest plots to visualize performance across sites
- Calculate I² statistics for heterogeneity quantification
- Discuss clinical implications of performance variation

### Model Updating Results (Item 24) - IF APPLICABLE (Table 4 or Supplement)

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
- Include ROC curves with confidence intervals and AUC values
- Create decision curve analysis plots for clinical utility
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
