Then we define the completion problem as follows:

$$
min (17) X
$$

such that ⊙ is the pointwise product. The following section presents the method to solve this problem.

# 5.1 Iterative Shrinkage Thresholding with Anderson acceleration

The Iterative Shrinkage Thresholding Algorithm (ISTA) is a class of first-order methods that can be seen as an extension of classical gradient methods, used to solve linear inverse problems such as ( 9 ). This algorithm is known for its simplicity and efficiency in addressing this type of problem. However, ISTA is known to converge slowly and exhibits a sublinear global rate of convergence. In [ 17 ], an extrapolation method is used to accelerate the algorithm, resulting in the Fast Iterative Shrinkage-Thresholding Algorithm (FISTA). In this work, we employ a different acceleration method, known as Anderson Acceleration (AA), to improve the performance of ISTA. The Anderson Acceleration (AA) method for fixed-point iterations, originally developed by D. G. Anderson, was primarily used in electronic structure computations. Despite its effectiveness, this method has not been as widely adopted as other acceleration techniques. In our specific problem, however, it demonstrates superior results in terms of precision compared to FISTA and other acceleration methods, as will be shown in the numerical results section. The new accelerated algorithm is presented in Algorithm 5 and is based on the work in [ 8 ], [ 18 ], and [ 7 ].

Let’s turn to the problem ( 9 ):

$$
min L(X, D(t); V) *t (18)
$$

$$
(19)
$$

The general solution to the problem ( 18 ) is given by

$$
Xk = Txt( Xk_1 (20) tDT
$$

such that T α : R M 1 × M 2 ×···× M N → R M 1 × M 2 ×···× M N is the shrinkage operator defined by:

$$
(21)
$$

The parameter t = 1 L , such that L is the Lipschitz continuous gradient of the function G . 1 2

Proposition 3. G is differentiable, the gradient is given by: and

$$
VG(X) = DT
$$

