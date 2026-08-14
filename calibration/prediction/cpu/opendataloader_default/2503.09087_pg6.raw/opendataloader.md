6 SHORTEST CIRCUITS IN HOMOLOGY CLASSES OF GRAPHS

v3

(a)

2 3 1

v4

1 2

v1 v2

1

v3

(b)

v4

v1 v2

Figure 1. An example for K4.

from v1. Initially we may let P follow either e14 or e12. Choose to follow e14. Keep extending P in this way, we may get P = e14e43e31e12e24e43e31. At this stage P is a circuit and the “while” loop is exited, and we have to translate P to ﬁnd a “non-saturated” vertex. The ﬁrst such a vertex we get is v4. By translation, now P becomes e43e31e12e24e43e31e14. Extending P, we will ﬁnally get a directionconsistent circuit C = e43e31e12e24e43e31e14e43e32e24 such that Cab = α.

3.2. Counting direction-consistent circuits: generalized BEST theorem. The well-known BEST theorem, named after de Bruijn and van Aardenne-Ehrenfest [vAEdB51] and Smith and Tutte [TS41], provides an eﬃcient algorithm of counting Eulerian cycles on an Eulerian digraph Go (meaning that the in-degree and out-degree at each vertex of Go are identical).

Recall that an arborescence T of Go with a root vertex w is a spanning tree of G such that all edges on T are oriented towards w with respect to o. Recall also that the Laplacian matrix of Go, denoted L(Go), is deﬁned as: (i) for i = j, (L(Go))ij is the negation of the number of positively oriented edges with respect to o with initial vertex vi and terminal vertex vj, and (ii) (L(Go))ii = − j =i(L(Go))ij. Removing the row and column of L(Go) with respect to w, we get the reduced Laplacian Lred(w)(Go) at w.

Denote by ec(G,o) the number of Eulerian cycles on Go, and Inw(G,o) the number of arborescences Go rooted at w. Then the BEST theorem states that ec(G,o) = Inw(G,o)· v∈V(G)(deg+o (v)−1)! where deg+o (v) is the out-degree of Go at v ∈ V (G). Note that by a directed version of Kirchhoﬀ’s matrix-tree theorem, Inw(G,o) is actually independent of w, and can be eﬃciently computed as the determinant of the reduced Laplacian matrix Lred(w)(Go).

Before making a generalization of the BEST theorem, we ﬁrst introduce a notion of weighted Laplacian here. Deﬁnition 3.5. Consider a graph G. Let α ∈ C1(G,Z) be universal. Let ce = degα(e) for all e ∈ E(G). Then α = e∈E

o(α)(G) ce · e with all ce > 0. The weighted Laplacian Lα(G) of G with respect to α is deﬁned as: (Lα(G))ij = − e∈E

o(α)(G),e(0)=vi,e(1) =vi ce for all diagonal entries. Removing the row and column of Lα with respect to w, we get the reduced weighted Laplacian Lred(α w)(G).

o(α)(G),e(0)=vi,e(1)=vj ce for all i = j, and (Lα(G))ii = e∈E

