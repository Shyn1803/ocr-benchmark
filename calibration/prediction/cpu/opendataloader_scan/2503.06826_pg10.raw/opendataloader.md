We are now ready to prove Theorem 1.3.

Proof of Theorem 1.3. Let X ⊆ V ( G ) be a subset given by Lemma 2.4. We pass on to Γ = G [ X ]. The graph Γ has N ≥ αn/ 128 vertices, and for β = αn/ (8 N ) and d = t/ 4, the following holds:

(i) Γ is a ( β,d )-expander, and

(ii)  for every partition V(T) an edge in F between A and B.

Let K = 25 /α 2 (the constant in the upper bound on the size of T in Lemma 3.3). Consider the family P of all ordered partitions V (Γ) = D ∪     k i =1 W i   ∪ U , where k ≥ 0 (this can be a diﬀerent number for diﬀerent partitions), such that the following holds:

- (P1) 2K N log N =: F[W;] is connected ,
- (P2) for every two distinct i,i ′ ∈ [ k ], there is an edge in Γ between W i and W i ′ , and


d|Dl/2.

The ﬁrst two properties imply that K k is a minor of Γ. By taking D = , k = 0 and U = V (Γ), we have

∅ that P is not empty. Consider a partition V (Γ) = D ∪     k i =1 W i   ∪ U in P which maximises | D | , tie-breaking by taking one which further maximises k . We prove that then necessarily

$$
QN k > 640
$$

As q = Θ(   nt/ log n ), this establishes the theorem. Suppose, towards a contradiction, that this is note the case. That is, k < q . Then

$$
i=1
$$

| | ≥ The property (P3) in the proof of Theorem 1.4 is identical to the one used here, and the only property of W used in the proof of Claim 3.1 and Claim 3.2 is the upper bound on | W | , which is identical to the one used here. Therefore, same as in the proof of Theorem 1.4, the following holds:

For every i ∈ [ k ]

Now we can ﬁnish the proof using Lemma 3.3. For each i ∈ [ k ], set U i = N Γ ( W i ) ∩ U . Then | U i | ≥ dℓ/ 2 =: s . For k < i ≤ q , take U i ⊆ U to be an arbitrary set of size s . Apply Lemma 3.3 with sets U 1 ,...,U q , which we indeed can do as qs > 2 | U | and | U | /s > log | U | , where the former follows from d ≥ t 0 ( α ) / 4 and the latter follows from d ≤ √ n . We obtain a subset T ⊆ U of size

$$
log log d
$$

