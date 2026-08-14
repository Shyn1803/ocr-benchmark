10 A. DJAMENT AND A. TOUZÉ

(2) For all objects x and y of B, the torsion groups T• = TorA• (φ∗hxBop,φ∗hyB) (calculated in the category of additive functors from A to abelian groups) satisfy

k ⊗Z Ti = 0 = TorZ1(k,Tj) = 0 , for 0 < i < e and 0 < j < e − 1.

The remainder of the section is devoted to the proof of theorem 3.4. This proof depends on the use of simplicial techniques, and in particular on variants of the Hurewicz theorem. For the convenience of the reader, the simplicial notions and results that we need are recalled in the appendix (section 6). The ﬁrst step of the proof is the following general lemma, which is of independent interest. It is well-known to experts, but we do not know any written reference for it.

Lemma 3.5. Let A : Aop → Z-Mod and B : A → Z-Mod be two additive functors, and let k[A] and k[B] denote the composition of these functors with the k-linearization functor k[−]. There is an isomorphism of k-modules, natural with respect to A and B:

k[A] ⊗k[A] k[B] ≃ k[A ⊗Z[A] B] . Proof. We ﬁrst recall concrete formulas for tensor products. For all commutative rings K, the tensor product F ⊗K[A] G can be concretely computed as the quotient of the direct sum x F(x) ⊗K G(x) indexed by a set of representatives of the isomorphism classes of objects of A, modulo the relations F(f)(s)⊗t = s⊗G(f)(t) for all morphisms f : x → y and for all elements s ∈ F(y) and t ∈ G(x). We will denote by s⊗t ∈ F ⊗K[A] G the class of an element s⊗t ∈ F(x)⊗K G(x). When G = Pc is a standard projective there is a ‘Yoneda isomorphism’

Υ : F ⊗K[A] Pc ≃ F(c) given by sending the class s ⊗ f with s ∈ F(x) and f ∈ A(c,x) to F(f)(s) (the inverse isomorphism sends u ∈ F(c) to u ⊗ idc ). Similarly, if F is additive and G = hc is a standard additive projective, there is an ‘additive Yoneda isomorphism isomorphism’

Υadd : F ⊗K[A] hc ≃ F(c) .

When k = Z, the isomorphism Υadd sends class s ⊗ f with s ∈ F(x) and f ∈ A(c,x) to F(f)(s).

We are now ready to construct the isomorphism of lemma 3.5. For all objects x of A, we let θA,B,x : k[A(x)] ⊗ k[B(x)] → k[A ⊗Z[A] B] be the k-linear map such that θA,B,x(s ⊗ t) = s ⊗ t for all s in A(x) and all t ∈ B(x). The maps θA,B,x induce a k-linear map, natural in A and B:

ΘA,B : k[A] ⊗k[A] k[B] → k[A ⊗Z[A] B] .

If B = hc is a standard projective additive, the composition k[Υadd] ◦ ΘA,B is equal to Υ, hence ΘA,B is an isomorphism in this case. Finite direct sums of standard projective additives are isomorphic to standard projective additives, hence ΘA,B is also an isomorphism if B is a ﬁnite direct sum of standard additive projectives. Now the source and the target of ΘA,B, viewed as functors of B preserve ﬁltered colimits of monomorphisms, which implies in turn that ΘA,B is an isomorphism if B is an arbitrary direct sum of standard projective additives.

Now let B be arbitrary and let ǫ : P → B be a projective simplicial resolution of B in A-Mod by direct sums of standard projective additives. Then we have a commutative square of simplicial k-modules in which the top row is an isomorphism,

