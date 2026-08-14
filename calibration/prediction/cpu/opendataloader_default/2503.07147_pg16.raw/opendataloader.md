Lemma 5.3. There is an n0 such that the following holds for all n ≥ n0, 2−9 < ε < 1, c > 0, r,t ≥ (log n)2 and s ≥ 20rt. Let G be an n-vertex (ε,c,s)-expander, let U ⊆ V (G) satisfy |U| ≤ 2n/3. Then, in G we can find either

- (a) 10|Ur| pairwise vertex-disjoint stars of size t, whose centers are in U and whose leaves are in V (G) − U, or

- (b) a bipartite subgraph H with vertex classes U and X ⊆ V (G) − U such that


- • |X| ≥ 2(logε|Un|)c and

- • every vertex in X has degree at least r in H and every vertex in U has degree at most 2t in H.


Proof. Take a maximal collection C of pairwise vertex-disjoint stars in G with t leaves, centres in U and leaves outside of U. Let C ⊆ U be the set of centres of these stars and L ⊆ V (G) − U be the set consisting of all their leaves. Suppose a) does not hold. Then we can assume that |C| ≤ 10|Ur| and thus |L| = |C| · t ≤ 10|Ur| · t, and, by the maximality of C, that there is no vertex in U − C with at least t neighbours in G in V (G) − (U ∪ L). Thus,

|U| 10r

|NG(U − C)| ≤ |C| + |L| + |U − C| · t ≤

+ |C| · t + |U − C| · t < 2|U| · t. (6)

We now construct a set X ⊆ V (G)−U and a bipartite subgraph H with vertex classes U and X using the following process, starting with X0 = ∅ and setting H0 to be the graph with vertex set U∪X0 and no edges. Let k = |V (G)−U| and label the vertices of V (G) − U arbitrarily as v1,...,vk. For each i ≥ 1, if possible, pick a star Si in G with centre vi and r leaves in U such that the vertices in U in the graph Hi−1 ∪ Si have degree at most 2t, and let Hi = Hi−1 ∪ Si and Xi = Xi−1 ∪ {vi}, while otherwise we set Hi = Hi−1 and Xi = Xi−1. Finally, let H = Hk and X = Xk = V (Hk) − U. We will now show that b) holds for this choice of H (with vertex classes U and X).

Firstly, observe that every vertex of U has degree at most 2t in Hi for each i ∈ [k] by construction, and that every vertex vi in X has degree exactly r in H, so the second condition in b) holds. Thus, we only need to show that |X| ≥ 2(logε|Un|)c holds.

To see this, let U′ be the set of vertices in U − C with degree exactly 2t in H. As each vertex in U − C has fewer than t neighbours in G in X − L (due to the maximality of the collection of stars C), the vertices in U′ must have at least t neighbours in H in X ∩ L. As each vertex in X ∩ L has r neighbours in H, we have

r|X ∩ L| t ≤

|U| · t 10r

= |U| 10

r t · |L| ≤

r t ·

|U′| ≤

.

Let B = C ∪ U′, so that

|U| 10r

+ |U| 10 ≤

|U| 2

|B| ≤

,

and, thus, |U − B| ≥ |U2|. Then, by Proposition 5.2 applied to U − B with d = r, we have either |NG(U − B)| ≥ s|U2−rB| or |NG,r(U − B)| ≥ ε|U−B| (logn)c . As

s|U − B| 2r ≥

s|U| 4r ≥ 5t|U|,

the former inequality contradicts (6), so we have that |NG,r(U − B)| ≥ ε(log|U−nB)c|. Every vertex vi in NG,r(U − B) has at least r neighbours in G in U − B, and vertices of U − B must all have degree strictly less than 2t in H (as they

are not in U′). This implies that every vi in NG,r(U − B), satisfies vi ∈ X, since we could add it along with some r of its neighbours while constructing H. Hence, NG,r(U − B) ⊆ X, and

ε|U| 2(log n)c

ε|U − B| (log n)c ≥

|X| ≥ |NG,r(U − B)| ≥

,

as required.

<table>
  <tr>
    <td> </td>
  </tr>
</table>


16

