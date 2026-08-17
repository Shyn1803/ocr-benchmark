# 2 Simple Proof

This section presents a simple proof of the Apex Minor Theorem. The next lemma is the key. A centre of a graph G is a vertex α ∈ V ( G ) such that max { dist( α,v ) : v ∈ V ( G ) } is equal to the radius of G .

Lemma 10 Let A for some 2 € V(A) . Let G be an A-minor-free with radius r centre &Then G Q has no kr x kr minor. grid graph and grid

Proof. We proceed by induction on r . In the r = 0 case, V ( G − α ) = ∅ and the result holds. Now consider the radius r case, and assume the radius r − 1 case holds. Let

Suppose for the sake of contradiction that G − α has a k r × k r grid minor. Partition this k r × k r grid into k × k subgrids, so that contracting each subgrid to a vertex gives a k r − 1 × k r − 1 grid.

First suppose that some k × k subgrid is contained in V r . Thus H is a minor of G [ V r ] . By construction, G [ V 0 ∪ ··· ∪ V r − 1 ] is connected. Let G ′ be obtained from G by contracting V 0 ∪ ··· ∪ V r − 1 to a vertex w . Since every vertex in V r has a neighbour in V r − 1 , every vertex in G ′ is at distance at most 1 from w . Since H is a minor of G [ V r ] , A is a minor of G ′ and thus of G , which is a contradiction.

Now assume that every k Let G' be obtained from G subgrids. So every vertex in G' is at distance at most r _ 1 from Q, and G' contains a X the assumed truth of the r = 1 case kr-1 grid

minor . grid

Lemmas 2 and 10 imply that for every apex graph A with t vertices, every A -minor-free graph G with radius r has no (2 t − 2) r × (2 t − 2) r grid minor. Equation (1) implies that tw( G ) ∈ O ∗ ((2 t ) 9 r ) . This completes our simple proof of the Apex Minor Theorem by Eppstein [18] (Theorem 4).

# 3 Polynomial Upper Bound

This section proves Theorem 5 from Section 1. We need the following straightforward lemma.

G k × ℓ H ( B u : u ∈ V ( H )) in the 2 k × 2 ℓ grid J , such that for each vertex u ∈ V ( H ) there is a vertex h u in B u incident to no edge of J representing an edge of H .

