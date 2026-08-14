4 T. GERHARDT, M. PEROUX,´ AND W.H.B. SORE´

We may refer to the triple (C,∆,ε) just as C if the comultiplication and counit are understood. We shall occasionally use the Sweedler notation and write ∆(c) = i c(1)

simply as: ∆(c) =

⊗ c(2)

i

i

c(1) ⊗ c(2) ∈ C ⊗ C.

(c)

We say C is cocommutative if τ ◦ ∆ = ∆, where τ : C ⊗ C → C ⊗ C swap the terms, i.e., τ(c ⊗ c′) = c′ ⊗ c. In other words, C is cocommutative if for all c ∈ C:

c(1) ⊗ c(2) =

(c)

c(2) ⊗ c(1).

(c)

A homomorphism of coalgebras (C,∆C,εC) → (D,∆D,εD) consists of a k-linear homomorphism f : C → D such that ∆D ◦f = (f ⊗f)◦∆C and εD ◦f = εC. We denote by coAlgk the induced category of k-coalgebras with coalgebra homomorphisms. Notice that coAlgk is equivalent to Alg(Vectopk ), the category of algebra objects in Vectopk .

- Deﬁnition 2.2. A k-bialgebra H is a k-vector space H together with a k-coalgebra structure (H,∆,ε) and a k-algebra structure (H,µ,η) such that ∆: H → H ⊗ H and ε: H → k are algebra homomorphisms (or equivalently, µ: H ⊗ H → H and η: k → H are coalgebra homomorphisms). We say H is commutative if it is commutative as an algebra, and we say H is cocommutative if it is cocommutative as a coalgebra. We say H is a Hopf algebra if there exists a k-linear function S: H → H (necessarily unique) such that µ ◦ (id ⊗ S) ◦ ∆ = η ◦ ε = µ ◦ (S ⊗ id) ◦ ∆.
- Deﬁnition 2.3. Given a k-coalgebra C, a right C-comodule (M,ρ) consists of a k-vector space M together with a k-linear homomorphism ρ: M → M ⊗ C that is coassociative and counital: (idM ⊗ ∆) ◦ ρ = (ρ ⊗ idC) ◦ ρ and (idM ⊗ ε) ◦ ρ = idM. A (right) C-colinear homomorphism f : (M,ρ) → (M′,ρ′) is a k-linear homomorphism f : M → M′ such that ρ′ ◦ f = (f ⊗ idC) ◦ ρ. Let coModC denote the category of right C-comodules with colinear homomorphisms. Left C-comodules are deﬁned completely analogously. If C is cocommutative, then left and right C-comodules are equivalent and we will simply refer to them as Ccomodules. We shall occasionally use the Sweedler notation for the coaction and write simply (m) m(0) ⊗ m(1) for ρ(m) = i m(0)i ⊗ m(1)i ∈ M ⊗ C for any m ∈ M.
- Deﬁnition 2.4. A right C-comodule M is ﬁnitely cogenerated if there exists a C-colinear monomorphism M ֒→ C⊕n := k⊕n ⊗ C.
- Deﬁnition 2.5. A right C-comodule M is injective if for every C-colinear monomorphism ι: X ֒→ Y and any C-colinear homomorphism f : X → M, there exists a C-colinear homomorphism g: Y → M such that g ◦ ι = f.


In particular, if M is a ﬁnitely cogenerated and injective right C-comodule, there exists another ﬁnitely cogenerated and injective right C-comodule N such that M ⊕ N ∼= C⊕n as comodules, for some n ≥ 0. Let Injfc(C) denote the category of ﬁnitely cogenerated and injective right C-comodules. Then, we have the following result.

Proposition 2.6. The category Injfc(C) is an exact category. Proof. The category coModC is an abelian category as ﬁnite limits and colimits in coModC are created under the forgetful functor coModC → Vectk. Consider a short exact sequence of right C-comodules:

0 M N P 0. If M and P are ﬁnitely cogenerated and injective, then so is M ⊕P, thus as N ∼= M ⊕P we can conclude.

Deﬁnition 2.7 ([KP25]). Given a k-coalgebra C, deﬁne its coalgebraic K-theory Kc(C) to be the algebraic K-theory spectrum K(Injfc(C)) of the exact category Injfc(C) of ﬁnitely cogenerated and injective right C-comodules.

The class of ﬁnitely cogenerated and injective comodules forms the class of dualizable objects in comodules with respect to a monoidal structure we now make precise. Recall that given a right C-comodule (M,ρ) and a left C-comodule (N,λ), the relative cotensor product M CN is deﬁned as the equalizer in Vectk:

ρ⊗1 1⊗λ

M CN M ⊗ N M ⊗ C ⊗ N.

