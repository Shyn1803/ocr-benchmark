Before we formally introduce this, we require the notion of computation tree and introduce some more notations.

Deﬁnition 1: [16] A computation tree corresponding to a message-passing decoder of the Tanner graph G is a tree that is constructed by choosing an arbitrary variable node in G as its root and then recursively adding edges and leaf nodes to the tree that correspond to the messages passed in the decoder up to a certain number of iterations. For each vertex that is added to the tree, the corresponding node update function in G is also copied.

Let G be the Tanner graph of a 3-left-regular code. Let H be the induced subgraph of a trapping set (a,b) contained in

- G with variable node set P ⊆ V and check node set W ⊆ C.

Let N(u) denote the set of neighbors of a node u. Let Tik(G) be the computation tree of graph G corresponding to a decoder

- F enumerated for k iterations with variable node vi ∈ V as its root. Let W ⊆ W denote the set of degree-one check nodes in the subgraph H. Let P ⊆ P denote the set of variable nodes in H where each variable node has at least one neighbor in W . During decoding on G, for a node vi ∈ P , let µl denote the message that vi receives from its neighboring degree-one check node in H in the lth iteration.

- Deﬁnition 2: A vertex w ∈ Tik(G) is said to be a descen-

dant of a vertex u ∈ Tik(G) if there exists a path starting from vertex w to the root vi that traverses through vertex u. The set of all descendants of the vertex u in Tik(G) is denoted as D(u). For a given vertex set U, D(U) (with some abuse of notation) denotes the set of descendants of all u ∈ U.

- Deﬁnition 3: Tik(H) is called the computation tree of the

subgraph H enumerated for k iterations for the decoder F, if ∀ cj ∈ W , µl is given for all l ≤ k, and if the root node vi ∈ P requires only the messages computed by the nodes in H and µl to compute its binary hard-decision value.

- Deﬁnition 4 (Isolation assumption): The computation tree


Tik(G) with the root vi ∈ P is said to be isolated if: (i) for any check node cj ∈ W that is in Tik(G) with vt ∈ P as its parent, D(cj) ∩ D(N(vt) \ cj) = ∅, and (ii) for any two check nodes cr,cs ∈ W \ W that are also in Tik(G), D(cr)∩D(cs) ⊆ (P ∪W). If Tik(G) is isolated ∀vi ∈ P, then the subgraph H is said to satisfy the isolation assumption in

- G for k iterations. Remark: The isolation assumption can still be satisﬁed even




when there are nodes in H that appear multiple times in Tik(G) as long as these nodes are not descendants of the degree-one check nodes. Whereas Gallager’s independence assumption will be violated if any node in H is repeated in Tik(G). Hence, isolation assumption is a weaker condition than independence. For clarity, we illustrate with an example shown in Fig. 1.

Example 1: Let us assume that the graph G of code C contains a subgraph H induced by a (6,2) trapping set. Fig. 1 shows the subgraph H, and the computation tree T32(G) of graph G with v3 as its root enumerated for two iterations. The

denotes a odd-degree check node. The solid lines represent connections within subgraph H and the dotted lines represent connections from the rest of the graph G outside the subgraph

v1 v2 v3

c6

c1 c2 c3 c4 c5

c7 c8 c9

c10

v4 v5 v6

(a)

v3

c8 c9

c7

v4 v5

c4 c1 c2 c5 v2 v1 v1 v2

(b)

Fig. 1. Subgraph H induced by (6,2) trapping set contained in G: (a) Tanner graph of H; (b) computational tree T32(G)

H. The isolation assumption is satisﬁed for two iterations if none of the descendants of the check nodes c7 and c8 appear as a descendant of check node c9 (similar condition has to hold for c10), and if the only common descendants of the degree-2 check nodes are nodes in H. But the independence assumption does not hold for two iterations.

Theorem 1 (Isolation theorem): Let G = {V ∪ C,E} of a 3-left-regular code which contains a subgraph H = {P ∪ W,E } that is induced by a trapping set (a,b). Let W ⊆ W denote the set of degree-one check nodes in H and let P ⊆ P denote the set of variable nodes in H where each has at least one neighbor in W . If r is input to decoder F from the BSC such that supp(r) ∈ P, and if H satisﬁes the isolation assumption in G for k iterations, then for each cj ∈ W , the message from cj to its neighbor in H in the lth iteration denoted by µl, is determined as the output of Φv(µl−1,µl−1,C) ∀l ≤ k.

Proof: This follows by looking at the computation tree Til(G) where l ≤ k with any vi ∈ P as its root. Let the initial messages passed from a variable node be ±µ0 ∈ M. Since supp(r) ∈ P, due to the isolation assumption, this means that all the variable nodes that are descendants to any cj ∈ W are initially correct. In the initial iteration, from the deﬁnition of Φc, the outgoing message of check nodes that are descendants to cj is µ0. In the next iteration, the variable nodes connected to these check nodes receive µ0 on all their edges due to the isolation assumption and send Φv(µ0,µ0,C) as their outgoing messages. Due to the deﬁnition of Φc, the check nodes connected to these nodes in Til(G) send µ1 which is simply Φv(µ0,µ0,C). This process inductively follows while traversing up the tree for l iterations. Moreover, computation of the hard-decision value for any node vi in H requires only messages from nodes in H in addition to µl.

Remark: Note that the isolation assumption and theorem can be restated for the min-sum decoder.

- Corollary 1: Consider the min-sum decoder for 3-left-

regular LDPC codes with Y = {±1}. If subgraph H contained in G satisﬁes the isolation assumption for k iterations, and if all variable nodes outside H are initially correct, then µl of the degree-one check node for the min-sum decoder is 2µl−1 +1.

- Corollary 2: If H is a subgraph contained in G such that


it satisﬁes the isolation assumption for k iterations, and if all variable nodes outside H are initially correct, then the computation tree Tik(G) with vi ∈ P is equivalent to Tik(H), provided µl for each degree-one check node in H is computed

