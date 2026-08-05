# Cosmological Quantum Information Transport (CQIT)

This repository now focuses on how redshift, photon loss, detector mode mismatch, noise, and horizons affect the **accessible quantum and classical information carried by light**.

The repository retains its historical `path-dependent-optical-expansion` name, but the original PDOE redshift mechanism is archived and falsified. See `docs/ARCHIVED_PDOE.md`.

## Is this new physics?

No. The central ingredients are established physics:

- finite-bandwidth redshift can act as coherent multimode mixing;
- wavepackets stretch in time and shift in frequency;
- photon loss and receiver mismatch reduce accessible channel capacity;
- horizon communication rates can tend to zero asymptotically.

The new research focus is an integrated **null-test framework**. It asks whether real data contain residual decoherence, polarization effects, timing anomalies, or excess noise beyond coherent redshift, ordinary loss, receiver mismatch, and known backgrounds.

## Standard channel

\[
\mathcal N_{\rm standard}
=\mathcal D_{\rm receiver}\circ\mathcal L_\eta\circ\mathcal U_z.
\]

Only a reproducible failure of this calibrated null model could become a candidate for new physics.

## Run

```bash
python -m pip install -e .[test]
pytest
python run_quantum_information_audit.py
python run_cqit_focus.py
```

## Validation

The v6 working tree passes **44 automated tests** locally. GitHub Actions tests Python 3.10 and 3.12.

## Research documents

- `docs/CQIT_RESEARCH_PROGRAM.md` — current focus and discovery standard
- `docs/V5_QUANTUM_INFORMATION_AUDIT.md` — executed redshift/information audit
- `docs/ARCHIVED_PDOE.md` — rejected original hypothesis
