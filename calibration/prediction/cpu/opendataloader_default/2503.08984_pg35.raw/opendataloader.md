# where ψ(x) = e|x|(1 + |x|) − 1.

We construct the coupling recursively. For the base case with t = 0, clearly P{G0e = Te0} = 1. Condition on Te2t = G2et (with an appropriate vertex mapping) and event C2t. We aim to

construct a coupling so that Te2t+1 = G2et+1 and Te2t+2 = G2et+2 with probability at least 1−n−Ω(1). Each vertex u in ∂G2et has Bu number of incident blue edges connecting to vertices in [n]\V (G2et),

where the Bu’s are i.i.d. Binom(n−|V (G2et)|,λ/n). Similarly, each vertex u in ∂Te2t has B˜u number of incident blue edges, where the B˜u’s are i.i.d. Pois(λ). Thus, we can couple Bu’s to B˜u′ s using (26) and take a union bound over u ∈ ∂G2et ≡ ∂Te2t. In particular,

P Bu = B˜u,∀u ∈ ∂G2et | G2et = Te2t,C2t ≥ 1 − ∂G2et λ2/n + ψ λ − (n − |V (G2et)|)λ/n ≥ 1 − (2kλ + 2)t log n λ2/n + O (2kλ + 1)t+1λ/n ≥ 1 − n−1+o(1),

where the second inequality holds because conditional on C2t, |∂G2et| ≤ (2kλ + 2)t log n and |V (G2et)| ≤ (2kλ + 1)t+1 log n. Thus, we have constructed a coupling such that Bu = B˜u for all u ∈ ∂G2et with probability at least 1 − n−1+o(1).

Recall that if event E2t occurs, the set of blue edges added to G2et+1 connect to distinct vertices in [n] \ V (G2et). Thus, on event E2t ∩ {Bu = B˜u,∀u ∈ ∂G2et}, there exists a one-to-one mapping from the vertices in ∂G2et+1 to vertices in ∂Te2t+1 such that G2et+1 = Te2t+1. Further, recall that on event E2t+1, each vertex u in ∂G2et+1 has exactly k incident red edges, and these red edges connect to distinct vertices in [n] \ V (G2et+1). Thus, on the event E2t+1 ∩ E2t ∩ {Bu = B˜u,∀u ∈ ∂G2et}, there exists a one-to-one mapping from the vertices in ∂G2et+2 to the vertices in ∂Te2t+2, so that Ge2t+2 = Te2t+2. In conclusion, we get that

P Ge2t+2 = T2t+2 | G2et = T2t,C2t ≥ P E2t+1 ∩ E2t ∩ {Bu = B˜u,∀u ∈ ∂G2et} | G2et = T2t,C2t ≥ P Bu = B˜u,∀u ∈ ∂G2et | G2et = T2t,C2t − P E2t+1 ∩ E2t c | G2et = T2t,C2t ≥ 1 − n−1+o(1),

where the last inequality holds by Lemma F.3, since we are assuming (2kλ + 2)t log n = no(1). Moreover,

P G2et+2 = T2t+2,C2t+2 | G2et = T2t,C2t ≥ P G2et+2 = T2t+2 | G2et = T2t,C2t − (1 − P C2t+2 | G2et = T2t,C2t ) ≥ 1 − n−Ω(1),

where the last inequality holds by combining the last displayed equation with Lemma F.2. It

35

