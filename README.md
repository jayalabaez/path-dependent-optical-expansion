# Cosmological Quantum Information Transport (CQIT)

This repository studies how redshift, photon loss, detector mismatch, noise, and horizons affect the information carried by light. It also maintains executable falsification tests for proposed alternatives to cosmological expansion.

The historical repository name is `path-dependent-optical-expansion`. The original circumference-driven PDOE mechanism is archived and falsified in `docs/ARCHIVED_PDOE.md`.

## Current v7 result

The newest audit tests the stationary continuous-loss law

\[
\frac{dE}{dr}=-\frac{H_0}{c}E,
\qquad
1+z=\exp(H_0r/c),
\]

with photon speed kept equal to `c`.

The pure model is **falsified** by five independent observational gates:

- DES Type Ia supernova time dilation;
- the physical CMB temperature at `z=0.89`;
- cosmic distance duality;
- distance duality even after adding an engineered pulse stretch;
- radial-versus-transverse BAO geometry.

A stochastic collision implementation is additionally forced into an extreme coherent limit: at `z=1`, ESPRESSO-like resolving power requires roughly `9.4×10^9` microscopic events with per-event logarithmic loss below `7.4×10^-11`.

The only broad escape is to modify pulse timing, radiation temperature, angular focusing, clocks, and rulers together. Operationally that becomes an evolving effective metric cosmology rather than simple tired light.

## CQIT null model

The information-transport program remains

\[
\mathcal N_{\rm standard}
=\mathcal D_{\rm receiver}\circ\mathcal L_\eta\circ\mathcal U_z.
\]

Only a reproducible residual beyond coherent redshift, ordinary loss, receiver mismatch, and known backgrounds could become a candidate for new physics.

## Run

```bash
python -m pip install -e .[test]
pytest
python run_quantum_information_audit.py
python run_cqit_focus.py
python run_continuous_loss_audit.py
```

## Validation

Before publication, v7 passed **12/12 new focused tests locally**. GitHub Actions runs the complete repository suite and every analysis script on Python 3.10 and 3.12.

## Research documents

- `docs/V7_CONTINUOUS_LOSS_FALSIFICATION.md` — new energy-loss theory audit
- `docs/CQIT_RESEARCH_PROGRAM.md` — current information-transport null tests
- `docs/V5_QUANTUM_INFORMATION_AUDIT.md` — redshift and quantum-information audit
- `docs/ARCHIVED_PDOE.md` — rejected original circumference hypothesis
