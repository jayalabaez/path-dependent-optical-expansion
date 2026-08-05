# Cosmological Quantum Information Transport (CQIT)

## Scientific status

CQIT is **not a new law of physics**. It is a research framework that combines established results from quantum field theory in curved spacetime, relativistic quantum information, and bosonic channel theory into one falsifiable receiver-level null model.

The standard channel is written schematically as

\[
\mathcal N_{\rm standard}
=\mathcal D_{\rm receiver}\circ\mathcal L_\eta\circ\mathcal U_z.
\]

- \(\mathcal U_z\): coherent redshift-induced dilation or multimode mixing;
- \(\mathcal L_\eta\): geometric, absorptive, and instrumental photon loss;
- \(\mathcal D_{\rm receiver}\): finite bandwidth, mode mismatch, readout noise, and calibration.

The scientific target is not to rediscover redshift. It is to search for a reproducible residual channel

\[
\mathcal N_{\rm observed}
\neq
\mathcal N_{\rm standard}
\]

that survives calibration and independent replication.

## What is already known

1. Realistic finite-bandwidth photons can undergo a unitary redshift transformation represented as multimode mixing.
2. A receiver that remains tuned to the emitted mode can experience severe apparent loss even when a matched receiver could recover the mode.
3. Pure loss reduces accessible classical and quantum communication rates.
4. Cosmological expansion can alter detector-to-detector channel capacities and field-mediated communication.
5. Horizon limits suppress communication asymptotically rather than flattening a wave at a finite edge.

## Potential research contribution

The potentially original part is the integrated software and statistical workflow:

1. infer the expected spectral-temporal dilation;
2. calibrate receiver mode mismatch;
3. infer ordinary transmissivity and noise;
4. test polarization, phase, timing, and entanglement residuals;
5. require multiple independent residuals before escalating a new-physics claim.

A literature search did not establish that this exact integrated diagnostic pipeline already exists. That is **not proof of novelty**. A formal novelty claim requires a systematic review and expert evaluation.

## Candidate observables

- spectral-mode fidelity after optimal redshift compensation;
- polarization-dependent phase or dephasing;
- excess entropy/noise beyond a pure-loss or thermal-loss model;
- violation of redshift composition consistency;
- anomalous entanglement degradation conditioned on successful detection;
- discrepancies between photon, gravitational-wave, and matter-clock channels.

## Discovery standard

One anomalous dataset is insufficient. A credible new-physics case requires:

- pre-registered null and alternative models;
- nuisance-parameter and detector-systematics control;
- look-elsewhere and trials corrections;
- at least two independent observables or experiments;
- external replication;
- a covariant physical model explaining the residual.

## Immediate roadmap

1. Replace synthetic losses with calibrated telescope/satellite link budgets.
2. Implement thermal-loss Gaussian channels and detector dark counts.
3. Add polarization density matrices and entanglement witnesses.
4. Fit real satellite quantum-communication or astronomical photon data.
5. Compare the null model with full QFT-in-curved-spacetime wavepacket calculations.
6. Seek review from relativistic quantum-information specialists before claiming novelty.

## Core literature anchors

- D. E. Bruschi and A. W. Schell, *Gravitational Redshift Induces Quantum Interference*, Annalen der Physik 535, 2200468; arXiv:2109.00728.
- L. A. Alanís Rodríguez, A. W. Schell, and D. E. Bruschi, *Introduction to gravitational redshift of quantum photons propagating in curved spacetime*; arXiv:2303.17412.
- A. Lapponi, O. Luongo, and S. Mancini, *How cosmological expansion affects communication between distant quantum systems*; arXiv:2408.02351.
- D. E. Bruschi, *Limits to the Validity of Gravitational Redshift as a Quantum-optical Multimode Mixer*, International Journal of Theoretical Physics (2026). This work warns that the simplified finite-mode mixer model has a limited small-redshift domain and may require as many auxiliary modes as modeled signal modes.

These references show why CQIT must treat the simple dilation model as a null approximation, not as a complete nonperturbative QFT description at arbitrary cosmological redshift.
