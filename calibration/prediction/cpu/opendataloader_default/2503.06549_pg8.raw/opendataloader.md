8 DECORRELATION TRANSITION IN THE WIGNER MINOR PROCESS

index i ∼ Na we have a transition (from strong dependence to independence) on a scale k ∼ N2(1−a)/3. The situation in the bulk, a = 1, is very different and will be explained separately at the end (see also Figure 2).

∼ N Na

i

dependent

dependent

N

independent

k

2(1−a) 3

![](<2503.06549_pg8_images/imageFile1.png>)

(A) (B)

FIGURE 2. (A): Decorrelation transition in the intermediate regime a ∈ [0,1). The figure depicts the shrinking spectrum of the minors H(N−k); the dashed line their largest eigen-

value. We consider a ∈ [0,1), fix an index i ∼ Na and track the trajectory of λi(N−k) as k decreases. This trajectory crosses the solid red line at the level k(a) ∼ N2(1−a)/3,

marking the phase transition: for k ≪ k(a), λi(N−k) and λ(iN) remain highly correlated, while for k ≫ k(a), λ(iN−k) becomes essentially independent of λ(iN). For a = 1, i.e. to the left of the dotted line (bulk regime), the eigenvalues remain correlated for any k. (B): Individual eigenvalues of H(N) and its first two minors in the extreme edge regime and in the bulk regime. In the edge regime, the i-th eigenvalues λ(iN),λ(iN−1),λi(N−2) ... stick to each other indicating very strong correlation. In the bulk regime the only correlation present is the one enforced by interlacing.

We now explain how to obtain the threshold k ∼ N2(1−a)/3 for a ∈ [0,1). We do not present the mathematical details for brevity, but just explain the general strategy. We separate the argument into two parts: we first show that the eigenvalues corresponding to indices i ∼ Na are (asymptotically) independent for k ≫ N2(1−a)/3 and then that they are strongly correlated for k ≪ N2(1−a)/3.

For k ≫ N2(1−a)/3, we follow a strategy similar to Section 3, i.e. we show the independence of the eigenvalues using a Dyson Brownian motion (DBM) argument. More precisely, we couple the time evolution of λ(iN)(t) and λ(iN−k)(t) under a Brownian matrix flow with two fully independent DBM flows µ(1)i (t),µ(2)i (t) showing that for larger times t they are close to each other. To control the coupling, technically this requires following analogue of the eigenvector overlap bound (cf. (3.1)):

N2(1−a)/3 k ∧ 1, i,j ∼ Na.

(2.8) ⟨wi(N),wj(N−k)⟩ 2 ≺

The proof of (2.8) is very similar to the one in Section 4.2 below, once it is taken into consideration that the local eigenvalue density is of order ∼ N(1−a)/3, when i ∼ Na. The bound (2.8) shows that the eigenvectors

of H(N) and H(N−k) are asymptotically orthogonal |⟨wi(N),wj(N−k)⟩| ≪ 1 for k ≫ N2(1−a)/3. Armed with this bound as an input, we can then proceed with a DBM argument similar to the one in Section 5.

The only difference is that in the current case we cannot directly rely on the results from [14, 53], which are formulated only in the regime i ∼ 1. However, inspecting their proof, it is clear that similar arguments can be extended to the regime i ∼ Na, for a ∈ (0,1). This gives the desired independence when k ≫ N2(1−a)/3.

For k ≪ N2(1−a)/3, we can follow a strategy similar to Section 7. As the level repulsion scale for

λ(in) − λ(i+1n) , for n ∈ [N − k,N], should now be changed to n−(2+a)/3−δ, the error term in each step of the recursion analogous to (7.11) will be N(a−1)/3+Cδ instead of N−1/3+Cδ. Hence, after k steps of the

