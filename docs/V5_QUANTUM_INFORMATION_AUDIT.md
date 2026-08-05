# V5 Quantum-Information Audit

## Question

Does progressively redshifted and fainter light lose or spread the information encoded in it, and does the electromagnetic wave become flat at the boundary of the observable universe?

## Result

The answer separates into three channels:

1. **Coherent redshift:** a realistic finite-bandwidth photon mode is dilated in frequency and stretched in time. The transformation preserves the mode norm. If polarization carries a qubit and both polarizations undergo the same dilation, the qubit remains pure.
2. **Mode mismatch:** a detector tuned to the emitted frequency may reject the shifted mode. A detector retuned to the received spectrum restores unit ideal mode fidelity. This is inaccessible information caused by a bad measurement basis, not destruction of the global photon state.
3. **Photon loss and noise:** geometric spreading, absorption, detector inefficiency and background noise act as lossy quantum channels. Their communication capacities approach zero as transmissivity approaches zero.

The wave does **not** become exactly flat at any finite redshift. Its observed frequency is

\[
\nu_{\rm obs}=\frac{\nu_{\rm emit}}{1+z}>0
\]

for every finite \(z\). Over a fixed observation interval it may appear nearly constant when fewer than one cycle is sampled. Near an idealized future de Sitter event horizon, redshift diverges and received information rate tends to zero only asymptotically as observer time tends to infinity.

## Test 1: finite-bandwidth photon redshift

For normalized spectral amplitude \(f(\nu)\), define

\[
f_z(\nu)=\sqrt{1+z}\,f[(1+z)\nu].
\]

Then

\[
\int |f_z(\nu)|^2d\nu
=
\int |f(u)|^2du
=1.
\]

The executed Gaussian-mode test preserves normalization to numerical precision. A detector projected onto \(f_z\) has capture probability one. A detector projected onto the unshifted mode \(f\) can have extremely small overlap once the spectrum moves outside its passband.

## Test 2: temporal spreading

Fourier dilation gives

\[
g_z(t)=\frac{1}{\sqrt{1+z}}g\left(\frac{t}{1+z}\right).
\]

Therefore a normalized wavepacket has

\[
\sigma_{t,z}=(1+z)\sigma_{t,0},
\]

while its peak arrival probability density falls as \(1/(1+z)\). The simulation verifies this scaling.

## Test 3: loss-channel capacity

For an ideal bosonic pure-loss channel of transmissivity \(\eta\) and mean input photon number \(N\), the classical capacity is

\[
C=g(\eta N),
\]

where

\[
g(x)=(x+1)\log_2(x+1)-x\log_2x.
\]

Thus \(C\to0\) as \(\eta\to0\). In a single-photon qubit erasure model, classical information is \(\eta\) bits/use and unassisted quantum capacity is

\[
Q=\max(0,2\eta-1).
\]

This demonstrates that faintness can eliminate recoverable communication rate even when each surviving photon retains its conditional encoded state.

## Test 4: finite-window flattening

A detector observing for duration \(T\) contains

\[
N_{\rm cycles}=\frac{\nu_{\rm emit}T}{1+z}
\]

carrier cycles. This is positive for every finite \(z\). For visible light at \(5\times10^{14}\) Hz and a one-second window, one cycle remains until approximately

\[
z\approx5\times10^{14}-1,
\]

far beyond any observed electromagnetic redshift. Optical detectors normally count quanta rather than directly following the optical carrier, making literal visual flattening even less relevant.

## Test 5: cosmological photon count rate

For an isotropic source in flat cosmology, the intercepted photon fraction scales as

\[
\eta_{\rm geo}=\frac{A}{4\pi D_M^2},
\]

and the observed photon count rate includes time dilation:

\[
\dot N_{\rm det}
=
\frac{\dot N_{\rm emit}\eta_{\rm geo}\eta_{\rm detector}}{1+z}.
\]

The simulation shows the accessible image/data rate falling because fewer photons are collected and because arrivals are slowed. Redshifted photon energy contributes an additional factor to received **power**, but not to the number of classical symbols carried by an ideally resolved surviving photon.

## Test 6: event horizon

For a source approaching the latest emission event that can reach an observer in de Sitter spacetime, define \(\epsilon>0\) as the normalized distance from that limiting emission event. Null propagation gives

\[
1+z=\frac{1+\epsilon}{\epsilon},
\qquad
\frac{R_{\rm obs}}{R_{\rm emit}}
=
\frac{\epsilon}{1+\epsilon}.
\]

For every finite \(\epsilon\), frequency and rate remain positive. As \(\epsilon\to0\), the redshift diverges and the rate tends to zero. This is an asymptotic causal-horizon effect, not a material wall where the wave suddenly flattens.

## What has been proved

Within standard coherent wavepacket propagation and standard loss-channel models:

- redshift alone does not erase a finite-bandwidth photon state;
- redshift changes which frequency/temporal mode contains the information;
- an unretuned receiver can mistake mode mismatch for loss;
- actual photon loss reduces classical and quantum communication capacity;
- finite redshift never produces an exactly zero-frequency wave;
- horizon information rate can approach zero asymptotically.

## What has not been proved

This does not prove that information is globally preserved in every realistic cosmological process. Scattering, absorption, gravitational lensing, plasma dispersion, source evolution, detector noise, inaccessible horizon degrees of freedom and quantum gravity can change the relevant channel. The audit also does not establish a new redshift theory; it tests the information content of redshifted light within explicit standard models.
