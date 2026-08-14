Then we define the completion problem as follows:

- 1

- 2∥W ⊙ (D ∗t X − Y)∥F + λ∥X∥1, (17)


min

X

such that ⊙ is the pointwise product. The following section presents the method to solve this problem.

# 5.1 Iterative Shrinkage Thresholding with Anderson acceleration

The Iterative Shrinkage Thresholding Algorithm (ISTA) is a class of first-order methods that can be seen as an extension of classical gradient methods, used to solve linear inverse problems such as (9). This algorithm is known for its simplicity and efficiency in addressing this type of problem. However, ISTA is known to converge slowly and exhibits a sublinear global rate of convergence. In [17], an extrapolation method is used to accelerate the algorithm, resulting in the Fast Iterative Shrinkage-Thresholding Algorithm (FISTA). In this work, we employ a different acceleration method, known as Anderson Acceleration (AA), to improve the performance of ISTA. The Anderson Acceleration (AA) method for fixed-point iterations, originally developed by D. G. Anderson, was primarily used in electronic structure computations. Despite its effectiveness, this method has not been as widely adopted as other acceleration techniques. In our specific problem, however, it demonstrates superior results in terms of precision compared to FISTA and other acceleration methods, as will be shown in the numerical results section. The new accelerated algorithm is presented in Algorithm 5 and is based on the work in [8], [18], and [7].

Let’s turn to the problem (9):

- 1

- 2∥D(t) ∗t X − Y∥2F + λ∥X∥1, (18)


L(X,D(t);Y) =

min

X

=G(X) + λ∥X∥1 (19) The general solution to the problem (18) is given by

Xk = Tλt(Xk−1 − tDT ∗t (D ∗t Xk−1 − Y), (20) such that Tα : RM

1×M2×···×MN → RM

1×M2×···×MN is the shrinkage operator defined by:

Tα(X)i

1i2...iN = (|Xi1i2...iN| − α)+sgn(Xi1i2...iN). (21) The parameter t =

1 L

, such that L is the Lipschitz continuous gradient of the function

G. Proposition 3. Consider the function G(X) = 21∥D ∗t X − B∥2F. G is differentiable, and the gradient is given by:

∇G(X) = DT ∗t (D ∗t X − B).

14

