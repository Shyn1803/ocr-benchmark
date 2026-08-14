Lemma 8.1.6. Suppose ℓ = 2 and (ℓ,n!) = 1 if we are in case O1. If φ ∈ Φss(G∗,Fℓ) is a generic semi-simple toral L-parameter, and µ ∈ X•(G∗) is a dominant cocharacter, then φ is µ-regular.

![](<2503.04623_pg54_images/imageFile1.png>)

Similarly, if φ♯ ∈ Φss(G♯,Fℓ) is a generic semi-simple toral L-parameter, and µ♯ ∈ X•(G♯) is a dominant cocharacter such that (ℓ,n!) = 1 if we are in case O1, then φ♯ is µ♯-regular.

![](<2503.04623_pg54_images/imageFile2.png>)

In particular, µ♯ can be chosen to be not ﬁxed by any non-trivial element of WG♯.

Proof. By base change [HL24, Lemma 4.22] and the isomorphism Equation (8.1), it suﬃces to prove for the general linear group GL(n), the split special orthogonal group SO(d(G)) and the split general spin group GSpin(d(G)). For general linear groups (i.e., in case U) this is proved in [HL24, Lemma 4.22], and the argument also works for G ∈ {SO(d(G)),GSpin(d(G))}:

The standard representation Std of Sp(2n(G∗)) or SO(2n(G∗)) has weights given by Weyl orbits of ω1. The standard representation extends to a standard representation of GSp(2n(G∗)) or GSO(2n(G∗)), and we write the highest weight of the standard representation of GSp(2n(G∗)) or GSO(2n(G∗)) as

ω1♯. Then it is clear that diﬀerence of the weights appearing in Std are coroots of G, thus φ is strongly µ-regular and φ♯ is strongly µ♯-regular, by deﬁnition of genericity. Thus, they are also µ-regular (resp. µ♯-regular) by the proof of [Ham24, Theorem 10.10].

![](<2503.04623_pg54_images/imageFile3.png>)

For other cocharacters, we ﬁrst recall that with Qℓ-coeﬃcients, the highest weight tilting module Tωi associated to ωi ∈ X•(Sp(2n(G∗))) is realized on the space of harmonic elements in ∧i( Std) as deﬁned in [GW09, §5.5.2], and it extends to a standard representation of GSp(2n(G∗)) with highest weight

denoted by ωi♯, and the same is true with Fℓ-coeﬃcients, where each highest weight tilting module associated to ωi♯ of GSp(2n(G∗)) is a direct sum of ∧i( Std), by our assumption on ℓ, cf. [Jan03, Page 286-287] and [Ham24, §10.1, Appendix B.2]. Similarly, with Qℓ-coeﬃcients, ∧i( Std) is isomorphic to the highest weight tilting module Tωi

![](<2503.04623_pg54_images/imageFile4.png>)

![](<2503.04623_pg54_images/imageFile5.png>)

associated to ωi ∈ X•(SO(2n(G∗))) for 1 ≤ i ≤ n(G∗) − 2, and ∧n(G

∗)−1( Std) is isomorphic to the highest weight tilting module Tωn(G∗)−1+ωn(G∗)

associated to ωn(G∗)−1 + ωn(G∗) ∈ X•(SO(2n(G∗))). On the other hand, ∧n(G

∗)−1( Std) is isomorphic to the direct sum of highest weight tilting modules T2ωn(G∗)−1

, cf. [GW09, Theorem 5.5.13], and these extends to a standard representation of GSp(2n(G∗)) with highest weight denoted by

and T2ωn(G∗)

ω1♯,...,ωn♯−2,ωn♯−1 + ωn♯−2,2ωn♯−1,2ωn♯−2,

![](<2503.04623_pg54_images/imageFile6.png>)

respectively. The same is true with Fℓ-coeﬃcients, where each highest weight tilting module associated to the above cocharacters of GSp(2n(G∗)) is a direct sum of ∧i( Std), by our assumption on ℓ, cf. [Jan03, Page 286-287] and [Ham24, §10.1, Appendix B.2].

Now all these highest weight tilting modules of G♯ with fundamental weights µ♯ appear as direct summand of tensor products of Std, so φ♯ is µ♯-regular by [Ham24, Proposition 10.12].

Finally, we can choose µ♯ appropriately such that under the isomorphism Equation (8.1)

× v∈Hom(K,Qp) GSpin(V ∗ ⊗K,v Qp) in case O GL(1)Q

![](<2503.04623_pg54_images/imageFile7.png>)

GL(1)Q

![](<2503.04623_pg54_images/imageFile8.png>)

![](<2503.04623_pg54_images/imageFile9.png>)

∼=

G♯Q

,

p

![](<2503.04623_pg54_images/imageFile10.png>)

× v∈Hom(K,Qp) GU(V ∗ ⊗K1,v Qp) in case U

![](<2503.04623_pg54_images/imageFile11.png>)

p

![](<2503.04623_pg54_images/imageFile12.png>)

![](<2503.04623_pg54_images/imageFile13.png>)

p

it is of the form (0,µ♯′,...,µ♯′) (i.e., trivial on the GL(1) factor and identical on the other factors), where µ♯′ is not ﬁxed by any non-trivial Weyl group element. Then µ♯ is not ﬁxed by any non-trivial Weyl group element.

8.2. Perverse t-exactness and vanishing results. In this subsection, we prove a perverse t-exactness result for Hecke operators, and deduce a vanishing result for cohomology of Shimura varieties with torsion coeﬃcients. We use notations related to BunG deﬁned in Section 3.1.

For any reductive group G over a non-Archimedean local ﬁeld K of characteristic 0 and any open substack U ⊂ BunG, there exists a perverse t-structure on Dlis(BunG,Fℓ) deﬁned as follows [HL24, Deﬁnition 4.11]: For each b ∈ B(G), denote db := 2ρG,νb where νb is the slope homomorphism of b, then an object A is contained in pD≤0(U,Fℓ) if i∗bA ∈ D≤d

![](<2503.04623_pg54_images/imageFile14.png>)

(Gb,Λ), and A is contained in pD≥0(U,Fℓ) if i!bA ∈ D≥d

![](<2503.04623_pg54_images/imageFile15.png>)

![](<2503.04623_pg54_images/imageFile16.png>)

b

(Gb,Λ). Here we recall that ib is the inclusion BunbG ⊂ BunG. We also need the notion of universally locally acyclic (ULA) objects [FS24, Deﬁnition IV.2.31]: The

b

full subcategory DULA(BunG,Fℓ) ⊂ Dlis(BunG,Fℓ) consists of objects A such that i∗bA ∈ Dadm(Gb,Fℓ) for each b ∈ B(G).

![](<2503.04623_pg54_images/imageFile17.png>)

![](<2503.04623_pg54_images/imageFile18.png>)

![](<2503.04623_pg54_images/imageFile19.png>)

We import Setup 7.2.2. In particular, F is a totally real number ﬁeld unramiﬁed at a prime p, G is a special orthogonal or unitary group over F with G∗ = G ⊗F (F ⊗ Qp), and G♯ is a central extension of G with G♯. Then we have the following local result on the perverse t-exactness of Hecke operators, which generalizes [HL24, Corollary 4.24] to special orthogonal groups and unitary groups:

54

