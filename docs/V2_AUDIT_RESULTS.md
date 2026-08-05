# Executed v2 audit results

Run date: 2026-08-05

## Numerical checks

- Ordinary spherical wave input wavelength: `1.0`
- Measured mean crest spacing: `1.0000073`
- Crest-spacing numerical standard deviation: `8.65e-4`
- Conclusion: spherical area growth changes the envelope, not the radial wavelength.

- Gauge-kinetic WKB law: `A ∝ B^{-1/2}`
- When `B` doubles from 1 to 2, amplitude falls to `1/sqrt(2) ≈ 0.7071` while the imposed phase wavelength remains fixed.
- Conclusion: the original `B(phi)F^2` action is an amplitude/opacity branch, not a phase-redshift completion.

- Pure conformal photon metric test: `c_gamma/c = 1` for every positive conformal factor.
- Conclusion: a conformal factor alone does not move the photon null cone.

- Disformal benchmark with `q=(D/C) phidot^2=0.1`: `c_gamma/c=sqrt(0.9)=0.9486833`.
- In a static universe, `z=1` requires `c_emit/c_obs=2`.
- Conclusion: the disformal branch can alter photon propagation, but a static explanation demands order-unity historical speed evolution rather than a tiny circumference effect.

## Multimessenger scale

For a persistent photon/graviton fractional speed difference over 40 Mpc:

- `1e-15` gives approximately `4.12 s` delay.
- `1e-9` gives approximately `4.12e6 s` (about 47.7 days).
- `1e-3` gives approximately `4.12e12 s` (about 130,000 years).

This calculation is an order-of-magnitude propagation test. Detailed source-emission delays and models in which photons and gravitational waves share the same effective metric require separate treatment.

## Hubble-curve diagnostic

The best one-parameter static curve against a selected flat-LambdaCDM *benchmark curve* remains

`p = 1.0549179`

with a small shape residual. This is not an observational likelihood and cannot be treated as evidence. The earlier repository overstated the significance of this exercise; v2 labels it explicitly as a degeneracy diagnostic only.

## Automated validation

- `12/12` tests passed.
- Package import passed after editable installation with build isolation disabled in the restricted runtime.

## Final branch verdict

The original theory does not survive in its initial form. The rigorous surviving question is narrower:

> Can a disformal or more general constitutive electromagnetic sector produce a cosmological optical redshift while satisfying time dilation, distance duality, BAO, CMB, polarization, and multimessenger tests, and while remaining observably distinct from an expanding metric?

That question remains open as a research program; no successful model has been obtained in this repository.
