# CIHR Project Grant: Non-RCT Expected Section Structure

Non-RCT CIHR Project Grants (registry, cohort, prediction model, biobank, AI/technology, observational) do not follow the mandatory RCT heading structure (Sections 1.1–3.3). However, competitive applications consistently include the following content areas, typically organized around Specific Aims.

## Expected Content Areas

### I. Background and Significance

**Purpose**: Establish the knowledge gap and justify why this study is needed.

**Expected content**:
- Burden of disease (Canadian and global epidemiology)
- Current standard of care or current approach
- Specific limitations of current knowledge (quantified where possible)
- Knowledge gaps addressed by this proposal (numbered, each mapping to a Specific Aim)
- Central/overarching hypothesis (explicitly stated)
- How this team/approach is positioned to address the gap

**Quality markers**:
- Canadian data cited prominently
- Own team's prior work referenced
- Knowledge gaps are specific and actionable (not vague)
- Each gap clearly leads to a Specific Aim
- Bold or underlined concluding statement of the central hypothesis

### II. Pilot / Preliminary Data

**Purpose**: Demonstrate that the applicant team has the expertise and data to execute the proposed study.

**Expected content**:
- Prior published work directly supporting feasibility
- Unpublished pilot data from the applicant team
- For registries: enrollment status, event rates, data quality metrics
- For prediction models: preliminary model performance (AUC, C-statistic)
- For AI: proof-of-concept results with architecture details
- Infrastructure already established (platforms, databases, biobanks)

**Quality markers**:
- Pilot data is from the applicant's own team (not just cited literature)
- Statistics are correctly reported (HR, CI, p-values, AUC with CI)
- Sample sizes stated for all pilot analyses
- Pilot population is comparable to proposed study population
- Enrollment trajectory supports feasibility claims

### III. Methods: Shared Infrastructure

**Purpose**: Describe the study design, population, and data collection common to all aims.

**Expected content**:
- Study design statement (prospective, retrospective, ambispective, registry-based)
- Setting (single-center, multi-center, number of sites)
- Inclusion and exclusion criteria (specific, not vague)
- Data collection procedures (eCRF, imaging protocols, biobanking, genomics)
- Core lab procedures (if applicable)
- Recruitment strategy with projected enrollment rates
- Timeline (enrollment period, follow-up duration)

**Quality markers**:
- Inclusion/exclusion criteria are precise and reproducible
- Each exclusion criterion is justified
- Data collection is standardized across sites (same eCRF, same protocols)
- Core lab quality assurance described (inter-observer agreement, reproducibility)
- Recruitment projections based on evidence (prior registry enrollment rates)

### IV–V. Methods: Specific Aims (one section per aim)

**Purpose**: Detail the methods for each Specific Aim.

**Expected content per aim**:
1. **Rationale** (with cited literature supporting the approach)
2. **Hypothesis** (explicitly stated as "We hypothesize that...")
3. **Specific population** (may differ from the overall study population)
4. **Outcomes/Endpoints**:
   - Primary outcome: exact definition, measurement, timing, data source
   - Secondary outcomes: same detail
   - Adjudication plan (if applicable)
5. **Data analysis**:
   - Statistical method (named, specific)
   - Candidate predictors/variables (listed, with justification)
   - Model building strategy (e.g., backward selection, LASSO)
   - Model selection criteria (e.g., AIC, BIC)
   - Discrimination metrics (C-statistic, AUC)
   - Calibration assessment (calibration slope, calibration plot)
   - Internal validation (bootstrapping, cross-validation)
   - External validation (named cohort, what metrics)
   - Missing data handling (multiple imputation, complete case, sensitivity)
   - Competing risks (if applicable: Fine-Gray, cause-specific hazards)
   - Pre-specified subgroups (sex, age, genotype, site)
   - Sensitivity analyses
6. **Sample size / Feasibility**:
   - Events-per-variable calculation (standard: 10 EPV)
   - Assumed event rate (with citation)
   - Required sample size derivation
   - Recruitment timeline showing target is achievable
   - External validation sample size
7. **Expected results and clinical impact**:
   - What deliverables (risk calculator, clinical tool, dataset)
   - How results change practice
   - Dissemination plan (web tool, guidelines, publications)
8. **Potential challenges and mitigation strategies**:
   - Each challenge has a specific mitigation (not vague reassurance)
   - Established collaborations as backup plans
   - Methodological safeguards (sensitivity analyses)

### VI. General Considerations

**Purpose**: Address cross-cutting themes required by CIHR.

**Expected subsections**:

#### Sex and Gender (SGBA+)
- Sex AND gender distinguished (not used interchangeably)
- Sex-stratified analyses in EACH aim (not just overall)
- Gender-specific considerations (access to care, treatment biases)
- Recruitment strategy for balanced enrollment
- Specific sex/gender interaction analyses

#### Patient Engagement
- Named patient partner(s)
- Specific contributions to study design, not just advisory
- Connection to patient organization (with support letter)
- Patient-oriented outcomes identified

#### Knowledge Translation (KT)
- Publication plan (target journals)
- Conference presentations
- Clinical tools (web calculators, apps)
- Guideline integration pathway (name the guideline body)
- Network dissemination (established societies, patient organizations)

#### Data Management and Privacy
- Data storage platform (named)
- De-identification procedures
- Security measures (firewalls, authentication, access control)
- Governance structure (steering committee, data access policies)
- Compliance with privacy legislation (name specific laws)

#### Team and Expertise
- NPA role and time commitment
- Each co-PA and co-A: name, expertise, specific contribution
- Site PIs identified
- Complementary expertise coverage (clinical, methodological, statistical, imaging, genetics, AI, patient engagement)
- Career stage of NPA (early career: additional mentorship described)
- Support letters referenced

#### Equity, Diversity, and Inclusion (EDI)
- Addresses diversity beyond sex/gender: race/ethnicity, socioeconomic status, geographic barriers
- Recruitment strategies for underrepresented populations
- For pan-Canadian studies: consideration of Indigenous communities, TCPS2 Chapter 9
- Acknowledgment of potential barriers to participation

#### Ethics and Regulatory
- REB/IRB approval status at coordinating center
- Multi-site REB harmonization plan
- Consent process described (including waiver of consent for retrospective/deceased, if applicable)
- Privacy law compliance (name specific laws: e.g., Law 25 in Quebec, PIPEDA, provincial equivalents)

#### Timeline and Milestones
- Year-by-year milestones (Year 1, Year 2, Year 3)
- Recruitment targets per year
- Key deliverable dates (model derivation, validation, tool launch)
- Gantt chart or equivalent visualization (recommended)

#### Training Plan
- Trainees named (PhD students, post-doctoral fellows, residents)
- Mentorship structure (who mentors whom)
- Skill development plan (courses, workshops, presentations)
- Career development support

#### Resources
- Existing infrastructure (registries, biobanks, core labs)
- Institutional support (salary, space, equipment)
- Leveraged funding (other grants that complement, not overlap)

## Section Numbering Convention

Non-RCT grants typically use one of:

| Convention | Example |
|-----------|---------|
| Roman numerals | I. Background, II. Pilot Data, III. Methods |
| Arabic with decimals | 1. Background, 1.1 Burden, 1.2 Gaps |
| Aim-based | Background → Pilot Data → Aim 1 → Aim 2 → General Considerations |
| Hybrid | I. Background → III. Methods: Registry → IV. Methods: Aim 1 |

The audit should work with any convention — match to content areas, not heading format.
