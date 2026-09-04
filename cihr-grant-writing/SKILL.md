---
name: cihr-grant-writing
description: Section-by-section guide for writing CIHR Project Grant applications, covering RCTs, AI/technology, observational studies, with scoring rubrics and templates. Use when drafting, reviewing, or scoring a CIHR grant application.
---

# CIHR Grant Writing Skill

## Overview

A section-by-section guide for writing CIHR Project Grant applications, modeled on the structure of the PANTHEON SLIM (Randomized Controlled Trial) grant and cross-referenced with the CardioAgent (AI/Technology) grant. This skill is generalizable across clinical trials, observational studies, AI/technology development, and other health research study designs.

Each section includes: **Requirements** (what must be present), **Expectations** (what reviewers look for), **Scoring Rubric** (weighted scoring criteria), and **Templates** (fill-in-the-blank scaffolds).

For CIHR-specific language tips, study type adaptations, and common reviewer critiques, see [the appendices](references/APPENDICES.md).

**Before drafting or revising, read Section 0 (Cross-Cutting Failure Modes) and Section 5 (Resubmission Discipline).** Section 0 covers the failures that move scores most and that authors are least able to see in their own work. Section 5 applies whenever the application has been reviewed before.

## SECTION 0: Cross-Cutting Failure Modes

These are the failure modes that repeatedly move CIHR scores, derived from analysing multiple review cycles of the same application across different committees. They are ordered by observed impact on score.

Three properties make them dangerous. First, most are **design or execution failures, not writing failures**, so line-editing does not fix them. Second, most are **locally invisible**: every individual sentence is true, and the defect only appears when two parts of the package are read against each other. Third, several are **self-inflicted and fully preventable**, which reviewers punish harder than genuine scientific uncertainty, because they read as carelessness about the trial itself.

A note on trajectory: a resubmission can score **worse** than its predecessor even when the science is better. Redesigning to fix a scientific criticism replaces a known, discounted weakness with fresh, unvetted execution errors, and reviewers who see contradictions in a revised application infer that the revision was rushed. Treat every resubmission as a new application that must survive Section 0 from scratch.

---

### F1. Numerical incoherence across documents is scored as a methods failure

**The failure.** The summary states one sample size and the body another; a figure shows a superseded endpoint; a provider count appears as three different numbers in three sections. Each statement is individually defensible. Together they are fatal.

**Why it costs so much.** Reviewers cannot audit your data, so they audit the one thing they can: whether your numbers agree with each other. A contradiction is read as direct evidence about how the trial will be run. This is the single most common cause of a large score drop, and it is scored under methodological rigour, not presentation.

**The rule.** Maintain one **canonical parameter set** and derive every appearance of every number from it. Any change to a canonical parameter triggers a full propagation pass across the body, summary, figures, budget, statistical memo, and response letter.

**What counts as a document.** Figures and tables are text. A flowchart carrying an outdated endpoint is the most damaging single error in this class because it is the first thing a reviewer looks at and the last thing an author remembers to regenerate. The same applies to embedded images, budget justifications, and appendices.

**Canonical parameter set (define these once, propagate everywhere):**

| Parameter | Notes |
|-----------|-------|
| Total N and per-arm N | Including the exact unrounded value if quoted anywhere |
| Number of sites, and the site list | Names must match support letters |
| Number of providers/clusters | One number, used in the power calculation and the model description |
| Control event rate and its source | Same wording every time |
| Effect size (state as one metric) | Do not mix RR, OR, and absolute difference across sections |
| Outcome window | Primary and each secondary |
| Power, alpha, loss to follow-up | |
| ICC / design effect | |
| Recruitment rate per site per month, and duration | Must multiply out to N |
| Study phase durations | Setup and main phase, must sum to the stated total |

---

### F2. The primary endpoint denominator must be the randomized population

**The failure.** The primary outcome is only measurable in the subset of participants who experience some post-randomization event: those who receive the confirmatory test, who are referred, who adhere, who survive to the assessment.

**Why it costs so much.** Conditioning on a post-randomization variable breaks randomization and reintroduces exactly the confounding the trial was built to eliminate. Reviewers raise this independently and repeatedly, and no amount of adjustment satisfies them, because the problem is structural rather than analytic. When the conditioning subset is small (for example, only 20% of enrolled participants receive the confirmatory test), reviewers also note that baseline balance in the analysed set is no longer guaranteed.

**The rule.** The numerator may be conditional; the denominator must be everyone randomized. Convert "time to X among those who got X" into "proportion of all randomized participants with X by time T". Participants who die, withdraw, or are never assessed are counted as not having the event under intention-to-treat, and sensitivity analyses bound the effect of that choice.

**Secondary benefit.** This usually simplifies the analysis from time-to-event with censoring and competing risks to a binary comparison, which removes a second family of reviewer objections.

---

### F3. The endpoint window must match the standard the field already accepts

**The failure.** The trial defines its own clinically meaningful window (for example, 90 days) when a national guideline or accepted access standard specifies another (for example, 30 days), and does not justify the difference.

**Why it costs so much.** Reviewers read a self-chosen, more permissive threshold as designing for feasibility or for a positive result rather than for clinical relevance. It also strands the trial: a positive result at a window nobody uses cannot change practice, which undermines the impact section too.

**The rule.** Anchor thresholds, windows, and risk categories to a named guideline and cite it. If you must deviate, justify the deviation explicitly and in advance, with the clinical reasoning stated. Extend the same discipline to the intervention: if the intervention produces categories (risk tiers, priority levels), those categories should map one-to-one onto the guideline's categories. Intermediate tiers that do not correspond to a guideline action are a recurring source of both reviewer confusion and internal inconsistency.

---

### F4. The sample size must be computed under the primary analysis model, and must reproduce

**The failure.** The power calculation uses a different method than the stated primary analysis (a t-test for a time-to-event endpoint, an unclustered z-test where the model is clustered), or the stated inputs do not arithmetically regenerate the stated N.

**Why it costs so much.** Statistical reviewers recompute. This is the most reliably checked calculation in the entire application, and a mismatch is unrecoverable within the review because it casts doubt on every other number. It is also the criticism most likely to persist across rounds, which reviewers explicitly note and penalize ("this was raised previously and not adequately addressed").

