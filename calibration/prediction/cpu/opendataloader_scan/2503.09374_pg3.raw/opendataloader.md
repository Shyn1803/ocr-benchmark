The paper is organized as follows: In section 2, we introduce Bayesian inversion framework and the Fisher information adaptive MALA. We outline the finite-dimensional Bayesian approach, describe the Fisher adaptive MALA process, and develop the convergence analysis. Section 3 presents numerical experiments for Bayesian inverse problems that demonstrate the effectiveness of this algorithm and compare its performance with other methods. Section 4 concludes the paper with a summary of the main findings and a discussion of potential directions for future research.

# 2 Fisher Adaptive MALA in Bayesian inversion

In this section, we review the Bayesian approach to inverse problems. Then, we apply the Fisher adaptive MALA to sample from the Bayesian posterior distributions arising in inverse problems.

# 2.1 Bayesian inversion framework

Throughout this work, we consider the inverse problem of finding an unknown parameter x ∈ R d from data y ∈ R n , where the relationship between x and y is described by the following model

$$
Y = (2.1)
$$

where F : R d → R n is referred as forward operator, and η represents the measurement noise, which is assumed to follow an n -dimensional Gaussian distribution. In the Bayesian framework, the vectors x , η and y are treated as random variables. Assuming that x and η are independent with π 0 as the prior distribution and η ∼ N (0 , Σ) as the Gaussian noise. The joint distribution of ( x,y ) is expressed as

$$
T(x,y) = T(y
$$

Furthermore, applying Bayes’ rule, the posterior distribution of the unknown parameter x from the observed data y is given by π ( y x ) π ( x )

$$
y) = x Z(y
$$

where, Z ( y ) is the normalization constant and

$$
4(x) := = (2.2)
$$

is the data fidelity term. For the prior distribution π 0 ( x ), we primarily assume a Gaussian prior with zero mean and covariance C , i.e. π 0 ( x ) = N (0 ,C ) and

$$

$$

Thus the posterior distribution can be expressed as:

$$
(2.3)
$$

Let π ( x ) = π ( x | y ) (here omit the conditioning of data y ), then the gradient of the log posterior is given by

$$
(2.4) =-C-1. log
$$

where ∇F ( x ) is the Fr ´ echet derivative of x .

A special case appears if F ( x ) is a linear mapping, such as F ( x ) = Fx . Then it is known from [ 19 ] that posterior distribution is Gaussian, i.e. π ( x | y ) = N ( µ post ,C post ) and the mean µ post and covariance matrix C post are given by − 1 ⊤ − 1 − 1 ⊤ − 1

$$
+ FT2-'F)-1 , (2.5) (C-1 Gpost Cpost
$$

and

$$
y) . (2.6)
$$

