Consider a potentially high-dimensional linear regression setting under random design, where the number of features p can possibly exceed the sample size n . We are given i.i.d. observations ( x i ,y i ), i = 1 ,...,n , of R p -valued feature vectors x i and R -valued responses y i satisfying

$$
= S; Bo + €i, i = 1,
$$

Here; Bo € RP is the unknown true coefficient vector _ Xi , Un) T Tn) T and € 2= (€1, En) T for the response vector, the feature matrix and the error vector; respectively; we have the linear model 02

$$
y = XBo + €. (1.1)
$$

The ridge regression (RR) estimator of β 0 is obtained as minimizer of the penalised least squares criterion ˆ RR 1 2 λ 2

$$
= with 4 (1.2) BeRP XBll2
$$

where λ ⩾ 0 is the penalty parameter. For λ = 0 we take the minimum-norm solution for ˆ β RR λ , see Section 2 below. In practice, the RR estimator ˆ β RR λ is calculated by iterative solvers, for which standard gradient descent (GD) or conjugate gradients applied to the normal equations (CGNE) are natural choices. The default option for ridge regression in the standard Python package scikit-learn [ 17 ] uses conjugate gradients, profiting from its fast numerical convergence. Ali, Kolter and Tibshirani [ 2 ] have shown for the unpenalized criterion ( = 0 in ( 1.2 )) that the

λ regularisation path of gradient flow (GF), the continuous-time analogue of gradient descent, can be very tightly bounded by the regularisation path of ridge regression, with a prediction error at each GF iterate bounded by a small factor times the RR prediction error under a naturally reparametrized ridge penalty λ ′ . In Proposition 3.2 below, we generalize this result to gradient flow solving the penalized criterion ( 1.2 ). Based on a precise non-asymptotic CG error control, our main result then bounds the prediction error for conjugate gradients after t iterations by the prediction error for gradient flow at iteration τ t (Theorem 3.7 ). The time reparametrisation τ t is genuinely data-dependent due to the nonlinear nature of CG, but explicit in terms of the CG residual polynomial. This comparison result is surprisingly strong and implies that CG has the same regularisation effects as gradient flow and a fortiori ridge regression. The constant involved in the bound only depends on the spectrum of the empirical covariance matrix of the feature vectors x i , which is discussed for polynomial eigenvalue decay, Marchenko-Pastur type spectral distributions and spiked covariance models in Example 3.9 . This result is thus in line with other recent comparison and implicit regularisation theorems like Ali, Dobriban and Tibshirani [ 1 ] for stochastic gradient flow in regression or Wu et al. [ 22 ] for standard gradient descent in logistic regression. The comparison result allows in particular to bound the CG oracle error (the minimal prediction error

along the CG regularisation path) by the corresponding GF and RR oracle errors. Establishing that the GD prediction risk is decaying monotonously along the iterates for large penalties λ in Proposition 3.11 , another application of the comparison result is the corresponding monotone bound on the CG errors. Since the main results are derived for in-sample prediction risk due to the intricate nonlinear dependencies in the CG iterates, we provide a transfer from in-sample to out-of-sample prediction risk in Proposition 3.13 . This high-probability result is essentially valid if the effective rank of the feature covariance matrix is small compared to the sample size. The theoretical results are then illustrated in a high-dimensional simulation and a real data example, where the regularisation paths of CG, GD and RR indeed closely resemble each other, see Section 4 .

