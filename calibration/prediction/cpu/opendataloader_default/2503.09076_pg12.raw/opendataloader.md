12 STEVEN KELK, SIMONE LINZ, AND CHARLES SEMPLE

end, let D be an agreement tree-child digraph for N and N′, and let cD and c′D be the cut size of D in N and N′, respectively. Then D is called a maximum agreement

tree-child digraph for N and N′ if the sum cD + c′D is minimum over all agreement tree-child digraphs for N and N′, in which case we denote this minimum number

by mtc(N,N′). To calculate mtc(N,N′), it follows from Proposition 4.3 that it is sufficient to consider a single extension of each agreement digraph for N and N′. Referring back to Figure 1, observe that each of the three phylogenetic digraphs D1, D2, and D3 is in fact an agreement digraph for the two tree-child networks N and N′ that are shown in the same figure.

Let N and N′ be two tree-child networks, let D be an agreement tree-child digraph for N and N′, and let R and R′ be an extension of D in N and N′, respectively. We note that, similar to the elements of an agreement forest, the elements in D can be embedded in N and N′. Intuitively, they can be thought of as subnetworks that are common to N and N′. On the other hand, the digraphs induced by the edges in ER −EM and ER′ −EM′, where M and M′ is the embedding that underlies R and R′, respectively, are not necessarily the same. Although each connected component in such a digraph is a rooted tree whose (unique) root is a vertex of M and M′, respectively, and whose edges are directed towards the root, one digraph may contain directed rooted trees with a small total number of unlabelled leaves and the other one may contain directed rooted trees with a much larger total number of unlabelled leaves.

Now, let N be a phylogenetic network on X, and let e = (u,v) be an edge in N. We consider the following three operations applied to N: SNPR± If u is a tree vertex, then delete e, suppress u, subdivide an edge that is not a descendant of v with a new vertex u′, and add the new edge (u′,v). SNPR− If u is a tree vertex and v is a reticulation, then delete e, and suppress u and v.

SNPR+ Subdivide e with a new vertex v′, subdivide an edge in the resulting network that is not a descendant of v′ with a new vertex u′, and add the new edge (u′,v′).

By definition of a tree vertex, u ̸= ρ if we apply an SNPR±. If it is not important which of SNPR−, SNPR+, and SNPR± has been applied to N we simply refer to it as an SNPR. By [6, Proposition 3.1], the operation is reversible, i.e. if N′ is a phylogenetic network on X that can be obtained from N by a single SNPR, then N can also be obtained from N′ by a single SNPR. Lastly, we note that the well-known rSPR operation is an application of SNPR± to a phylogenetic tree.

Let N and N′ be two phylogenetic networks on X. An SNPR sequence σ for N and N′ is a sequence

σ = (N = N0,N1,N2,...,Nt = N′)

of phylogenetic networks on X such that, for all i ∈ {1,2,...,t}, we have Ni is obtained from Ni−1 by a single SNPR in which case, we say that σ connects N and N′. We refer to t as the length of σ. Let t± be the number of phylogenetic networks

