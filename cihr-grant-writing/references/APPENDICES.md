# CIHR Grant Writing Appendices

## APPENDIX A: CIHR-Specific Language and Formatting Tips

1. **Use CIHR vocabulary:** "nominated principal applicant" (not "PI"), "principal applicant" (not "co-PI"), "co-applicant" (not "co-investigator"), "collaborator" (not "consultant")
2. **Sex and gender:** Always separate sex (biological) from gender (social construct); use CIHR SGBA+ framework
3. **Patient engagement:** Use "patient partner" not "patient representative"; reference CIHR Strategy for Patient-Oriented Research (SPOR)
4. **Knowledge translation:** This is CIHR's preferred term over "dissemination" or "implementation"
5. **Indigenous health:** If relevant, reference CIHR Institute of Indigenous Peoples' Health guidelines; use respectful terminology (First Nations, Inuit, Metis Peoples)
6. **Formatting:** Use numbered subsections (1.1, 1.2, etc.); bold/underline key statements; use bullet points for criteria; include figures/tables where possible
7. **Page limits:** Respect CIHR page limits strictly. The research proposal is typically limited to 13 pages for a Project Grant.
8. **References:** Use numbered Vancouver style; cite Canadian data prominently; cite your own team's work

---

## APPENDIX B: Adapting This Template by Study Type

### For Randomized Controlled Trials (PANTHEON model)
- Section 1.3 emphasizes clinical equipoise and treatment gap
- Section 2 uses full trial design subsections (2.1-2.19)
- DSMB is mandatory
- Pilot vs. phase III distinction is critical for objective hierarchy

### For AI/Technology Development Studies (CardioAgent model)
- Section 1.3 emphasizes diagnostic error rates and technology limitations
- Section 2 organizes around Aims (Aim 1: Technical Validation, Aim 2: Clinical Validation, Aim 3: Prospective Evaluation)
- Include a "Pilot Data" section with performance tables (F1, AUROC, sensitivity)
- Address privacy, on-premises deployment, and regulatory pathway (SaMD)
- Include fairness/bias monitoring framework

### For Observational Studies
- Section 1.3 emphasizes knowledge gap from existing observational data limitations
- Section 2 focuses on cohort definition, exposure/outcome definitions, confounding control
- No DSMB required; describe data governance instead
- Address causal inference limitations explicitly

### For Systematic Reviews and Meta-Analyses
- Section 1.3 emphasizes inconsistency in existing evidence
- Section 2 describes search strategy, inclusion/exclusion for studies, risk of bias assessment, synthesis methods
- Register protocol with PROSPERO
- Follow PRISMA guidelines

---

## APPENDIX C: Common Reviewer Critiques and How to Preempt Them

| Common Critique | How to Preempt |
|----------------|----------------|
| "The sample size is inadequate" | For pilot: explicitly state sample size calculation is not applicable and explain why. For confirmatory: provide sensitivity analyses. |
| "The team lacks expertise in X" | Ensure all key expertise areas are covered in Section 3.2; add co-applicants if gaps exist |
| "Sex and gender analysis is superficial" | Integrate SGBA+ at every objective level; collect sex AND gender separately; address non-traditional risk factors |
| "Patient engagement is tokenistic" | Name the patient partner; describe their specific contributions; reference CEPPP or SPOR framework |
| "The comparator is not justified" | Cite guidelines and evidence for comparator choice; acknowledge evidence gaps in comparator arm |
| "Clinical outcomes are not adjudicated" | For pilot: state explicitly that adjudication is not needed and justify. For confirmatory: describe full adjudication plan with central reader model |
| "The study is not feasible" | Provide evidence for recruitment rate; cite similar studies' recruitment; list site capacities |
| "Unclear how results will be used" | State the explicit pipeline: pilot -> phase III -> guidelines; name the guideline body |
| "Relying on AI to evaluate AI is risky" | Describe human adjudication with central reader model; specify sample size for adjudication; use subspecialty core labs |
| "The proposal lacks innovation" | Distinguish from prior work clearly; state what is novel about the approach, population, or endpoint |
| "There is a significant editing error between the summary and the body" | Run the consistency gate (SKILL 5.2). One canonical parameter set, propagated; regenerate every figure |
| "The primary outcome is only evaluated in the subset who receive the test" | Make the denominator all randomized participants; count unascertained outcomes as non-events under ITT (F2) |
| "The chosen window is not in line with current clinical practice" | Anchor the window to a named guideline and cite it; map intervention categories onto guideline actions (F3) |
| "The sample size calculation does not match the primary analysis model" | Compute power under the primary model; show the derivation path so a reader can reproduce N (F4) |
| "This was raised by the previous reviewer but was not adequately addressed" | Track every prior comment to a disposition; where not adopted, say so with reasoning rather than staying silent (5.4) |
| "The model will have convergence issues with so few events per cluster" | Compute events per cluster; use GEE with robust standard errors; report ICC and design effect (F5) |
| "The assumed loss to follow-up appears overoptimistic" | Give the empirical source for the assumption and show the design survives a worse value (F6) |
| "Feasibility of the proposed data linkage has not been shown" | Do not make the primary endpoint depend on it; state access mechanism, granularity, cost, and agreement status; attach letters (F7) |
| "Support letters from participating institutions are absent" | One signed letter per participating institution; start collecting eight weeks out (F8) |
| "Provider behaviour may bias the endpoint since they are unblinded" | Move the endpoint from provider action to objectively ascertained clinical result; blind ascertainment and analysis (F9) |
| "All sites are high-level centres, unclear if it works elsewhere" | Add sites in the target implementation setting; pre-specify a resource-level subgroup with interaction test (F10) |
| "The model's performance data are unpublished" | Publish development and validation before or alongside the trial application; state status honestly (F11) |
| "Knowledge translation is weak given the knowledge users on the grant" | For each named knowledge user, state the action and mechanism, not the venue (F12) |
| "Unclear how the algorithm will actually shorten the pathway" | State the causal mechanism explicitly in one sentence, and quantify the gap it closes with your own data |
| "The same abbreviation is used for two different terms" | Build an abbreviation registry; one expansion per abbreviation across the package |
