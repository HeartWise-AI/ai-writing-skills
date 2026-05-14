# CONSORT Flow and Table 1 Denominator Template

Use this template for any medical-AI manuscript with exclusions, linked datasets, multiple cohorts, or more than 20% of available data excluded.

## 1. Flow diagram data table

Use these rows to build Figure 1. Every branch needs a reason and count.

| Stage | Count | Exclusion reason | Remaining count | Notes |
|-------|-------|------------------|-----------------|-------|
| Available records, studies, encounters, or patients | [n] | Not applicable | [n] | Define starting unit |
| Excluded: duplicate or repeated records | [n] | [reason] | [n] | State deduplication rule |
| Excluded: missing required input | [n] | [reason] | [n] | Define required input |
| Excluded: missing reference standard | [n] | [reason] | [n] | State reference standard |
| Excluded: inadequate quality | [n] | [reason] | [n] | Define quality rule |
| Eligible for model development | [n] | Not applicable | [n] | State unit |
| Training split | [n] | Not applicable | [n] | Include event count |
| Tuning or validation split | [n] | Not applicable | [n] | Include event count |
| Internal test split | [n] | Not applicable | [n] | Include event count |
| External validation cohort | [n] | Not applicable | [n] | Include event count |

## 2. Exclusion summary

| Starting count | Final analytic count | Excluded count | Excluded percent | Flow diagram required |
|----------------|----------------------|----------------|------------------|-----------------------|
| [n] | [n] | [n] | [0.0%] | yes/no |

Rule: if excluded percent is greater than 20%, include a CONSORT-style flow diagram in the main manuscript or first supplement figure.

## 3. Unit of analysis statement

```text
The unit of analysis was [unit] for model training, [unit] for internal validation, [unit] for external validation, and [unit] for clinical reporting. When multiple [lower-level units] were available for one patient, [aggregation rule] was used before patient-level reporting.
```

## 4. Table 1 skeleton with denominators

| Characteristic | Training cohort, n = [n] | Internal test cohort, n = [n] | External cohort, n = [n] | Missing, n (%) |
|----------------|--------------------------|-------------------------------|--------------------------|----------------|
| Age, mean (SD) | [value] | [value] | [value] | [n (%)] |
| Sex, women, n (%) | [n (%)] | [n (%)] | [n (%)] | [n (%)] |
| Race or ethnicity, n (%) | [n (%)] | [n (%)] | [n (%)] | [n (%)] |
| Disease severity, n (%) | [n (%)] | [n (%)] | [n (%)] | [n (%)] |
| Outcome events, n (%) | [n (%)] | [n (%)] | [n (%)] | [n (%)] |
| Scanner, vendor, or acquisition protocol, n (%) | [n (%)] | [n (%)] | [n (%)] | [n (%)] |
| Follow-up, median (IQR), months | [value] | [value] | [value] | [n (%)] |

## 5. Denominator audit

- Every table row includes its denominator.
- Every Results subsection states patient count or analysis-unit count.
- Event counts are included for every performance metric.
- Missingness is reported for key predictors, labels, and follow-up.
- Cohort names match exactly across Figure 1, Table 1, Results, and Abstract.
- Abstract metrics match the corresponding Results table to the second decimal.
