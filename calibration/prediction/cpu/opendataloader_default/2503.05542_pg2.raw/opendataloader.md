L. Hucker, M. Reiß, T. Stark/Comparing regularisation paths 2

Consider a potentially high-dimensional linear regression setting under random design, where the number of features p can possibly exceed the sample size n. We are given i.i.d. observations (xi,yi), i = 1,...,n, of Rp-valued feature vectors xi and R-valued responses yi satisfying

yi = x⊤i β0 + εi, i = 1,...,n.

Here, β0 ∈ Rp is the unknown true coefficient vector. The error variables εi satisfy E[εi |Xi] = 0 and Var(εi |Xi) = σ2 for some noise level σ > 0. Using the notation y := (y1,...,yn)⊤, X := (x1,...,xn)⊤ and ε := (ε1,...,εn)⊤ for the response vector, the feature matrix and the error vector, respectively, we have the linear model

y = Xβ0 + ε. (1.1) The ridge regression (RR) estimator of β0 is obtained as minimizer of the penalised least squares

criterion

βˆλRR := argmin

Eλ(β) with Eλ(β) := 21n∥y − Xβ∥2 + λ2∥β∥2, (1.2)

β∈Rp

where λ ⩾ 0 is the penalty parameter. For λ = 0 we take the minimum-norm solution for βˆλRR, see Section 2 below. In practice, the RR estimator βˆλRR is calculated by iterative solvers, for which standard gradient descent (GD) or conjugate gradients applied to the normal equations (CGNE) are natural choices. The default option for ridge regression in the standard Python package scikit-learn [17] uses conjugate gradients, profiting from its fast numerical convergence.

Ali, Kolter and Tibshirani [2] have shown for the unpenalized criterion (λ = 0 in (1.2)) that the regularisation path of gradient flow (GF), the continuous-time analogue of gradient descent, can be very tightly bounded by the regularisation path of ridge regression, with a prediction error at each GF iterate bounded by a small factor times the RR prediction error under a naturally reparametrized ridge penalty λ′. In Proposition 3.2 below, we generalize this result to gradient flow solving the penalized criterion (1.2). Based on a precise non-asymptotic CG error control, our main result then bounds the prediction error for conjugate gradients after t iterations by the prediction error for gradient flow at iteration τt (Theorem 3.7). The time reparametrisation τt is genuinely data-dependent due to the nonlinear nature of CG, but explicit in terms of the CG residual polynomial. This comparison result is surprisingly strong and implies that CG has the same regularisation effects as gradient flow and a fortiori ridge regression. The constant involved in the bound only depends on the spectrum of the empirical covariance matrix of the feature vectors xi, which is discussed for polynomial eigenvalue decay, Marchenko-Pastur type spectral distributions and spiked covariance models in Example 3.9. This result is thus in line with other recent comparison and implicit regularisation theorems like Ali, Dobriban and Tibshirani [1] for stochastic gradient flow in regression or Wu et al. [22] for standard gradient descent in logistic regression.

The comparison result allows in particular to bound the CG oracle error (the minimal prediction error along the CG regularisation path) by the corresponding GF and RR oracle errors. Establishing that the GD prediction risk is decaying monotonously along the iterates for large penalties λ in Proposition 3.11, another application of the comparison result is the corresponding monotone bound on the CG errors. Since the main results are derived for in-sample prediction risk due to the intricate nonlinear dependencies in the CG iterates, we provide a transfer from in-sample to out-of-sample prediction risk in Proposition 3.13. This high-probability result is essentially valid if the effective rank of the feature covariance matrix is small compared to the sample size. The theoretical results are then illustrated in a high-dimensional simulation and a real data example, where the regularisation paths of CG, GD and RR indeed closely resemble each other, see Section 4.

