# Path-Dependent Optical Expansion (PDOE)

Exploratory, falsifiable framework testing whether cosmological redshift could arise from an evolving electromagnetic optical background rather than solely from metric expansion.

## Scientific status

This is a speculative research program, not evidence of a new law of nature.

The investigation rejects several intuitive but incorrect mechanisms:

- ordinary spherical wavefront growth changes amplitude, not radial wavelength;
- direct circumference coupling depends on beam geometry and an arbitrary origin;
- a scalar gauge-kinetic factor `B(phi) F^2` changes amplitude transport but does not produce phase redshift at leading geometric-optics order;
- a purely conformal optical metric does not define a distinct photon light cone in four-dimensional source-free electromagnetism.

The surviving research branch is an evolving disformal or constitutive optical background. It is mathematically open but strongly constrained by supernova time dilation, distance duality, CMB spectral preservation, BAO, polarization, and multimessenger propagation.

## Core no-go result

A local, conservative photon theory in a stationary vacuum conserves the Hamiltonian frequency associated with time-translation symmetry. A genuine distance-only redshift therefore requires at least one of the following: an evolving background, dissipation/scattering, a preferred medium or Lorentz violation, or nonlocal propagation.

## Run

```bash
python -m pip install -r requirements.txt
python run_analysis.py
pytest -q
```

Outputs are written to `results/`.

## Validation

The published version passes **12/12 automated tests**.

## Current conclusion

The original circumference-driven idea is rejected. The only retained core possibility is an evolving disformal/constitutive electromagnetic background, which is no longer a simple consequence of wavefront circumference growth and may be observationally equivalent to an evolving effective geometry unless it produces a distinct multimessenger signature.
