![](<2503.09087_pg6_images/imageFile1.png>)

03

04

![](<2503.09087_pg6_images/imageFile2.png>)

U1

Figure 1. An example for K 4 .

from v 1 . Initially we may let P follow either e 14 or e 12 . Choose to follow e 14 . Keep extending P in this way, we may get P = e 14 e 43 e 31 e 12 e 24 e 43 e 31 . At this stage P is a circuit and the “while” loop is exited, and we have to translate P to ﬁnd a “non-saturated” vertex. The ﬁrst such a vertex we get is v 4 . By translation, now P becomes e 43 e 31 e 12 e 24 e 43 e 31 e 14 . Extending P , we will ﬁnally get a directionconsistent circuit C = e 43 e 31 e 12 e 24 e 43 e 31 e 14 e 43 e 32 e 24 such that C ab = α .

# 3.2. Counting direction-consistent circuits: generalized BEST theorem.

The well-known BEST theorem, named after de Bruijn and van Aardenne-Ehrenfest [vAEdB51] and Smith and Tutte [TS41], provides an eﬃcient algorithm of counting Eulerian cycles on an Eulerian digraph G o (meaning that the in-degree and out-degree at each vertex of G o are identical).

Recall that an arborescence T of G o with a root vertex w is a spanning tree of G such that all edges on T are oriented towards w with respect to o . Recall also that the Laplacian matrix of G o , denoted L ( G o ), is deﬁned as: (i) for i   = j , ( L ( G o )) ij is the negation of the number of positively oriented edges with respect to o with initial vertex v i and terminal vertex v j , and (ii) ( L ( G o )) ii = −   j   = i ( L ( G o )) ij . Removing the row and column of L ( G o ) with respect to w , we get the reduced Laplacian L red( w ) ( G o ) at w . o o

Denote by ec( G, ) the number of Eulerian cycles on G o , and In w ( G, ) the number of arborescences G o rooted at w . Then the BEST theorem states that ec( G, o ) = In w ( G, o ) ·   v ∈ V ( G ) (deg + o ( v ) − 1)! where deg + o ( v ) is the out-degree of G o at v ∈ V ( G ). Note that by a directed version of Kirchhoﬀ’s matrix-tree theorem, In w ( G, o ) is actually independent of w , and can be eﬃciently computed as the determinant of the reduced Laplacian matrix L red( w ) ( G o ).

Before making a generalization of the BEST theorem, we ﬁrst introduce a notion of weighted Laplacian here.

Deﬁnition 3.5. Consider a graph G . Let α ∈ C 1 ( G, Z ) be universal. Let c e = deg α ( e ) for all e ∈ E ( G ). Then α =   e ∈ E o ( α ) ( G ) c e · e with all c e > 0. The weighted Laplacian L α ( G ) of G with respect to α is deﬁned as: ( L α ( G )) ij = −   e ∈ E o ( α ) ( G ) , e (0)= v i , e (1)= v j c e for all i   = j , and ( L α ( G )) ii =   e ∈ E o ( α ) ( G ) , e (0)= v i , e (1)   for all diagonal entries. Removing the row and column of L α with respect to w , we get the reduced weighted Laplacian L red( w ) α ( G ).

