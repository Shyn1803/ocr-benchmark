that, by the assumption in ( 5.26b ),

$$
tn lim sup un (t)dt | to
$$

    which contradicts ( A.10 ) and concludes the assertion.

# APPENDIX B. MEASURE-PRESERVING DIFFEOMORPHISMS

Let ( M,g ) be a smooth connected, orientable Riemannian manifold with Riemannian volume measure vol g . We collect here some auxiliary results about the group Diﬀ + 0 ( g ) of all compactly non-identical, orientation-preserving, vol g -preserving diﬀeomorphisms. +

Firstly, let us recall that Diﬀ 0 ( g ) is the (inﬁnite-dimensional) Lie group corresponding to the Lie algebra of div g -free vector ﬁelds on M with the Lie derivative as its Lie bracket. Let us further recall some virtually well-known results about the natural action of Diﬀ + 0 ( g ) on M . The following may be easily inferred from the arguments in [ 13 , § 3].

Lemma B.1 (Extension lemma) . Let ( M,g ) be in addition open or boundaryless, and K ⊂ M be any contractible compact subset. Then, every smooth vector ﬁeld on K has a compactly supported, div g -free extension to the whole of M .

As an immediate consequence, we see that the Lie algebra of div g -free vector ﬁelds is inﬁnite-dimensional, thus so is Diﬀ + 0 ( g ).

0 on M for every k ∈ N 1 . In particular, it acts transitively on M .

B.1. Actions on measures. In the following, let B 1 ⊂ R d be the open unit ball equipped with the standard Euclidean metric g e .

Lemma B.3. Let ν be any ﬁnite measure on B 1 invariant for the (   ♯ ) -action of Diﬀ + 0 ( g e ) . Then ν ∝ L d   B 1 . In particular, ν has no singular continuous part.

Proof. Let Q 1 ,Q 2 ⊂ B 1 be arbitrary closed cubes with equal volume, deﬁne K as the closed convex hull of Q 1 ∪ Q 2 , and let w be the vector ﬁeld on K deﬁning the translation of Q 1 to Q 2 . By Lemma B.1 applied to K and w , there exists a compactly supported div g e -free vector ﬁeld w ′ on M extending w on K . Then, the ﬂow of w ′ at time 1 is a compactly non-identical orientation-preserving, L d preserving diﬀeomorphism on M mapping Q 1 to Q 2 . In other words, Diﬀ + 0 ( g e ) acts transitively on all closed cubes in B 1 , hence, by continuity, on the family C of all semi-closed cubes Q of the form Q : = x + q [0 , 1) d with x ∈ R d , q ∈ Q + and such that Q ⊂ B 1 .

Since ν is invariant, by a standard decomposition argument, for every rational q ∈ Q + and every Q ∈ C with qQ ∈ C we have ν ( qQ ) = q d νQ . Now, let Q 0 ∈ C be ﬁxed, and set c : = νQ 0 / L d Q 0 . For every Q 1 ∈ C there exists q ∈ Q + and x ∈ R d so that Q 1 = x + qQ 0 . For such q , by invariance of ν and of L d (also under rescaling),

$$
vQ1 '(qQo) = csd (
$$

Since C is a π -system generating the Borel σ -algebra of B 1 , it follows by a standard monotone class argument that ν = c L d as Borel measures on B 1 , which concludes the proof.  