**The rule.**
- The power calculation and the primary analysis must use the same model family and the same effect metric.
- A reader must be able to reproduce N from the stated inputs alone. Show the path: unadjusted N, then each inflation factor, then the final N.
- State exactly one effect metric for the primary endpoint and use it everywhere. If the analysis model yields an odds ratio, report an odds ratio. Converting to a relative risk requires standardization and bootstrapped intervals, which adds machinery and a further chance of inconsistency for no gain when the outcome is rare and OR approximates RR.
- Do not double-count inflation. Loss to follow-up either attenuates the effect estimate or reduces the analysed N; it rarely does both. If the denominator is all randomized participants and unascertained outcomes are counted as non-events, there is **no N inflation for loss to follow-up**, and the attrition assumption belongs in the sensitivity analyses instead.
- If the achieved N exceeds the calculated minimum, say so plainly ("provides more than 80% power") rather than reverse-engineering an inflation factor to make the numbers land.
- Name the statistician who performed the calculation, and give them a role in the application.

---

### F5. Match the model to the cluster structure and the event density

**The failure.** A mixed-effects model with a random intercept per cluster is proposed when there are many clusters, few participants per cluster, and a rare outcome, so most clusters contribute zero events.

**Why it costs so much.** The model will not converge reliably, and the conditional effect it estimates is not the quantity the trial is meant to report. Statistical reviewers identify this immediately from the ratio of clusters to events.

**The rule.** Compute events per cluster before choosing the model. When events per cluster are sparse, prefer a marginal model (generalized estimating equations with robust sandwich standard errors), which estimates a population-averaged effect and is robust to the working correlation structure. Retain the random-effects model as a sensitivity analysis. Report the ICC and the implied design effect explicitly, and state whether the design effect materially changes N. When randomization is at the individual level rather than the cluster level, say so, because the clustering penalty is much smaller and reviewers will otherwise assume the worst.

**Related trap.** Do not describe randomization as stratified by a factor it is not stratified by. Stratification claims are checked against the randomization section, and a mismatch between the two (or between the grant and the response letter) is an F1 failure with statistical consequences.

---

### F6. Every design assumption is adversarially checked for optimism

**The failure.** Loss to follow-up of "under 5%", high adherence, full recruitment from month one, complete data capture. Each is stated without evidence.

**Why it costs so much.** Reviewers treat optimistic assumptions as a proxy for the team's realism about operations. Optimism about attrition specifically is flagged in nearly every round of every trial application.

**The rule.** For each of loss to follow-up, recruitment rate, adherence or fidelity, and completeness of outcome ascertainment: state the assumed value, give the empirical source (your own pilot, a comparable published trial, or site data), and show that the design survives a worse value. Prefer the conservative end of your own pilot's confidence interval.

**Watch for self-contradiction.** Attrition, completion, and linkage-failure rates are often quoted in three different sections from three different denominators, producing numbers that appear to contradict each other (for example, a 98% completion rate in the pilot section and a 38% unlinked rate in the attrition section, supporting an 8% assumption). If several rates coexist legitimately, define each one's denominator in the sentence where it appears.

**Do not overstate the pilot.** If the pilot's confidence intervals cross the null, say that it supports feasibility, the event rate, and the ICC, but not efficacy. Reviewers check pilot confidence intervals and penalize claims built on wide ones.

---

### F7. Feasibility of data access and capacity is evidence, not assertion

**The failure.** The application asserts that outcomes will be captured through a provincial or regional data holding, a cross-institution record system, or partner registries, without evidence that such access has been granted for this study.

**Why it costs so much.** Reviewers frequently have direct experience that the named mechanism is slow, restricted, or legally constrained. An unevidenced access claim on which the primary endpoint depends is treated as a threat to trial completion.

**The rule.** Do not let the primary endpoint depend on any data source you cannot demonstrate access to. Ascertain the primary endpoint locally, within institutions where you have executed agreements, and treat external sources as recoverable additions. For each external source, state the access mechanism, the granularity (aggregate counts versus participant-level), the cost, the agreement status, and include the supporting letter. The same evidentiary standard applies to throughput claims: if the endpoint requires a test completed within a window, give per-site turnaround data showing the window is achievable.

---

### F8. Administrative completeness is scored under Expertise and Resources

**The failure.** Missing institutional support letters, letters only from industry partners or international collaborators, unnamed site leads, or inconsistent names and credentials.

**Why it costs so much.** This sits in a section that otherwise scores well, and it converts a strength into a listed shortcoming for zero scientific reason. It is entirely preventable with lead time.

**The rule.** Every participating site needs a signed letter from that institution, not from an individual collaborator elsewhere. Every site named in the methods must appear in the team section, the site list, the budget, and the letters, with consistent institution names and spellings. Where a letter is not yet signed, state its status and the activation contingency rather than staying silent. Start letter collection at least eight weeks before the deadline, because this is the item most often lost to timing.

---

### F9. Do not let unblinded provider behaviour define the endpoint

**The failure.** In an open-label trial of a decision-support or care-pathway intervention, the primary endpoint is something the unblinded provider directly controls, such as whether a referral or order is placed.

**Why it costs so much.** Providers who know the allocation may change ordering behaviour, so the endpoint measures the awareness of being studied rather than the intervention.

**The rule.** Move the endpoint one step downstream, from the provider's action to an objectively ascertained clinical result, captured from records rather than reported by the provider. Then reduce the residual bias structurally: balance allocation within provider where the design allows, keep outcome ascertainment and analysis blinded, and monitor control-arm behaviour over time for contamination. State the residual risk in the limitations rather than claiming it is eliminated.

---

### F10. The site mix must include the setting where the intervention should matter most

**The failure.** Every site is a high-resource academic centre, while the intervention's rationale is that it helps where expertise or capacity is scarce.

**Why it costs so much.** It creates a direct contradiction between the significance argument and the design, and it limits generalizability to precisely the settings that least need the intervention.

**The rule.** Include sites representing the target implementation setting, name their leads, and pre-specify a resource-level subgroup analysis with an interaction test. Make sure that subgroup actually appears in the subgroup analysis section, not only in the site rationale.

---

### F11. For AI and technology studies, the evidence status of the artefact is itself scored

**The failure.** The model's performance rests on a preprint, a manuscript under review, or unpublished internal data.

**Why it costs so much.** Reviewers flag it every round and cannot verify the numbers that the entire proposal depends on.

