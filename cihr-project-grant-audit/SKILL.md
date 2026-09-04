---
name: cihr-project-grant-audit
description: Audit non-RCT CIHR Project Grant applications and resubmissions for aim-method traceability, reviewer-response closure, cross-document consistency, feasibility, statistics, and terminology. Use when auditing, reviewing, responding to reviewers, or QCing a non-RCT CIHR grant.
---

# CIHR Project Grant Audit (Non-RCT)

## Overview

Systematic audit of a CIHR Project Grant application for a non-RCT study (registry, cohort, prediction model, biobank, AI/technology, observational). Produces a structured checklist (markdown), applies tracked changes for fixable issues, and adds comments for items requiring investigator judgment.

Non-RCT CIHR grants typically organize around **Specific Aims**, each with its own rationale, hypothesis, endpoints, and analysis plan — rather than the numbered RCT section structure (1.1–3.3). This audit is designed for that architecture.

The audit has eight parts. Each part can surface issues that require either tracked changes (fixable problems) or comments (judgment calls).

## Prerequisites

Before starting the audit:

1. Extract the .docx text using `python-docx` or direct XML parsing
2. Identify the document's section structure (headings, subheadings, Roman numerals, etc.)
3. Build a section index mapping heading text to paragraph positions
4. If a budget file is provided, extract its text as well
5. Note: .docx text extraction loses formatting (italics, superscripts, subscripts). Flag items requiring .docx-level verification (gene name italicization, superscript reference numbers, subscript terms)

## Part A: Aim-Objective-Hypothesis-Endpoint-Methods Traceability Matrix

Every **Specific Aim** — and every **sub-aim** (1A, 1B, 1C, 2A, 2B, etc.) — must have a complete chain:

1. **Aim statement** — a high-level goal (e.g., "Aim 1: Arrhythmic risk prediction")
2. **Rationale** — why this aim matters, grounded in cited literature
3. **Hypothesis** — a testable prediction (must appear explicitly as "We hypothesize that...")
4. **Endpoints/Outcomes** — primary and secondary outcomes with exact definitions (measurement, timing, data source, adjudication plan)
5. **Analysis plan** — statistical method, model structure, covariates, validation approach, pre-specified subgroups
6. **Sample size/feasibility** — event counts, required N, recruitment evidence
7. **Expected results** — anticipated clinical impact and deliverables

### Procedure

1. Extract each Specific Aim from the document (look for "Aim 1", "Aim 2", "Specific Aim", or equivalent heading patterns). Also identify sub-aims (1A, 1B, 1C, etc.) — each sub-aim is treated as a separate traceability chain.

2. For each aim and sub-aim, locate and verify:

   a. **Hypothesis present?** Search for explicit hypothesis statement. Flag if missing or vague.
   b. **Endpoints defined?** For each stated outcome:
      - Is the outcome precisely defined (not just named)?
      - Is the measurement method specified (instrument, data source, timing)?
      - Are primary vs. secondary vs. exploratory outcomes clearly distinguished?
      - **Adjudication**: For composite endpoints, is each component defined? Who adjudicates events? What criteria are used? Is adjudication blinded? If different aims have different endpoint types (e.g., arrhythmic vs. HF), verify that adjudicators have relevant expertise for each aim's endpoints.
   c. **Analysis plan complete?** For each endpoint:
      - Is the statistical method named (e.g., Cox regression, logistic regression, C-statistic)?
      - Are covariates/candidate predictors listed?
      - Is the validation strategy described (internal: bootstrapping/cross-validation; external: named cohort)?
      - For each named external validation cohort: does the text confirm which required predictor variables are available in that cohort?
      - Are pre-specified subgroups listed (sex, age, genotype, site)?
      - Is handling of missing data described (e.g., multiple imputation)?
      - Are competing risks addressed if relevant? For prediction models, Fine-Gray subdistribution hazards are appropriate. For etiologic/causal aims, cause-specific hazards may be more informative. Verify the chosen approach matches the aim's purpose.
      - For exploratory analyses (PCA, dimension reduction, "we will also explore..."): is there a pre-specified stopping rule, multiple testing strategy, and acknowledgment that results are hypothesis-generating?
   d. **Sample size justified?**
      - Is the events-per-variable rule applied (e.g., 10 EPV)?
      - Is the assumed event rate cited with source?
      - Does the recruitment projection support the required N?
      - Is a worst-case scenario considered?
      - For sub-aims: is sample size separately justified (not just inherited from the parent aim)?
      - For AI/deep learning sub-aims: is the training set size justified relative to model complexity? Is the number of events in the test set sufficient for reliable performance estimation (typically >50–100 events per TRIPOD-AI)? Flag when test sets have very few events.
      - For recruitment feasibility projections: verify that the reference population (registry, clinic volume) matches the proposed study population. Extrapolations from registries with different disease populations should be flagged.
   e. **Literature-methods alignment?** (see Part G for full procedure)
      - Does the cited literature actually support the chosen methods and candidate predictors?

