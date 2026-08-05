# Path-Dependent Optical Expansion (PDOE)

Exploratory, falsifiable framework testing whether cosmological redshift could arise from a universal optical scaling field rather than solely from metric expansion.

## Scientific status

This is a speculative research program, not evidence of a new law of nature. The direct circumference-only mechanism is rejected: ordinary spherical spreading changes amplitude, not radial wavelength. The retained candidate is a covariant path-dependent optical scaling law.

## Minimal phenomenology

\[
\frac{d\ln\omega}{ds}=-\Gamma,\qquad
1+z=\exp\left(\int \Gamma\,ds\right).
\]

A viable model must also reproduce event time dilation, distance duality, achromatic propagation, image sharpness, CMB spectral preservation, and multimessenger constraints.

## Run

```bash
python -m pip install -r requirements.txt
python run_analysis.py
pytest -q
```

Outputs are written to `results/`.

## Current conclusion

- Ordinary spherical-wave expansion: no wavelength growth.
- Beam-expansion coupling `Gamma = alpha theta_opt`: fails source/beam-geometry independence.
- Universal optical-scaling field: mathematically testable but not yet distinct from an effective expanding geometry.

## V3 decisive falsification

The minimal smooth **photon-only** static optical-redshift completion is now
falsified by GW170817. At the host redshift `z≈0.0098`, it predicts photons would
arrive about 666,000 years before a gravitational wave traveling on the ordinary
matter metric; the observed gamma-ray lag was only about 1.74 seconds. The
static Euclidean branch also predicts a distance-duality factor
`eta=1/(1+z)` instead of `eta=1`.

The only remaining loopholes require photons and GWs to share the same evolving
effective metric, an engineered non-monotonic/high-redshift transition, or a
constitutive geometry that also changes beam focusing. These are open research
possibilities, not validated explanations.

Run:

```bash
python run_falsification.py
pytest -q
```

## V4 comprehensive audit

The repository tests the surviving model classes against the physical CMB
temperature history, blackbody phase-space transport, FIRAS spectral
distortions, BAO radial/transverse geometry, redshift drift, GRB dispersion,
FRB photon-mass limits, atomic-clock drift, and polarization.

The scientific classification is:

- photon-only static-space explanations: falsified;
- dissipative, dispersive, massive-photon, and gauge-kinetic variants: excluded
  or strongly constrained;
- universal coherent achromatic effective metric: mathematically open, but no
  longer physically distinct from an evolving geometry without an additional
  observable prediction.

Run:

```bash
python run_comprehensive_audit.py
pytest -q
```

See `docs/V4_COMPREHENSIVE_AUDIT.md`.

## V5 quantum-information audit

V5 separates coherent redshift from detector mismatch and photon loss. A finite-bandwidth photon mode is coherently dilated in frequency and stretched in time while preserving its norm and any independently encoded polarization qubit. A detector left at the emitted frequency can miss the photon, but a matched detector recovers unit mode fidelity. Geometric loss and noise reduce channel capacity toward zero.

The electromagnetic wave does not become exactly flat at any finite redshift. Near a future event horizon, observable frequency and information rate approach zero only asymptotically.

The full suite passes **35/35 software tests**. This validates the calculations and code paths, not a new cosmological theory.

Run:

```bash
python run_quantum_information_audit.py
pytest -q
```

See `docs/V5_QUANTUM_INFORMATION_AUDIT.md`.