**The rule.** Publish the development and validation work before, or alongside, the trial application, and give its status honestly. Beyond publication status, address as a checklist:
- **Comparator framing.** Compare the tool against the full clinical assessment it would displace, including existing biomarkers and clinical judgement, not against a narrow component such as unaided interpretation of the raw signal. Reviewers reframe this comparison themselves if you do not.
- **Model lock and drift.** State that weights are frozen for the trial's duration, and how drift would be detected and handled.
- **Fairness at development, not deployment.** Report established fairness metrics from the validation stage. Deferring fairness to the trial reads as deferring it indefinitely, and conventional sex or gender subgroup analyses are underpowered when the trial is not sized for interaction.
- **Partial verification bias.** If diagnostic accuracy is a secondary aim and only a subset receives the reference standard, the accuracy estimate is biased. Justify a verification substudy in both arms with its own sample size, powered on the lower confidence bound of negative predictive value or sensitivity.
- **Data governance.** State explicitly where the model executes, whether identifiable data leaves the institution, which privacy regimes apply, and what each site must sign. Institutional willingness to permit external hosting is a live reviewer concern. **Check the budget against this claim.** A cloud, hosting, or compute line item sitting under an on-premise claim is a direct contradiction on the exact point the reviewer asked about, and the budget is the more believable document. If both are true, say what each resource holds.
- **Adherence to the recommendation is a trial-critical parameter.** If clinicians ignore the output, the trial is uninformative. Define a concordance threshold, monitor it in real time, and tie it to a pre-specified remediation or stopping rule.

---

### F12. Knowledge translation is judged on mechanisms and named users, not venues

**The failure.** The KT plan lists journals and conferences, while the application names knowledge users, decision-makers, and patient partners on the team.

**The rule.** For each named knowledge user, state what they will do with the result and through what mechanism: the guideline committee and the specific standard it would revise, the health-technology assessment body and the analysis it needs, the decision-support integration and who builds it, the patient-facing materials and who leads them. Publications are the floor, not the plan.

---

## SECTION 1: The Need for a Trial / Study

**Weight: 25/100**

This section must build the case that your study addresses a critical, unmet need. It follows a hierarchical argument structure.

---

### 1.1 What is the problem to be addressed?

**Weight: 5/25**

#### Requirements

- [ ] State the clinical/scientific problem in 2-3 sentences maximum
- [ ] Define the specific patient population or target group
- [ ] Identify what is currently unknown or what practice gap exists
- [ ] State why current evidence is insufficient (e.g., "no RCT has addressed...", "current AI tools lack...")
- [ ] Use underline/bold formatting to emphasize the key population and the key gap

#### Expectations

- The problem statement should be immediately understandable to a non-specialist reviewer
- Frame as a patient-centered or health-system problem, not just a scientific curiosity
- Quantify the problem where possible (mortality rates, error rates, prevalence)
- Explicitly state the knowledge gap that this study will fill

#### Template

> The problem to be addressed is that [specific clinical/scientific gap] in [target population] is unknown/unresolved. [Current approach or standard of care] represents [limitation], but [it has only been studied in X / no evidence supports Y / current tools cannot Z]. [Quantify the consequence of not addressing this gap].

#### Scoring Rubric

| Criterion | Weight | 5 (Excellent) | 3 (Good) | 1 (Weak) |
|-----------|--------|---------------|----------|----------|
| Clarity of problem | 2/5 | Immediately clear, specific, and compelling | Understandable but somewhat vague | Confusing or overly broad |
| Evidence of gap | 2/5 | Systematic review or guideline gap cited; no existing RCT/study identified | Literature cited but gap not well-defined | No evidence that gap exists |
| Patient/population focus | 1/5 | Specific population clearly defined with prevalence data | Population mentioned but not well-characterized | No clear target population |

---

### 1.2 What are the principal research questions to be addressed?

**Weight: 5/25**

#### Requirements

- [ ] State the **overarching objective** in one sentence (use the study acronym if applicable)
- [ ] State the **central hypothesis** clearly
- [ ] Define the **primary objective** with a feasibility/success threshold (for pilot) or primary endpoint (for phase III)
- [ ] List **secondary objectives** (numbered, 2-4 items)
- [ ] List **exploratory objectives** (numbered, 2-5 items)
- [ ] For each objective level (primary/secondary/exploratory), state whether results will be evaluated by sex and gender subgroups
- [ ] For pilot/feasibility studies: primary objective MUST be operational (e.g., recruitment rate), not clinical

#### Expectations

- Objectives must follow a clear hierarchy: Primary > Secondary > Exploratory
- The primary objective must be answerable with the proposed design and sample size
- For pilot studies: clinical outcomes are exploratory only (state this explicitly)
- Sex and gender analysis commitment should be present at every objective level
- Use CIHR-specific language: "patient-oriented," "sex and gender-based analysis (SGBA+)"

#### Template

> **Overarching objective:** The overarching objective of the "[STUDY ACRONYM]" [study type] is to [determine/evaluate/develop] [intervention/technology] [in what population] [to achieve what].
>
> **Central hypothesis:** We hypothesize that [intervention/approach] will [expected effect] compared with [comparator] in [population].
>
> **Primary objective:** To [specific measurable objective]. **Success threshold:** [define].
>
> **Secondary objectives:**
> i. To [objective 1];
> ii. To [objective 2].
>
> **Exploratory objectives:**
> i. To [objective 1];
> ii. To [objective 2];
> iii. To [objective 3].

#### Scoring Rubric

| Criterion | Weight | 5 (Excellent) | 3 (Good) | 1 (Weak) |
|-----------|--------|---------------|----------|----------|
| Hypothesis clarity | 2/5 | Testable, specific, directional hypothesis with clear comparator | Hypothesis present but vague | No hypothesis or untestable statement |
| Objective hierarchy | 2/5 | Clear primary with feasible threshold; logical secondary and exploratory | Objectives present but hierarchy unclear | Objectives conflated or missing levels |
| SGBA+ integration | 1/5 | Sex/gender analysis specified at each objective level | Mentioned but not integrated into objectives | Absent |

---

### 1.3 Why is a trial/study needed now?

**Weight: 10/25**

This is the most critical subsection of the entire "Need" section. It builds the scientific rationale through a logical chain of evidence. Use numbered subsections (1.3.1, 1.3.2, etc.).

#### Requirements

