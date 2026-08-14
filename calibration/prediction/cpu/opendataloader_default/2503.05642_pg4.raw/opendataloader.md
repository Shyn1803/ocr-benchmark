BoGrape, Xie and Zhang, et al.

For graph G, denote lu as the label of node u, eu,v as the shortest path from u to v (which may not be unique), and du,v as the shortest distance from node u to v (which is unique). Borgwardt and Kriegel (2005) define an SP kernel between graphs G1 = (V 1,E1) and G2 = (V 2,E2) as:

kSP(G1,G2) =

2,v2) k(·,·) compares the labels and lengths of two shortest paths:

k(eu

1,v1,eu

u1,v1∈V 1,u2,v2∈V 2

) · ke(du

# 2,v2) · kv(lv

k(eu

1,v1,eu

2,v2) = kv(lu

# ,lu

1,v1,du

# ,lv

# )

1

2

1

2

where kv is a kernel comparing node labels, ke is a kernel comparing path lengths. Both kv and ke are usually chosen as Dirac kernels, giving the explicit representation of the SP kernel as:

1 n21n22

kSP(G1,G2) =

) · 1(du

2,v2) · 1(lv

1(lu

# = lu

1,v1 = du

# = lv

) (SP)

1

2

1

2

u1,v1∈V 1,u2,v2∈V 2

where n21

1n22 is introduced as a normalizing coefficient with n1,n2 as the number of nodes in graph G1,G2, respectively. Note that each node may have more problem-specific features beyond a single label. From here on, we use X = (G,F) to denote an attributed graph with G as the underlying labeled graph and F as node features. Intuitively, we can compare the features of two nodes instead of labels in kv. However, this could unnecessarily reduce the number of matching paths between two graphs, as requiring identical node features is restrictive and may introduce additional subgraph information into path comparison. Another option is to use a more complicated kernel kv that measures similarity between features of two nodes, which may significantly increase the computational cost of optimization (similarity is computed for all node pairings). Therefore, we borrow from Cui and Yang (2018) the idea to separate the implicit and explicit information of graphs, i.e., the kernel value between two attributed graphs X1,X2 becomes:

# k(X1,X2) = α · kG(G1,G2) + β · kF(F1,F2) (3)

where kG is any graph kernel, kF is any kernel over features, and α,β are trainable parameters controlling the trade-off between graph similarity and feature similarity. Appendix A.4 describes an example of kF.

Since node label is usually included as a node feature and considered in kF term, and comparing labels in Eq. (SP) increases the complexity of our optimization formulations, we propose a simplified shortest-path (SSP) kernel corresponding to an unlabeled SP kernel:

1 n21n22

1 n21n22

kSSP(G1,G2) =

Ds(G1) · Ds(G2) (SSP)

1(du

1,v1 = du

2,v2) =

u1,v1∈V 1,u2,v2∈V 2

0≤s<min(n1,n2)

where Ds(G) := |{(u,v) | u,v ∈ V, du,v = s}| is the number of shortest paths with length s in graph G = (V,E).

- Lemma 3.1. SP and SSP kernels are positive definite (PD).

Proof. Borgwardt and Kriegel (2005) prove the SP kernel is PD. The SSP kernel is a special case of the SP kernel where all nodes have the same label, hence is also PD.

<table>
  <tr>
    <td> </td>
  </tr>
</table>


Observe that both the SP and SSP kernels are linear kernels if we pre-process all shortest paths in each graph and count the number of each length of shortest path. Such linearity simplifies the optimization step (which still requires the non-trivial representation of shortest paths), but reduces the representation ability of the graph kernels and limits the maximal rank of the covariance matrix. Motivated by the practically strong performance of exponential kernels such as RBF kernel, Matérn kernel, graph diffusion kernel (Oh et al., 2019), etc., we propose the following two nonlinear graph kernels based on SP and SSP kernels:

kESP(G1,G2) = exp(kSP(G1,G2))/σk2 (ESP) kESSP(G1,G2) = exp(kSSP(G1,G2))/σk2 (ESSP)

where variance σk2 is added to control the magnitude of kernel value. Note that we could also add variance to SP and SSP kernels, but it would be absorbed by α,β.

- Lemma 3.2. ESP and ESSP kernels are PD.


Proof. SP and SSP kernels can be rewritten into linear forms, so ESP and ESSP are exponential kernels, which are known to be PD (Fukumizu, 2010). The nonlinear kernels introduce additional difficulties for optimization as discussed in Section 3.4, but demonstrate better empirical performance compared to their linear counterparts, owing to increased representation ability.

<table>
  <tr>
    <td> </td>
  </tr>
</table>


4

