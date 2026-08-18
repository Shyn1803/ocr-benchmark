# 4.3 Proof of Upper Bound of Theorem 2

We aim to prove Theorem 2 by induction n . Clearly it is enough to show Theorem 2 for all induced subgraphs of Λ U . The base cases are when n ≤ 7, which are easily veriﬁed. For the inductive step, suppose n ≥ 8 and Λ U [ S ] is an n -vertex subgraph of Λ U with e edges. Additionally, suppose Λ U [ S ] has the maximum number of edges out of all n -vertex subgraphs of Λ U . The inductive hypothesis is that all n ′ -vertex subgraphs of Λ U , where 3 ≤ n ′ < n , have at most e ( n ′ ) edges.

Claim 15.

Proof. Λ U [ S ] must be connected, otherwise we could translate a connected component of Λ U [ S ] to form additional edges contradicting the maximality of Λ U [ S ]. Suppose Λ U [ S ] had a cut vertex v . When we remove v from Λ U [ S ] we create two connected components G 1 = Λ U [ S 1 ] and G 2 = Λ U [ S 2 ] with n 1 and n 2 vertices, and e 1 and e 2 edges. Case 1: n < 4 or n < 4 . Without loss of generality suppose n 3. If

1 2 1 ≤ n 1 = 1, there is 1 edge removed when deleting S 1 from Λ U [ S ]. Applying the inductive hypothesis to the remaining graph we obtain e ≤ e ( n − 1) + 1 ≤ e ( n ). So supposing that n 1 ∈ { 2 , 3 } , then there are at most 6 edges removed when deleting G 1 from Λ U . Then the inductive hypothesis implies

$$
< 6(n n1) = 4v6(n 96n 63 for n1 = 2,3 if n 2 6.
$$

Case 2: n 1 ,n 2 ≥ 4 . Applying the inductive hypothesis to G 1 and G 2 we obtain

$$
e < = 4v6n1 6 + 4v6n2 6 + deg(v) 6n = 6 = 4v6(n 5) 6 = 4v18 + deg(v) 6n1 6n2
$$

We can bound the degree of v by noticing the neighbourhood of v must be disconnected. It is easy to see through Menger’s theorem that the neighbourhood of v in Λ U is 4-connected, which implies that the degree of v in Λ U [ S ] is at most 8, hence

$$
6n 6 96n 63 for n 2 7. D
$$

Claim 16. We may assume there is no line parallel to an element in U intersecting Λ but disjoint from S , and with vertices from S on either side of the line.

Proof. Suppose there is such a line L . Since Λ U [ S ] is 2-connected there must be at least two edges of Λ U [ S ] that cross L . If L is parallel to a short edge (say parallel to g 1 ), the only edges of Λ U [ S ] that can cross L will be long edges perpendicular to L (in direction g 1 − 2 g 2 ). We shift a set of vertices on one side of the line towards L along one of the directions in U . This is depicted in Figure 11, where the part of S above L is shifted by − g 2 . Notice that each

