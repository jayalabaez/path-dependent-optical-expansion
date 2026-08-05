# V4 Comprehensive Falsification Audit

## Scope and caution

This audit tests classes of optical-redshift theories, not every mathematically
possible model. A failure applies only when the assumptions of the test match
the proposed completion. The audit is designed to prevent a successful
redshift-distance curve from being mistaken for a complete cosmology.

The central question is now narrower than the original idea:

> Can an electromagnetic constitutive background generate cosmological
> redshift without ordinary metric expansion while preserving all measured
> propagation, thermodynamic, geometric, and multimessenger relations?

## Executive verdict

1. **Circumference-driven stretching is falsified.** Ordinary spherical-wave
   spreading changes the amplitude and beam area, not the radial wavelength.
2. **Smooth photon-only optical redshift in static matter spacetime is
   falsified.** GW170817/GRB 170817A excludes the required differential
   propagation by over twelve orders of magnitude.
3. **A constant past radiation bath with redshift acquired only after emission
   is falsified.** The CMB was locally measured to be hotter at redshift 0.89.
4. **Dissipative, scattering, frequency-dependent, massive-photon, and
   gauge-kinetic implementations are independently constrained or excluded.**
5. **The only broadly surviving class is a coherent, achromatic universal
   effective metric shared by photons, gravitational waves, matter clocks, and
   beam focusing.** Operationally, this is an evolving geometry and is no
   longer the original claim that light alone stretches while space remains
   static.

## 1. Physical CMB temperature at redshift 0.89

ALMA molecular absorption measurements give

\[
T_{\rm CMB}(0.89)=5.13\pm0.06\;{\rm K}.
\]

Standard adiabatic evolution predicts

\[
T_0(1+z)=5.151\;{\rm K},
\]

which differs by only `-0.35 sigma`. A static radiation bath remaining at the
present temperature, `2.72548 K`, differs by

\[
40.1\sigma.
\]

The equivalent parameter in

\[
T(z)=T_0(1+z)^{1-\beta}
\]

is

\[
\beta=0.0065\pm0.0184,
\]

consistent with zero.

**Interpretation:** the measurement is local to the absorber epoch. It is not
merely an observation of photons after they later accumulated a redshift. The
past radiation field was physically hotter. A globally evolving optical field
can imitate this scaling, but then photon energies evolve everywhere with
cosmic time; the mechanism is no longer path length or circumference alone.

## 2. CMB spectrum: what fails and what survives

A coherent achromatic effective metric obeying Liouville transport preserves

\[
\frac{I_\nu}{\nu^3}
\]

along rays. The code verifies numerically that a blackbody at
`T_emit=(1+z)T0` maps exactly to a blackbody at `T0`, with RMS numerical residual
below `1e-12`.

This means that the near-perfect CMB blackbody does **not** falsify every
optical-metric theory. It instead strongly constrains mechanisms involving:

- stochastic photon energy loss,
- scattering,
- photon conversion or destruction,
- frequency-dependent refractive evolution,
- incorrect phase-space or arrival-rate transformations.

The updated FIRAS analysis gives `|mu| < 47e-6` at 95% confidence. In the
small-distortion approximation this corresponds to an energy-injection budget
of roughly

\[
\left|\frac{\Delta\rho_\gamma}{\rho_\gamma}\right|
\lesssim 3.35\times10^{-5}
\]

for processes producing a mu distortion.

## 3. BAO radial-versus-transverse geometry

For the static exponential mapping

\[
D(z)=\frac{c}{H_0}\ln(1+z),
\]

the effective radial Hubble factor is

\[
H_{\rm eff}(z)=H_0(1+z).
\]

If the angular distance remains Euclidean, the Alcock-Paczynski combination is

\[
F_{\rm AP}^{\rm static}=(1+z)\ln(1+z).
\]

Compared with a flat `Omega_m=0.3` LCDM reference, the executed differences are
approximately:

- `+5.4%` at `z=0.5`,
- `+1.7%` at `z=1`,
- `-13.2%` at `z=2.33`.

DESI DR2 measures both radial and transverse BAO distances with high precision
using more than 14 million galaxies and quasars. A single static redshift law
cannot independently tune both directions. A rigorous DESI covariance
likelihood remains a next implementation task, but the 5--13% geometric
mismatch identifies the branch as highly implausible given the percent-level
BAO program.

**Likelihood limitation:** v4 does not yet include a full Pantheon+ or DESI
covariance likelihood. The public Pantheon+ distance and covariance products
were located, but the full covariance ingestion was not completed in this
runtime. The present BAO calculation is therefore a geometry diagnostic, not a
published-data parameter fit.

The escape route is to modify angular focusing and area distance as well. That
is precisely an effective optical metric, not a propagation-only energy loss.

## 4. Redshift drift: a future direct sign test

For the smooth optical-index model

\[
n(t)=e^{H_0t},
\]

a fixed source has

\[
\dot z=H_0z.
\]

At `z=3.962`, the model predicts a spectroscopic velocity drift

