6 LUIGI LOMBARDI

is the origin of Y ). Then Db(Unip(X)) ≃ Db(Coh{ˆ0}(Y )) and, by Corollary 2.3 and Proposition 3.6, there is no smooth projective variety M such that Db(Unip(X)) is equivalent to Db(Coh(M)).

In the positive-dimensional case the characterization of point like objects in DbZ(Coh(X)) is possible under a positivity assumption on the restriction of the canonical bundle to the support. Proposition 3.8. Suppose ωX|Z or ωX−1|Z is ample. Then the point like objects of DbZ(Coh(X)) are the objects isomorphic to ι!ZC(p)[r] where p ∈ Z is a closed point and r ∈ Z.

Proof. Let P be a point like object in DbZ(Coh(X)) and denote by Hj the cohomology sheaves of ιZP. Note that the Hj’s are coherent sheaves on X supported in Z. Since SZ(P) ≃ P[dimX], we have the following isomorphisms:

ι!Z(ιZP ⊗ ωX) ≃ P ιZι!Z(ιZP ⊗ ωX) ≃ ιZP ιZι!ZιZP ⊗ ωX ≃ ιZP ιZP ⊗ ωX ≃ ιZP.

By taking cohomology we have

(3) Hj ⊗ ωX ≃ Hj for all j.

Now we show that Hj is supported in dimension zero for any j. Suppose ωX|Z is ample, the other case being similar. Let k > 0 be an integer such that N := ωX⊗k|Z is very ample and let i: Z ֒→ X be the inclusion map (here Z is equipped with the reduced induced subscheme structure). Then the Hilbert polynomial of Pi∗Hj(m) = χ(i∗Hj ⊗ N⊗m) has degree equal to

sj := dimSupp(i∗Hj) = dimSupp(Hj)

([Ser55, p. 276, Proposition 6]). Moreover, by tensoring (3) with positive powers of ωX and by restricting the isomorphisms to Z, we ﬁnd

i∗Hj ⊗ N ≃ i∗Hj for all j.

Therefore Pi∗Hj(m) = Pi∗Hj⊗N(m) = Pi∗Hj(m+1) for all m ∈ Z which is impossible if deg Pi∗Hj > 0. Hence sj = 0 for all j and ιZP ≃ C(p)[r] for some closed point p ∈ Z and r ∈ Z by Lemma 3.4. It follows that P ≃ ι!ZC(p)[r].

Example 3.9. We construct further instances of equivalences between derived categories with support extending the equivalences (1). Denote by

R: Aut0(X) × Pic0(X) → Aut0(Y ) × Pic0(Y )

the Rouquier isomorphism induced by an equivalence F : Db(Coh(X)) → Db(Coh(Y )) (cf. [Rou11, The´ore`me 4.18] or [Huy06, Proposition 9.45], and [PS11, p.531, footnote (1)]). By following [Lom14,

Proposition 3.1], if α ∈ Pic0(X) is a topologically trivial line bundle such that H0(X,ωX⊗k0 ⊗ α) = 0 for some k0 ∈ Z, then R(idX,α) = (idY ,β) for some β ∈ Pic0(Y ) and moreover there are isomorphisms Rk : H0(X,ωX⊗k ⊗ α) → H0(Y,ωY⊗k ⊗ β) for all k ∈ Z. As in [Tod06], one can prove that if E ∈ ωX⊗k ⊗ α and E′ = Rk(E) ∈ ωY⊗k ⊗ β is the corresponding divisor, then F restricts to an equivalence of triangulated categories DbSupp(E)(Coh(X)) ≃ DbSupp(E′)(Coh(Y )).

