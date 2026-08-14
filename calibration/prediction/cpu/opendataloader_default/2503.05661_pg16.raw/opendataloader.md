distance at least K from each of u,v,w. We cannot have dG(w,Q(x,y)) < K since then we get dG(x,w) < K + K = 2K, which is impossible as x ∈ P(u,v). Similarly, we cannot have dG(u,Q(x,y)) < K. Assume, by way of contradiction, dG(v,Q(x,y)) < K. Then, there is a vertex z ∈ Q(x,y) with dG(v,z) < K. Assuming, without loss of generality, dG(x,z) ≤ dG(z,y), we get dG(v,x) ≤ dG(v,z)+dG(z,x) ≤ K−1+(K−1)/2 = 3/2(K−1) < ⌊32K⌋. The latter contradicts the choice of vertex vu as being a vertex of P(u,v) ∩ DG(v,⌊32K⌋) furthest (along the path P(u,v)) from v. This proves that the K1,3-minor constructed is K-fat.

![](<2503.05661_pg16_images/imageFile1.png>)

![](<2503.05661_pg16_images/imageFile2.png>)

Now, we can assume that all three paths P(vu,uv), P(vw,wv), P(uw,wu) are pairwise at distance at least K. In this case, we can build a K-fat K3-minor in G. Set Hv := G[DG(v,⌊32K⌋)], Hu := G[DG(u,⌊32K⌋)], Hw := G[DG(w,⌊32K⌋)]. It is easy to see that these connected subgraphs Hv,Hw,Hu and paths P(vu,uv), P(vw,wv), P(uw,wu) form a K-fat K3minor in G. Recall that dG(v,P(u,w)) ≥ 4K, dG(u,P(v,w)) ≥ 4K and dG(w,P(u,v)) ≥ 4K. Hence, if dG(V (Hv),V (Hu)) < K, then dG(v,u) < ⌊23K⌋ + K + ⌊23K⌋ ≤ 4K, which is impossible. If dG(V (Hv),P(uw,wu)) < K, then dG(v,P(u,w)) < ⌊32K⌋ + K < 3K, which is also impossible. By symmetries, the K3-minor constructed is K-fat. ⊔⊓

![](<2503.05661_pg16_images/imageFile3.png>)

![](<2503.05661_pg16_images/imageFile4.png>)

![](<2503.05661_pg16_images/imageFile5.png>)

![](<2503.05661_pg16_images/imageFile6.png>)

![](<2503.05661_pg16_images/imageFile7.png>)

![](<2503.05661_pg16_images/imageFile8.png>)

Note that, in the proof of Lemma 12, we constructed very speciﬁc K-fat (K3,K1,3)-minors. In our K-fat K3-minor, the connected subgraphs H1,H2,H3 are disks. In our K-fat K1,3minor, the connected subgraphs H1,H2,H3 are singletons and the paths Pi,0, i = 1,2,3, are shortest paths. Even more speciﬁc K-fat (K3,K1,3)-minors were obtained in [1]. It was shown that if a graph G contains no (≥ K)-subdivision of K3 as a geodesic subgraph and no (≥ 3K)subdivision of K1,3 as a 3-quasi-geodesic subgraph, then pb(G) ≤ 18K + 2 (see [1] for details and deﬁnitions).

From Lemma 12, we immediately get the following corollary.

Corollary 7. If G has neither K-fat K3-minor nor K-fat K1,3-minor, then mci(G) ≤ 4K−1. In particular, mci(G) ≤ 4 · mﬁ(G) + 3.

Proof. The ﬁrst part of Corollary 7 follows from Lemma 12. For the second part, let mﬁ(G) = K −1. Then, G has neither K-fat K3-minor nor K-fat K1,3-minor. By the ﬁrst part, mci(G) ≤ 4K − 1 = 4(K − 1) + 3 = 4 · mﬁ(G) + 3. ⊔⊓

Combining Lemma 11 and Corollary 7 with Theorem 4, we get. Theorem 5. For every graph G,

mﬁ(G) ≤ mci(G) ≤ 4 · mﬁ(G) + 3, mﬁ(G) ≤ pl(G) ≤ 16 · mﬁ(G) + 10, mﬁ(G) 2

≤ pat(G) ≤ 8 · mﬁ(G) + 5,

![](<2503.05661_pg16_images/imageFile9.png>)

mﬁ(G) − 1 2

≤ adc(G) ≤ 16 · mﬁ(G) + 10,

![](<2503.05661_pg16_images/imageFile10.png>)

mﬁ(G) ≤ ∆(G) ≤ 16 · mﬁ(G) + 12,

mﬁ(G) 4

≤ dsp(G) ≤ dpr(G) ≤ 8 · mﬁ(G) + 5,

![](<2503.05661_pg16_images/imageFile11.png>)

mﬁ(G) 2

≤ pcc(G) ≤ 16 · mﬁ(G) + 10.

![](<2503.05661_pg16_images/imageFile12.png>)

16

