) with r ≥ 2. We add a new hyperplane h to A(H). Let Ai and Ai+1 be the corresponding arrangement before and after h is added, respectively. For each cell cj in Ai, we denote the corresponding cell in Ai+1 by c¯j. If cj ̸= c¯j, we denote the two connected cells that bisect c¯j by c′j and c′′j , respectively. We show that there exists a (vc¯

be two nodes in G(A(H)) connected by a path P = (vc

vc

,...,vc

1

r

r

)-path P′ in G(Ai+1). First, let c1 = c¯1. If c2 = c¯2, we can choose P′ = (vc

,vc¯

1

2

). If c2 ̸= c¯2, the connectivity of c′2 and c′′2 ensures that we can choose P′ ∈ (vc

,vc

1

2

),(vc

) .

,vc′2

,vc′′2

1

1

Second, let c1 ̸= c¯1. As c1 and c2 are connected in G(Ai), it follows that c′1 or c′′1 is connected to c¯2 in G(Ai+1). In the first case, we can choose P′ ∈ (vc′1

) depending on whether c2 is divided by h or not. In the second case, we can replace c′1 by c′′1 and obtain the sought path. Inductively, there exists a (vc¯

),(vc′1

),(vc′1

,vc

,vc′2

,vc′′2

2

)-path P′ in G(Ai+1) and the claim follows.

,vc¯

1

r

<table>
  <tr>
    <td> </td>
  </tr>
</table>


The graph connectivity ensures that, starting from any node vc′, all nodes vc in G(A(H=)) can be reached using a breadth-first search. The choice of the incidence graph G(A(H=)) prevents us from reaching nodes that do not belong to a cell of A(H=). The incidence graph G(A(H=)) can be easily derived from the incidence lattice G′(A(H=)) constructed in the algorithm of Edelsbrunner et al. (1986) to compute the arrangement A(H=). If two cells c1 and c2 share a common face f of dimension p − 1, there exists a node vf′ in G′(A(H=)) and an edge from vf′ to each of the nodes vc′

belonging to the cells c1 and c2. In G(A(H=)), there is an edge between vc

and vc′

1

2

and we store the information to which separating hyperplane h(e,f) this edge belongs. This requires constant time per face of dimension p−1 and, thus, the graph G(A(H=)) can be obtained in time linear in the number of faces of dimension p − 1 of A(H=) from G′(A(H=)). Of course, we store the representative point from the relative interior of each cell. We are now ready to state our improved algorithm.

and vc

1

2

Theorem 3.6. Let p ≥ 2. Algorithm 2 solves the p-parametric matroid problem in time O(m2pf(m)).

15

