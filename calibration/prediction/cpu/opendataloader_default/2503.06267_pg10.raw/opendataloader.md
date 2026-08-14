10 HIGINIO SERRANO, BERNARDO URIBE, AND MIGUEL XICOTÉNCATL

A subrepresentation of a representation V of the magnetic point group (G,ϕ) is a subspace W ⊂ V such that the restriction of the G-action to W is also a representation of (G,ϕ). A representation V of (G,ϕ) is irreducible if its only representations are V and 0.

Now, the category of representations of finite magnetic groups is semisimple.

Proposition 1.9. Every representation of a finite magnetic group is a sum of irreducible representations.

Which follows from Maschke’s lemma applied to representations of magnetic groups. Lemma 1.10 (Maschke). If W is a subrepresentation of V of a finite magnetic group, then there exists a subrepresentation W′ of V such that V = W ⊕ W′. Proof. Write V as a direct sum V = W ⊕U (with U not necessary a subrepresentation) and consider the projection π1 : V −→ W given by π1(w + u) = w. Define

π : V −→ W

(1.10) g · π1(g−1 · v).

v  −→

g∈G

The morphism π is in HomRep(G,ϕ)(V,W) because if h ∈ G and v ∈ V, then

(1.11) g · π1(g−1 · (h · v))

π(h · v) =

g∈G

(1.12) g · π1((g−1h) · v)

# =

g∈G

(1.13) (hh−1g) · π1((h−1g)−1 · v)

# =

g∈G

(1.14) (h−1g) · π1((h−1g)−1 · v)

# = h ·

g∈G

- (1.15) l · π1(l−1 · v)
- (1.16) = h · π(v)

The morphism π is surjective, this follows since π1(w) = w for w ∈ W, so π(w) = |G|w. If we denote by W′ = kerπ, then we have the decomposition as a direct sum of representations of (G,ϕ)

- (1.17) V Imπ ⊕ kerπ = W ⊕ W′.


# = h ·

l∈G

# □

One key step required to classify the irreducible representations of magnetic groups (G,ϕ) is to construct the induced representations of the core G0 ≤ G. Definition 1.11. Let (G,ϕ) be a finite magnetic point group and V a representation of the core group G0. The induced representation of V is the complex vector space

IndG(G,ϕ)

(1.18) V := C[G,ϕ] ⊗C[G0] V

0

