18 QINGYUN ZENG

- (1) The global section functor Γ : ModSX → ModSX(X)

![](<2503.08457_pg18_images/imageFile1.png>)

![](<2503.08457_pg18_images/imageFile2.png>)

is exact and establishes an equivalence of categories between the category of sheaves of right SX-modules and the category of right modules over the global sections SX(X) of SX.

![](<2503.08457_pg18_images/imageFile3.png>)

![](<2503.08457_pg18_images/imageFile4.png>)

![](<2503.08457_pg18_images/imageFile5.png>)

- (2) If F ∈ ModSX locally has ﬁnite resolutions by ﬁnitely generated free SX-modules, then Γ(X, F) has a ﬁnite resolution by ﬁnitely generated projective modules.

![](<2503.08457_pg18_images/imageFile6.png>)

![](<2503.08457_pg18_images/imageFile7.png>)

![](<2503.08457_pg18_images/imageFile8.png>)

![](<2503.08457_pg18_images/imageFile9.png>)

- (3) The derived category of perfect complexes of sheaves DPerf(ModSX) is equivalent to the derived category of perfect complexes of modules DPerf(ModSX(X)).


![](<2503.08457_pg18_images/imageFile10.png>)

![](<2503.08457_pg18_images/imageFile11.png>)

By this theorem, there is a (strict) perfect complex of A0-modules (E,E0) and a quasi-

isomorphism e0 : (E•,E0) → (F•,F0) = (Γ(M, C∞F ), D). We shall follow the argument of Theorem 3.2.7 of [Blo05] to construct the higher components Ei of Z-connection along with the higher components of a morphism ei.

![](<2503.08457_pg18_images/imageFile12.png>)

On F•, we have a Z-connection

F = D ⊗ 1 + 1 ⊗ d : F• → F• ⊗A0 A• . The idea is to transfer this Z-connection to E• which is compatible with the quasiisomorphism on H0’s. Note that we have an induced connection

Hk : Hk(F•,F0) → Hk(F•,F0) ⊗A0 A1

for each k. First we will transfer this connection to a connection on Hk(E•,E0), and we have the following commutative diagram

Hk

- Hk(E•,E0) Hk(E•,E0) ⊗A0 A1
- Hk(F•,F0) Hk(F•,F0) ⊗A0 A1


e0 e0⊗1

Hk

Note that e0 ⊗ 1 is a quasi-isomorphism since A• is ﬂat over A0. We need the following lemma.

Lemma 2.10. Given a bounded complex of ﬁnitely generated projective A0-modules (E•,E0) with connections Hk : Hk(F•,F0) → Hk(F•,F0) ⊗A0 A1 for each k, there exists connections

H˜ k : Ek → Ek ⊗A0 A1 lifting Hk, i.e.

H˜ kE0 = (E0 ⊗ 1)H˜ k

for each k and the connection induced on the cohomology is Hk.

Proof. This is Lemma 3.2.8 in [Blo05] and Lemma 4.6 in [BS14]. Since E• is bounded, let [N, M] be its magnitude. Pick some arbitrary connection ∇ on EM. Consider the following diagram whose rows are exact

