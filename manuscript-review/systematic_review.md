# Reviewing a systematic review or meta-analysis of prediction models

Read this before Step 0 when the manuscript pools or summarizes other groups' models. The General Comments (G1 to G4) and the section checklists still apply; this file replaces the parts written for a single-model development paper.

## What changes

| Single-model paper | Systematic review or meta-analysis |
| --- | --- |
| TRIPOD+AI | PRISMA 2020, with TRIPOD-SRMA for reviews of prediction models |
| Model development subsection | Eligibility, search, selection, extraction (CHARMS items) |
| Internal and external validation | Which estimate was taken from each study, and why |
| Failure-mode panel | Risk of bias with PROBAST+AI, per domain |
| CONSORT flow | PRISMA flow |
| Table 1 baseline characteristics | Table 1 characteristics of included studies |

## Checklist

Items marked (RA) come from Robert's comments on a retinal-imaging cardiovascular meta-analysis, November 2026.

- **Every pooled estimate is self-contained (RA).** It states the outcome, the prediction horizon, the number of studies, the model input class, and the validation type. Two pooled estimates in the same paragraph say what separates them. FAIL: "three studies yielded an AUROC of 0.86" next to "three studies yielded an AUROC of 0.71" with no horizon and no statement that the first predicts a calculated score and the second predicts events.
- **Synonymous metrics are declared once (RA).** If C-statistic and AUROC are pooled together, Methods says they are treated as equivalent for binary outcomes, and the text then uses one term.
- **Head-to-head comparisons with guideline scores are counted (RA).** Results state how many included studies compared the model with an established score, which score, and the result. The Abstract carries the count.
- **Comparators are tabulated (RA).** One table of every established score named: reference, inputs, outcome definition as worded in the source, horizon, endorsing guideline and jurisdiction. Outcome labels in the text follow the table (atherosclerotic cardiovascular disease is not general cardiovascular disease).
- **Extraction mechanics go to the Supplement (RA).** Conversion formulas, variance approximations, estimate-selection rules, and software arguments leave the main text with a citation at the point of removal. Main text keeps: databases and dates, eligibility in one paragraph, pooling model, heterogeneity measures, bias tool.
- **A data-scaling figure is offered (RA).** Performance against development sample size or event count, log x axis, one point per model. It is not a standard meta-analysis figure and it is the one an artificial intelligence readership asks for.
- **The standard-alone arm is extracted from the same studies.** G4's three-arm figure needs the clinical model's own discrimination in each study that reports it, not only the image-only and combined arms.
- **Cohort overlap is stated.** When several studies draw on one cohort, each pooled estimate says how many independent cohorts it contains, and overlapping estimates are not pooled as independent.
- **Estimate selection is not "best per study".** Taking the highest reported value in each study biases the pooled estimate upward. Require the prespecified primary model, or a sensitivity analysis with the lowest.
- **Small pools are exploratory.** With fewer than five studies, report the prediction interval beside the confidence interval, make no subgroup or superiority claim, and say so in the Abstract.
- **Overlapping intervals are not differences (RA).** Between-study or between-modality contrasts without a paired test are "numerically higher, with overlapping 95% CIs".
- **Translation evidence is specific (RA).** Regulatory status follows G4. Workflow studies report who acquired the input, how long it took, what was done with the result, and whether care changed.
- **The reference list is checked for duplicates.** A citation manager merge often leaves the same paper under two or three numbers.

Length budgets from Step 0.5 apply to the main text. The characteristics-of-included-studies table and the study-level performance table are exempt.
