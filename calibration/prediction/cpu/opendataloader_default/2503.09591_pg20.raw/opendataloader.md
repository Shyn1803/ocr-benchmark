4.3 Proof of Upper Bound of Theorem 2

We aim to prove Theorem 2 by induction n. Clearly it is enough to show Theorem 2 for all induced subgraphs of ΛU. The base cases are when n ≤ 7, which are easily veriﬁed. For the inductive step, suppose n ≥ 8 and ΛU[S] is an n-vertex subgraph of ΛU with e edges. Additionally, suppose ΛU[S] has the maximum number of edges out of all n-vertex subgraphs of ΛU. The inductive hypothesis is that all n′-vertex subgraphs of ΛU, where 3 ≤ n′ < n, have at most e(n′) edges.

- Claim 15. We may assume ΛU[S] is 2-connected.

Proof. ΛU[S] must be connected, otherwise we could translate a connected component of ΛU[S] to form additional edges contradicting the maximality of ΛU[S]. Suppose ΛU[S] had a cut vertex v. When we remove v from ΛU[S] we create two connected components G1 = ΛU[S1] and G2 = ΛU[S2] with n1 and n2 vertices, and e1 and e2 edges.

Case 1: n1 < 4 or n2 < 4. Without loss of generality suppose n1 ≤ 3. If n1 = 1, there is 1 edge removed when deleting S1 from ΛU[S]. Applying the inductive hypothesis to the remaining graph we obtain e ≤ e(n − 1) + 1 ≤ e(n). So supposing that n1 ∈ {2,3}, then there are at most 6 edges removed when deleting G1 from ΛU. Then the inductive hypothesis implies

e ≤ 6(n − n1) − 4 6(n − n1) − 6 + 6 ≤ 6n −

![](<2503.09591_pg20_images/imageFile1.png>)

√96n − 63 for n1 = 2,3 if n ≥ 6. Case 2: n1,n2 ≥ 4. Applying the inductive hypothesis to G1 and G2 we

![](<2503.09591_pg20_images/imageFile2.png>)

obtain

e ≤ 6n1 − 4√6n1 − 6 + 6n2 − 4√6n2 − 6 + deg(v) ≤ 6n − 6 − 4 6(n − 5) − 6 − 4

![](<2503.09591_pg20_images/imageFile3.png>)

![](<2503.09591_pg20_images/imageFile4.png>)

![](<2503.09591_pg20_images/imageFile5.png>)

√

![](<2503.09591_pg20_images/imageFile6.png>)

18 + deg(v).

We can bound the degree of v by noticing the neighbourhood of v must be disconnected. It is easy to see through Menger’s theorem that the neighbourhood of v in ΛU is 4-connected, which implies that the degree of v in ΛU[S] is at most 8, hence

e ≤ 6n − 6 − 4 6(n − 5) − 6 − 4

![](<2503.09591_pg20_images/imageFile7.png>)

√

![](<2503.09591_pg20_images/imageFile8.png>)

24 + 8 ≤ 6n −

√96n − 63 for n ≥ 7.

![](<2503.09591_pg20_images/imageFile9.png>)

![](<2503.09591_pg20_images/imageFile10.png>)

![](<2503.09591_pg20_images/imageFile11.png>)

![](<2503.09591_pg20_images/imageFile12.png>)

![](<2503.09591_pg20_images/imageFile13.png>)

- Claim 16. We may assume there is no line parallel to an element in U intersecting Λ but disjoint from S, and with vertices from S on either side of the line.


Proof. Suppose there is such a line L. Since ΛU[S] is 2-connected there must be at least two edges of ΛU[S] that cross L. If L is parallel to a short edge (say parallel to g1), the only edges of ΛU[S] that can cross L will be long edges perpendicular to L (in direction g1 − 2g2). We shift a set of vertices on one side of the line towards L along one of the directions in U. This is depicted in Figure 11, where the part of S above L is shifted by −g2. Notice that each

20

