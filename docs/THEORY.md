# PDOE v2: first-principles theory audit

## Scientific status

PDOE is a falsification program, not a discovery claim. Version 2 removes two mechanisms that do not actually generate the requested phase redshift and isolates the narrow class of models that remain mathematically relevant.

## 1. Observable definition

For a wave covector `k_mu` and an observer four-velocity `u^mu`, the measured angular frequency is

\[
\omega=-u^\mu k_\mu,
\qquad
1+z=\frac{\omega_{\rm em}}{\omega_{\rm obs}}.
\]

A theory must change this invariant observer-wave relation. Increasing a wavefront's circumference is not enough.

## 2. Standard geometric optics

Use a WKB field

\[
A_\mu=\Re\{(a_\mu+\cdots)e^{iS/\epsilon}\},
\qquad k_\mu=\nabla_\mu S.
\]

At leading order Maxwell theory gives

\[
k^\mu k_\mu=0,
\qquad
k^\nu\nabla_\nu k^\mu=0.
\]

At transport order the beam amplitude responds to optical expansion. Schematically,

\[
\nabla_\mu(\mathcal A^2 k^\mu)=0,
\qquad
\frac{d\ln\mathcal A}{ds}=-\frac{\theta_{\rm opt}}{2}.
\]

Thus beam area and brightness evolve while radial phase spacing remains fixed in flat stationary space.

## 3. Stationary-spacetime no-go statement

Assume:

1. local conservative propagation;
2. a time-independent background/effective metric;
3. a well-defined Hamiltonian `H(x,k)` with no explicit time dependence;
4. no scattering, absorption, stochastic medium, or nonlocal memory.

Hamilton's equation gives

\[
\frac{dk_t}{d\lambda}=-\frac{\partial H}{\partial t}=0.
\]

Equivalently, a stationary timelike Killing field supplies a conserved photon energy. Therefore a cumulative frequency loss depending only on distance cannot occur under these assumptions.

A static-universe PDOE must break at least one assumption by introducing an evolving background, dissipation, a preferred medium/Lorentz violation, or nonlocality.

## 4. Rejected circumference coupling

For beam area `A`,

\[
\theta_{\rm opt}=\frac{1}{A}\frac{dA}{ds}.
\]

The proposed law

\[
\frac{d\ln\lambda}{ds}=\alpha\theta_{\rm opt}
\]

makes redshift depend on focusing, aperture, source geometry, lensing, and an arbitrary launch radius. It is not a universal cosmological law.

## 5. Rejected gauge-kinetic completion

Consider

\[
S_\gamma=-\frac14\int d^4x\sqrt{-g}\,B(\phi)F_{\mu\nu}F^{\mu\nu}.
\]

The modified Maxwell equation is

\[
\nabla_\mu(BF^{\mu\nu})=0.
\]

In geometric optics the leading eikonal equation is still `k^2=0`. The scalar prefactor enters the amplitude transport approximately as

\[
\nabla_\mu(B\mathcal A^2 k^\mu)=0.
\]

It can change intensity, inferred photon number, and the effective fine-structure constant, but it does not supply the desired independent phase/frequency drift at leading order.

## 6. Rejected pure conformal optical metric

A pure optical metric

\[
\tilde g_{\mu\nu}=C(\phi)g_{\mu\nu}
\]

is insufficient. Source-free Maxwell theory in four dimensions is conformally invariant, and conformal transformations preserve the null cone. A conformal factor alone therefore does not create a distinct photon-propagation redshift.

## 7. Retained core branch: disformal scalar-photon coupling

The minimal relevant electromagnetic sector has the structure

\[
\mathcal L_\gamma=-\frac14\left[
\lambda(\phi,X)F_{\mu\nu}F^{\mu\nu}
+\mu(\phi,X)F^\mu{}_{\alpha}F^{\nu\alpha}\phi_\mu\phi_\nu
\right].
\]

Equivalently, photons may propagate in an effective metric

\[
\tilde g_{\mu\nu}=C(\phi,X)g_{\mu\nu}+D(\phi,X)\phi_\mu\phi_\nu.
\]

For homogeneous `phi(t)` in an FRW matter metric,

\[
d\tilde s^2=-(C-D\dot\phi^2)dt^2+C a^2(t)d\mathbf x^2,
\]

and

\[
\frac{c_\gamma^2}{c^2}=1-\frac{D}{C}\dot\phi^2.
\]

The photon frequency scales as

\[
\omega\propto\frac{c_\gamma}{a},
\qquad
1+z_\gamma=\frac{a_{\rm obs}}{a_{\rm em}}
\frac{c_{\gamma,\rm em}}{c_{\gamma,\rm obs}}.
\]

This is an endpoint/evolving-background effect, not a consequence of spherical circumference. In a truly static universe it requires

\[
\frac{c_{\gamma,\rm em}}{c_{\gamma,\rm obs}}=1+z.
\]

That is a large speed evolution: a source at `z=1` requires a factor of two.

## 8. Frontier branch: constitutive/metric-affine optics

A rank-four electromagnetic constitutive tensor can modify the principal symbol of Maxwell's equations and hence the light cone. Current metric-affine work shows that such sectors can also generate birefringence, polarization mixing, intensity anomalies, and departures from photon-number conservation. These are testable signatures, but this branch is more general and less economical than the disformal model.

## 9. Surviving scientific question

The original question is now sharpened:

> Can an evolving, gauge-invariant optical constitutive background reproduce the full cosmological redshift, time dilation, distance duality, BAO geometry, CMB spectrum, and multimessenger propagation while remaining observationally distinct from an expanding metric?

No such successful model has been demonstrated here. Version 2 establishes the equations and no-go boundaries needed to test one honestly.
