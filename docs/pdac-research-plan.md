# PDAC research plan — dataset-first model development

**Status:** numerical baseline implemented; GEO series-level provenance audit started. No biological model has yet been calibrated to these datasets.

## Research question

Can patient-derived PDAC organoid response heterogeneity be quantified from measured growth/response phenotypes, and can baseline molecular features explain a reproducible fraction of that variation?

The first target is **in-vitro organoid response**, not an individual patient's tumor or clinical outcome. Patient-level translation is a separate validation problem.

## Verified data distinctions

The machine-readable source registry is `data/pdac_datasets.json`. Current series-level checks establish:

- **GSE235548** — 30 GEO RNA-seq samples across eight patient-derived organoid lines; the GEO record lists baseline and a subset exposed to gemcitabine plus paclitaxel. The study reports image-derived response and single-organoid heterogeneity metrics. GEO's expression files are not themselves a complete longitudinal response matrix. The publication supplements and exact GSM-to-organoid/response mapping must be recovered before fitting.
- **GSE169321** — 20 transcriptomic samples representing ten matched primary-tissue/organoid pairs: five treatment-naive and five after neoadjuvant FOLFIRINOX. GEO provides TPM and raw-count matrices. The paper describes organoid sensitivity assays to 5-FU, irinotecan, and oxaliplatin, but the assay phenotype table is not present as a GEO expression matrix; recover it separately and map it to organoid IDs.
- **GSE186960** — six PANC-1 cell-line/resistant-derivative single-cell samples. Use as a mechanistic stress-test only, never as a patient-derived organoid calibration cohort.
- **GSE297770** — five control 3D-organoid RNA-seq samples in GEO. Although the associated publication reports drug-sensitivity experiments, the GEO series itself does not list treatment-arm RNA-seq or response labels. Treat as transcriptomic context until publication phenotype tables are recovered and linked.
- **phs001611.v1.p1** — published 66-organoid pharmacotyping cohort with access restrictions for some data and a small matched clinical subset. Access, data files, and endpoint definitions require separate verification.

Series-level metadata checks are not a complete sample-level audit. Never infer a response label from gene expression, sample title alone, or the publication's narrative. All sample-to-organoid, treatment, dose, timepoint, replicate, and assay links must be explicit.

## First falsifiable hypothesis

**Hypothesis H1:** among patient-derived PDAC organoid lines exposed to the same regimen and assay conditions, measured response distributions differ materially between organoid lines and within individual lines; baseline transcriptomic features may explain some between-line variation, but will not be treated as a validated predictor unless performance survives leave-one-organoid-line-out validation.

Pre-register the response endpoint and direction before analysis. Prefer the study's validated growth-rate normalized response metric if its definition and raw/processed values can be recovered. Otherwise use the exact published endpoint (e.g. AUC) without converting it into IC50 or growth rate. Do not combine Gem-Pac and FOLFIRINOX drug assays as interchangeable treatments.

## Modeling sequence

### Phase 0 — numerical baseline

The existing logistic ODE and RK4 implementation is a numerical-methods baseline only. It does not represent PDAC biology.

### Phase 1 — data provenance and sample manifest

1. Retrieve GEO SOFT/MINiML metadata and supplementary files for GSE235548 and GSE169321.
2. Retrieve the publication supplements containing image-derived response metrics / organoid drug sensitivity.
3. Build one row per measurement, not merely one row per RNA-seq sample. Include GSM, organoid line, patient-level group ID (pseudonymized), treatment, drug, dose, exposure duration, assay type, replicate, endpoint, unit, source file, source row, retrieval date, and SHA-256.
4. Preserve raw source files; derive versioned analysis tables.
5. Fail closed on missing/ambiguous mappings, conflicting labels, duplicate measurements, and unknown units.
6. Keep all observations from one patient/organoid line in one validation fold.

### Phase 2 — descriptive and statistical baseline

- Plot measured response distributions by organoid line, treatment, dose, and replicate.
- Quantify within-line and between-line variation using a hierarchical model or variance decomposition.
- Report replicate reliability and assay-specific missingness.
- If only a small number of independent organoid lines is available, report effect estimates and uncertainty; do not train a high-dimensional ML predictor.
- Establish simple baselines before any transcriptome model.

### Phase 3 — candidate mechanistic model

Only if compatible time-course or dose-response observations exist, evaluate a two-compartment in-vitro model:

`dS/dt = r_S S(1-(S+R)/K) - k_S(D)S`

`dR/dt = r_R R(1-(S+R)/K) - k_R(D)R`

where `S` and `R` are operationally defined sensitive and resistant in-vitro subpopulations, `D` is measured drug exposure, and kill terms are fitted only to measured response data. This is a candidate phenomenological model, not an established PDAC mechanism. It cannot establish clonal lineage, molecular mechanism, or patient response without independent experiments.

### Phase 4 — validation

- Hold out entire organoid lines/patients, not random technical replicates.
- Use study-held-out validation only after assay and endpoint harmonization.
- Report RMSE/MAE for continuous endpoints, rank correlation for ranking, calibration, uncertainty intervals, negative controls, and failure cases.
- Keep retrospective clinical associations separate from in-vitro prediction; association does not establish treatment benefit.

## Explicit exclusions

- No patient-specific prediction or treatment recommendation.
- No claims of tumor shrinkage, cure, or clinical efficacy from a toy ODE.
- No pooling cell-line, organoid, tissue, and patient outcomes as if they were interchangeable.
- No fitting until response labels, units, sample mappings, and assay conditions are verified.

## Immediate next executable task

Recover the publication supplement phenotype tables for GSE235548 and GSE169321, create a checksummed sample/measurement manifest, and independently validate every mapping against the GEO SOFT/MINiML records. Then decide whether the available independent organoid count supports a statistical response analysis; do not start model training prematurely.
