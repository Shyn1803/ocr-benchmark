respective circles intersect on ℓ k +1 . Observe that with this operation, the minimum distance between any two vertices is still d .

Next, we process first pairs. Observe that no vertex can be involved in several first pairs. Otherwise it is not on the outer face. However, a vertex can be contained in a first and another pair and it is also possible that a vertex closing another face is contained in a first pair. So some of the vertices might already have a fixed position. However, it is not possible that both vertices of a first pair are contained in another pair or close a face. Otherwise, the predecessor of the first pair was an internal vertex. So, we first process the first pairs that share a vertex with another pair or where one of its vertices close a face and reduce their distance to d . Then we can also process all the other first pairs. In the end all pairs have distance d and d is still the minimum distance between any two vertices on ℓ k +1 . This concludes the construction for Items 1 and 2.

The strips are defined as follows: Let u ∈ V k − 1 and let v 1 ,...,v h be the children of u from left to right. We partition the strip S u into the strips S v 1 ,...,S v h by splitting S u at an arbitrary spot between x r v i − 1 and x ℓ v i , for i = 2 ,...,h . If a vertex has two parents then its strip is the union of the two portions obtained from its parents.

By construction, all edges of G s have length at most one. It remains to show that edges in E ℓ have length greater than one. So let w j w k ∈ E ℓ with w j ∈ V j , w k ∈ V k , and j ≤ k . Since G is bipartite, we can exclude k = j and k = j + 2. If k − j ≥ 3 then y k − y j > k − 1 − j ≥ 2. Hence, the distance between w j and w k is greater than one. If k − j = 1 then the parent w if w k is in V j . By construction, we know that the distance between w j and any child of w is greater than one. ◀

Figure 8 For each grid

# longest possible short edge

![](<2503.07361_pg12_images/imageFile1.png>)

3 n 2

2 n 2

2 n 2

3 n 2

shortest possible long edge

▶ Theorem 9. A dichotomous ordinal graph G = ( V,E s ∪ E ℓ ) admits a geometric realization if the set of short edges induces a subgraph of the grid.

Proof. Extend G s = ( V,E s ) by the remaining grid edges and require the new edges to be long. We now perturb the grid. For each grid point ( i,j ), 1 ≤ i ≤ n , 1 ≤ j ≤ n of the original grid, there are four possible choices with the x-coordinates in 2 or in 2 + i and the y-coordinates jn 2 or jn 2 + j . See Fig. 8. In the case where i = 1 choose as x-coordinate n 2 or n 2 + 1. Similarly, if j = 1 choose as y-coordinate n 2 or n 2 + 1. If i > 1, we choose the x-coordinate in 2 if the edge between ( i − 1 ,j ) and ( i,j ) is short and in 2 + i otherwise.

