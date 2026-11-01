# PDAC research plan — dataset-first model development

**Status:** evidence inventory created; no biological model has yet been calibrated to these datasets.

## Research question

Can a reproducible, low-dimensional tumor-burden model capture treatment-associated growth suppression and resistant-subpopulation behavior in pancreatic ductal adenocarcinoma (PDAC) organoid experiments?

The first target is **in-vitro organoid response**, not an individual patient's tumor or clinical outcome. A separate translational validation stage is required before any patient-level interpretation.

## Evidence inventory

The machine-readable source registry is `data/pdac_datasets.json`. The initial candidates are:

- **GSE235548** — eight PDAC organoid lines, baseline and a subset treated with gemcitabine plus paclitaxel; includes transcriptomic and single-organoid response/heterogeneity analysis. The 30 GEO samples must be mapped by sample accession before fitting.
- **GSE169321** — ten organoid lines and 20 tissue/organoid transcriptomic samples; includes neoadjuvant FOLFIRINOX context and in-vitro sensitivity assays for 5-FU, irinotecan, and oxaliplatin.
- **GSE186960** — PANC-1 gemcitabine exposure/acquired-resistance single-cell model; use only as a mechanistic stress test.
- **GSE297770** — a candidate independent 3D organoid dataset; phenotype and sample mapping still need auditing.
- **phs001611.v1.p1** — a high-value published 66-organoid pharmacotyping cohort, with access restrictions for some data and only a small matched clinical follow-up subset.

These sources have different experimental units and cannot be pooled naively. Cell lines, patient-derived organoids, primary tissues, and clinical outcomes must remain separately labeled.

## Modeling sequence

### Phase 0 — existing numerical baseline

The repository's logistic ODE and RK4 implementation is a numerical-methods baseline only. It does not represent PDAC biology and must not be relabeled as a cancer-specific model.

### Phase 1 — data ingestion and provenance

1. Download only public processed files initially.
2. Save original files unchanged under a documented data policy; do not commit large raw sequencing files.
3. Record retrieval metadata and SHA-256 checksums.
4. Build sample manifests from GEO sample accessions and the associated publication supplements.
5. Verify treatment, dose, timepoint, organoid line, replicate, and assay columns before modeling.
6. Fail closed on missing or ambiguous sample-to-treatment mappings.

### Phase 2 — quantitative response baselines

Before adding a mechanistic model, compute and report:
- untreated-versus-treated growth/response contrasts where longitudinal measurements exist;
- dose-response summaries and normalized AUC/IC50 only where the original phenotype data support them;
- replicate variability and organoid-to-organoid heterogeneity;
- simple baseline predictors with patient/organoid-level held-out splits.

Transcriptomic expression by itself is not a measured drug response. Do not infer IC50 or growth rates from expression matrices without a separately validated model.

### Phase 3 — candidate mechanistic model

Only if compatible time-course or dose-response observations are available, evaluate a two-compartment model:

`dS/dt = r_S S(1-(S+R)/K) - k_S(D)S`

`dR/dt = r_R R(1-(S+R)/K) - k_R(D)R`

where `S` and `R` represent sensitive and resistant in-vitro subpopulations, `D` is measured drug exposure, and drug-kill terms are fitted only to observed response data. This is a candidate hypothesis, not an established PDAC mechanism. Parameters must have units, provenance, confidence intervals, and sensitivity analysis.

### Phase 4 — validation

- Fit on selected organoid lines and evaluate on held-out organoid lines.
- Test transfer to an independent dataset only after harmonizing assay, drug, dose, and endpoint definitions.
- Report RMSE/MAE for continuous outcomes, rank correlation for response ranking, uncertainty intervals, calibration, negative controls, and failure cases.
- Keep clinical cohort analyses separate and exploratory; retrospective associations do not establish treatment benefit.

## Explicit exclusions

- No patient-specific prediction or treatment recommendation.
- No claims of tumor shrinkage, cure, or clinical efficacy from a toy ODE.
- No mixing of cell-line and organoid measurements as if they were interchangeable.
- No model fitting until sample-level metadata and response endpoints are verified.

## Current next executable task

Retrieve and checksum the processed supplementary files for GSE235548 and GSE169321, then create a sample manifest that links each GEO sample accession to organoid line, treatment, dose/timepoint, replicate, and data file. This is the gate before biological model implementation.
