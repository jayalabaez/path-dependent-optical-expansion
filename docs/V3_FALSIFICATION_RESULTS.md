# V3 decisive falsification results

## Scope

This audit tests the minimal smooth completion in which matter spacetime is static,
photons propagate through a homogeneous evolving optical index `n(t)`, and
gravitational waves remain on the ordinary matter metric.

The model uses

```
c_gamma = c / n(t),
1 + z = n_obs / n_emit.
```

Choosing the smooth index history that reproduces the local Hubble relation gives

```
n(t) = exp[H0 (t - t0)].
```

For a source observed at redshift `z`, the photon and standard-metric GW travel
times are

```
t_gamma = ln(1+z)/H0,
t_GW    = z/H0.
```

Therefore

```
Delta t = [z - ln(1+z)]/H0.
```

## GW170817 result

Using `z=0.0098` and `H0=70 km s^-1 Mpc^-1`, the model predicts that the photon
signal should arrive about **666,000 years before** the gravitational wave.
GW170817 and GRB 170817A instead arrived only `1.74 +/- 0.05 s` apart.

The effective average photon-speed excess is approximately `4.89e-3`, whereas
the published multimessenger constraint is of order `3e-15` on the relevant
fractional GW-photon speed difference. The smooth photon-only model misses the
bound by more than twelve orders of magnitude.

**Verdict:** the full local cosmological redshift cannot be produced by this
smooth photon-only constitutive background.

Under the additional linearized assumption that a small optical component shares
the same smooth history, GW170817 limits that component to below roughly
`6.1e-13` of the observed local redshift.

## Time dilation

A homogeneous time-varying optical index is not killed by supernova time dilation
alone. Differentiating the null-path integral for adjacent pulses gives

```
dt_obs / dt_emit = n_obs / n_emit = 1+z.
```

So this branch reproduces the observed `(1+z)` event-duration stretch
kinematically.

## Distance duality

In static Euclidean geometry with photon number conserved,

```
D_L = r(1+z),
D_A = r,
eta = D_L / [(1+z)^2 D_A] = 1/(1+z).
```

At `z=1`, this predicts `eta=0.5`, rather than the Etherington value `eta=1`.
The branch is therefore excluded unless the constitutive background also changes
beam focusing and angular geometry.

If focusing is modified exactly enough to restore distance duality, the theory is
functionally an evolving optical metric rather than a simple redshift-in-static-
space mechanism.

## What remains open

1. A universal effective metric shared by photons and gravitational waves.
2. A strongly non-monotonic or impulsive optical history engineered to evade
   integrated speed constraints.
3. A high-redshift-only transition that is negligible over the GW170817 path.
4. A constitutive theory with modified focusing that passes distance duality,
   polarization, CMB, BAO, and standard-siren tests.

These loopholes are not confirmations. They are narrower hypotheses requiring
new actions, stability analysis, and global data fits.
