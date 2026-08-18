of f , denoted by c ( f ), as any directed S -path from u to v that utilizes only forward arcs from ( ).

▶ Definition 13 (certification of an arc set) . Consider an ordered partition P σ = ( V 1 ,...,V ℓ ) of an ordered tournament T σ and let F be a set of some backward arcs of T σ . We say that we can certify F whenever it is possible to find a set F = { c ( f ) : f ∈ F } of arc-disjoint certificates for the arcs in F .

▶ Definition 14 (safe partition) . Consider an ordered partition P σ = ( V 1 ,...,V ℓ ) of an ordered tournament T σ . Let B E denote the set of all backward arcs in A B ( T σ ,P σ ). For a vertex subset S ⊆ V ( T ), we say P σ is a S -safe partition if we can certify B E .

σ σ σ a minimum subset feedback arc set in the directed graph D σ . Specifically, given a directed graph D σ , and a vertex subset S ⊆ V σ , it refers to the cardinality of the smallest set F ⊆ A of arcs whose removal (or reversal) renders D σ S -acyclic. Given a tournament, for an arc subset A ′ ⊆ A [ T ], the directed graph T [ A ′ ] is defined by the subgraph T containing the arc set A ′ . More specifically, T [ A ′ ] = ( V ( T ) ,A ′ ). For a ease of notation, when the subset is clear to the context, we use Sfas ( D σ ) instead of Sfas ( D σ ).

▶ Lemma 15. Consider an ordered partition P σ = ( V 1 ,...,V ℓ ) of an ordered tournament T σ and a terminal set S ⊆ V ( T ) . If P σ is a S -safe partition then,

$$
Sfas(To) =
$$

Moreover, there exists a minimum sized S -feedback arc set of T σ containing B E , where B E denote the set of all backward arcs in A B ( T σ ,P σ ) .

Proof. A into A1 and Az, we have

$$
Sfas(To 2 Sfas(To[A1]) + Sfas(To [A2]) .
$$

Specifically, for the partition of

$$
Sfas(To_
$$

Next, we need to show that

$$
Sfas(To_
$$

This assertion holds because, after reversing all arcs in B E , each remaining directed S -cycle is contained within T σ [ V i ] for some i ∈ [ ℓ ]. In other words, once all arcs in B E are reversed, every S -cycle is entirely contained within T σ [ A I ( T σ ,P σ )]. Observe that as P σ is S -safe, the set of all backward arcs of A B ( T σ ,P σ ), i.e., B E can be certified using only arcs from A B ( T σ ,P σ ). This concludes the proof of the first part of the lemma. Essentially, we have shown the existence of a minimum-sized S -feedback arc set for T σ that includes B E . This completes the proof of the lemma. ◀

Construction of a S -safe partition. Recall that an S -triangle is a directed cycle of length three that includes at least one vertex from S . It is clear that the number of arc-disjoint S triangles provides a lower bound for the size of the smallest S -feedback arc set in a tournament. We illustrate how this set can be utilized to identify a safe partition in polynomial time.

