# 2 Simple Proof

This section presents a simple proof of the Apex Minor Theorem. The next lemma is the key. A centre of a graph G is a vertex α ∈ V (G) such that max{dist(α,v) : v ∈ V (G)} is equal to the radius of G.

- Lemma 10. Let A be a planar graph such that A − z is a minor of the k × k grid for some z ∈ V (A). Let G be an A-minor-free graph with radius r and centre α. Then G − α has no kr × kr grid minor.

Proof. We proceed by induction on r. In the r = 0 case, V (G − α) = ∅ and the result holds. Now consider the radius r case, and assume the radius r − 1 case holds. Let Vi := {x ∈ V (G) : distG(x,α) = i} for i ∈ {0,...,r}. So V0 = {α} and V0 ∪···∪Vr = V (G). Suppose for the sake of contradiction that G − α has a kr × kr grid minor. Partition this kr × kr grid into k × k subgrids, so that contracting each subgrid to a vertex gives a kr−1 × kr−1 grid.

First suppose that some k × k subgrid is contained in Vr. Thus H is a minor of G[Vr]. By construction, G[V0 ∪ ··· ∪ Vr−1] is connected. Let G′ be obtained from G by contracting V0 ∪ ··· ∪ Vr−1 to a vertex w. Since every vertex in Vr has a neighbour in Vr−1, every vertex in G′ is at distance at most 1 from w. Since H is a minor of G[Vr], A is a minor of G′ and thus of G, which is a contradiction.

Now assume that every k × k subgrid intersects V1 ∪ ··· ∪ Vr−1. Let G′ be obtained from G by contracting each subgrid to a vertex, and deleting any vertices in Vr not in one of the subgrids. So every vertex in G′ is at distance at most r − 1 from α, and G′ − α contains a kr−1 × kr−1 grid minor. Since G′ is a minor of G, G′ is A-minor-free. Hence G′ contradicts the assumed truth of the r − 1 case.

Therefore, G − α has no kr × kr grid minor.

<table>
  <tr>
    <td> </td>
  </tr>
</table>


Lemmas 2 and 10 imply that for every apex graph A with t vertices, every A-minor-free graph G with radius r has no (2t − 2)r × (2t − 2)r grid minor. Equation (1) implies that tw(G) ∈ O∗((2t)9r). This completes our simple proof of the Apex Minor Theorem by Eppstein [18] (Theorem 4).

3 Polynomial Upper Bound

This section proves Theorem 5 from Section 1. We need the following straightforward lemma.

- Lemma 11. If a graph G is a minor of the k × ℓ grid, then there is an H-model (Bu : u ∈ V (H)) in the 2k × 2ℓ grid J, such that for each vertex u ∈ V (H) there is a vertex hu in Bu incident to no edge of J representing an edge of H.


5

