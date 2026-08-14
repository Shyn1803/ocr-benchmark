14 BHARGAB DAS AND APRAMEYO PAL

Note that X is Panchishkin ordinary if there exist a Greenberg local condition ∆ such that (X,∆) is 0Panchiskin and all Hodge–Tate weights of Fp+

X (resp. of X/Fp+

X) are positive (resp. non-positive) for

i

i

i = 1,2. Example 3.12. —

- (i) Let x ∈ Wcl(f,bal)(O) be an O-valued arithmetic point and let us denote X(x) := X ⊗xO for X = T1,T2, and T3. Then

δPan(T3(x),∆(g,bal)) = 0; δPan(T2(x),tr* ∆(g,bal)) = 1 = δPan(T1(x),tr* ∆(g,bal)).

- (ii) Let x ∈ Wclf (O) be an O-valued arithmetic point and let us denote X(x) := X ⊗x O for X = T1,T2, and T3. Then


δPan(T3(x),∆g) = 0 = δPan(T2(x),∆bal); δPan(T2(x),tr* ∆g) = 2 = δPan(T1(x),tr* ∆g).

- Remark 3.13. Using the Panchiskin defect we can indicate why the factorization problem for algebraic p-adic L-functions we consider in this article is considerably more challenging than those problems considered earlier in [Gre82, Pal18, BCS23]. All the factorizations result in op. cite are obtained when the associated pairs are either 0-Panchiskin or 1-Panchiskin while we also consider the 2-Panchiskin pairs (cf. [BCS23, §4.3.2]). This discussion also gives evidence towards the existence of higher rank Euler systems assumed in Section 6 (cf. [LZ20b]).

3.3. Remarks on Tamagawa Factors. Let v ∤ p∞ be a place in F. Suppose ϕ: GF

v

→ GLR(V ) be a continuous GF

v

-representation, where V is a free module of ﬁnite rank over a complete Noetherian local ring R with ﬁnite residue ﬁeld of characteristic p.

- Remark 3.14. When R = Zp, F = Q, the p-adic valuation of the order of H1(Iv,V )Fr


v=1

R−tors is the local Tamagawa factor at v (see [FPR94, §I.4.2.2]). So it vanishes if H1(Iv,V ) is a free R-module. In this philosophy, we would concentrate on the following conditions:

• The R-module H1(Iv,V ) is free. This discussion about the Tamagawa factor is needed for veriﬁcation that our Selmer complexes are perfect.

3.3.1. Let Iv(p)⊳Iv be the unique subgroup satisfying Iv/Iv(p) ∼= Zp. Let us ﬁx a topological generator t ∈ Iv/Iv(p). (cf. [NSW08, §7.5.2])

Lemma 3.15. —

- (1) The R-module V I

(p)

v is free of ﬁnite rank.

- (2) The complex C•(Iv,V ) is quasi-isomorphic to the perfect complex

··· → 0 → V I

(p)

v −−→t−1 V I

(p)

v → 0 → ··· concentrated in degrees 0 and 1.

- (3) For any ring homomorphism R → S, the induced map V I


(p)

(p)

v ⊗R S → (V ⊗R S)I

v is an isomorphism. Therefore in the derived category

RΓ(Iv,V ) ⊗LR S −→∼ RΓ(Iv,V ⊗R S) Proof. The statement (1) and (2) follows from [Nek06, §7.5.8]. To prove (3), [Nek06, §7.5.8] gives the inclusion V I

(p)

(p)

v → V is split, the R-module V/V I

v is ﬂat. hence we have an exact sequence of S-modules

(p)

(p)

0 −→ V I

v ⊗R S −→ V ⊗R S −→ V/V I

v ⊗R S −→ 0. Moreover, the group Iv(p) acts trivially on the ring S. Since ϕ(Iv(p)) is ﬁnite and p ∤ #ϕ(Iv(p)), we have e :=

1 #ϕ(Iv(p)) g∈ϕ(I

g ∈ O[ϕ(Iv(p))]

![](<2503.07542_pg14_images/imageFile1.png>)

(p) v )

Therefore we have

(p)

(p)

(p)

(p)

v ⊗R S) = e(V/V I

v = e(V/V I

v ⊗R S)I

(V/V I

v ) ⊗R S = 0 . This shows that the canonical homomorphism V I

(p)

(p)

v ⊗R S → (V ⊗R S)I

v is an isomorphism. Corollary 3.16. Suppose ϕ(Iv) is ﬁnite and p ∤ #ϕ(Iv) then R-module H1(Iv,V ) is free. Proof. Follows from Lemma 3.15 since in this scenario we have isomorphism of R-modules H1(Iv,V ) ∼= V I

(p)

v .

