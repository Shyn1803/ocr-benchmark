# 56:2 Crossing Number of 3-Plane Drawings

that transforms one copy of an edge to another passes over a vertex. Interestingly, the upper bound for 3-planar graphs is tight in this more general setting only [4, 6].

The crossing number of a drawing Γ is the number of edge crossings in Γ. The crossing number cr(G) of a graph G is the minimum crossing number over all drawings of G. By definition every k-planar graph G admits a k-plane drawing and thus

cr(G) ≤

km 2

, (S)

where m denotes the number of edges in G. For a k-planar graph, this simple inequality connects upper bounds on the number of edges with lower bounds on the crossing number. Both of these come together in the well-known Crossing Lemma [2, Chapter 45], as the best constants in the Crossing Lemma are obtained by analyzing k-plane drawings [1, 6, 10, 11]. Conversely, combining the lower bound on cr(G) from the Crossing Lemma with an upper bound on cr(G) we obtain an upper bound on the number of edges in G. While (S) would work here, it is probably not an ideal choice because the graphs for which (S) is tight might be very different from those graphs that have a maximum number of edges, for any fixed n. For instance, for a 1-planar graph G we have cr(G) ≤ n − 2 [17, Proposition 4.4], which beats the bound we get by plugging m ≤ 4n − 8 into (S) by a factor of two. Can we obtain similar improvements by bounding cr(G) in terms of n, rather than m, for k ≥ 2?

Indeed, very recently it has been shown that cr(G) ≤ 3.3n if G is 2-planar and cr(G) ≤ 6.6n if G is 3-planar [3]. There is some indication that the bound for 2-planar graphs could be tight up to an additive constant, as it is achieved by the standard drawings of optimal 2-planar graphs (Figure 1). But the crossing number of these graphs is not known.

Figure 1 Construction by Pach and Tóth [15, Figure 3]. Left: A planar drawing with pentagonal faces. Right: To each pentagonal face all diagonals are added.

In contrast, there exists a family of simple 3-planar graphs with 5.5n − 15 edges whose standard drawings have 5.5n−21 crossings (Figure 2). Thus, there is a gap of 1.1n between the lower and the upper bound for the crossing number of 3-plane drawings.

<table>
  <tr>
    <td> </td>
    <td> </td>
    <td> </td>
  </tr>
  <tr>
    <td> </td>
    <td> </td>
    <td> </td>
  </tr>
</table>


Figure 2 Construction from [11, Figure 8]. Left: A cylinder with two layers, each consisting of three hexagonal faces. Right: To each face of a layer all but one diagonal is added. To the top and bottom face six diagonals are added. Missing diagonals are represented by dashed lines.

