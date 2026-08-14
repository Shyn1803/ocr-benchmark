4 JOSEPH HELFER, ERIC JOVINELLY, ERIC LARSON, ANDA TENIE, CHENGXI WANG

the structure of a G-equivariant bundle – i.e., a G-action on π∗E by vector bundle automorphisms making the projection π∗E → X equivariant. By fpqc descent, this gives an equivalence of categories

π∗: Vect(X/G) → VectG(X).

That is, we can study vector bundles on X/G in terms of equivariant vector bundles on X. The bundles on X/G which are pulled back along X/G → pt/G correspond to the equivariant vector bundles on X of the form X × V −→π1 X for some G-representation V , where G acts simultaneously on both factors of X×V . As a special case, vector bundles on BG = pt/G correspond to equivariant vector bundles on pt, i.e., G-representations.

2.3. Common groups and classes. The following notation is consistent with [Lar21].

- Definition 2.1. Throughout this paper, let G denote the wreath product G .= (Gm × Gm) ⋊ Z/2Z,

where the action of Z/2Z on Gm × Gm permutes its factors.

One can describe representations of G through the sign representation Γ of Z/2Z and representations of Gm.

- Definition 2.2. We let Ln denote the 1-dimensional representation of Gm with weight n. Set

La

1,...,an .= La

1 ⊕ ... ⊕ La

n

. Let Wa

1,...,an be the representation of G whose underlying vector space is Wa

1,...,an .= La

1,...,an ⊕ La

1,...,an and where Gm × Gm ⊂ G acts naturally on La

1,...,an ⊕ La

1,...,an and Z/2Z permutes its factors.

Lastly, we let V denote the standard representation of GL2 and set Vn .= SymnV ∗ as well as Vn(m) .= Vn ⊗ (detV )⊗m.

- Definition 2.3. With the above notation, set αi = ci(V ) ∈ CH∗(BGL2), βi = ci(W1) ∈ CH∗(BG),


γ = c1(Γ) ∈ CH∗(BZ/2Z),

and for i = 1,2 let ti ∈ CH∗ B(Gm × Gm) be the pullback of c1(L1) along the i-th projection map B(Gm × Gm) → BGm.

Whenever we are working in the Chow ring of a space equipped with a map to BGL2, BG, or B(Gm × Gm), we will denote by αi βi, etc., the pullbacks of these classes from CH∗(BGL2), etc. We have the following explicit presentations of these rings:

Lemma 2.4 ([Tot14, Theorem 2.13 and Lemma 2.12; Lar21, Theorem 5.2 and Lemma 7.1]). We have the presentations

CH∗(BGL2) ∼= Z[α1,α2], CH∗(BG) ∼= Z[β1,β2,γ]/(2γ,γ2+β1γ), CH∗ B(Gm × Gm) ∼= Z[t1,t2]. Moreover, the norm (or transfer map) from Gm × Gm to G – in other words, the pushforward π∗: CH∗(Gm × Gm) → CH∗(G) along the index 2 inclusion Gm × Gm → G – is given by

π∗(1) =2 π∗(ta1) =β1π∗(ta1−1) − β2π∗(ta1−2) for a ≥ 2 π∗(t1) =β1 + γ π∗(ta1tb2) =β2min(a,b)π∗(t|1a−b|),

