# Cancer research roadmap: evidence before claims

This plan is the research track for GoodbyeCancer. It prioritizes reproducible, narrowly scoped questions over broad claims of a cure.

## Workstream A — numerical verification (implemented)

- Toy logistic ODE integrated with RK4.
- Compare numerical solution to analytical reference.
- Automated tests and CI smoke artifact.
- Interpretation is explicitly limited to numerical software verification.

## Workstream B — genomic evidence pipeline (next)

1. Define one concrete cancer-biology question and the relevant cancer type/cell context before selecting a model.
2. Record each model's training domain, context window, output semantics, and known limitations.
3. Use public reference data with stable identifiers, licenses, provenance, and versioned preprocessing.
4. Split training/calibration and evaluation data to avoid leakage; where possible, validate on independent datasets and cell contexts.
5. Report uncertainty, calibration, baselines, negative controls, and failure cases—not only best-case scores.
6. Keep sequence-derived model scores as hypothesis-generating signals until independently supported by experimental evidence.

## Workstream C — mechanistic simulation

Only after a cancer-specific question and data are selected, add a model of the relevant mechanism (for example, pathway dynamics or tumor–microenvironment interactions). Define state variables, assumptions, parameter sources, units, solver, and sensitivity analysis. Do not treat a generic growth curve as tumor biology.

## Acceptance gates

- **Reproducible:** fixed model/data versions, parameters, environment, and machine-readable output.
- **Numerically verified:** solver/reference checks and convergence tests pass.
- **Biologically evaluated:** comparison against appropriate external experimental data with uncertainty and limitations documented.
- **Clinically unproven unless separately demonstrated:** computational performance alone cannot support treatment recommendations or claims of patient benefit.

## Scope boundary

This repository is a research and engineering tool. It is not a diagnostic device, treatment recommender, or substitute for qualified medical care. No model output here should be used to make decisions about an individual patient's care.
