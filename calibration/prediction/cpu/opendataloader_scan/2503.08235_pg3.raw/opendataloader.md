# 2. Multiparameter quantum estimation: precision, sloppiness and incompatibility

In this section, we provide the theoretical framework, definitions and metrics used throughout the paper. We consider finite dimensional systems and a family of quantum states ρ λ encoding the values of d real parameters, denoted as a vector λ = ( λ 0 ,λ 1 ,...,λ d ) T . If we perform a positive operator-valued measurement (POVM) Π with elements { Π k } satisfying Π k ≥ 0 and   k Π k = I , the measurement outcome k is obtained with probability p λ ( k ) = Tr[ ρ λ Π k ]. The estimator function based on the result is denoted as ˆ λ ( k ). The performance of the estimator is assessed by the covariance matrix V ( ˆ λ ) with elements

$$
= (k)[Âp(k) = Ev(Âv)J[Âv(k) = Ek(Âv)]:
$$

where E k ( ˆ λ µ ) is the expectation value of ˆ λ µ over the probability distribution p λ ( k ).

In classical multiparameter estimation, when the estimators satisfying the locally unbiased conditions:

$$
E (Â) = Â
$$

where ∂ µ = ∂ ∂λ µ , then the CRB [51] holds

$$
1 V(Â) 2 MF
$$

where M is the number of repeated measurements and F is the FI matrix with elements defined by

$$
k Fuv px (k) = px (k) log log
$$

The CRB can be saturated in the asymptotic limit of an infinite number of repeated experiments using Bayesian or maximum likelihood estimators [52].

Due to the non-commutativity of the operators on H , the quantum analogue of the FI cannot be uniquely introduced. In fact, there exist several different definitions of quantum Fisher information. The most celebrated and useful approaches are based on the so-called symmetric logarithmic derivative (SLD) operators L S µ [53] and right logarithmic derivative (RLD) operators L R µ [54, 55], defined as follows

$$
2
$$

$$
pxLR
$$

We denote the corresponding SLD and RLD quantum Fisher information matrices (QFIM) as Q and J , respectively, with elements

$$
Quv Tr 2 Juv Tr
$$

