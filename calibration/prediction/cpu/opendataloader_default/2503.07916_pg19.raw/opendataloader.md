Convexification With Viscocity for EIT 19 are met. An explanation of the stopping criterion (8.4) is provided below.

We introduce the random noise in the observation data in (2.13) as follows: gξ

0 (x,x0) = g0 (x,x0)(1 + δξ0 (x)), x ∈ ∂Ω, gξ

0

(8.5)

1 (x,x0) = g1 (x,x0)(1 + δξ1 (x)), x ∈ Γ,

1

where ξ0 is the uniformly distributed random variable in the interval [−1,1] depending on the point x ∈ ∂Ω. Also, ξ1 is the uniformly distributed random variable in the interval [−1,1] depending on the point x ∈ Γ, and δ = 0.03 corresponds to the 3% noise level. Since we deal with the first φ−derivatives of the noisy functions gξ

0

0 (x,x0) and gξ

1

1 (x,x0), we have to design a numerical method to differentiate the noisy data. First, we use the natural cubic splines to approximate the noisy input data (8.5). Next, we use the derivatives of those splines to approximate the derivatives of corresponding noisy observation data. We generate the corresponding cubic splines in (0,2π) with the mesh grid size hφ = π/100, and then we calculate their derivatives to approximate the first derivatives with respect to φ.

We choose the optimal pair of parameters (α,ε) by the trial and error procedure for the reference Test 1. For each considered pair (α,ε), we test different values of the parameter λ to obtain its optimal value λopt (α,ε) for this pair. Once the so chosen triple (α,ε,λ) of parameters is selected, we consider it as the optimal choice of parameters. An important point to make here is that exactly the same triple of optimal parameters is used for all follow up tests when imaging letters below. However, when using the CT scan of the abdomen below, we deal with a different medium. This means that we repeat the procedure of our choice of parameters again for this case.

# Remarks 8.1:

- (i) As the test media, we intentionally choose letter-like shapes of inclusions in the first series of numerical experiments and the CT scans of the abdomen in the second series. This is done to demonstrate that our technique works well for complicated media.
- (ii) The above procedure of the choice of an optimal triple (α,ε,λ) of parameters is similar to the conventional calibration procedure, which is often used in many real World applications. Furthermore, quite similar procedures were used in all above cited works [18, 19, 20, 22, 23, 24] on the numerical studies of the convexification method for CIPs.
- (iii) Even though theorems of our convergence analysis are valid only for sufficiently large values of the parameter λ, we have discovered in all our works on the convexification listed in item 2 that actually optimal values of λ belong to the interval λ ∈ [1,5]. In fact, this is similar with many asymptotic theories. Indeed, it is typically established in such a theory that if a certain parameter X is sufficiently large, then a certain formula Y provides a good approximation for a process. However, it is also typical that in a computational practice only numerical experiments can tell one which exactly values of X are appropriate ones.


