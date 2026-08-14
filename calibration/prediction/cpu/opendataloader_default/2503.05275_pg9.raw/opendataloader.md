9

Let p := ⌊θn⌋. Take 4p mutually disjoint vertex sets S1,S2,... ,S2p,T1,T2,... ,T2p from V (H) \ V (P′) with iP(Si) = (m,k − ℓ − m) and iP(Ti) = (m − 1,k − ℓ − m + 1) for i ∈ [2p]. We denote the union of these Si and Ti, i ∈ [2p] by R1. So R1 ⊆ V (H) \ V (P′), |R1| = 4(k − ℓ)p and iP(R1) = 2p(m,k − ℓ − m) + 2p(m − 1,k − ℓ − m + 1). Thus P′ can absorb R1, that is, there exists an ℓ-path P with the same ordered ends as P′, where V (P) = V (P′) ∪ R1. Now we show that P is the desired absorbing ℓ-path. Note that |V (P)| ≤ γn. Fix any set X ⊆ V (H) \ V (P) with |X| ≤ p and (k − ℓ) | |X| as required by the lemma. Suppose further that iP(X) = (t,s) = x(m,k − ℓ − m) + y(m − 1,k − ℓ − m + 1). Then we have

- x = t − (m−k1)(−ℓt+s)

![](<2503.05275_pg9_images/imageFile1.png>)

- y = (t+k−s)ℓm − t.


![](<2503.05275_pg9_images/imageFile2.png>)

Since t+s = |X|, (k−ℓ) | |X| and m/(k−ℓ) ≤ 1, we get that x,y are integers and |x|,|y| ≤ |X| < 2p. Thus iP(X∪R1) = (x+2p)(m,k−ℓ−m)+(y+2p)(m−1,k−ℓ−m+1), where x+2p > 0,y+2p > 0 and |X ∪ R1| ≤ 4(k − ℓ)p + p ≤ (k − ℓ)β2k−2ℓ+4n. So P′ can absorb X ∪ R1, that is, P can absorb X.

To complete the proof of Lemma 3.5, it remains to prove Claim 3.9.

Proof of Claim 3.9. Let S := {v1,v2,... ,vk−ℓ} be a (k − ℓ)-set. Fix a k-partite k-graph A(k,ℓ) on [V1A,V2A,... ,VkA] satisfying Proposition 3.7 with |A(k,ℓ)| = r ≤ k4 and V (A(k,ℓ)) = S′ ∪ X, where |S′| = k − ℓ. Without loss of generality, suppose |S′ ∩ ViA| = 1 for i ∈ [k − ℓ]. Let b := (4k − 2ℓ − 1)(k − ℓ) + r. Since (a,k − a) ∈ IPµ(H′), the number of edges whose index vectors are (a,k − a) is at least µnk. Note that t1 := |S ∩ V1| ≤ a and |S ∩ V2| ≤ k − a by S ∈ S. Since A(k,ℓ) is k-partite, by the supersaturation result (see [6]) on the subgraph of H that consists of all edges of index vector (a,k − a), H contains βnr copies of A(k,ℓ) each with V1A,... ,VtA1 ⊆ V1 and VtA

1+1,... ,VkA−ℓ ⊆ V2. For such a copy A of A(k,ℓ), we denote by SA′ as the set of k − ℓ vertices given in Proposition 3.7 (2). So iP(SA′ ) = iP(S) for each such A.

Consider a copy of A(k,ℓ) in H which we denote by A. Note that each of V1,V2 is (β,2)-closed in H. Without loss of generality, suppose SA′ = {w1,w2,... ,wk−ℓ} such that vi,wi are (β,2)reachable for i ∈ [k − ℓ] by iP(SA′ ) = iP(S). By the deﬁnition of reachability, for each i ∈ [k − ℓ], there are at least βn4k−2ℓ−1 (4k − 2ℓ − 1)-sets Ti such that there exist ℓ-paths Pi1,Pi2,Pi3,Pi4 with V (Pi1 ∪ Pi2) = Ti ∪ {vi} and V (Pi3 ∪ Pi4) = Ti ∪ {wi}, where Pi1 has the same ends as Pi2, and Pi3 has the same ends as Pi4. So there are at least βk−ℓ+1nb choices for A ∪ T1 ∪ T2 ∪ ··· ∪ Tk−ℓ as an ordered set. Among them, at most (k − ℓ)nb−1 of them intersect S and at most b2nb−1 of them contain repeated vertices. Thus there are at least βk−ℓ+1nb/2 b-tuples avoiding S such that A,T1,T2,... ,Tk−ℓ are pairwise vertex-disjoint.

Now it remains to show that the b-tuple corresponding to A∪T1∪T2∪···∪Tk−ℓ is an S-absorber. Firstly, Ti ∪ {wi}, i ∈ [k − ℓ] spans two vertex-disjoint ℓ-paths of length two, which together with the spanning ℓ-path in A \ {w1,w2,... ,wk−ℓ} form a family of 2k − 2ℓ + 1 ℓ-paths which span V (A) ∪ T1 ∪ T2 ∪ ··· ∪ Tk−ℓ. Secondly, H[Ti ∪ {vi}] forms two vertex-disjoint ℓ-paths of length two for i ∈ [k − ℓ], which together with the spanning ℓ-path in A gives a family of 2k − 2ℓ + 1 ℓ-paths which span S ∪ V (A) ∪ T1 ∪ T2 ∪ ··· ∪ Tk−ℓ and have the same ends as the family of ℓ-paths above. So the b-tuple corresponding to A ∪ T1 ∪ T2 ∪ ··· ∪ Tk−ℓ is an S-absorber (cf. Figure 1).

3.3. Proofs of Theorem 1.4 and Theorem 1.5. We prove Theorem 1.4 by following the common approach of absorption (cf. [18, 27]). That is, we decompose the proof in the usual way into the absorbing path lemma, the reservoir lemma, the connecting lemma and the path cover lemma. We will use these lemmas to ﬁnd an absorbing path and a reservoir ﬁrstly, and then we cover the majority of vertices by vertex-disjoint ℓ-paths. We connect up all these ℓ-paths to form an ℓ-cycle. Finally, we absorb the leftover vertices into the absorbing path, thereby completing a Hamilton ℓ-cycle.

