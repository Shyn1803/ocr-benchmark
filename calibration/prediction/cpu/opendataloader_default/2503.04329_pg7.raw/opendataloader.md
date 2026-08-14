- Deﬁnition 2.9. Given z = (z1,...,zn) ∈ Cn, deﬁne zh := (z1,...,zh−1,zh,zh+1,...,zn), for any h ∈ {1,...,n}. A set D ⊂ Cn is called symmetric if it is invariant with respect to complex conjugation in any variable, i.e. if z ∈ D ⇐⇒ zh ∈ D, for every h = 1,...,n.

![](<2503.04329_pg7_images/imageFile1.png>)

![](<2503.04329_pg7_images/imageFile2.png>)

![](<2503.04329_pg7_images/imageFile3.png>)

Let {e1,...,en} be an orthonormal basis of Rn and denote with {eK}K∈P(n) a basis of R2

n

.

- Deﬁnition 2.10. Let D ⊂ Cn be an open symmetric set and consider a function F : D ⊂

Cn → Rm ⊗ R2

n

, F(z) = K∈P(n) eKFK(z) with FK : D → Rm. We call F a stem function if FK(zh) = (−1)|K∩{h}|FK(z) or equivalently

![](<2503.04329_pg7_images/imageFile4.png>)

FK(zh) =

![](<2503.04329_pg7_images/imageFile5.png>)

FK(z) if h ∈/ K −FK(z) if h ∈ K,

(8)

for every z ∈ D, every K ∈ P(n) and any h ∈ {1,...,n}. Again, we use the symbol Stem(D) to denote the set of stem functions F : D → Rm ⊗ R2

n

. Equip R2

n

with the family of commutative complex structures J = Jh : R2

n

→ R2

n n

h=1 , where each Jh is deﬁned over any basis element eK of R2

n

as

Jh(eK) := (−1)|K∩{h}|eK∆{h} =

eK∪{h} if h ∈/ K −eK\{h} if h ∈ K,

where K∆H = (K ∪ H) \ (K ∩ H) and extend it by linearity to all R2

n

. J induces a family of commutative complex structure on Rm ⊗ R2

n

(by abuse of notation, we use the same symbol) J = Jh : Rm ⊗ R2

n

→ Rm ⊗ R2

n n

h=1 according to the formula Jh(x ⊗ a) := x ⊗ Jh(a) ∀x ∈ Rm, ∀a ∈ R2

n

. We can associate two Cauchy-Riemann operators to each complex structure Jh.

- Deﬁnition 2.11. Given a stem function F ∈ Stem(D) ∩ C1(D), we deﬁne


- 1

![](<2503.04329_pg7_images/imageFile6.png>)

- 2


- 1

![](<2503.04329_pg7_images/imageFile7.png>)

- 2


∂F ∂βh

∂F ∂βh

∂F ∂αh − Jh

∂F ∂αh

![](<2503.04329_pg7_images/imageFile8.png>)

+ Jh

∂hF :=

, ∂hF :=

.

![](<2503.04329_pg7_images/imageFile9.png>)

![](<2503.04329_pg7_images/imageFile10.png>)

![](<2503.04329_pg7_images/imageFile11.png>)

![](<2503.04329_pg7_images/imageFile12.png>)

![](<2503.04329_pg7_images/imageFile13.png>)

We call F = K∈P(n) eKFK h-holomorphic (with respect to J ) if F ∈ ker∂h and it is called holomorphic if it is h-holomorphic for every h = 1,...,n.

We can give the deﬁnition of holomorphic stem function through a system of Cauchy-Riemann equations. Proposition 2.3 ([18],Lemma 3.12). Let F be a stem function. Then F is h-holomorphic if and only if

∂FK∪{h} ∂βh

∂FK∪{h} ∂αh

∂FK ∂αh

∂FK ∂βh

= −

, ∀K ∈ P(n),h ∈/ K. (9)

=

,

![](<2503.04329_pg7_images/imageFile14.png>)

![](<2503.04329_pg7_images/imageFile15.png>)

![](<2503.04329_pg7_images/imageFile16.png>)

![](<2503.04329_pg7_images/imageFile17.png>)

For any J1,...Jn ∈ S, deﬁne φJ

(zn)) ∈ (Rm+1)n, where φJ is deﬁned in (3).

: Cn ∋ (z1,...,zn)  → (φJ

1 × ... × φJ

(z1),...,φJ

1

n

n

7

