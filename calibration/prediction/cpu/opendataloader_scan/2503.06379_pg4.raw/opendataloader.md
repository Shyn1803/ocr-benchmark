# 2 Homotopy of C p ( G )

In this section, we review some of the standard facts of order complexes of posets. See the ﬁrst two parts of Smith’s book[9] for more details.

Let ( P , ≤ ) be a poset (short for partially ordered set). The order complex ∆ P of P consists of all ﬁnite chains in P , including the empty set. The chain of length i in P consisting of i + 1 elements is called an i -simplex in ∆ P . In particular, the empty set ∅ is the ( − 1) -simplex. It is well-known that such (abstract) simplicial complex ∆ P can be embedded into a Euclidean topological space as a subspace denoted by | ∆ P| , so-called the geometric realization of ∆ P . We abbreviate | ∆ P| as |P| here.

A poset map f : ( P , ≤ P ) → ( Q , ≤ Q ) of posets P , Q , is a set-theoretical map such that x ≤ P y implies f ( x ) ≤ Q f ( y ) . It is routine to check that a poset map f : P → Q naturally induces a simplicial map ∆ f between order complexes ∆ P and ∆ Q , and f also induces a continuous map | f | : |P| → |Q| . The following lemma gives a suﬃcient condition for the homotopy between two continuous maps induced by poset maps.

Lemma 2. [9, Lemma 3.1.7] Suppose that f, g : P → Q satisfy f, g are poset maps with f ≤ g , that is, f ( x ) ≤ g ( x ) for each x ∈ P . Then f and g are homotopic, that is, | f | , | g | : |P| → |Q| are homotopic.

Recall that topological spaces X and Y are homotopy equivalent if there are continuous maps f : X → Y and g : Y → X whose compositions satisfy the homotopies g ◦ f ≃ Id X and f ◦ g ≃ Id Y . For posets P , Q , P and Q are said to be homotopy-equivalent if |P| and |Q| are homotopy-equivalent, simply denoted by P ≃ Q .

For a prime p and a group G , we denote

$$
Ip(G) = P; € Sylp(G) for all 1 < i < s, and s 2 1}
$$

by the set of all intersections of some Sylow p -subgroups of G .

Lemma 3. Let G be a group and p be a prime. Write

$$

$$

Then C p ( G ) is homotopy-equivalent to C ( I p ( G )) .

Proof.

$$
f (Hs) : 0 P 1 HCPeSylp (G) HSPeSylp(G)
$$

