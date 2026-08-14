12 JONAS STELZIG

2.2. The compact K¨ahler case. An important class of compact manifolds are those admitting a K¨hler metric. This includes all complex submanifolds of projective space.

In this case, the cohomological story greatly simplifies: Roughly speaking, all cohomologies are determined by Dolbeault cohomology. More precisely: Proposition 2.3 (The ∂∂¯-Lemma, [DGMS75]). For any bicomplex A = (A,∂,∂¯), the following assertions are equivalent:

- (1) For any a ∈ A such that ∂a = ∂a¯ = 0 and a = db for some b ∈ A, there exists a c ∈ A such that a = ∂∂c¯ .
- (2) There is an isomorphism A ≅ Asq ⊕ Adot, where Asq is a direct sum of squares, i.e. bicomplexes of the form


- (2.3)

C C

C C,

where all arrows are ±id and all other maps vanish, and Adot is a direct sum of dots, i.e. one-dimensional bicomplexes with all differentials being zero.

- (3) All maps in the diagram

(2.4)

HBC(A)

H∂¯(A) HdR(A) H∂(A)

HA(A) are isomorphisms.

- (4) The spectral sequences in the previous diagram degenerate, and the




filtrations on de Rham cohomology are n-opposed, i.e. bp,qk = 0 unless k = p + q.

Moreover, for a compact K¨ahler manifold X, the bicomplex AX satisfies these conditions.

A complex manifold X for which AX satisfies the above conditions is called a ∂∂¯-manifold. Compact K¨hler manifolds are ∂∂¯-manifolds, but the converse it not true. A broader class is for example given by those manifolds bimeromorphic to compact K¨hler manifolds, i.e. Fujiki’s class C, but also these do not exhaust all ∂∂¯-manifolds, see e.g. [Fri19], [Li24], [KS23a].

One readily checks that all cohomologies introduced above are compatible with direct sums, vanish on squares and are one-dimensional on dots. Thus, as soon as a cohomology allows to reconstruct the information on the position of the dots, e.g. Dolbeault cohomology, or de Rham cohomology

