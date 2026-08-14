# 12 Geometric Realizations of Dichotomous Ordinal Graphs

respective circles intersect on ℓk+1. Observe that with this operation, the minimum distance between any two vertices is still d.

Next, we process first pairs. Observe that no vertex can be involved in several first pairs. Otherwise it is not on the outer face. However, a vertex can be contained in a first and another pair and it is also possible that a vertex closing another face is contained in a first pair. So some of the vertices might already have a fixed position. However, it is not possible that both vertices of a first pair are contained in another pair or close a face. Otherwise, the predecessor of the first pair was an internal vertex. So, we first process the first pairs that share a vertex with another pair or where one of its vertices close a face and reduce their distance to d. Then we can also process all the other first pairs. In the end all pairs have distance d and d is still the minimum distance between any two vertices on ℓk+1. This concludes the construction for Items 1 and 2.

The strips are defined as follows: Let u ∈ Vk−1 and let v1,...,vh be the children of u from left to right. We partition the strip Su into the strips Sv

by splitting Su at an arbitrary spot between xrv

,...,Sv

1

h

, for i = 2,...,h. If a vertex has two parents then its strip is the union of the two portions obtained from its parents.

and xℓv

i−1

i

By construction, all edges of Gs have length at most one. It remains to show that edges in Eℓ have length greater than one. So let wjwk ∈ Eℓ with wj ∈ Vj, wk ∈ Vk, and

- j ≤ k. Since G is bipartite, we can exclude k = j and k = j + 2. If k − j ≥ 3 then yk − yj > k − 1 − j ≥ 2. Hence, the distance between wj and wk is greater than one. If
- k − j = 1 then the parent w if wk is in Vj. By construction, we know that the distance between wj and any child of w is greater than one. ◀


longest possible short edge

3n2

2n2

n2

n2 2n2 3n2

shortest possible long edge

Figure 8 For each grid point (i, j), 1 ≤ i ≤ n, 1 ≤ j ≤ n there are four possible points. If i > 1, the x-coordinate is in2 if the edge between (i − 1, j) and (i, j) is short and in2 + i otherwise. If j > 1, the y-coordinate is jn2 if the edge between (i, j − 1) and (i, j) is short and jn2 + j otherwise.

▶ Theorem 9. A dichotomous ordinal graph G = (V,Es ∪ Eℓ) admits a geometric realization if the set of short edges induces a subgraph of the grid.

Proof. Extend Gs = (V,Es) by the remaining grid edges and require the new edges to be long. We now perturb the grid. For each grid point (i,j), 1 ≤ i ≤ n, 1 ≤ j ≤ n of the original grid, there are four possible choices with the x-coordinates in2 or in2 + i and the y-coordinates jn2 or jn2 + j. See Fig. 8. In the case where i = 1 choose as x-coordinate n2 or n2 + 1. Similarly, if j = 1 choose as y-coordinate n2 or n2 + 1. If i > 1, we choose the x-coordinate in2 if the edge between (i − 1,j) and (i,j) is short and in2 + i otherwise.