- [ ] **1.3.1 Burden of disease/problem:** Canadian and global epidemiological data with citations
- [ ] **1.3.2 Current standard of care/approach:** What is currently done and why it works (partially)
- [ ] **1.3.3 Limitations of current approach:** Why the standard of care is insufficient (quantify risks, error rates, costs)
- [ ] **1.3.4 Emerging evidence for the proposed approach:** What new evidence suggests a better strategy exists
- [ ] **1.3.5 Evidence gap in the target population:** Demonstrate that the proposed approach has NOT been studied in your specific population (cite systematic review or guideline gap)
- [ ] **1.3.6 Specific technical/clinical gap:** Address any unique safety or feasibility concerns
- [ ] **1.3.7 Sex and gender representation gap:** Demonstrate that prior studies lacked adequate sex/gender representation and analysis
- [ ] Use bold/underline for the key concluding statement of the evidence gap
- [ ] Include at least one citation from your own team's prior work in this field

#### Expectations

- Build the argument like a legal brief: each subsection leads logically to the next
- Use Canadian data prominently (CIHR is a Canadian funder) or primarily
- Demonstrate clinical equipoise with real-world data (e.g., practice variation showing disagreement)
- The final statement should be a bold, underlined, definitive assertion of the knowledge gap
- Reference your own prior work to show you are the right team to address this gap
- For AI/technology studies: address current limitations of existing AI approaches and why yours is different

#### Template for Key Concluding Statement

> **There is thus an important knowledge gap to support the use of [proposed approach] in [target population], despite the fact that this population represents [quantify the size/importance of the population].**

#### Scoring Rubric

| Criterion | Weight | 5 (Excellent) | 3 (Good) | 1 (Weak) |
|-----------|--------|---------------|----------|----------|
| Burden of disease (Canadian context) | 2/10 | Canadian-specific epidemiology with recent data and economic impact | Some Canadian data but incomplete | No Canadian data or only global |
| Logical argument chain | 3/10 | Each subsection flows naturally to the next; unavoidable conclusion | Generally logical but some jumps | Disjointed; conclusion not supported |
| Evidence of gap | 3/10 | Systematic review or guideline development process cited showing no existing evidence | Literature review shows gap but not systematic | Assertion without evidence |
| Own prior work cited | 1/10 | Multiple relevant team publications integrated into rationale | One team publication mentioned | No team publications cited |
| Sex/gender gap identified | 1/10 | Specific data on under-representation with quantification | General statement about sex/gender gaps | Not mentioned |

---

### 1.4 How will the results of this trial/study be used?

**Weight: 3/25**

#### Requirements

- [ ] For pilot studies: state that results will inform the design of a phase III confirmatory study
- [ ] For confirmatory studies: state that results will influence clinical guidelines
- [ ] Describe the dissemination plan: conferences, journals, social media, public engagement
- [ ] State whether the study could transition to the next phase seamlessly (adaptive design)
- [ ] Explain why CIHR funding is required (e.g., no industry interest due to generic drugs / public health focus)
- [ ] Name the specific guideline body or clinical practice that would be impacted

#### Scoring Rubric

| Criterion | Weight | 5 (Excellent) | 3 (Good) | 1 (Weak) |
|-----------|--------|---------------|----------|----------|
| Impact pathway | 2/3 | Clear pipeline from pilot to phase III to guidelines with named bodies | General pathway described | Vague impact statement |
| Dissemination plan | 1/3 | Multiple channels: conferences, journals, media, patient engagement | Basic plan (journal + conference) | No plan |

---

### 1.5 Are there any risks to the safety of participants?

**Weight: 2/25**

#### Requirements

- [ ] State the risk profile of the intervention explicitly
- [ ] For de-escalation studies: emphasize that no NEW risks are expected
- [ ] For technology studies: address privacy, data security, and potential for misdiagnosis
- [ ] Acknowledge theoretical risks and cite evidence that these have NOT been observed in comparable populations
- [ ] Describe monitoring mechanisms (DSMB, adverse event reporting)

#### Scoring Rubric

| Criterion | Weight | 5 (Excellent) | 3 (Good) | 1 (Weak) |
|-----------|--------|---------------|----------|----------|
| Risk characterization | 1/2 | Comprehensive, evidence-based risk assessment with mitigation | Risks mentioned with some mitigation | Risks not addressed or dismissed |
| Safety monitoring | 1/2 | DSMB, adverse event protocol, stopping rules defined | Some monitoring described | No safety monitoring plan |

---

## SECTION 2: The Proposed Trial / Study Design

**Weight: 40/100**

This section covers all methodological details. Each subsection maps to a specific CIHR review criterion.

---

### 2.1 What is the proposed trial/study design?

**Weight: 5/40**

#### Requirements

- [ ] State the study design using standard terminology (e.g., "pilot, multi-center, double-blinded, pragmatic, patient-centered RCT")
- [ ] State whether it is a pilot/feasibility study or a confirmatory study
- [ ] If pragmatic: reference PRECIS-2 tool and justify pragmatic elements
- [ ] Describe patient engagement strategy: patient partners on steering committee, co-development of protocol
- [ ] For AI/technology: describe the validation framework (retrospective + prospective phases)
- [ ] Include a study flowchart figure

#### Template

> The proposed [study] is a [phase], [number of sites]-center, [blinding], [pragmatic/explanatory], and [patient-centered] [study type] designed to [primary purpose]. [Population] will be eligible. [Brief description of randomization/allocation]. The [pragmatic/explanatory] design ensures that [justification].

#### Scoring Rubric

| Criterion | Weight | 5 (Excellent) | 3 (Good) | 1 (Weak) |
|-----------|--------|---------------|----------|----------|
| Design appropriateness | 2/5 | Design perfectly matches research question; standard terminology used | Appropriate design but not fully justified | Design-question mismatch |
| Patient engagement | 2/5 | Named patient partner on steering committee; co-developed protocol; EDI principles | Patient input mentioned but not structured | No patient engagement |
| Study flowchart | 1/5 | Clear, comprehensive flowchart with all study phases and timelines | Flowchart present but incomplete | No flowchart |

---

### 2.2 What are the planned trial interventions?

**Weight: 4/40**

#### Requirements

- [ ] Describe the experimental intervention with dose/frequency/route/duration
- [ ] Describe the control intervention with the same level of detail
- [ ] Justify the choice of comparator with evidence and guideline references
- [ ] Address regulatory requirements (e.g., Health Canada Clinical Trial Application)
- [ ] Describe management of participants on prior therapies (switching protocols)
- [ ] State that all other treatments follow standard of care (pragmatic principle)
- [ ] Describe post-study care plan

