# 7 Additional families of graphs

## 7.1 Asteroidal triple-free graphs

An asteroidal triple in a graph G is a set T of 3 vertices such that G[T] is independent and every pair of vertices in T can be joined by a path that avoids the neighborhood of the third vertex in T. A graph G is asteroidal triple-free (AT-free) if G does not contain an asteroidal triple. Various classes of graphs are known to be AT-free, for example, interval graphs, cocomporability graphs and permutation graphs (see e.g. [COS97]). We show that all these classes have a bounded ratio by proving the following theorem.

- Theorem 7.1. For every asteroidal triple-free graph G, we have γ(G) ⩽ 3 · ρ(G). Proof. Our proof is based on the following property.
- Theorem 7.2. [COS97] Every connected asteroidal triple-free graph contains a pair of vertices such that any path between this pair of vertices is dominating.

Let G be an AT-free graph. By Theorem 7.2 there is a pair of vertices u,v ∈ V (G) such that any path between u and v is dominating. Let Π = π1,π2,...,πp be the shortest path between u and v. Thus, we have γ(G) ⩽ p. On the other hand as Π is a shortest path in G, by taking the set of vertices {π3i+1 | 0 ⩽ i ⩽ ⌊p/3⌋ − 1} we get a packing in G. Therefore, ρ(G) ⩾ ⌊p/3⌋ ⩾ ⌊γ(G)/3⌋.

<table>
  <tr>
    <td> </td>
  </tr>
</table>


7.2 Convex graphs

A bipartite graph G = (X ∪ Y,E) is convex if and only if one of the color classes, without loss of generality X, has an ordering such that for all y ∈ Y the vertices adjacent to y are consecutive in the ordering. We refer to this ordering as convex ordering.

- Theorem 7.3. For every convex graph G, we have γ(G) ⩽ 3 · ρ(G).


Proof. We can assume that G does not have an isolated vertex. We will encode convex graphs using points and intervals in R. In particular, if the convex ordering of X is x1,...,xn, we use the embedding π : X → R defined as π(xi) = i, and for each y ∈ Y , we associate the interval ι(y) = {π(x) : x ∈ NG(y)}, see Figure 4 for an illustration. For subsets X′ ⊆ X and Y ′ ⊆ Y , we use the notation π(X′) = π(x) : x ∈ X′ and ι(Y ′) = ι(y) : y ∈ Y ′ . In this encoding, the image of a set S ⊆ V (G) is a union of points and intervals, corresponding to the vertices in S ∩ X and S ∩ Y , respectively.

ι(y4)

x1 x2 x3 x4 x5 x6 x7 x8

ι(y3)

ι(y5)

ι(y1) ι(y2)

1 2 3 4 5 6 7 8

=

=

=

=

=

=

=

=

y1 y2 y3 y4 y5

π(x5)

π(x6)

π(x7)

π(x8)

π(x1)

π(x2)

π(x3)

π(x4)

Figure 4: The embeddings π and ι.

16

