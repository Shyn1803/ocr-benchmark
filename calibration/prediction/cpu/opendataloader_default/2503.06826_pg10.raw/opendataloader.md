We are now ready to prove Theorem 1.3.

Proof of Theorem 1.3. Let X ⊆ V (G) be a subset given by Lemma 2.4. We pass on to Γ = G[X]. The graph Γ has N ≥ αn/128 vertices, and for β = αn/(8N) and d = t/4, the following holds:

- (i) Γ is a (β,d)-expander, and
- (ii) for every partition V (Γ) = R ∪ A ∪ B with |R| ≤ αN/16 and |A|,|B| ≥ βN/4, there is an edge in Γ between A and B.


Let K = 25/α2 (the constant in the upper bound on the size of T in Lemma 3.3). Consider the

family P of all ordered partitions V (Γ) = D ∪ ki=1 Wi ∪ U, where k ≥ 0 (this can be a diﬀerent number for diﬀerent partitions), such that the following holds:

- (P1) For every i ∈ [k]: |Wi| = 2KNdlogN =: ℓ and Γ[Wi] is connected,

![](<2503.06826_pg10_images/imageFile1.png>)

![](<2503.06826_pg10_images/imageFile2.png>)

- (P2) for every two distinct i,i′ ∈ [k], there is an edge in Γ between Wi and Wi′, and
- (P3) |D| ≤ αN/(32d) and |NΓ(D) ∩ U| < d|D|/2.


The ﬁrst two properties imply that Kk is a minor of Γ. By taking D = ∅, k = 0 and U = V (Γ), we have that P is not empty. Consider a partition

V (Γ) = D ∪ ki=1 Wi ∪ U in P which maximises |D|, tie-breaking by taking one which further maximises k. We prove that then necessarily

αN 64ℓ

k ≥

=: q.

![](<2503.06826_pg10_images/imageFile3.png>)

![](<2503.06826_pg10_images/imageFile4.png>)

As q = Θ( nt/ logn), this establishes the theorem. Suppose, towards a contradiction, that this is note the case. That is, k < q. Then

|W| =

k

Wi < αN/64,

i=1

from which we conclude |U| ≥ N/2, with room to spare.

The property (P3) in the proof of Theorem 1.4 is identical to the one used here, and the only property of W used in the proof of Claim 3.1 and Claim 3.2 is the upper bound on |W|, which is identical to the one used here. Therefore, same as in the proof of Theorem 1.4, the following holds:

- • For every i ∈ [k] we have |NΓ(Wi) ∩ U| ≥ d|Wi|/2, and
- • Γ[U] is a connected (β/2,d/2)-expander.


Now we can ﬁnish the proof using Lemma 3.3. For each i ∈ [k], set Ui = NΓ(Wi) ∩ U. Then |Ui| ≥ dℓ/2 =: s. For k < i ≤ q, take Ui ⊆ U to be an arbitrary set of size s. Apply Lemma 3.3 with sets U1,...,Uq, which we indeed can do as qs > 2|U| and |U|/s > log|U|, where the former follows from d ≥ t0(α)/4 and the latter follows from d ≤

√n. We obtain a subset T ⊆ U of size

![](<2503.06826_pg10_images/imageFile5.png>)

log |U| log d ≤ ℓ,

|T| ≤ K |U| s

qs |U|

·

log

![](<2503.06826_pg10_images/imageFile6.png>)

![](<2503.06826_pg10_images/imageFile7.png>)

![](<2503.06826_pg10_images/imageFile8.png>)

10