3. **Cross-aim consistency check**: After auditing each aim individually, compare across aims:
   - Do gene lists, predictor lists, or variable definitions differ between aims? If so, is the rationale for the difference explicitly stated?
   - Is missing data handling described for every aim (not just the first)? A cross-reference such as "as per Aim 1" is acceptable only if the referenced approach fully applies. If the new aim has different variables, different cohort characteristics, or different missingness patterns, the strategy should be independently described.
   - Are endpoint definitions consistent where they should be (e.g., "sustained VA" in background vs. Aim 1)?
   - If aims share a cohort, is the derivation/validation split described for each aim?

4. **Design-specific bias check**: For ambispective/retrospective-prospective designs, verify:
   - Is time zero clearly defined?
   - Is immortal time bias addressed?
   - Is informative censoring discussed?
   - Are secular trends in treatment acknowledged?
   - For retrospective components: is ascertainment bias addressed?
   - For registry/cohort studies with treatment changes over follow-up: is time-varying treatment handled appropriately (time-dependent covariates, landmark analysis, or marginal structural models)? A single baseline measurement of medication may introduce bias.

5. Flag gaps:
   - **GAP**: Component entirely missing (e.g., no hypothesis for Aim 2, no adjudication plan)
   - **PARTIAL**: Component present but incomplete (e.g., analysis plan says "Cox regression" without specifying covariates, competing risks, or validation)
   - **MISMATCH**: Component present but inconsistent with another part of the chain (e.g., hypothesis mentions "outperform LVEF alone" but analysis plan doesn't include a comparison to LVEF-only model)
   - **OK**: Complete and internally consistent

### Output Format

| Aim | Component | Content Summary | Status | Notes |
|-----|-----------|----------------|--------|-------|
| 1 | Hypothesis | "multimodality approach can outperform..." | OK | Testable, specific |
| 1 | Primary endpoint | Sustained VA (VT, ICD therapy, SCD) | OK | Well-defined with adjudication |
| 1A | Analysis plan | Cox PH, backward selection, C-statistic | OK | Comprehensive |
| 1B | Sample size | External validation N | PARTIAL | Split between derivation/validation not pre-specified |
| 1C | Sample size | ML training set | GAP | No minimum N justified for deep learning |
| 2 | Missing data | Not mentioned | GAP | Only Aim 1 describes multiple imputation |
| Cross-aim | Gene lists | Aim 1 vs Aim 2 differ | MISMATCH | BAG3 added, DES/TMEM43 dropped; rationale not stated |

### Common Issues

- Hypothesis is stated in the background/rationale but not repeated in the aim-specific methods section
- Exploratory analyses mentioned in passing but with no formal analysis plan
- Validation cohort referenced by name but without confirming it has the same variables
- Candidate predictors in the analysis plan don't fully match those in the rationale or pilot data
- Composite endpoints list components without defining each or specifying adjudication
- AI/ML aims describe model architecture but lack a plan for comparing to a simpler baseline model
- Event rate assumptions drawn from studies with different inclusion criteria
- Sub-aims inherit sample size from parent aim without separate justification
- Different gene lists across aims without explicit rationale for the difference
- Missing data strategy described in one aim but not carried through to subsequent aims

## Part B: Cross-Reference Verification

Every internal reference ("Section X", "Aim 1A", "see above", "as described in...", "see support letter from...") must point to real content.

### Procedure

1. Use regex to find all internal references. Patterns include:
   - `Section [IVX]+` or `Section \d+`
   - `Aim \d+[A-C]?`
   - `see (above|below|Section|Aim|Table|Figure)`
   - `as described (in|above|below|previously)`
   - `see (support |reference )?letter(s)? from`
   - `presented in Section`
   - Parenthetical references like `(Section II)` or `(see Aim 1A)`
   - Role-based references: `co-A [Name]`, `co-PA [Name]`, `NPA`, `the NPA`
   - Empty parentheses `()` or `( )` — likely stripped URLs from .docx export

2. For each reference:
   - Note the source location (which section makes the reference)
   - Note the target (what is being referenced)
   - Verify the target exists and contains the claimed content

3. For every person named in a "support letter from Dr. X" reference, verify they appear in the Expertise section with a role description.

4. Flag issues:
   - **OK**: Referenced content exists and matches the claim
   - **BROKEN**: Target section/figure/table does not exist
   - **STALE**: Target exists but content doesn't match what's claimed
   - **VAGUE**: Reference is too imprecise to verify (e.g., "as mentioned above" without specifying where)
   - **STRIPPED**: Empty parentheses indicating a removed URL/hyperlink

### Common Issues

- Support letters referenced by name but the letter author's role isn't described in the team section
- "See preliminary results" without specifying which subsection of pilot data
- Figure/Table references that don't match actual numbering
- Cross-references between aims that claim shared methods but the methods differ in detail
- "As described above" spanning multiple pages — reader cannot locate the referent
- Empty parentheses `()` where URLs were stripped during document conversion
- A person named as co-A for a specific task (e.g., event adjudication) who does not appear in the site PI list or team expertise section

### Output Format

| Reference Text | Source Location | Target | Status | Notes |
|---------------|----------------|--------|--------|-------|
| "see Section II" | Aim 1 rationale | Section II: Pilot Data | OK | |
| "support letter from Dr. X" | Section VI | Support letters | OK | Letter included |
| "as described above" | Aim 2 methods | Unclear | VAGUE | Which section? |
| "()" after platform name | Section III | URL | STRIPPED | Hyperlink removed |
| "co-A Rivard" | Aim 1 outcomes | Section VI Expertise | BROKEN | Rivard not in expertise section |

## Part C: Non-RCT Grant Section Completeness

Non-RCT CIHR Project Grants do not follow the mandatory RCT heading structure (1.1–3.3). Instead, check against the expected content areas for a competitive application. Compare the document against the reference structure in `references/cihr-non-rct-sections.md`.

### Procedure

1. Extract all section headings from the document
2. Map each heading to the expected content areas
3. Flag missing content areas (not just missing headings — the content may exist under a different heading)
4. Verify that each content area has substantive treatment (not just a sentence)

### Expected Content Areas

| Area | Required? | Typical Heading | What to Check |
|------|-----------|----------------|---------------|
| Background & Knowledge Gap | Yes | "Background", "Introduction" | Burden of disease, current standard, specific gaps |
| Central Hypothesis | Yes | Within background or separate | Explicitly stated, testable |
| Pilot/Preliminary Data | Yes | "Pilot Data", "Preliminary Results" | Own team's data, not just literature |
| Study Design & Population | Yes | "Methods", "Study Design" | Design type, inclusion/exclusion, setting |
| Specific Aims (each) | Yes | "Aim 1", "Aim 2" | Each aim has full chain (Part A) |
| Outcomes/Endpoints | Yes | Within aims or separate | Defined per aim with adjudication |
| Analysis Plan | Yes | Within aims or separate | Statistical methods per aim |
| Sample Size/Feasibility | Yes | Within aims or separate | Power/events per variable |
| Sex & Gender (SGBA+) | Yes | "Sex and Gender" | Not tokenistic — integrated into aims; sex AND gender addressed separately; stratified analyses committed |
| EDI (Equity, Diversity, Inclusion) | Yes | Within SGBA+ or separate | Addresses diversity beyond sex/gender: race/ethnicity, socioeconomic status, geographic barriers; recruitment strategies for underrepresented populations |
| Patient Engagement | Yes | "Patient Engagement" | Named patient partners, specific contributions to design/conduct/dissemination |
| Knowledge Translation | Yes | "Knowledge Translation", "KT" | Dissemination plan, guideline pathway, clinical tools |
| Team & Expertise | Yes | "Expertise", "Team" | Each member's role and contribution |
| Data Management & Privacy | Yes | "Data Management" | Storage, security, governance |
| Ethics & Regulatory | Yes | Within methods or separate | REB approval, multi-site harmonization, consent process, privacy law compliance |
| Timeline & Milestones | Yes | "Timeline", Gantt chart | Year-by-year milestones, recruitment targets, deliverable dates |
| Training Plan | Recommended | Within expertise or separate | Trainees named, mentorship structure, skill development |
| Resources | Recommended | "Resources" | Infrastructure, existing support |
| Potential Challenges | Recommended | "Challenges", "Limitations" | Mitigation strategies — specific, not vague |
| Concluding Remarks | Recommended | "Concluding Remarks" | Summary of significance |

### Common Issues

- SGBA+ reduced to a single paragraph stating "sex will be included as a covariate" — should pervade aims
- Patient engagement section names a foundation but doesn't describe specific contributions to the study design
- Knowledge translation limited to "conferences and publications" without naming guideline bodies or clinical tools
- No explicit mention of EDI considerations beyond sex/gender
- Challenges section lists problems but mitigation strategies are vague or absent
- No timeline or milestones — CIHR expects year-by-year deliverables
- Ethics section limited to one sentence about REB approval at a single site; no discussion of multi-site harmonization
- Trainees mentioned in passing ("trainees are expected to contribute") but no structured training plan

## Part D: Budget-Protocol Alignment

If a budget file is provided, verify bidirectional alignment between budget and protocol.

If no budget file is provided, list all protocol commitments that imply costs (personnel, equipment, biobanking, genotyping, imaging transfers, core labs, travel, data platforms) and flag them as **UNVERIFIABLE**. This serves as a checklist for when the budget becomes available.

### Procedure

1. Extract budget line items with amounts and justifications
2. For each budget item, verify it maps to a protocol commitment:
   - Personnel: role described in the team/expertise section
   - Equipment: needed for procedures described in the protocol
   - Biobanking/genotyping: matches the sample processing described
   - Data linkages/transfers: required for the endpoints and data sources described
   - Core labs: match the imaging/analysis infrastructure described
   - Travel: justified by multi-site coordination needs
3. For each protocol commitment, verify budget support:
   - Number of sites: personnel and coordination budgets cover all sites?
   - Sample sizes: biobanking and genotyping budgets match target enrollment?
   - Imaging transfers: platform fees budgeted?
   - Training/student support: matches described trainee involvement?

### Output Format

| Category | Budget Item | Amount | Protocol Section | Alignment | Issues |
|----------|-----------|--------|-----------------|-----------|--------|

## Part E: Content Issues (Garbled Text, Duplicates, Formatting)

Scan the full document text for garbled text, missing spaces, duplicate fragments, and formatting errors.

### Procedure

1. **Garbled text detection**: Search for patterns indicating splice errors from tracked-change acceptance:
   - Period immediately followed by lowercase letter with no space: `\.\w` (excluding known abbreviations like "e.g.", "i.e.", "et al.", "vs.", decimal numbers, URLs)
   - Orphan fragments: short phrases (< 5 words) that don't connect grammatically to surrounding text
   - Possessive markers without antecedent: `'s` preceded by whitespace or punctuation instead of a noun
   - Sentence fragments ending abruptly mid-thought

2. **Missing spaces**: Search for:
   - Lowercase immediately followed by uppercase: `[a-z][A-Z]` (e.g., "patientsThe" should be "patients. The")
   - Digit immediately followed by letter in non-standard ways: `\d[a-zA-Z]` (excluding units like "3D", "p53", "12-lead", known abbreviations)
   - Period followed by uppercase with no space: `\.[A-Z]` (excluding abbreviations)
   - Reference number fused with following text: `\d{1,3}[A-Z][a-z]` (e.g., "15We" — superscript reference merged with next word)

3. **Duplicate fragments**: Search for:
   - Near-identical sentences or phrases within 500 characters of each other
   - Paragraphs that restate the same information in slightly different words (content duplication across sections)
   - Repeated references to the same fact in close proximity (e.g., enrollment count stated in both pilot data and methods)

4. **Reference number issues**:
   - Establish a baseline: if all references appear as inline numbers (e.g., "individuals.1"), this is a .docx text extraction artifact, not a document error. Note this once and do not flag each instance individually.
   - Flag genuinely inconsistent reference formatting (some superscripted, some inline)
   - Duplicate reference citations

5. **Empty URL placeholders**: Search for empty parentheses `\(\s*\)` — these typically indicate stripped hyperlinks from .docx export. Flag each and note the context (platform name, website, etc.).

6. **Grammar errors**: Beyond formatting issues, check for grammatical errors in critical sentences (hypothesis statements, method descriptions, endpoint definitions):
   - Subject-verb agreement errors
   - Missing words (e.g., "nor does there evidence" → missing "exist")
   - Incomplete sentences

7. **Formatting consistency**:
   - Section reference format: "Section II" vs "section II" vs "Sec II" — pick canonical and flag deviations
   - List formatting: mixing numbered lists (1-, 2-) with bullet points within the same section
   - Parenthetical style: "(see X)" vs "— see X" — flag inconsistencies
   - Hyphenation: "non-ischemic" vs "nonischemic" — flag inconsistencies

8. **Paragraph numbering gaps**: In .docx text extraction, non-contiguous paragraph numbers indicate removed elements (figures, tables, text boxes). Flag these as potential missing content and note that figures/tables should be reviewed in the original .docx.

## Part F: Terminology and Abbreviation Consistency

Automatically discover and audit **all** abbreviations, key terms, cohort names, gene names, and recurring terminology in the document. This part is **grant-agnostic** — it builds registries dynamically from the document text rather than checking against a hardcoded list.

### Step 1: Auto-Discover Abbreviations

Scan the entire document to build an abbreviation registry using these detection patterns:

1. **Parenthetical definitions** (most reliable): `full term (ABBR)` pattern
   - Regex: `([A-Za-z][\w\s\-/]+)\s*\(([A-Z][A-Za-z0-9\-+/]{1,15})\)`
   - Captures: the full term + its abbreviation
   - Example: "non-ischemic cardiomyopathy (NICM)" → registers NICM, defined at this location

2. **Undefined uppercase sequences**: Find all tokens matching `[A-Z]{2,}[a-z0-9+\-]*` that were NOT captured by pattern 1
   - These are abbreviations used without a parenthetical definition in the document
   - Filter out: section headings in all-caps, Roman numerals (I, II, III, IV, V, VI), single-letter variables, reference numbers
   - Each needs investigation: is it a universally known abbreviation? Or does it need a definition?

3. **Lowercase/mixed-case abbreviations**: Catch patterns like `eGFR`, `eCRF`, `co-A`, `co-PA`, `NT-proBNP`
   - Regex: `\b[a-z]+[A-Z][A-Za-z]*\b` for camelCase
   - Regex: `\b[a-z]+-[A-Z]+[a-z]*\b` for hyphenated role abbreviations
   - Regex: `\b[A-Z]{1,3}-[a-z]+[A-Z][A-Za-z]*\b` for compound biomarker names

### Step 2: Audit Each Discovered Abbreviation

For every abbreviation found in Step 1, check:

| Check | Rule | Flag |
|-------|------|------|
| Defined at first use? | First occurrence must be `full term (ABBR)` | **UNDEFINED** — no parenthetical definition found before first use |
| Used after definition? | Must appear at least once after its definition | **UNUSED** — defined but never used again (clutter) |
| Used consistently? | After definition, the full term should not reappear (use the abbreviation) | **INCONSISTENT** — full term reappears after abbreviation was defined |
| Defined only once? | Should not be re-defined later | **REDEFINED** — `full term (ABBR)` appears more than once |
| Used before definition? | No uses should precede the definition | **PREMATURE** — abbreviation appears before its parenthetical definition |

**"Universally known" threshold**: For CIHR grants, assume reviewers include at least one non-clinical methodologist and one patient partner. Abbreviations not universally known outside the specific clinical field should be defined at first use. Examples that likely need definition: disease-specific abbreviations (NICM, ARVC, HCM), imaging modalities (CMR, TTE, LGE), clinical scores (NYHA), biomarkers (NT-proBNP, eGFR). Examples that likely do NOT need definition: DNA, RNA, URL, PhD, MD.

**CIHR-specific role abbreviations**: NPA (Nominated Principal Applicant), co-PA (Co-Principal Applicant), co-A (Co-Applicant) are standard CIHR terms. They should still be defined at first use in the grant body, but their absence is a minor issue rather than a critical gap.

### Step 3: Auto-Discover Key Terms and Check Consistency

Identify recurring domain-specific terms and check for naming drift:

1. **Cohort/study names**: Find all capitalized proper nouns or named entities that appear 3+ times. For each:
   - List all variant forms (e.g., "CaNICM", "CaNICM registry", "the CaNICM study")
   - Verify referent is always unambiguous
   - If multiple registries/cohorts exist, verify each reference clearly identifies which one

2. **Endpoint/outcome terms**: Extract all phrases near "outcome", "endpoint", "primary", "secondary", "composite", "event". For each unique endpoint:
   - Collect every variant phrasing across the document
   - Flag if the same outcome uses different wording in different sections
   - Flag if composite endpoint components differ between where they are listed

3. **Statistical method terms**: Extract all named statistical methods (search for "regression", "model", "analysis", "test", "statistic", "score"). For each:
   - Collect all variant forms
   - Identify the most complete form as canonical
   - Flag naming inconsistencies
   - **Check proper noun spelling**: For named methods (Harrell's C, Kaplan-Meier, Cox, Akaike, Fine-Gray, Bayesian), verify consistent and correct spelling across the document

4. **Gene/protein names**: Find gene-like tokens (2-6 uppercase letters, optionally followed by digits). For each:
   - Check if italicized (gene names should be italicized per HUGO/HGNC convention) — **note**: this check requires the original .docx; text extraction loses italics formatting. Flag for .docx-level verification.
   - Check if gene lists are consistent across sections (e.g., if "high-risk genes" is defined as a specific set, does the set stay the same across aims? If different, is the rationale for different lists explicitly stated?)
   - Check variant nomenclature consistency (e.g., "p.Arg14del" vs "R14del")

5. **Person/institution names**: Extract all named individuals and institutions. For each:
   - Collect all variant forms
   - Verify consistent role labeling ("co-A" vs "co-PA" vs "collaborator")
   - Verify all site PIs mentioned in methods also appear in the site list section
   - Verify all individuals referenced as "support letter from Dr. X" are listed in the team section
   - Verify all individuals assigned specific tasks (e.g., "event adjudication by co-A Roberts and Rivard") appear in the expertise section

### Output Format

| Category | Term | Variants Found | First Occurrence (para #) | Definition Location | Issues |
|----------|------|---------------|--------------------------|--------------------|---------|
| Abbreviation | NICM | NICM, non-ischemic cardiomyopathy | Para 2 | Para 2: "Non-ischemic cardiomyopathy (NICM)" | OK |
| Abbreviation | GDMT | GDMT, guideline-directed medical therapy | Para 3 | Para 3 | INCONSISTENT: full term reused in para 28 after definition |
| Abbreviation | AIC | AIC | Para 31 | Para 36: "Akaike information criterion (AIC)" | OK (defined at first non-passing use) |
| Abbreviation | NPA | NPA | Para 14 | None | UNDEFINED: CIHR role term, minor |
| Endpoint | Primary (Aim 1) | "sustained VA", "ventricular arrhythmia", "VA" | Para 30 | — | 3 variant forms across document |
| Gene list | High-risk VA genes | {FLNC,DES,PLN,DSP,LMNA,TMEM43,RBM20} | Para 28 | — | List differs in Aim 2 (adds BAG3, drops DES/TMEM43); rationale not stated |
| Stat method | C-statistic | "Harrell's C-statistic", "Harrel's C-statistic" | — | — | Misspelling: "Harrel" should be "Harrell" |
| Institution | MHI | "Montreal Heart Institute", "MHI" | Para 11 | Para 14 | 2 forms used |

## Part G: Literature-Methods Alignment

Verify that cited literature actually supports the methodological choices AND epidemiological claims made in the grant.

### Procedure

1. For each aim's **candidate predictors/variables**:
   - Is each predictor justified by cited literature (meta-analysis, prior study, or own pilot data)?
   - Does the cited study actually support the claimed association, or is it tangential?
   - Are effect sizes from cited literature consistent with what's claimed in the text?

2. For each aim's **statistical approach**:
   - Is the chosen method appropriate for the data structure (time-to-event → survival analysis, binary → logistic regression)?
   - If a specific approach is cited as precedent (e.g., "following a similar approach as X"), does the cited study actually use that approach?
   - Are validation methods consistent with cited methodological standards?
   - **Methodology currency**: Is the chosen approach current best practice? For prediction models, check compliance with TRIPOD (Transparent Reporting of a Multivariable Prediction Model) guidelines and PROBAST (Prediction model Risk Of Bias ASsessment Tool). For AI/ML prediction models, check TRIPOD-AI (data preprocessing described, model interpretability addressed via saliency maps/SHAP, prospective validation plan). Flag traditional approaches that contemporary guidelines advise against (e.g., backward stepwise selection vs. penalized regression like LASSO/elastic net) unless explicitly justified.

3. For **sample size justifications**:
   - Are event rates cited from studies with comparable populations?
   - If multiple event rate estimates are cited, is the range honestly represented?
   - Does the chosen "conservative" estimate actually come from the most comparable study?

4. For **pilot data claims**:
   - Are statistics correctly reported (HR, CI, p-values match what's stated)?
   - Are pilot results from the applicant's own work, or repurposed from collaborators?
   - Is the pilot population comparable to the proposed study population?
   - **Confidence interval width**: Are CIs around pilot estimates narrow enough to support the claims being built on them? Flag wide CIs (e.g., AUC 0.87 [0.73–0.97] spans from "fair" to "near-perfect") and note the uncertainty.

5. For **epidemiological/rationale claims**: Check that prevalence figures, event rates, and burden-of-disease statistics in the background/rationale section are supported by citations. An unsupported prevalence figure is as problematic as an unsupported statistical choice.

6. **Evidence quality check**: For each cited reference supporting a key claim, note whether it is:
   - **Peer-reviewed**: published in a journal
   - **Preprint**: medRxiv, bioRxiv, SSRN, etc.
   - **Unpublished**: "unpublished data", "manuscript under review"
   - Flag claims where major methodological decisions rest on non-peer-reviewed evidence.

7. Flag issues:
   - **SUPPORTED**: Literature clearly supports the claim (peer-reviewed)
   - **WEAK**: Literature is tangential, from a substantially different population, or based on preprint/unpublished data
   - **OVERCLAIMED**: The text overstates what the cited literature shows
   - **UNSUPPORTED**: No citation provided for a key claim (methodological or epidemiological)
   - **INCONSISTENT**: Cited effect size doesn't match what's stated in the text

### Output Format

| Claim | Citation(s) | Evidence Quality | Assessment | Notes |
|-------|------------|-----------------|------------|-------|
| "LGE predictive of VA (HR 2.37)" | Pilot data (MHI cohort) | Own data | SUPPORTED | Correctly reported |
| "event rate of 4.5% in meta-analysis" | Ref 39 | Peer-reviewed | SUPPORTED | Meta-analysis of 11,000 patients |
| "NICM PGS may predict incident NICM" | Ref 30 (medRxiv) | Preprint | WEAK | Not peer-reviewed; major predictor (PGSNICM) rests on this |
| "PGS will be incorporated into practice in the very near future" | Refs 31-32 | Peer-reviewed | OVERCLAIMED | Consensus statements discuss potential, don't recommend |
| "Only 5% of patients with ICD having appropriate therapy" | None | — | UNSUPPORTED | Common estimate but no citation provided |
| Backward stepwise selection by AIC | Standard | — | WEAK | TRIPOD recommends against stepwise; penalized regression preferred unless justified |

## Part H: Reviewer-Response and Resubmission Closure

Use this part whenever prior reviews, a response-to-reviewers document, or an earlier application is available. A persuasive response is not proof that a concern has been addressed. Closure requires the response claim, the revised application, and every dependent document to agree.

### H1. Build a Reviewer Concern Registry

Extract every substantive concern, including comments embedded in strengths, budget recommendations, sex/gender appraisals, and repeated concerns from earlier rounds. Keep separate rows when one reviewer sentence contains multiple causal issues.

For each concern, record:

1. Review round, reviewer, criterion, and exact concern
2. Root concept, such as endpoint validity, verification bias, feasibility, or statistical alignment
3. Whether the concern recurred in an earlier round
4. Applicant response and claimed change
5. Exact revised-application location
6. Cross-document dependencies, including summary, figures, budget, letters, and statistical appendices
7. Residual risk and any evidence still required

Treat recurrence as evidence that the prior response failed at the implementation or communication layer. Do not answer a repeated concern with more reassurance. Identify what the reviewer could not verify and add the missing evidence or change the design.

### H2. Canonical Parameter and Cross-Document Control

Create a canonical parameter ledger before judging consistency. At minimum include:

- Study design and unit of randomization
- Stratification and clustering variables
- Number and type of sites
- Recruitment period, follow-up period, and total duration
- Number of providers and participants
- Primary endpoint definition, denominator, and time window
- Control event rate, target effect, alpha, power, attrition or under-ascertainment assumption, ICC, and final sample size
- Primary analysis model and effect measure
- Intervention tiers, thresholds, and recommended actions
- Substudy size and allocation
- Data-linkage sources and consent model

Search every application component for stale values, including text boxes, figures, captions, tables, tracked changes, comments, headers, summaries, budgets, and support letters. A consistency table is valid only if generated from the current files. Never state that old values were removed without executing the search.

Flag:

- **CONTRADICTION**: Two current documents state incompatible values or methods
- **STALE**: A prior value remains in a figure, summary, comment, or dependent file
- **UNVERIFIED**: The response claims propagation but a dependent file is missing or was not inspected
- **CONSISTENT**: All inspected current documents match the canonical ledger

### H3. Endpoint, Estimand, and Ascertainment Audit

For each primary and key secondary endpoint, write the full causal chain:

`randomization -> intervention exposure -> clinician or system action -> reference-standard measurement -> endpoint ascertainment -> analysis`

Then verify:

- The endpoint measures a clinically meaningful outcome, not only an operational intermediate, unless the operational outcome is the explicit study objective
- The time window is clinically justified and matches the intervention recommendation
- The denominator is explicit and identical in the endpoint, sample-size, and analysis sections
- Events, missing outcomes, absence of testing, death, and loss to follow-up are distinct states
- Outcome ascertainment is equally available across randomized arms
- If reference-standard testing depends on the intervention or clinician behavior, verification bias is addressed through universal ascertainment, random verification sampling in both arms, inverse-probability methods, or a justified sensitivity framework
- The comparator represents actual standard clinical assessment, including relevant non-AI information, rather than an artificially weak comparator
- Post-randomization behavior that is part of the intervention mechanism is not incorrectly described as eliminated confounding

For diagnostic or triage trials, calculate the verification fractions by arm and risk group. Diagnostic performance estimated only among tested participants is conditional performance, not population performance. Label it accordingly unless the design corrects partial verification.

### H4. Analysis and Sample-Size Coherence

Reproduce the sample-size calculation from the stated inputs. Do not accept a quoted software output or rounded total without executable verification.

Check that:

- The powered effect matches the exact control and intervention rates
- Relative risk, odds ratio, hazard ratio, and absolute difference are not used interchangeably
- Attrition inflation is compatible with the endpoint denominator and missing-data definition
- The sample-size method matches the primary analysis or is explicitly justified as a valid approximation
- Randomization level, clustering level, and correlation structure are distinguished
- Sparse clusters and rare events will not make the chosen model unstable
- The number of clusters, cluster-size distribution, and expected events per cluster support GEE, mixed-effects, or frailty estimation
- Stratification factors included in the model will not cause separation or overfitting
- Control-rate, adherence, capacity, prevalence, ICC, and loss assumptions receive sensitivity analyses when power is fragile
- Interim sample-size re-estimation timing is stated as a proportion of the final sample and updated when the total sample changes

When reviewers question a model, the response must name the revised estimator, clustering unit, working correlation or random-effects structure, effect measure, covariate adjustment, and sensitivity model. Statements such as "we adjusted the analysis" are insufficient.

### H5. Operational Feasibility as a Testable Contract

Convert every feasibility assurance into observable evidence or a pre-specified gate:

- Run-in duration has objectives, data collected, responsible personnel, exit criteria, and remediation rules
- Recruitment arithmetic reconciles sites, providers, monthly rate, and recruitment duration
- Intervention fidelity is monitored in real time with a defined numerator, denominator, threshold, and response
- Resource capacity supports the endpoint window at every site, with site-specific evidence where capacity is causal to the endpoint
- External records and administrative linkage have named data custodians, legal pathways, agreements, costs, and fallback plans
- Consent waivers, patient contact, and verification substudies have non-overlapping, explicit consent rules
- Site participation is supported by current letters that match the final protocol and site role
- Regulatory, privacy, cybersecurity, and data-residency claims match the actual architecture and budget

Classify commitments as **CONFIRMED**, **CONTINGENT**, or **UNSUPPORTED**. Do not convert contingent approvals, unsigned letters, estimates, or planned agreements into confirmed facts in the response letter.

### H6. AI Evidence Maturity and Implementation Validity

For AI-enabled proposals, also verify:

- Peer-review status of the foundational model and whether unpublished evidence carries a major claim
- Training, internal validation, external validation, and prospective evaluation populations are clearly separated
- Performance is reported across intervention-relevant risk tiers and key subgroups
- Model version, weights, threshold, preprocessing, and update policy are frozen or governed during the trial
- Drift monitoring and site transportability are addressed without changing the evaluated intervention mid-trial
- Human workflow, alert uptake, and resource constraints are part of the effectiveness model
- Comparison against standard clinical assessment and simpler baselines is planned
- Fairness assessment includes calibration and error rates by clinically relevant groups, not only conventional interaction tests
- Implementation outputs lead to concrete decisions, such as workflow changes, policy briefs, regulatory steps, or guideline engagement

### H7. Adjudicate Closure Conservatively

Assign one status to every concern:

- **ADDRESSED**: The revised application contains a complete, internally consistent change and all dependent artifacts agree
- **PARTIALLY ADDRESSED**: A meaningful change exists, but evidence, propagation, feasibility, or methodological detail remains incomplete
- **NOT ADDRESSED**: The response repeats rationale, promises future work, or lacks a corresponding application change
- **CONTRADICTED**: The response claims a change that the current application or another artifact disproves
- **NOT APPLICABLE**: The concern no longer applies because the relevant aim, endpoint, site, or procedure was removed, with removal verified across artifacts
- **HUMAN DECISION REQUIRED**: Closure depends on an investigator choice, external agreement, clinical threshold, or data not present in the package

Do not use **ADDRESSED** when the only evidence is the response letter. Unsupported certainty is worse than an explicit residual action because reviewers can detect the mismatch.

### H8. Resubmission Output Matrix

| Round / Reviewer | Concern | Root Concept | Response Claim | Revised Grant Evidence | Cross-Document Check | Status | Remaining Action |
|------------------|---------|--------------|----------------|------------------------|----------------------|--------|------------------|

End the audit with:

1. Recurrent patterns across review rounds
2. Concerns fully closed
3. Concerns partially closed or contradicted
4. Exact edits applied
5. Human or external dependencies
6. A fresh canonical-parameter search result
7. A statement of which files, figures, and pages were executed or inspected

## Applying Fixes

After completing the audit:

### Tracked Changes (for fixable issues)

Use the body-swap serialization approach for Word XML manipulation:
1. Parse document.xml with lxml
2. Modify the `<w:body>` element (add `<w:del>` and `<w:ins>` elements)
3. Serialize only the body: `etree.tostring(body, encoding='unicode')`
4. Replace the `<w:body>...</w:body>` region in the original XML string
5. This preserves namespace declarations that lxml would otherwise mangle

For text replacements that span multiple `<w:r>` elements:
- Collect all non-deleted runs, concatenate their text
- Find the match position in the concatenated string
- Map back to affected runs
- Remove affected runs, insert: before-text run + `<w:del>` + `<w:ins>` + after-text run

Use author "Claude (Audit)" and a fixed date for all changes.

### Comments (for judgment calls)

For issues requiring investigator review:
1. Add `<w:commentRangeStart>` before the target paragraph's first run
2. Add `<w:commentRangeEnd>` and `<w:commentReference>` after the last run
3. Add the comment text to `word/comments.xml`
4. Add the author to `word/people.xml` (check namespace prefix — may be `w15:` not `w:`)
5. Escape any `<` or `>` characters in comment text

### Output Checklist

Save the audit results as a markdown checklist file alongside the document. Structure:
- Part A: Traceability matrix (including cross-aim consistency)
- Part B: Cross-reference table
- Part C: Section completeness table
- Part D: Budget alignment table (if budget provided) or cost-implied items list
- Part E: Content issues list with fix status
- Part F: Terminology consistency table
- Part G: Literature-methods alignment table (including evidence quality)

## Quick Reference: What Gets a Tracked Change vs a Comment

| Issue Type | Action |
|-----------|--------|
| Garbled text / splice error | Tracked change |
| Missing space | Tracked change |
| Missing word (grammar) | Tracked change |
| Duplicate fragment | Tracked change (delete duplicate) |
| Abbreviation used before definition | Comment (flag location; author decides where to define) |
| Abbreviation defined but never used | Tracked change (remove definition, use full term) |
| Full term used after abbreviation defined | Tracked change (replace with abbreviation) |
| Abbreviation redefined | Tracked change (remove second definition) |
| Cross-reference broken | Comment (flag with suggested target) |
| Cross-reference vague | Comment (suggest specific section) |
| Empty URL placeholder | Comment (note the stripped URL context) |
| Endpoint definition mismatch between sections | Comment (flag both locations, ask which is canonical) |
| Missing analysis plan for an endpoint | Comment (flag the gap, suggest what's needed) |
| Hypothesis missing for an aim | Comment (flag the aim, note expected location) |
| Literature overclaim | Comment (quote the actual finding from the cited paper) |
| Preprint-based major claim | Comment (note evidence quality concern) |
| Statistical method naming inconsistency | Tracked change (standardize to canonical form) |
| Proper noun misspelling (e.g., Harrel → Harrell) | Tracked change |
| Gene name not italicized | Tracked change (verify in .docx) |
| Gene list inconsistency across aims | Comment (flag both locations, ask for rationale) |
| Person/institution naming inconsistency (minor) | Comment noting canonical form |
| Content duplication across sections | Comment (flag both locations, suggest which to keep) |
| Missing timeline/milestones | Comment (note CIHR expectation) |
| Missing EDI discussion | Comment (note CIHR expectation) |
| Missing adjudication plan for composite endpoint | Comment (flag which endpoints lack adjudication) |

## Quick Reference: Non-RCT vs RCT Audit Differences

| Aspect | RCT Audit | Non-RCT Audit (this skill) |
|--------|-----------|---------------------------|
| Section structure | CIHR mandatory 1.1–3.3 headings | Flexible, aim-based organization |
| Traceability chain | Objective → Endpoint → Analysis | Aim → Hypothesis → Endpoint → Methods → Sample size |
| Sub-aims | Usually not applicable | Common (1A, 1B, 1C); each needs own chain |
| Randomization/blinding | Required sections | N/A |
| DSMB | Required | Typically N/A (no intervention) |
| Intervention description | Required (experimental + control) | N/A |
| Validation strategy | May not apply | Critical for prediction models |
| Pilot data | May be in "Prior work" section | Often a dedicated section |
| Competing risks | May not apply | Frequently relevant (death as competing risk) |
| Design-specific biases | Protocol violations, unblinding | Immortal time, ascertainment, informative censoring |
| AI/ML components | Optional | Common; check architecture, training/test split, baseline comparison |
| Recruitment | Per-arm calculation | Total enrollment with event rate justification |
| Methodology guidelines | CONSORT, SPIRIT | TRIPOD, PROBAST (for prediction models) |
| Timeline | Trial phases/milestones | Year-by-year deliverables |
