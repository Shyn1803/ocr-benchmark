7

Proposition 3.6 ( [15, Corollary 1.4]). Consider the assumption in Theorem 3.5. Then, Sel±p∞(E/K∞) has no proper Λ-submodules with ﬁnite index.

By the above proposition and a property of the Fitting ideal (cf. [10, Lemma A.7]), we have

FittΛ Sel±p∞(E/K∞)∨ = charΛ Sel±p∞(E/K∞)∨ . (3.1) Last, we prove the control theorem for Sel±p∞(E/K∞) in our situation by the similar arguments

to [1]. We prepare the following lemma for the proof. Let w be a prime of K∞ above p.

Lemma 3.7. The natural map fn± : H±1 (Kn,p,E[p∞]) −→ H±1 (K∞,w,E[p∞])[ωn±] is injective, and the cokernel of fn± is a ﬁnite group for any positive integer n. Here, we deﬁne H±1 (K∞,w,E[p∞]) := lim

H±1 (Kn,p,E[p∞]).

−→

Proof. Note that we have E[p∞]GK∞,p = 0 by [15, Proposition 3.2]. By Inﬂation-Restriction exact sequence, we see that the canonical map

fn : H1(Kn,p,E[p∞]) −→ H1(K∞,p,E[p∞])Gal(K∞,p/Fn,p) = H1(K∞,p,E[p∞])[ωn] is injective. Since the map fn± is the restriction of fn to H±1 (Kn,p,E[p∞]), fn± is also injective. For the claim for Coker fn±, it suﬃces to show that both the Zp-coranks of H±1 (Kn,p,E[p∞])

and H±1 (K∞,w,E[p∞])[ωn±] are same. Since we have H±1 (K∞,w,E[p∞])∨ ≃ Λ2 as Λ-module by the Rubin conjecture, we see that

H±1 (K∞,w,E[p∞])[ωn±]∨ ≃ (H±1 (K∞,w,E[p∞]))∨/ωn±(H±1 (K∞,w,E[p∞]))∨ ≃ Λ2/ωn±Λ2.

On the other hand, we have H±1 (Kn,p,E[p∞]) = E(Kn,p)± ⊗ (Qp /Zp) by the deﬁnition. Thus, we see that H±1 (Kn,p,E[p∞])∨ ≃ Λ2n/ωn±Λ2n by Proposition 3.4. Therefore, the Zp-rank of H±1 (Kn,p,E[p∞]) and H±1 (K∞,w,E[p∞])[ωn±] are the same.

Proposition 3.8. Consider the assumption in Theorem 3.5. Then, the canonical homomorphism Sel±p∞(E/K∞)[ωn±] −→ Sel±p∞(E/Kn)[ωn±] is injective, and the order of the cokernel is ﬁnite for any n. Proof. We take the ﬁnite subset Σ = {p} ∪ {bad primes of E}. Then, we have the following commutative diagram:

H1(KΣ/Kn,E[p∞])[ωn±] a

0 Sel±p (E/Kn)[ωn±]

![](<2503.09034_pg7_images/imageFile1.png>)

![](<2503.09034_pg7_images/imageFile2.png>)

![](<2503.09034_pg7_images/imageFile3.png>)

![](<2503.09034_pg7_images/imageFile4.png>)

![](<2503.09034_pg7_images/imageFile5.png>)

s±n

h±n

0 Sel±p (E/K∞)[ωn±] H1(KΣ/K∞,E[p∞])[ωn±]

![](<2503.09034_pg7_images/imageFile6.png>)

![](<2503.09034_pg7_images/imageFile7.png>)

![](<2503.09034_pg7_images/imageFile8.png>)

H1(Kn,vn,E[p∞])[ωn±] H±1 (Kn,vn,E[p∞])

,

![](<2503.09034_pg7_images/imageFile9.png>)

vn|v v∈Σ

![](<2503.09034_pg7_images/imageFile10.png>)

gn±= gn,v± n

H1(K∞,v∞,E[p∞])[ωn±] H±1 (K∞,v∞,E[p∞])[ωn±]

.

![](<2503.09034_pg7_images/imageFile11.png>)

v∞|v v∈Σ

Since we have E[p∞]GK∞ = 0, the map H1(KΣ/Kn,E[p∞]) −→ H1(KΣ/K∞,E[p∞])[ωn] induced by the restriction map is isomorphism by the Inﬂation-Restriction exact sequence. There-

fore, h±n is also isomorphism. By the snake lemma, s±n is injective, and it suﬃces to calculate the kernel of gn±.

We ﬁrst consider the case v ∈ Σ \ {p}. Then, K∞,v∞/Kn,vn is the trivial extension or the unramiﬁed Zp-extension. If the extension K∞,v∞/Kn,vn is trivial, then it is clear that Kergn,v± n = 0. Assume that K∞,v∞/Kn,vn is the unramiﬁed Zp-extension. Write Bv∞ := E[p∞]GK∞,v∞ . We consider the exact sequence

0 H1(K∞,v∞/Kn,vn,Bv∞) H1(Kn,vn,E[p∞]) H1(K∞,v∞,E[p∞])

![](<2503.09034_pg7_images/imageFile12.png>)

![](<2503.09034_pg7_images/imageFile13.png>)

![](<2503.09034_pg7_images/imageFile14.png>)

