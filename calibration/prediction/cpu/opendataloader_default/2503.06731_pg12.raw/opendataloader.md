- 3. To define the associator, notice that for V,W,U ∈ Rep(A), both the spaces (V ⊗W)⊗U and V ⊗ (W ⊗ U) are given by the retract of the idempotent

V ⊗ W ⊗ U −→ V ⊗ W ⊗ U, v ⊗ w ⊗ u  −→ 1(1).v ⊗ 1(2).w ⊗ 1(3).u,

which can be verified using (Axiom 1). We then define the associator aV,W,U as the canonical map between the two retracts. One can check that aV,W,U is an A-module map, and satisfies the pentagon equation.

- 4. Given V ∈ Rep(A), we set the left unitor lV : Al ⊗ V −→ V to be the restriction of the map Al ⊗ V −→ V, x ⊗ v  −→ x.v

on Al ⊗ V ; we set the right unitor rV : V ⊗ Al −→ V to be the restriction of the map V ⊗ Al −→ V, v ⊗ y  −→ εrr(y).v

on V ⊗ Al. One can check that lV and rV are indeed invertible A-module maps, and satisfy the triangle equations.

- 5. The left dual V L of an object V ∈ Rep(A) is given by the dual vector space V ∗ := Hom(V,k) endowed with the A-action


x.ω = ω(S(x).−), ∀ω ∈ V ∗,x ∈ A. Similarly, the right dual V R of V is given by V ∗ endowed with A-action x.ω = ω(S−1(x).−), ∀ω ∈ V ∗,x ∈ A.

Secondly, note that Rep(A) is clearly a finite k-linear category, with the tensor product ⊗ being bi-k-linear. This concludes our construction of Rep(A).

1.20 Example. We illustrate the above construction of Rep(A) when A is the weak Hopf algebra B ⊗ Bop defined in Example 1.17. Since a left A-module is precisely a B-B-bimodule, Rep(A) is equivalent to BiMod(B|B) as categories. It remains to find the monoidal structure on Rep(A). Given left A-modules V and W, which we identify as B-B-bimodules, the underlying vector space of V ⊗ W is the retract of the idempotent

V ⊗ W −→ V ⊗ W, v ⊗ w  −→ v.p(1) ⊗ p(2).w . The action of a ⊗ b ∈ B ⊗ Bop on V ⊗ W is given by the restriction of the map

V ⊗ W −→ V ⊗ W, v ⊗ w  −→ a.v.p(1) ⊗ p(2).w.b on V ⊗W. Using Corollary 1.5, it can be shown that the B-B-bimodule V ⊗W is precisely V ⊗B W.

To find the tensor unit of Rep(B ⊗ Bop), one first computes

εlr : B ⊗ Bop −→ B ⊗ Bop, a ⊗ b  −→ ab ⊗ 1; εrr : B ⊗ Bop −→ B ⊗ Bop, a ⊗ b  −→ 1 ⊗ ab. 12

