Lemma 5.3. There is an no such that the following holds for all n > no, 2 2Ort. can find either 2-9

| U | 10 r pairwise vertex-disjoint stars of size t , whose centers are in U and whose leaves are in V ( G ) − U , or

(b)

ε | U | 2(log n ) c and

and every vertex in U has degree at most 2 t in H .

Proof. Take a maximal collection C of pairwise vertex-disjoint stars in G with t leaves, centres in U and leaves outside of U . Let C ⊆ U be the set of centres of these stars and L ⊆ V ( G ) − U be the set consisting of all their leaves. Suppose a) does not hold. Then we can assume that | C | ≤ | U | 10 r and thus | L | = | C | · t ≤ | U | 10 r · t , and, by the maximality of C , that there is no vertex in U − C with at least t neighbours in G in V ( G ) − ( U ∪ L ). Thus,

$$
JU| 6
$$

We now construct a set X ⊆ V ( G ) − U and a bipartite subgraph H with vertex classes U and X using the following process, starting with X 0 = ∅ and setting H 0 to be the graph with vertex set U ∪ X 0 and no edges. Let k = | V ( G ) − U | and label the vertices of V ( G ) − U arbitrarily as v 1 ,...,v k . For each i ≥ 1, if possible, pick a star S i in G with centre v i and r leaves in U such that the vertices in U in the graph H i − 1 ∪ S i have degree at most 2 t , and let H i = H i − 1 ∪ S i and X i = X i − 1 ∪ { v i } , while otherwise we set H i = H i − 1 and X i = X i − 1 . Finally, let H = H k and X = X k = V ( H k ) − U . We will now show that b) holds for this choice of H (with vertex classes U and X ).

Firstly, observe that every vertex of U has degree at most 2 t in H i for each i ∈ [ k ] by construction, and that every vertex v i in X has degree exactly r in H , so the second condition in b) holds. Thus, we only need to show that | X | ≥ ε | U | 2(log n ) c holds.

To see this, let U ′ be the set of vertices in U − C with degree exactly 2 t in H . As each vertex in U − C has fewer than t neighbours in G in X − L (due to the maximality of the collection of stars C ), the vertices in U ′ must have at least t neighbours in H in X ∩ L . As each vertex in X ∩ L has r neighbours in H , we have

$$
rIXnLl JUL t t t 10r 10
$$

Let B = C ∪ U ′ , so that

$$
1Or 10 2
$$

slU _ BI Then; by Proposition 5.2 to U _ B with d = r. 2r Or B)| 2 As applied

$$
slU _ BI 2 5t|U| 2r 4r
$$

the former inequality contradicts ( 6 ), so we have that | N G,r ( U − B ) | ≥ ε | U − B | (log n ) c . Every vertex v i in N G,r ( U − B ) has at least r neighbours in G in U − B , and vertices of U − B must all have degree strictly less than 2 t in H (as they are not in U ′ ). This implies that every v i in N G,r ( U − B ), satisfies v i ∈ X , since we could add it along with some r

as required.

$$
(log n)c 2(log n)-
$$

