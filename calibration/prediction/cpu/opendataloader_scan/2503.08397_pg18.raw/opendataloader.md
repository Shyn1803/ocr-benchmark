target dataset T 0 , and therefore the TransPCA method would not be able to improve estimation accuracy of the factor strengths.

# 6 Useful Dataset Selection

In Section 2, we assume that all informative datasets   X ( k ) ,k ∈ A   are known in advance and the informative level is measured by equation (2.3). Corollary 3.1, Theorem 3.2 and Theorem 5.2 all assume that ε = o   1 / √ N 1 − α s   , which ensures that the oracle TransPCA estimators are consistent. However, in practice, we do not know the index set A in advance. Therefore, we need to select informative datasets from a huge amount of source panels to avoid negative transfer.

In the first step of the oracle TransPCA procedure,   Q (0) w is composed of the leading s eigenvectors of   P w , which can also be viewed as the solution of the following optimization problem

$$
(0) = arg max Tktr ke{O}UA
$$

Note that under Assumption 5,

$$
< tr (6.1) 2
$$

the informative level of the auxiliary datasets can be measured by tr   consider the following rectified problem

$$
= arg max Totr Tk max tr (6.2) QTQ=Is, QeRNxs ke[K] Pâ(
$$

where   T =   k ∈{ 0 }∪ [ K ] T k , τ ∈ [0 ,s ] is a threshold parameter. If τ = 0, it indicates that all auxiliary datasets are integrated together to estimate Q (0) w without any selection of datasets. If τ = s , it is equivalent to performing PCA solely based on the target dataset.

Note that the optimization problem in (6.2) involves combinatorial non-convex optimization, which makes it difficult and computationally expensive to obtain the global maximizer. As an alternative, we adopt the cyclic coordinate descent algorithm to numerically search for the local maximum of (6.2). Specifically in the