#### Scoring Rubric

| Criterion | Weight | 5 (Excellent) | 3 (Good) | 1 (Weak) |
|-----------|--------|---------------|----------|----------|
| Intervention clarity | 2/4 | Fully specified with dose, route, frequency, duration for both arms | Mostly specified but some gaps | Vague intervention description |
| Comparator justification | 1/4 | Evidence-based with guideline reference; addresses evidence gaps in comparator choice | Some justification | No justification for comparator |
| Regulatory and practical | 1/4 | Regulatory pathway identified; switching protocols; post-study care | Some practical issues addressed | Regulatory/practical issues ignored |

---

### 2.3 Allocation to trial groups

**Weight: 2/40**

#### Requirements

- [ ] State allocation ratio (e.g., 1:1)
- [ ] State stratification variables with justification (cite validation of stratification tool)
- [ ] State block sizes
- [ ] Name the randomization platform/system
- [ ] For non-RCT designs: describe sampling or allocation strategy

#### Scoring Rubric

| Criterion | Weight | 5 (Excellent) | 3 (Good) | 1 (Weak) |
|-----------|--------|---------------|----------|----------|
| Randomization rigor | 2/2 | Validated stratification tool cited; appropriate block sizes; named platform | Randomization described but not fully detailed | No randomization details |

---

### 2.4 Methods for protecting against sources of bias

**Weight: 2/40**

#### Requirements

- [ ] Describe blinding strategy (who is blinded: participants, investigators, outcome assessors)
- [ ] Describe allocation concealment method
- [ ] For AI studies: describe blinding of human evaluators to AI outputs
- [ ] Address potential sources of bias specific to your design

#### Scoring Rubric

| Criterion | Weight | 5 (Excellent) | 3 (Good) | 1 (Weak) |
|-----------|--------|---------------|----------|----------|
| Bias protection | 2/2 | Double-blind with allocation concealment; all bias sources addressed | Single-blind or partial concealment | Open-label without justification |

---

### 2.5 Inclusion/exclusion criteria

**Weight: 3/40**

#### Requirements

- [ ] List inclusion criteria as bullet points
- [ ] List exclusion criteria as bullet points
- [ ] For pragmatic trials: explicitly state that few exclusion criteria are used to maximize generalizability
- [ ] Justify any exclusion criterion that removes a specific subpopulation
- [ ] Describe screening log data collection: baseline characteristics, sex, gender, race, ethnicity, reasons for exclusion
- [ ] Address EDI: describe strategies to include underrepresented populations (e.g., Indigenous communities)
- [ ] For heterogeneous populations: acknowledge heterogeneity and state how subgroups will be characterized

#### Scoring Rubric

| Criterion | Weight | 5 (Excellent) | 3 (Good) | 1 (Weak) |
|-----------|--------|---------------|----------|----------|
| Criteria appropriateness | 1/3 | Pragmatic criteria maximizing generalizability; each exclusion justified | Reasonable criteria but some unjustified exclusions | Overly restrictive or unjustified |
| EDI integration | 1/3 | Named strategies for diverse recruitment; screening log captures demographics | EDI mentioned but no concrete strategy | No EDI consideration |
| Population characterization | 1/3 | Heterogeneity acknowledged; subgroup plan described | Some acknowledgment | Assumed homogeneity |

---

### 2.6-2.7 Treatment duration and follow-up

**Weight: 2/40**

#### Requirements

- [ ] State treatment duration with start and end points
- [ ] State follow-up visit schedule with specific time points
- [ ] State visit modalities (in-person, telephone, video)
- [ ] State total study duration (recruitment + follow-up)
- [ ] State recruitment period duration

#### Scoring Rubric

| Criterion | Weight | 5 (Excellent) | 3 (Good) | 1 (Weak) |
|-----------|--------|---------------|----------|----------|
| Timeline completeness | 2/2 | All durations specified; flexible visit modalities; realistic timeline | Mostly specified | Incomplete or unrealistic |

---

### 2.8 Primary and secondary outcome measures

**Weight: 6/40**

#### Requirements

- [ ] **Primary outcome:** State with exact definition, measurement method, and success threshold
- [ ] **Secondary outcomes:** List each with definition (numbered, 2-5 items)
- [ ] **Exploratory outcomes:** List each with definition (numbered, 3-6 items)
- [ ] For pilot studies: primary outcome MUST be feasibility-related (recruitment rate, adherence, etc.)
- [ ] For clinical trials: use standardized endpoint definitions (e.g., Academic Research Consortium, BARC bleeding)
- [ ] For AI studies: define accuracy metrics (AUROC, F1, sensitivity, specificity) and reference standards
- [ ] Include patient-oriented outcomes
- [ ] For novel endpoints: describe the development methodology (e.g., discrete-choice experiment)
- [ ] **Denominator is the randomized population** (see F2). The primary outcome must not be conditional on a post-randomization event such as receiving a confirmatory test, being referred, or adhering
- [ ] **Outcome window matches an accepted guideline or standard**, cited (see F3); any deviation is justified explicitly
- [ ] **The primary endpoint is not an action controlled by an unblinded provider** (see F9)
- [ ] Ascertainment method stated for the primary endpoint, and it does not depend on a data source whose access is unevidenced (see F7)
- [ ] No secondary outcome restates the primary outcome (see 5.3)

#### Scoring Rubric

| Criterion | Weight | 5 (Excellent) | 3 (Good) | 1 (Weak) |
|-----------|--------|---------------|----------|----------|
| Primary outcome definition | 2/6 | Precisely defined with validated measurement method and threshold | Defined but threshold unclear | Vague or inappropriate primary outcome |
| Outcome hierarchy | 2/6 | Clear primary/secondary/exploratory with appropriate scope at each level | Hierarchy present but some misclassification | No hierarchy or outcomes conflated |
| Standardized definitions | 1/6 | All endpoints use published consensus definitions with citations | Most endpoints standardized | Custom definitions without justification |
| Patient-oriented outcomes | 1/6 | Named patient-oriented outcomes with development methodology | Patient outcomes mentioned | No patient-oriented outcomes |

---

### 2.9 How will outcomes be measured at follow-up?

**Weight: 2/40**

#### Requirements

