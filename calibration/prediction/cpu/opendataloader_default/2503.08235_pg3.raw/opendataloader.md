# 2. Multiparameter quantum estimation: precision, sloppiness and incompatibility

3

In this section, we provide the theoretical framework, definitions and metrics used throughout the paper. We consider finite dimensional systems and a family of quantum states ρλ encoding the values of d real parameters, denoted as a vector λ = (λ0,λ1,...,λd)T. If we perform a positive operator-valued measurement (POVM) Π with elements {Πk} satisfying Πk ≥ 0 and k Πk = I, the measurement outcome k is obtained with probability pλ(k) = Tr[ρλΠk]. The estimator function based on the result is denoted as λˆ(k). The performance of the estimator is assessed by the covariance matrix V(λˆ) with elements

Vµν =

k

pλ(k)[λˆµ(k) − Ek(λˆν)][λˆν(k) − Ek(λˆν)].

where Ek(λˆµ) is the expectation value of λˆµ over the probability distribution pλ(k).

In classical multiparameter estimation, when the estimators satisfying the locally unbiased conditions:

Eν(λˆ) = λˆ ∂µEk(λˆν) = δµν, where ∂µ = ∂λ∂

, then the CRB [51] holds V(λˆ) ≥

µ

1 MF

,

where M is the number of repeated measurements and F is the FI matrix with elements defined by

∂µpλ(k)∂νpλ(k) pλ(k)

Fµν =

pλ(k)∂µ log pλ(k)∂ν log pλ(k) =

.

k

k

The CRB can be saturated in the asymptotic limit of an infinite number of repeated experiments using Bayesian or maximum likelihood estimators [52].

Due to the non-commutativity of the operators on H, the quantum analogue of the FI cannot be uniquely introduced. In fact, there exist several different definitions of quantum Fisher information. The most celebrated and useful approaches are based on the so-called symmetric logarithmic derivative (SLD) operators LSµ [53] and right logarithmic derivative (RLD) operators LRµ [54, 55], defined as follows

LSµρλ + ρλLSµ 2

∂µρλ =

, ∂µρλ = ρλLRµ.

We denote the corresponding SLD and RLD quantum Fisher information matrices (QFIM) as Q and J, respectively, with elements

- 1

- 2


Tr ρλ{LSµ,LSν} , Jµν = Tr ρλLRµLRν † .

Qµν =

