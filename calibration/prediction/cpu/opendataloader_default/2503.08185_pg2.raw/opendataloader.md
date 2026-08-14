2 MIXING TIME OF A MATRIX RANDOM WALK

where Entπ(f2) = Eπ[f2 log f2]−Eπ[f2]log Eπ[f2] is the entropy of f2, and where EP(f,f) is the Dirichlet form deﬁned by

EP(f,f) =

π(x)P(x,y)(f(x) − f(y)) f(x).

x,y∈Ω

A classical result is that tmix(P,ε) ≤ CLS(P) log log

1 π⋆

![](<2503.08185_pg2_images/imageFile1.png>)

+ 2log

1 ε

![](<2503.08185_pg2_images/imageFile2.png>)

,

where π⋆ = minx∈Ω π(x) (see for instance [5] and [11]). Since in our case we have π⋆ ≍ 2n12 , we see that Theorem 1 will follow from the following proposition.

![](<2503.08185_pg2_images/imageFile3.png>)

- Proposition 2. The logarithmic Sobolev constant of P satisﬁes CLS(P) n2 .

In the above proposition and in the rest of the paper, the notation un vn means that there exists an absolute constant c > 0 such that for all n ≥ 1, we have un ≤ cvn.

Interestingly, a crucial ingredient in the proof of Proposition 2 is the bound of O(n) on the Poincare´ constant (inverse of the spectral gap), obtained by Kassabov [9]. Remark 1. Proposition 2 even yields an upper bound of O(n2 log n) for the ℓ2-mixing time, at least for the continuous-time and lazy versions of the chain.

We also study another chain on Ω, whose kernel is denoted by Q, and whose dynamics is as follows: if the current state is a matrix x ∈ Ω with rows ℓ1,... ,ℓn, then an index i between 1 and n is chosen uniformly at random, and row ℓi is replaced by ℓi + j =i ajℓj, wit (aj)j =i independent Bernoulli random variables with parameter 1/2. In other words, the chain Q randomizes a uniformly chosen row, conditionally on the event that the resulting matrix is invertible (it is the Gibbs sampler for the joint distributions of rows). The following proposition shows that the mixing time of Q lies between nlog n and 4nlog n whatever the value of the threshold ε, establishing a pre-cutoﬀ.

- Proposition 3. For all ε ∈ (0,1), there exists a constant cε > 0 such that nlog n − cεn ≤ tmix(Q,ε) ≤ 4nlog n − 2nlog log n + cεn.


In particular, the chain Q has a pre-cutoﬀ.

2. Related work

To our knowledge, the chain P was ﬁrst studied by Diaconis and Saloﬀ-Coste [6], who used a comparison with another chain on Ω studied by Hildebrand [8] to get an upper bound of O(n2) on the relaxation time (the inverse of the spectral gap), implying an upper bound of O(n4) on the ℓ2-mixing time. Then the results of Kassabov [9] on the Kazhdan constant yield an upper bound of O(n3) on the ℓ2-mixing time, which was the best known upper bound for total variation mixing as well. As for the lower bound, a simple counting

argument shows that the total-variation mixing time can be lower bounded by Ω log n2n (which is actually an estimate of the diameter of the underlying graph, see Andre´n et al.

![](<2503.08185_pg2_images/imageFile4.png>)