- [ ] State the data source for each outcome category (screening logs, medical charts, self-report, imaging)
- [ ] State whether endpoints will be adjudicated (and by whom) or not adjudicated (justify for pilot)
- [ ] Describe adverse event and serious adverse event monitoring
- [ ] For AI studies: describe the reference standard / ground truth generation process (e.g., central reader model)

#### Scoring Rubric

| Criterion | Weight | 5 (Excellent) | 3 (Good) | 1 (Weak) |
|-----------|--------|---------------|----------|----------|
| Measurement rigor | 2/2 | Each outcome has specified data source; adjudication plan clear; AE monitoring | Mostly specified | Measurement methods unclear |

---

### 2.10 Sample size justification

**Weight: 4/40**

#### Requirements

- [ ] For pilot/feasibility studies: state explicitly that formal sample size calculation is not applicable; provide expected enrollment range based on recruitment assumptions
- [ ] For confirmatory studies: provide full power calculation with alpha, beta, effect size, and assumptions
- [ ] State the basis for effect size assumptions (prior studies, pilot data, clinical significance)
- [ ] Address multiple comparisons if applicable
- [ ] For AI studies: justify the number of cases for training/validation/testing; describe stratified sampling for rare conditions
- [ ] **The calculation uses the same model family and effect metric as the primary analysis** (see F4)
- [ ] **A reader can reproduce N from the stated inputs alone.** Show unadjusted N, each inflation factor, and the final N
- [ ] Exactly one effect metric is used for the primary endpoint throughout the application
- [ ] Inflation factors are not double-counted; if unascertained outcomes are counted as non-events on an all-randomized denominator, loss to follow-up does not inflate N (see F4)
- [ ] Cluster structure addressed: events per cluster computed, ICC and design effect stated, model chosen accordingly (see F5)
- [ ] Every assumption has a named empirical source, and the design is shown to survive a worse value (see F6)
- [ ] The named statistician appears in the team section

#### Scoring Rubric

| Criterion | Weight | 5 (Excellent) | 3 (Good) | 1 (Weak) |
|-----------|--------|---------------|----------|----------|
| Sample size appropriateness | 2/4 | Fully justified with transparent assumptions; sensitivity analyses | Calculation present but assumptions not fully justified | No calculation or unrealistic assumptions |
| Effect size basis | 2/4 | Based on own pilot data or meta-analysis of comparable studies | Based on literature but indirect evidence | Arbitrary or unjustified effect size |

---

### 2.11-2.14 Practical considerations

**Weight: 4/40**

Covers: health service research issues, recruitment, compliance, and loss to follow-up.

#### Requirements

- [ ] **Recruitment:** State expected rate per site per month with evidence; describe recruitment process; state total expected enrollment
- [ ] **Compliance:** Describe adherence monitoring strategy; cite expected adherence/discontinuation rates from prior trials; describe patient-partner involvement in adherence strategies
- [ ] **Loss to follow-up:** State expected rate with evidence; describe retention strategies; commit to identifying barriers
- [ ] For all three: state that sex/gender disparities will be monitored and mitigated

#### Scoring Rubric

| Criterion | Weight | 5 (Excellent) | 3 (Good) | 1 (Weak) |
|-----------|--------|---------------|----------|----------|
| Recruitment feasibility | 2/4 | Evidence-based rate; named sites with capacity; prior recruitment experience | Rate stated but evidence weak | No evidence of feasibility |
| Adherence/retention plan | 2/4 | Proactive monitoring with iterative strategies; patient partner involvement; sex/gender analysis | Basic plan | No plan |

---

### 2.15 Number of centers

**Weight: 1/40**

#### Requirements

- [ ] List all centers with site PI name and role
- [ ] Include geographic diversity (for Canadian multi-center: multiple provinces)
- [ ] Reference letters of support from each site
- [ ] For international sites: describe regulatory coordination plan
- [ ] **A signed letter exists from each participating institution**, not from an individual collaborator elsewhere; letters from industry partners and international collaborators do not substitute (see F8)
- [ ] Site names, spellings, and lead names are identical across the methods, team section, budget, and letters
- [ ] Where a letter is unsigned, its status and the site activation contingency are stated
- [ ] **The site mix includes the setting where the intervention should matter most** (see F10), with a matching pre-specified subgroup analysis
- [ ] Per-site provider counts sum to the stated total provider count

---

### 2.16-2.18 Analysis plan

**Weight: 5/40**

#### Requirements

- [ ] **Type of analyses:** For pilot: explicitly state "most analyses will be descriptive"; for confirmatory: state primary statistical test
- [ ] Describe analysis for each outcome level (primary, secondary, exploratory)
- [ ] State whether intention-to-treat or per-protocol analysis (or both)
- [ ] **Frequency of analyses:** State whether interim analyses are planned; describe DSMB access to data
- [ ] **Subgroup analyses:** List pre-specified subgroups (sex, gender, site, risk score); state whether interaction testing will be performed
- [ ] For AI studies: describe performance metrics, calibration, and fairness analyses across demographic subgroups
- [ ] The model matches the cluster structure and event density; a marginal model (GEE with robust standard errors) is preferred over random intercepts when events per cluster are sparse (see F5)
- [ ] Stratification factors named in the analysis match those named in the randomization section exactly
- [ ] Every subgroup promised elsewhere in the application (including in the response letter and the site rationale) appears in this section (see F10)
- [ ] Sensitivity analyses named in other sections actually appear here, with matching names

#### Scoring Rubric

| Criterion | Weight | 5 (Excellent) | 3 (Good) | 1 (Weak) |
|-----------|--------|---------------|----------|----------|
| Statistical rigor | 3/5 | Appropriate methods for each outcome; multiple comparison handling; ITT specified | Generally appropriate but some gaps | Inappropriate methods or no plan |
| Subgroup/SGBA+ | 2/5 | Pre-specified sex/gender subgroups at all objective levels; fairness metrics for AI | Some subgroup analysis planned | No subgroup analysis |

---

### 2.19 Prior pilot work / Preliminary data

**Weight: 2/40**

#### Requirements

- [ ] Describe all preliminary studies that inform this proposal (surveys, observational studies, pilot data)
- [ ] For each: state IRB status, funding source, and how results will inform the current study
- [ ] Demonstrate that these studies were conducted independently (no overlapping funds)
- [ ] For AI studies: present preliminary performance data in table format (model comparison)
- [ ] State how the totality of the preliminary program will inform the proposed study

#### Scoring Rubric

