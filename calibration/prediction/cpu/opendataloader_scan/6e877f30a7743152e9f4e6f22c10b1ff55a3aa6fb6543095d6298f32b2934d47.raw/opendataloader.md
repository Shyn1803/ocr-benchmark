Before we formally introduce this, we require the notion of computation tree and introduce some more notations. Deﬁnition 1: [16] A computation tree corresponding to a

message-passing decoder of the Tanner graph G is a tree that is constructed by choosing an arbitrary variable node in G as its root and then recursively adding edges and leaf nodes to the tree that correspond to the messages passed in the decoder up to a certain number of iterations. For each vertex that is added to the tree, the corresponding node update function in G is also copied. Let G be the Tanner graph of a 3-left-regular code. Let H

be the induced subgraph of a trapping set ( a,b ) contained in G with variable node set P ⊆ V and check node set W ⊆ C . Let N ( u ) denote the set of neighbors of a node u . Let T k i ( G ) be the computation tree of graph G corresponding to a decoder F enumerated for k iterations with variable node v i ∈ V as its root. Let W   ⊆ W denote the set of degree-one check nodes in the subgraph H . Let P   ⊆ P denote the set of variable nodes in H where each variable node has at least one neighbor in W   . During decoding on G , for a node v i ∈ P   , let µ l denote the message that v i receives from its neighboring degree-one check node in H in the l th iteration. k

Deﬁnition 2: A vertex w ∈ T i ( G ) is said to be a descendant of a vertex u ∈ T k i ( G ) if there exists a path starting from vertex w to the root v i that traverses through vertex u . The set of all descendants of the vertex u in T k i ( G ) is denoted as D ( u ) . For a given vertex set U , D ( U ) (with some abuse of notation) denotes the set of descendants of all u ∈ U . k

Deﬁnition 3: T i ( H ) is called the computation tree of the subgraph H enumerated for k iterations for the decoder F , if ∀ c j ∈ W   , µ l is given for all l ≤ k , and if the root node v i ∈ P requires only the messages computed by the nodes in H and µ l to compute its binary hard-decision value. Deﬁnition 4 (Isolation assumption): The computation tree

Definition 4 (Isolation assumption ): The   computation tree TF (G) with the root v; € P is said to be isolated if: (i) for any check node cj € W' that is in Tk(G) with Ut € P' = 0, two check nodes Cr; Cs W W' that are also in Tk (G), D(cr)nD(cs) € (PUW). If Tk (G) is isolated € P, then the subgraph G for k iterations . Vvi

Remark: The isolation assumption can still be satisﬁed even when there are nodes in H that appear multiple times in T k i ( G ) as long as these nodes are not descendants of the degree-one check nodes. Whereas Gallager’s independence assumption will be violated if any node in H is repeated in T k i ( G ) . Hence, isolation assumption is a weaker condition than independence. For clarity, we illustrate with an example shown in Fig. 1. Example 1: Let us assume that the graph G of code

Example I: Let us assume that   the graph G of code C contains a subgraph H induced by a (6,2) trapping set Fig. 1 shows the subgraph H, and the computation tree T32(G) of graph G with v3 as its root enumerated for two iterations. The denotes a odd-degree check node_ The solid lines represent connections within subgraph H and the dotted lines represent connections from the rest of the graph G outside the subgraph H . The isolation assumption is satisfied for two iterations if none of the descendants of the check nodes cz and c8 appear as a descendant of check node c9 (similar condition has to hold for c1o), and if the only common descendants of the degree-2 check nodes are nodes in H. But the independence assumption does not hold for two iterations Theorem 1 (Isolation theorem): Let G {VU C,E} of 3-left-regular code which contains  a subgraph {PU W;E' } that is induced by trapping set (a,b). Let W' = W denote the set of degree-one check nodes in H and let P' = P denote   the set of   variable  nodes in H where each has at least one neighbor in W'_ If r is input to decoder 9 from the BSC such that € P , and if H satisfies the isolation assumption in G for then for   each Cj € W' the message from cj to its neighbor in H in the as the output of supp(r)

![](<6e877f30a7743152e9f4e6f22c10b1ff55a3aa6fb6543095d6298f32b2934d47_images/imageFile1.png>)

C5

C4

C1o

V4

V6

Vs

Fig. 1. Subgraph H induced by (6,2) trapping set contained in G : (a) Tanner graph of H ; (b) computational tree T 2 3 ( G )

Φ v ( µ l − 1 ,µ l − 1 , C) ∀ l ≤ k . Proof: This follows by looking at the computation tree T l i ( G ) where l ≤ k with any v i ∈ P   as its root. Let the initial messages passed from a variable node be ± µ 0 ∈ M . Since supp ( r ) ∈ P , due to the isolation assumption, this means that all the variable nodes that are descendants to any c j ∈ W   are initially correct. In the initial iteration, from the deﬁnition of Φ c , the outgoing message of check nodes that are descendants to c j is µ 0 . In the next iteration, the variable nodes connected to these check nodes receive µ 0 on all their edges due to the isolation assumption and send Φ v ( µ 0 ,µ 0 , C) as their outgoing messages. Due to the deﬁnition of Φ c , the check nodes connected to these nodes in T l i ( G ) send µ 1 which is simply Φ v ( µ 0 ,µ 0 , C) . This process inductively follows while traversing up the tree for l iterations. Moreover, computation of the hard-decision value for any node v i in H requires only messages from nodes in H in addition to µ l .

Remark: Note that the isolation assumption and theorem can be restated for the min-sum decoder. Corollary 1: Consider the min-sum decoder for 3-left-

regular LDPC codes with Y = {± 1 } . If subgraph H contained in G satisﬁes the isolation assumption for k iterations, and if all variable nodes outside H are initially correct, then µ l of the degree-one check node for the min-sum decoder is 2 µ l − 1 +1 . Corollary 2: If H is a subgraph contained in G such that

it satisﬁes the isolation assumption for k iterations, and if all variable nodes outside H are initially correct, then the computation tree T k i ( G ) with v i ∈ P is equivalent to T k i ( H ) , provided µ l for each degree-one check node in H is computed

