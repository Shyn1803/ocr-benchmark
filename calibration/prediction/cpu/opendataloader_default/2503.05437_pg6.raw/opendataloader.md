with arbitrary λ and arbitrary coefficients ci. They satisfy

u ∈ Hs(Ω), p ∈ Hs−1(Ω) ∀s < 1 + λ, and the parameter λ can be chosen such that the test example has the desired regularity.

# 3.2 Boundary conditions

- As in Subsection 2.2, the coefficients ci and the parameter λ can be used to satisfy homogeneous boundary conditions. Two boundary conditions for both θ = 0 and θ = ω give a homogeneous linear system of 4 equations which has a non-trivial solution iff the determinant vanishes. This condition is used to find again a countable number of values of λ. Let us sketch this approach for the case of Dirichlet boundary conditions and λ ̸= 0.

The condition U(0) = 0 leads to

Ur(0) Uθ(0)

=

c1 + (1 − λ)c3 c2 + (1 + λ)c4

=

0 0

, i.e.

c1 c2

= −(1 − λ)c3 −(1 + λ)c4

,

hence

U(ω) = −(1 − λ)c3U(1)(ω) − (1 + λ)c4U(2)(ω) + c3U(3)(ω) + c4U(4)(ω). The 2 × 2 linear system U(ω) = 0 for the coefficients c3 and c4 has the determinant 4(sin2 λω − λ2 sin2 ω) = 4(sinλω − λsinω)(sinλω + λsinω). (3.2)

This means that for given angle ω one gets the corresponding exponents λ ∈ C by solving (separately) the two transcendental, scalar equations sinλω = ±λsinω. All values Reλ ∈ [21,4] are given for ωk = kπ/10, k = 4,5,...,20, in [Dau89].

3.3 Weak and very weak solutions

- As in Subsection 2.3, the pair (u,p) is a weak solution for λ > 0 and a very weak solution for −min(1,ξ) < λ ≤ 0, where


ξ = min{Reλ > 0: λ satisfies (3.2)}

in the case of Dirichlet boundary conditions. The weak solution (u,p) ∈ H1(Ω) × L20(Ω) is defined by

(∇u,∇v) − (∇ · v,p) = 0 ∀v ∈ H01(Ω), (∇ · u,q) = 0 ∀q ∈ L20(Ω).

The very weak solution (y,p) ∈ L2(Ω)×P′ with P = {v ∈ H1(Ω)∩L20(Ω) : r−1v ∈ L2(Ω)} is defined by

(u,−∆v + ∇q) − (∇ · v,p) = ⟨u,qn − ∂nv⟩Γ ∀(v,q) ∈ V where V := {(v,q) ∈ H01(Ω) × L20(Ω): − ∆v + ∇q ∈ L2(Ω),∇ · v ∈ P}, see [ALP24].

6

