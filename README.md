# GoodbyeCancer — reproducible cancer-simulation research

**Status: research prototype; not a diagnostic or treatment system.**

This repository starts a falsifiable, reproducible computational research track for cancer biology. The first model is deliberately small: a logistic growth ODE used to verify numerical integration, time-step convergence, parameter validation, and machine-readable run records before adding real biological complexity.

## What this prototype can and cannot say

- It demonstrates a software workflow for running and checking a toy growth model.
- It does **not** model an individual patient, a specific cancer subtype, tumor heterogeneity, immune response, metastasis, or treatment efficacy.
- It does **not** establish a cure, recommend treatment, or substitute for experimental/clinical evidence.
- Simulated time is a model variable. Advancing it faster than wall-clock time does not make biology in the real world run faster.

## Model

For normalized burden (x(t)), intrinsic growth rate (r), and carrying capacity (K):

`dx/dt = r x (1 - x/K)`

For (r > 0), (K > 0), and (x(0) > 0), the analytical solution is:

`x(t) = K / (1 + ((K - x0) / x0) exp(-r t))`

The prototype integrates with classical fourth-order Runge–Kutta (RK4), then compares its result with the analytical solution. This is a numerical verification benchmark—not a validated tumor biology model.

## Run locally (Python 3.10+)

```bash
python -m unittest discover -s tests -v
python -m src.simulate --duration 10 --dt 0.1 --output results/run.json
```

No third-party packages or network access are required.

## Reproducibility contract

Each run records model name, parameters, time step, simulated duration, final simulated state, analytic reference, absolute error, and solver metadata. Tests enforce input constraints, positivity/bounds for the reference case, and convergence as the time step is refined.

## Roadmap

1. Establish the numerical baseline and automated tests.
2. Add versioned, published reference datasets and documented provenance.
3. Add cancer-relevant models only with clear assumptions, calibrated parameters, uncertainty analysis, and external validation.
4. Keep hypothesis generation separate from any clinical decision-making.

## Research integrity

A passing test means the stated software properties passed. It does not mean the model predicts real cancer outcomes. Every future model must state its biological scope, evidence source, validation target, known failure modes, and intended use.
