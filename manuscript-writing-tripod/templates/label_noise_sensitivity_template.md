# Label-Noise Sensitivity Analysis Template

Use this template when labels come from reports, billing codes, NLP pipelines, LLM extraction, single-reader interpretation, or any source weaker than adjudicated ground truth.

## 1. Label source inventory

| Cohort | Label source | Reference standard level | Human adjudication available | Notes |
|--------|--------------|--------------------------|------------------------------|-------|
| Internal development | [source] | [gold / adjudicated / report-derived / code-derived] | [yes/no] | [notes] |
| Internal validation | [source] | [gold / adjudicated / report-derived / code-derived] | [yes/no] | [notes] |
| External validation | [source] | [gold / adjudicated / report-derived / code-derived] | [yes/no] | [notes] |

## 2. Random audit design

- Audit sample size: [n]
- Sampling frame: [cohort, class balance, time period]
- Adjudicators: [number and expertise]
- Adjudication procedure: [independent review, consensus, tie-breaker]
- Blinding: [model output blinded yes/no]
- Primary audit endpoint: extraction correctness at the unit of analysis

## 3. Extraction accuracy

| Label class | Audit n | True positives | False positives | False negatives | Precision | Recall | Common error mode |
|-------------|---------|----------------|-----------------|-----------------|-----------|--------|-------------------|
| [class 1] | [n] | [n] | [n] | [n] | [0.00] | [0.00] | [text] |
| [class 2] | [n] | [n] | [n] | [n] | [0.00] | [0.00] | [text] |

## 4. Report-derived versus adjudicated confusion matrix

| Report-derived label | Adjudicated class 1 | Adjudicated class 2 | Adjudicated class 3 |
|----------------------|---------------------|---------------------|---------------------|
| Class 1 | [n] | [n] | [n] |
| Class 2 | [n] | [n] | [n] |
| Class 3 | [n] | [n] | [n] |

## 5. Like-for-like validation table

| Cohort | Reference standard | AUROC | AUPRC | Sensitivity | Specificity | PPV | NPV |
|--------|--------------------|-------|-------|-------------|-------------|-----|-----|
| Internal validation | Gold or adjudicated | [0.00] | [0.00] | [0.00] | [0.00] | [0.00] | [0.00] |
| Internal validation | Noisy label | [0.00] | [0.00] | [0.00] | [0.00] | [0.00] | [0.00] |
| External validation | Noisy label | [0.00] | [0.00] | [0.00] | [0.00] | [0.00] | [0.00] |

## 6. Sensitivity bound

State the assumed label sensitivity and specificity from the audit, then report how the external metric changes under plausible label-error scenarios.

| Scenario | Assumed label sensitivity | Assumed label specificity | Corrected AUROC or bound | Interpretation |
|----------|---------------------------|---------------------------|---------------------------|----------------|
| Base case | [0.00] | [0.00] | [0.00] | [text] |
| Lower-bound error | [0.00] | [0.00] | [0.00] | [text] |
| Upper-bound error | [0.00] | [0.00] | [0.00] | [text] |

## 7. Clean-label sensitivity

If a clean adjudicated subset exists, evaluate or retrain on that subset and report whether the headline conclusion changes.

| Analysis | Training labels | Evaluation labels | n | Events | AUROC | Calibration slope | Conclusion changed |
|----------|-----------------|-------------------|---|--------|-------|-------------------|--------------------|
| Primary | [source] | [source] | [n] | [n] | [0.00] | [0.00] | [yes/no] |
| Clean-label sensitivity | [source] | [source] | [n] | [n] | [0.00] | [0.00] | [yes/no] |

## 8. Manuscript wording

Methods:

```text
Labels for [cohort] were derived from [source]. To quantify extraction error, we audited a random sample of [n] [unit] with adjudication by [reviewers]. We estimated per-class precision and recall and used these values to bound the external validation metric under plausible label-error scenarios.
```

Results:

```text
In the adjudication audit, label extraction precision ranged from [0.00] to [0.00] and recall ranged from [0.00] to [0.00]. The external AUROC was [0.00] using report-derived labels and ranged from [0.00] to [0.00] after label-noise sensitivity analysis.
```

Limitations:

```text
External validation relied on [label source], which is less certain than [gold standard]. We therefore report like-for-like internal performance against the same label source and provide a sensitivity bound rather than interpreting the external metric as a pure measure of transportability.
```
