For graph G , denote l u as the label of node u , e u,v as the shortest path from u to v (which may not be unique), and d u,v as the shortest distance from node u to v (which is unique). Borgwardt and Kriegel (2005) define an SP kernel between graphs G 1 = ( V 1 ,E 1 ) and G 2 = ( V 2 ,E 2 ) as:

$$
ksP(G1 ,G2)
$$

paths:

$$
= kv(lu1 = ) ke(du1,v
$$

1 1 2 2 1 2 · 1 1 2 2 · 1 2 where k v is a kernel comparing node labels, k e is a kernel comparing path lengths. Both k v and k e are usually chosen as Dirac kernels, giving the explicit representation of the SP kernel as:

$$
ksP(G' ,G2) = 1(lu1 = 1(du1,v = ,02 ) . 1(lv1 = (SP) lvz )
$$

where 1 n 2 1 n 2 2 is introduced as a

Note that each node may have more problem-specific features beyond a single label. From here on, we use X = ( G,F ) to denote an attributed graph with G as the underlying labeled graph and F as node features. Intuitively, we can compare the features of two nodes instead of labels in k v . However, this could unnecessarily reduce the number of matching paths between two graphs, as requiring identical node features is restrictive and may introduce additional subgraph information into path comparison. Another option is to use a more complicated kernel k v that measures similarity between features of two nodes, which may significantly increase the computational cost of optimization (similarity is computed for all node pairings). Therefore, we borrow from Cui and Yang (2018) the idea to separate the implicit and explicit information of graphs, i.e., the kernel value between two attributed graphs X 1 ,X 2 becomes: 1 2 1 2 1 2

$$
(3
$$

between graph similarity and feature similarity. Appendix A.4 describes an example of kF

Since node label is usually included as a node feature and considered in k F term, and comparing labels in Eq. (SP) increases the complexity of our optimization formulations, we propose a simplified shortest-path (SSP) kernel corresponding to an unlabeled SP kernel:

$$
kssP(G1 ,G2) = = (SSP)
$$

∈ ∈ ≤ where D s ( G ) := |{ ( u,v ) | u,v ∈ V, d u,v = s }| is the number of shortest paths with length s in graph G = ( V,E ) . Lemma 3.1. SP and SSP kernels are positive definite (PD).

where all nodes have the same label, hence is also PD.

Observe that both the SP and SSP kernels are linear kernels if we pre-process all shortest paths in each graph and count the number of each length of shortest path. Such linearity simplifies the optimization step (which still requires the non-trivial representation of shortest paths), but reduces the representation ability of the graph kernels and limits the maximal rank of the covariance matrix. Motivated by the practically strong performance of exponential kernels such as RBF kernel, Matérn kernel, graph diffusion kernel (Oh et al., 2019), etc., we propose the following two nonlinear graph kernels based on SP and SSP kernels:

$$
kEsP(G' ,G2) = (ESP)
$$

$$
kEssP(G1 , G2) = exp(kssp ESSP) (G' ,
$$

where variance σ 2 k is added to control the magnitude of kernel value. Note that we could also add variance to SP and SSP kernels, but it would be absorbed by α,β .

Lemma 3.2. ESP and ESSP kernels are PD.

Proof. SP and SSP kernels can be rewritten into linear forms, so ESP and ESSP are exponential kernels, which are known to be PD (Fukumizu, 2010).

The nonlinear kernels introduce additional difficulties for optimization as discussed in Section 3.4, but demonstrate better empirical performance compared to their linear counterparts, owing to increased representation ability.

