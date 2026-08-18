− is the Dirichlet form deﬁned by

$$

$$

classical result is that

$$
+ 2log log log
$$

where π ⋆ = min x ∈ Ω π ( x ) (see for instance [ 5 ] and [ 11 ]). Since in our case we have π ⋆ ≍ 1 2 n 2 , we see that Theorem 1 will follow from the following proposition.

Proposition 2. The logarithmic Sobolev constant of P satisﬁes

$$
Cs (P) n2
$$

In the above proposition and in the rest of the paper, the notation u n   v n means that there exists an absolute constant c > 0 such that for all n ≥ 1, we have u n ≤ cv n .

Interestingly, a crucial ingredient in the proof of Proposition 2 is the bound of O ( n ) on the Poincare´ constant (inverse of the spectral gap), obtained by Kassabov [ 9 ].

Remark 1. Proposition 2 even yields an upper bound of O ( n 2 log n time, at least for the continuous-time and lazy versions of the chain.

is as follows: if the current state is a matrix x ∈ Ω with rows ℓ 1 ,... ,ℓ n , then an index i between 1 and n is chosen uniformly at random, and row ℓ i is replaced by ℓ i +   j   = i a j ℓ j , wit ( a j ) j   = i independent Bernoulli random variables with parameter 1 / 2. In other words, the chain Q randomizes a uniformly chosen row, conditionally on the event that the resulting matrix is invertible (it is the Gibbs sampler for the joint distributions of rows). The following proposition shows that the mixing time of Q lies between n log n and 4 n log n whatever the value of the threshold ε , establishing a pre-cutoﬀ.

Proposition 3. For all ε ∈ (0 , 1) , there exists a constant c ε > 0 such that

$$
n n = Cen < tmix(Q, €) < 4n n 2n log n + Cen _ log log' log '
$$

In particular, the chain Q has a pre-cutoﬀ.

# 2 RELATED WORK

To our knowledge, the chain P was ﬁrst studied by Diaconis and Saloﬀ-Coste [ 6 ], who used a comparison with another chain on Ω studied by Hildebrand [ 8 ] to get an upper bound of O ( n 2 ) on the relaxation time (the inverse of the spectral gap), implying an upper bound of O ( n 4 ) on the ℓ 2 -mixing time. Then the results of Kassabov [ 9 ] on the Kazhdan constant yield an upper bound of O ( n 3 ) on the ℓ 2 -mixing time, which was the best known upper bound for total variation mixing as well. As for the lower bound, a simple counting argument shows that the total-variation mixing time can be lower bounded by Ω   n 2 log n   (which is actually an estimate of the diameter of the underlying graph, see Andre´n et al.

