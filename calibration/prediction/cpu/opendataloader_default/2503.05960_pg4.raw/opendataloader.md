4 DANIEL BUMP AND SLAVA NAPRIEKO

We thank Amol Aggarwal, Andrew Hardt and Travis Scrimshaw for helpful conversations about the groupoid.

2. Groupoids

A groupoid is a set G with a partially deﬁned composition. This consists of a map µ : S −→ G, where S is a subset of G ×G. If a, b ∈ G we say that the product a⋆b is deﬁned if (a, b) ∈ S, and then we write a⋆b = µ(a, b). The groupoid is also required to have an “inverse map” x  → x′ from G → G. The inverse map is more commonly denoted as x  → x−1, but we will be concerned with a groupoid whose elements are matrices, and we will reserve the notation x−1 for the matrix inverse. The following axioms are required.

- Axiom 1 (Associative Law). If a ⋆ b and b ⋆ c are deﬁned then (a ⋆ b) ⋆ c and a ⋆ (b ⋆ c) are deﬁned, and they are equal.

We say that a⋆b⋆c is deﬁned if a⋆b and b⋆c are deﬁned, and then we denote (a⋆b)⋆c = a ⋆ (b ⋆ c) as a ⋆ b ⋆ c.

- Axiom 2 (Inverse). The compositions a ⋆ a′ and a′ ⋆ a are always deﬁned. Thus if a ⋆ b is deﬁned, then a⋆b⋆b′ is deﬁned, and this is required to equal a. Similarly a′ ⋆a⋆b is deﬁned, and this is required to equal b.


Example 2.1. A category C is small if its class of objects is a set. A small category is a groupoid category if every morphism is an isomorphism. Assuming this, the disjoint union

G =

Hom(A, B)

A,B∈C

is a groupoid, with the ⋆ operation being composition: thus if a ∈ Hom(A, B) and b ∈ Hom(C, D), then a ⋆ b is deﬁned if and only if B = C. The groupoid axioms are clear.

- Lemma 2.2. In a groupoid, we have (a′)′ = a. Moreover if a ⋆ b is deﬁned then so is b′ ⋆ a′ and (a ⋆ b)′ = b′ ⋆ a′.

Proof. Since (a′)′⋆a′ and a′⋆a are both deﬁned, by the Associative Law the product (a′)′⋆a′⋆a is deﬁned, and using the Inverse Axiom, this equals both (a′)′ and a. For the second assertion, assume a ⋆ b is deﬁned. It follows from the axioms that

(a ⋆ b)′ = (a ⋆ b)′ ⋆ a ⋆ b ⋆ b′ ⋆ a′ = b′ ⋆ a′. Given a groupoid G, let us say an element A is idempotent if A⋆A is deﬁned and A⋆A = A.

- Lemma 2.3. An element A ∈ G is an idempotent if and only if A = g ⋆ g′ for some g ∈ G. If A is idempotent then A = A′.

Proof. It is easy to check that g ⋆ g′ is idempotent. Conversely if A is idempotent, then A = A⋆A′ since A = A⋆A = A⋆A⋆A′ = A⋆A′, and so A can be written g ⋆g′ with g = A. Now if A = g ⋆ g′ then A = A′ as a consequence of Lemma 2.2.

- Lemma 2.4. If g ∈ G then there are unique idempotents A and B such that g = g ⋆ A and g = B ⋆ g.


Proof. We can take A = g′ ⋆ g, and this is an idempotent such that g ⋆ A = g. Conversely if A′ is any other element such that g ⋆ A′ = g, then g−1 ⋆ g = g−1 ⋆ g ⋆ A′ = A′, so A′ = A. The statements about B are proved similarly.

