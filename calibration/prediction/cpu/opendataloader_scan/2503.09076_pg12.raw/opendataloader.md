end, let D be an agreement tree-child digraph for N and N ′ , and let c D and c ′ D be the cut size of D in N and N ′ , respectively. Then D is called a maximum agreement tree-child digraph for N and N ′ if the sum c D + c ′ D is minimum over all agreement tree-child digraphs for N and N ′ , in which case we denote this minimum number by m tc ( N , N ′ ). To calculate m tc ( N , N ′ ), it follows from Proposition 4.3 that it is sufficient to consider a single extension of each agreement digraph for N and N ′ . Referring back to Figure 1, observe that each of the three phylogenetic digraphs D 1 , D 2 , and D 3 is in fact an agreement digraph for the two tree-child networks N and N ′ that are shown in the same figure.

Let N and N ′ be two tree-child networks, let D be an agreement tree-child digraph for N and N ′ , and let R and R ′ be an extension of D in N and N ′ , respectively. We note that, similar to the elements of an agreement forest, the elements in D can be embedded in N and N ′ . Intuitively, they can be thought of as subnetworks that are common to N and N ′ . On the other hand, the digraphs induced by the edges in E R − E M and E R ′ − E M ′ , where M and M ′ is the embedding that underlies R and R ′ , respectively, are not necessarily the same. Although each connected component in such a digraph is a rooted tree whose (unique) root is a vertex of M and M ′ , respectively, and whose edges are directed towards the root, one digraph may contain directed rooted trees with a small total number of unlabelled leaves and the other one may contain directed rooted trees with a much larger total number of unlabelled leaves.

Now, let N be a phylogenetic network on X , and let e = ( u,v ) be an edge in N . We consider the following three operations applied to N :

that is not descendant of v with a new vertex u' and add the new edge (u' , v) . edge

SNPR − If u is a tree vertex and v is a reticulation, then delete e , and suppress u and v .

SNPR + Subdivide e with a new vertex v ′ , subdivide an edge in the resulting network that is not a descendant of v ′ with a new vertex u ′ , and add the new edge ′ ′

By definition of a tree vertex, u ̸ = ρ if we apply an SNPR ± . If it is not important which of SNPR − , SNPR + , and SNPR ± has been applied to N we simply refer to it as an SNPR. By [6, Proposition 3.1], the operation is reversible , i.e. if N ′ is a phylogenetic network on X that can be obtained from N by a single SNPR, then N can also be obtained from N ′ by a single SNPR. Lastly, we note that the well-known rSPR operation is an application of SNPR ± to a phylogenetic tree.

Let N and N ′ be two phylogenetic networks on X . and N ′ is a sequence

$$

$$

of phylogenetic networks on X such that, for all i ∈ { 1 , 2 ,...,t } , we have N i is obtained from N i − 1 by a single SNPR in which case, we say that σ connects N and N ′ . We refer to t as the length of σ . Let t ± be the number of phylogenetic networks