| Criterion | Weight | 5 (Excellent) | 3 (Good) | 1 (Weak) |
|-----------|--------|---------------|----------|----------|
| Preliminary evidence | 2/2 | Multiple complementary preliminary studies with IRB approval; results directly inform design | Some pilot work described | No preliminary work |

---

## SECTION 3: Trial / Study Management

**Weight: 15/100**

---

### 3.1 Day-to-day management arrangements

**Weight: 5/15**

#### Requirements

- [ ] Name the coordinating center / academic research organization (with experience record)
- [ ] Describe: contract management, site coordination, electronic case report forms, database management, data governance, medical monitoring, regulatory submissions, statistical analysis, DSMB coordination
- [ ] Describe monitoring plan (in-person vs. remote; frequency)
- [ ] Describe data security: source document storage, de-identification, platform name
- [ ] For AI studies: describe data pipeline, model deployment infrastructure, and privacy architecture (on-premises, VPC)

#### Scoring Rubric

| Criterion | Weight | 5 (Excellent) | 3 (Good) | 1 (Weak) |
|-----------|--------|---------------|----------|----------|
| Operational infrastructure | 3/5 | Named CRO/coordinating center with track record; all operational elements addressed | Most elements described | Vague or no operational plan |
| Data management and security | 2/5 | Named platform; de-identification protocol; monitoring plan | Basic data management described | No data management plan |

---

### 3.2 Role of each principal applicant and co-applicant

**Weight: 5/15**

#### Requirements

- [ ] For each team member: Name, degree, role (NPA/PA/Co-A), career stage, institution, specific contribution
- [ ] Nominated Principal Applicant: must be "ultimately responsible for all aspects"
- [ ] Describe the executive committee composition
- [ ] Show complementary expertise across team (clinical, methodological, statistical, patient engagement, regulatory, EDI)
- [ ] For multi-center: identify site PIs
- [ ] Reference letters of support

#### Scoring Rubric

| Criterion | Weight | 5 (Excellent) | 3 (Good) | 1 (Weak) |
|-----------|--------|---------------|----------|----------|
| Team completeness | 3/5 | All necessary expertise covered; each member has defined role; no redundancy | Most expertise covered | Key expertise gaps |
| Leadership clarity | 2/5 | NPA clearly responsible; executive committee defined; mentorship relationships explicit | Leadership structure unclear | No governance structure |

---

### 3.3 Steering committee and DSMB

**Weight: 5/15**

#### Requirements

NOTE: This may be optional depending on the study type.

- [ ] **Steering committee:** List composition (executive committee + site PIs + patient partner)
- [ ] **DSMB:** State coordinating body; meeting frequency; charter development; composition (clinician chair + statistician minimum)
- [ ] For pilot studies: state that DSMB will NOT terminate for efficacy/futility but MAY terminate for safety
- [ ] For confirmatory studies: define stopping rules (efficacy, futility, safety)

#### Scoring Rubric

| Criterion | Weight | 5 (Excellent) | 3 (Good) | 1 (Weak) |
|-----------|--------|---------------|----------|----------|
| Governance structure | 3/5 | Complete steering committee with patient partner; DSMB with charter and stopping rules | Basic governance described | No governance structure |
| Safety monitoring | 2/5 | DSMB with appropriate scope for study phase; regular meetings | Some safety monitoring | No safety monitoring plan |

---

## SECTION 4: General Considerations (Cross-Cutting Themes)

**Weight: 10/100**

These themes must be woven throughout the proposal but are often evaluated as a standalone criterion.

---

### 4.1 Sex, Gender, and Equity (SGBA+)

**Weight: 4/10**

#### Requirements

- [ ] Define how sex and gender will be collected (female/male/other for sex; woman/man/X gender/other for gender)
- [ ] Commit to sex- and gender-stratified analyses at each objective level
- [ ] Collect gender-specific and sex-specific non-traditional risk factors
- [ ] Address historical under-representation of women/gender minorities in your field
- [ ] Describe mitigation strategies if disparities are observed
- [ ] For AI studies: describe fairness monitoring across demographic subgroups (demographic parity, equalized odds)
- [ ] State sampling strategies to achieve sex balance (e.g., "approximately 50% women")

---

### 4.2 Patient Engagement

**Weight: 3/10**

#### Requirements

- [ ] Name the patient partner(s) on the steering committee
- [ ] Describe their specific contributions (protocol co-development, recruitment strategies, adherence strategies, knowledge mobilization)
- [ ] Reference EDI framework used (e.g., CEPPP Learning Together Evaluation Framework)
- [ ] Describe patient-oriented outcome development (if applicable)
- [ ] Include letter of collaboration from patient engagement center

---

### 4.3 Knowledge Translation and Dissemination

**Weight: 3/10**

#### Requirements

- [ ] Describe publication plan: target journal tier, conference presentations
- [ ] Describe public engagement: social media, mainstream media, patient communities
- [ ] For AI studies: describe open-source release plans and platform accessibility
- [ ] State how results will be incorporated into clinical guidelines (name the guideline body)
- [ ] Describe regulatory pathway if applicable (Health Canada SaMD, Clinical Trial Application)
- [ ] **For each knowledge user named on the application, state what they will do with the result and through what mechanism** (see F12). A plan consisting of journals and conferences is scored as weak when knowledge users are on the team

---

## SECTION 5: Resubmission Discipline

Applies whenever the application has been reviewed before. Most resubmissions fail for reasons that have nothing to do with the science of the revision.

### 5.1 The response letter is a contract

Reviewers on a resubmission read the response letter first, then check it against the body. Every claim in the letter is a promise that must be verifiable in the resubmitted documents.

**Requirements**

- [ ] Every commitment in the letter points to a specific section number, and that section actually contains the promised content
- [ ] Every parameter quoted in the letter matches the body exactly (see 5.2)
- [ ] No claim describes a design feature that is not in the body (for example, claiming randomization is stratified by a factor that the randomization section does not list)
- [ ] Nothing is described as "retained as a secondary endpoint" unless it appears in the secondary outcomes list
- [ ] Nothing is described as "pre-specified" unless it appears in the analysis or subgroup section
- [ ] Where a criticism is accepted but only partly resolved, say so and state what remains, rather than claiming full resolution

**The consistency-audit table trap.** Including a table that certifies every number as concordant is powerful, and it inverts badly. If a reviewer spot-checks one row and finds the grant does not contain the value the table certifies, the table becomes affirmative evidence of carelessness across the whole application, and it damages more than having no table at all. **Verify every row against the current document text immediately before submission, not against your intent.** A row may only claim a value the reader can find.

