The paper is organized as follows: In section 2, we introduce Bayesian inversion framework and the Fisher information adaptive MALA. We outline the finite-dimensional Bayesian approach, describe the Fisher adaptive MALA process, and develop the convergence analysis. Section 3 presents numerical experiments for Bayesian inverse problems that demonstrate the effectiveness of this algorithm and compare its performance with other methods. Section 4 concludes the paper with a summary of the main findings and a discussion of potential directions for future research.

# 2 Fisher Adaptive MALA in Bayesian inversion

In this section, we review the Bayesian approach to inverse problems. Then, we apply the Fisher adaptive MALA to sample from the Bayesian posterior distributions arising in inverse problems.

## 2.1 Bayesian inversion framework

Throughout this work, we consider the inverse problem of finding an unknown parameter x ∈ Rd from data y ∈ Rn, where the relationship between x and y is described by the following model

y = F(x) + η, (2.1)

where F : Rd → Rn is referred as forward operator, and η represents the measurement noise, which is assumed to follow an n-dimensional Gaussian distribution. In the Bayesian framework, the vectors x, η and y are treated as random variables. Assuming that x and η are independent with π0 as the prior distribution and η ∼ N(0,Σ) as the Gaussian noise. The joint distribution of (x,y) is expressed as

π(x,y) = π(y | x)π0(x).

Furthermore, applying Bayes’ rule, the posterior distribution of the unknown parameter x from the observed data y is given by

π(y|x)π0(x)

Z(y) ∝ exp(−Φ(x))π0(x), where, Z(y) is the normalization constant and

π(x | y) =

- 1

- 2 F(x) − y 2Σ =


Φ(x) :=

- 1

- 2


(F(x) − y)⊤Σ−1(F(x) − y), (2.2)

is the data fidelity term. For the prior distribution π0(x), we primarily assume a Gaussian prior with zero mean and covariance C, i.e. π0(x) = N(0,C) and

- 1

- 2∥x∥2C} = exp{−


- 1

- 2


x⊤C−1x}. Thus the posterior distribution can be expressed as:

π0(x) ∝ exp{−

- 1

- 2


x 2C}. (2.3) Let π(x) = π(x | y) (here omit the conditioning of data y), then the gradient of the log posterior is given by ∇log π(x) = −C−1x − ∇Φ(x) and ∇Φ(x) = (∇F(x))⊤Σ−1(F(x) − y), (2.4)

π(x | y) ∝ exp{−Φ(x) −

where ∇F(x) is the Frechet´ derivative of x.

A special case appears if F(x) is a linear mapping, such as F(x) = Fx. Then it is known from [19] that posterior distribution is Gaussian, i.e. π(x | y) = N(µpost,Cpost) and the mean µpost and covariance matrix Cpost are given by

Cpost = (C−1 + F⊤Σ−1F)−1, µpost = CpostF⊤Σ−1y, (2.5) and

∇Φ(x) = F⊤Σ−1(Fx − y). (2.6)

3