\[
\dot v_{\rm opt}=+0.0171\;{\rm m\,s^{-1}\,yr^{-1}}.
\]

Flat LCDM with `Omega_m=0.3` predicts

\[
\dot v_{\Lambda{\rm CDM}}=-0.00497\;{\rm m\,s^{-1}\,yr^{-1}}.
\]

The signs differ. The current three-epoch ESPRESSO result is consistent with
zero at roughly `-3.5 +/- 3.6 m/s/yr`, so it is not yet sensitive enough. A
future Sandage-Loeb detection can directly distinguish the models without a
standard candle or ruler.

## 5. Achromaticity and dispersion

GRB 221009A time-of-flight measurements constrain a linear energy-dependent
photon-speed correction with a scale above `5.9 E_Pl` for the subluminal case.
The corresponding allowed fractional speed correction at `1 eV` is only

\[
|\delta v/c|\lesssim1.39\times10^{-29}.
\]

Therefore, any constitutive model that generates cosmological optical redshift
through appreciable frequency-dependent propagation is excluded. A viable
model must be essentially achromatic over radio through TeV photon energies.

## 6. Massive-photon implementation

Well-localized fast radio bursts constrain the photon mass to approximately

\[
m_\gamma<7.1\times10^{-51}\;{\rm kg}
\]

at 2 sigma in the cited 2023 analysis; a 2025 update reports a similar, slightly
tighter one-sigma scale near `4.8e-51 kg`.

At an optical energy of `1 eV`, the 2023 2-sigma bound implies

\[
1-v/c\lesssim7.9\times10^{-30}.
\]

A Proca-like photon mass is therefore far too small to produce the required
cosmological redshift or timing stretch.

## 7. Conditional atomic-clock constraint

The fractional Hubble rate is

\[
H_0\simeq7.16\times10^{-11}\;{\rm yr^{-1}}.
\]

Optical-clock comparisons constrain the present temporal variation of the
fine-structure constant at approximately

\[
\dot\alpha/\alpha=1.0(1.1)\times10^{-18}\;{\rm yr^{-1}}.
\]

If the same scalar responsible for optical redshift changes `alpha` at order
its optical-index evolution, the mismatch is about

\[
6.5\times10^7.
\]

This is **conditional**, not model-independent. A pure disformal change of the
photon cone need not change `alpha`; a gauge-kinetic `B(phi)F^2` completion does,
but that branch already fails as a leading eikonal redshift mechanism.

## 8. Polarization and birefringence

A parity-even disformal optical metric predicts no cosmic polarization
rotation and is compatible with a null result. Parity-odd constitutive terms
can rotate polarization and are directly testable.

ACT DR6 reports a tentative uniform cosmic-birefringence angle near

\[
\beta_{\rm CB}=0.215^\circ\pm0.074^\circ,
\]

but the authors emphasize unresolved instrumental systematics and do not claim
a firm cosmological detection. This is neither confirmation nor decisive
falsification of PDOE. It is a possible independent channel for a specified
parity-odd action.

## 9. Complete survival map

### Falsified

- circumference/beam-area wavelength stretching,
- stationary local conservative distance-only redshift,
- smooth photon-only optical-index Hubble law,
- constant past CMB temperature with post-emission redshift only,
- static Euclidean optical redshift without modified focusing,
- massive-photon cosmological redshift,
- appreciably dispersive optical redshift.

### Strongly constrained

- dissipative/scattering/photon-conversion models,
- gauge-kinetic scalar models that vary `alpha`,
- photon/GW separate metrics or Shapiro delays,
- parity-odd or birefringent constitutive tensors.

### Still mathematically open

- a universal, coherent, achromatic effective metric shared by photons, GWs,
  matter clocks, and area focusing;
- an engineered high-redshift transition screened at the GW170817 epoch;
- a nonlocal theory with a complete unitary and causal construction;
- a full metric-affine constitutive geometry passing hyperbolicity,
  polarization, lensing, BAO, CMB, growth, and early-universe tests.

The first surviving option is operationally an evolving spacetime geometry. It
may be a field redefinition or alternative frame of an expanding-universe
model rather than a physically distinct replacement.

## 10. Tests still required before any approval

No version can be scientifically approved without all of the following:

1. Specify one covariant action, including the matter and gravitational sectors.
2. Prove hyperbolicity, absence of ghosts, causal cones, and a well-posed initial
   value problem.
3. Derive geometric-optics phase, amplitude, polarization, photon-number, and
   focusing equations from that action.
4. Fit Pantheon+, DES-SN5YR, DESI DR2 BAO, CMB anisotropies and lensing with full
   public covariances.
5. Compute recombination, sound horizon, BBN, structure growth, weak lensing,
   and standard-siren predictions.
6. Show a statistically meaningful improvement over LCDM after parameter
   penalties, not merely an equally good curve.
7. Produce a prediction that differs from metric expansion and can be tested
   prospectively, especially redshift drift or messenger-dependent distances.

## Validation

The V4 repository passes **26/26 automated tests** locally. The comprehensive
script writes the survival matrix and diagnostic plots to `results/`.