**Categorize each response honestly.** Reviewers respond well to a stated non-adoption with reasoning and badly to a silent one. Use three categories: accepted and changed (with section reference), accepted in part (with what remains and why), and not adopted (with the reasoning and any mitigation).

### 5.2 The pre-submission consistency gate

Run this as a mechanical pass after the final content edit and before submission. It is not proofreading, and it is not optional: this is the gate for F1, the highest-impact failure mode.

**Procedure**

1. Write the canonical parameter set (the table in F1) into a single scratch file.
2. For each parameter, search every document in the package for every occurrence and every variant spelling or format (`5,700` / `5700` / `n=5700`; `30-day` / `30 days` / `within one month`).
3. Record each hit with its location and value.
4. Reconcile every hit against the canonical value. Any mismatch is a blocking defect.
5. Verify derived arithmetic actually multiplies out: sites x rate per site per month x months must equal N; phase durations must sum to the stated total; per-arm N must double to total N; site-level provider counts must sum to the total provider count.
6. Repeat for figures and tables by opening each one, including embedded images. Regenerate any figure containing a superseded value.
7. Re-verify the response letter and any audit table against the final text, last.

**Documents in scope:** proposal body, one-page summary, response to reviewers, budget and budget justification, statistical memo, summary of progress, figures, tables, and support letters.

**Search targets that most often drift:** total N, per-arm N, number of sites, number of providers or clusters, interim analysis N and its percentage, outcome window, effect size and its metric, control event rate, loss to follow-up, power, recruitment rate, study duration, phase durations, and risk-tier names.

**Highest-yield checks, in order:**

| Check | Why it is first |
|-------|----------------|
| Figures against body text | Most damaging, most often missed, invisible in text search |
| Summary against body | The specific error that has drawn the harshest published criticism |
| Cluster or provider count | Typically appears in three places and drifts in all three |
| Interim analysis N against its stated percentage of total N | Breaks silently whenever total N changes |
| Recruitment arithmetic | Rarely recomputed after N changes |
| Superseded design elements | Risk tiers, windows, and endpoints removed in one section but surviving in others |
| Budget line items against methods claims | A line item is a factual assertion about how the study will run, and it is read as more truthful than the prose |

**Budget line items are claims about the design.** Read every line item as a reviewer would
and ask what it implies about the methods. A line item that implies infrastructure, data
flows, personnel, or procedures the methods section denies or omits is a contradiction, and
reviewers weight the budget heavily because it is where intentions become concrete. This
matters most when a line item touches a concern a reviewer has already raised: an equipment
or hosting line that contradicts a data-governance claim, a per-site line that implies a
different number of sites, or personnel that imply a different scale of recruitment.

### 5.3 Purging a superseded design element

When a revision removes a design element (a risk tier, an endpoint, an outcome window, a site), the element survives in places that do not mention it by name. This is the single most common source of resubmission inconsistency.

- [ ] Search the removed element's name and every synonym across all documents
- [ ] Check the objectives list, which often retains the old endpoint as a now-duplicated secondary objective
- [ ] Check the secondary outcomes list for the same duplication
- [ ] Check the analysis section, monitoring thresholds, and stopping rules, which reference tiers by name
- [ ] Check the impact and implementation sections, which describe the future clinical pathway using the old categories
- [ ] Check figures and tables
- [ ] Confirm the new primary endpoint does not now appear verbatim as a secondary objective or secondary outcome

**Duplicate-endpoint check.** After changing a primary endpoint, read the primary outcome and the secondary outcomes side by side. If any secondary restates the primary, either delete it or relabel it explicitly (for example, as the former primary retained at a different window).

### 5.4 What reviewers reward and punish across rounds

- **Punished hardest:** a criticism raised in a prior round and not adequately addressed. Reviewers say so explicitly and score accordingly. If you do not adopt a prior recommendation, state why in the response letter rather than leaving it unmentioned.
- **Punished:** contradictions in a document that was just revised, which read as evidence the revision was rushed.
- **Rewarded:** structural responses over incremental ones. Changing the endpoint to remove a bias objection scores better than adding an adjustment to accommodate it.
- **Rewarded:** accurate self-limitation. Stating that the pilot supports feasibility but not efficacy, or that a residual bias is bounded rather than eliminated, builds credibility that carries into the assumptions the reviewer cannot check.
- **Neutral, not positive:** an improved score on one criterion does not protect the others. Committees change between rounds, and a new committee brings new priorities.

### 5.5 Committee fit

The same application scores differently in different committees. Note which committee reviewed prior rounds and what it emphasized: a methods-focused committee will weight the statistical sections most heavily, while a health-services committee will weight implementation, costing, and system impact. When resubmitting to a different committee, re-read the whole application against that committee's priorities rather than only patching the prior reviewers' comments.

---

## Overall Scoring Summary

| Section | Weight | Key Question |
|---------|--------|--------------|
| 0. Summary of Progress | 10/100 | Is this investigator the right person to do this work? |
| 1. The Need | 25/100 | Is this an important, unanswered question? |
| 2. The Proposed Study | 40/100 | Is the methodology rigorous and feasible? |
| 3. Trial Management | 15/100 | Can this team execute this study? |
| 4. General Considerations | 10/100 | Does this study address equity, patient engagement, and impact? |
| **TOTAL** | **100/100** | |

### Score Interpretation

- **90-100:** Fundable as-is. Minor revisions only.
- **75-89:** Competitive. Address reviewer concerns in specific sections.
- **60-74:** Needs significant revision. Major gaps in 1-2 sections.
- **Below 60:** Fundamental redesign needed.

### Blocking defects

The following override the section scores. An application with any of these is not ready to submit regardless of how well the rest scores, because each one is read by reviewers as evidence about trial conduct rather than as a writing problem.

| Blocking defect | Failure mode |
|-----------------|--------------|
| Any parameter contradicts itself across the package, including in figures | F1 |
| The primary endpoint denominator is not the randomized population | F2 |
| The sample size does not reproduce from its stated inputs, or uses a different model than the primary analysis | F4 |
| The primary endpoint depends on a data source whose access is unevidenced | F7 |
| A participating site has no signed institutional letter | F8 |
| The response letter claims something the body does not contain | 5.1 |
