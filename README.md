# Path-Dependent Optical Expansion (PDOE)

Exploratory, falsifiable framework testing whether cosmological redshift could arise from an evolving electromagnetic optical background rather than solely from metric expansion.

## Scientific status

This is a speculative research program, not evidence of a new law of nature.

The investigation rejects several intuitive but incorrect mechanisms:

- ordinary spherical wavefront growth changes amplitude, not radial wavelength;
- direct circumference coupling depends on beam geometry and an arbitrary origin;
- a scalar gauge-kinetic factor `B(phi) F^2` changes amplitude transport but does not produce phase redshift at leading geometric-optics order;
- a purely conformal optical metric does not define a distinct photon light cone in four-dimensional source-free electromagnetism.

The retained research space is an evolving disformal or constitutive optical background. It is strongly constrained and must not be described as a confirmed explanation.

## Core no-go result

A local, conservative photon theory in a stationary vacuum conserves the Hamiltonian frequency associated with time-translation symmetry. A genuine distance-only redshift therefore requires at least one of the following: an evolving background, dissipation/scattering, a preferred medium or Lorentz violation, or nonlocal propagation.

## V3 decisive falsification

The minimal smooth **photon-only** static optical-redshift completion is falsified by GW170817.

For a homogeneous index history that reproduces the local Hubble relation,

```text
n(t) = exp[H0(t-t0)]
t_gamma = ln(1+z)/H0
t_GW = z/H0
```

At the GW170817 host redshift `z≈0.0098`, this predicts photons would arrive about **666,000 years before** a gravitational wave traveling on the ordinary matter metric. GRB 170817A was observed only about **1.74 seconds after** GW170817.

The effective average photon-speed excess is approximately `4.89e-3`, exceeding the relevant multimessenger bound used in the audit by more than `10^12`. Under an additional smooth small-contribution assumption, the local photon-only optical fraction is constrained below roughly `6.1e-13` of the observed redshift.

The static Euclidean branch also predicts

```text
eta = D_L / [(1+z)^2 D_A] = 1/(1+z)
```

instead of the Etherington value `eta=1`. At `z=1`, its prediction is `eta=0.5`.

## What remains open

- a universal effective metric shared by photons and gravitational waves;
- a highly non-monotonic or impulsive optical history;
- a high-redshift-only transition negligible along the GW170817 path;
- a constitutive geometry that also changes beam focusing and passes distance duality, polarization, CMB, BAO, and standard-siren tests.

These loopholes are not confirmations. If photons and gravitational waves share the same evolving geometry, the proposal is no longer a photon-specific alternative and may be operationally equivalent to metric evolution.

## Run

```bash
python -m pip install -r requirements.txt
python run_analysis.py
python run_falsification.py
pytest -q
```

Outputs are written to `results/`.

## Validation

Version 0.3.0 passes **17/17 automated tests** locally. GitHub Actions tests Python 3.10 and 3.12.
