Lemma 3.2. Let M be an R-module. Suppose that I is an ideal of R and N ∈ mod R such that SuppN ⊂ V (I). Then the following assertions hold for any non-negative integer n.

- (1) If ExtiR(R/I,M) ∈ S for 0 i n, then ExtiR(N,M) ∈ S for 0 i n.
- (2) If TorRi (R/I,M) ∈ S for 0 i n, then TorRi (N,M) ∈ S for 0 i n.


Proof. Since N is ﬁnitely generated, it follows from [13, Theorem 6.4] that there exists a chain 0 = N0 ⊂ N1 ⊂ ··· ⊂ Nk = N of submodules of N such that for each i we have Nj/Nj−1 ∼= R/pj with pj ∈ SuppN.

(1) Note that HomR(R/I,E) is an injective R/I-module for any injective R-module E by [12, Lemma 3.5]. For each pj, by [15, Theorem 10.64], there is a spectral sequence

E2p,q = ExtpR/I(R/pj,ExtqR(R/I,M)) ⇒ ExtnR(R/pj,M).

Being a subquotient of a ﬁnite direct sum of copies of ExtqR(R/I,M) ∈ S , we have that E2p,q ∈ S for 0 q n and any p. Since E∞p,q is isomorphic to a subquotient of E2p,q, we have E∞p,q ∈ S for 0 q n and any p. Hence ExtiR(R/pj,M) ∈ S for 0 i n. Consequently, applying the functor ExtiR(−,M) to exact sequences 0 → Nj−1 → Nj → Ni/Nj−1 → 0 yields that ExtiR(N,M) ∈ S for 0 i n.

(2) can be proved similarly by using [15, Theorem 10.60].

![](<2503.06354_pg6_images/imageFile1.png>)

![](<2503.06354_pg6_images/imageFile2.png>)

![](<2503.06354_pg6_images/imageFile3.png>)

![](<2503.06354_pg6_images/imageFile4.png>)

- (3.3) Let I = (x1,x2,··· ,xn) be an ideal of R and M a complex of R-modules. In the following, we use K(I) to denote the Koszul complex with respect to I = (x1,x2,··· ,xn). The Koszul complex K(I) is a bounded complex of ﬁnite free modules. Then we deﬁne Hi(K(I),M) := TorRi (K(I),M) = Hi(K(I)⊗RM) and Hi(K(I),M) := ExtiR(K(I),M) = Hi(HomR(K(I),M)).
- (3.4) The preceding lemma allows us to extend some parts of [3, Theorem 2.8] to modules which are not necessarily ﬁnitely generated.


√

√

![](<2503.06354_pg6_images/imageFile5.png>)

![](<2503.06354_pg6_images/imageFile6.png>)

Proposition 3.5. Let M be an R-module. If I and J are ideals of R such that

J, then the following assertions are equivalent for any non-negative integer n.

I =

- (1) ExtiR(R/I,M) ∈ S for 0 i n.
- (2) ExtiR(R/J,M) ∈ S for 0 i n.
- (3) Hi(K(I),M) ∈ S for 0 i n.
- (4) Hi(K(J),M) ∈ S for 0 i n.


Proof. (1) ⇔ (2) follows from Lemma 3.2(1). (1) ⇒ (3) There is a spectral sequence

E2p,q = ExtqR(Hp(K(I)),M) ⇒ Hp+q(K(I),M).

6

