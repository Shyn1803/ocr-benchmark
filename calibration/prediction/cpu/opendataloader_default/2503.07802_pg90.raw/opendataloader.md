90 LORENZO DELLO SCHIAVO AND GIACOMO ENRICO SODINI

so that, by the assumption in (5.26b),

2

tn

Γ(θ − 1)t10−θ Eθ(un) = 0 , which contradicts (A.10) and concludes the assertion.

u′n(t)dt

≤ limsup

limsup

n

n

t0

Appendix B. Measure-preserving diffeomorphisms

Let (M,g) be a smooth connected, orientable Riemannian manifold with Riemannian volume measure volg. We collect here some auxiliary results about the group Diﬀ+0 (g) of all compactly non-identical, orientation-preserving, volg-preserving diﬀeomorphisms.

Firstly, let us recall that Diﬀ+0 (g) is the (inﬁnite-dimensional) Lie group corresponding to the Lie algebra of divg-free vector ﬁelds on M with the Lie derivative as its Lie bracket. Let us further recall some virtually well-known results about the

natural action of Diﬀ+0 (g) on M. The following may be easily inferred from the arguments in [13, §3].

Lemma B.1 (Extension lemma). Let (M,g) be in addition open or boundaryless, and K ⊂ M be any contractible compact subset. Then, every smooth vector ﬁeld on K has a compactly supported, divg-free extension to the whole of M.

As an immediate consequence, we see that the Lie algebra of divg-free vector ﬁelds is inﬁnite-dimensional, thus so is Diﬀ+0 (g). Proposition B.2 (Transitivity, [13, Thm. A, §3, p. 98]). Diﬀ+0 (g) acts k-transitively on M for every k ∈ N1. In particular, it acts transitively on M.

B.1. Actions on measures. In the following, let B1 ⊂ Rd be the open unit ball equipped with the standard Euclidean metric ge.

Lemma B.3. Let ν be any ﬁnite measure on B1 invariant for the ( ♯)-action of Diﬀ+0 (ge). Then ν ∝ L d B

. In particular, ν has no singular continuous part.

1

Proof. Let Q1,Q2 ⊂ B1 be arbitrary closed cubes with equal volume, deﬁne K as the closed convex hull of Q1 ∪ Q2, and let w be the vector ﬁeld on K deﬁning the translation of Q1 to Q2. By Lemma B.1 applied to K and w, there exists a compactly supported divg

-free vector ﬁeld w′ on M extending w on K. Then, the ﬂow of w′ at time 1 is a compactly non-identical orientation-preserving, L dpreserving diﬀeomorphism on M mapping Q1 to Q2. In other words, Diﬀ+0 (ge) acts transitively on all closed cubes in B1, hence, by continuity, on the family C of all semi-closed cubes Q of the form Q := x + q [0,1)d with x ∈ Rd, q ∈ Q+ and such that Q ⊂ B1.

e

![](<2503.07802_pg90_images/imageFile1.png>)

Since ν is invariant, by a standard decomposition argument, for every rational q ∈ Q+ and every Q ∈ C with qQ ∈ C we have ν(qQ) = qdνQ. Now, let Q0 ∈ C be ﬁxed, and set c := νQ0/L dQ0. For every Q1 ∈ C there exists q ∈ Q+ and x ∈ Rd so that Q1 = x+qQ0. For such q, by invariance of ν and of L d (also under rescaling), νQ1 = ν(qQ0) = qdνQ0 = qdcL dQ0 = cL d(qQ0) = cL dQ1 .

Since C is a π-system generating the Borel σ-algebra of B1, it follows by a standard monotone class argument that ν = cL d as Borel measures on B1, which concludes the proof.

