# Failure-Mode Panel Template

Use this template to prepare a standard supplementary panel before submission. Adapt strata to the clinical domain and modality.

## Panel A. Confusion matrix by clinically meaningful stratum

Examples of strata: anatomic region, vessel, territory, view, scanner, vendor, cohort, disease severity, reader group, or acquisition protocol.

| Stratum | True positive | False positive | True negative | False negative | Error rate | Dominant failure pattern |
|---------|---------------|----------------|---------------|----------------|------------|--------------------------|
| [stratum 1] | [n] | [n] | [n] | [n] | [0.0%] | [text] |
| [stratum 2] | [n] | [n] | [n] | [n] | [0.0%] | [text] |

## Panel B. Calibration

- Calibration plot by risk decile or clinically meaningful probability bins
- Calibration slope and intercept
- Expected calibration error if used locally
- Separate calibration by external cohort when sample size permits

## Panel C. Subgroup or acquisition heatmap

| Group | n | Events | AUROC | Sensitivity | Specificity | Calibration slope | Notes |
|-------|---|--------|-------|-------------|-------------|-------------------|-------|
| Sex: women | [n] | [n] | [0.00] | [0.00] | [0.00] | [0.00] | [text] |
| Sex: men | [n] | [n] | [0.00] | [0.00] | [0.00] | [0.00] | [text] |
| Age: [group] | [n] | [n] | [0.00] | [0.00] | [0.00] | [0.00] | [text] |
| Vendor: [name] | [n] | [n] | [0.00] | [0.00] | [0.00] | [0.00] | [text] |

## Panel D. Representative false-positive and false-negative cases

Include 6 to 12 cases when image sharing and consent rules permit. Each case should include the input image or signal, model score, reference label, clinician label when available, and a one-line clinical narrative.

| Case | Error type | Unit of analysis | Model score | Reference label | Clinician decision | One-line clinical narrative | Likely failure driver |
|------|------------|------------------|-------------|-----------------|--------------------|-----------------------------|-----------------------|
| 1 | False positive | [unit] | [0.00] | [label] | [decision] | [text] | [text] |
| 2 | False negative | [unit] | [0.00] | [label] | [decision] | [text] | [text] |

## Panel E. Operator-versus-model concordance

Use this when the model is compared with operator, clinician, or reader decisions.

| Clinician decision | Model positive | Model negative | Discordance rate | Outcome available | Interpretation |
|--------------------|----------------|----------------|------------------|-------------------|----------------|
| Treat / positive | [n] | [n] | [0.0%] | [yes/no] | [text] |
| Do not treat / negative | [n] | [n] | [0.0%] | [yes/no] | [text] |

Required framing:

```text
Discordance was treated as a signal for further review and hypothesis generation, not as evidence that either the model or recorded clinical decision was correct in isolation.
```

## Figure caption checklist

- State the unit of analysis.
- State the cohort and denominator for each panel.
- Define every abbreviation in the caption.
- State whether thresholds were prespecified or selected on internal validation.
- Keep the panel readable at 100% print scale.
