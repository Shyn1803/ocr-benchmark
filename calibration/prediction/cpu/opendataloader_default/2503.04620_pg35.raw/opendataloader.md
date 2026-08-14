where we define

a˜k =

0, for k = 0 bkk, for k = 1,2,...,r

and ˜bk = −akk,for k = 1,2,...,r. (181)

It is assumed that both ar and br are nonzero; otherwise, they should be removed, and r should be reduced.

- Step 2: Define the coefficients hj as

hj =

 



a˜r−j + i˜br−j, j = 0,1,...,r − 1, 2˜a0, j = r, a˜j−r − i˜bj−r, j = r + 1,r + 2,...,2r.

(182)

Since a˜0 = 0, it follows that hr = 0.

- Step 3: Next, define a 2r × 2r matrix B with entries Bkj as

Bkj =

 



δk,j−1, for k = 1,2,...,2r − 1, −

hj−1 a˜r − i˜br

, for k = 2r,

(183)

where δk,j−1 is the Kronecker delta function. For example, when r = 2, the matrix B is explicitly

B =

  

0 1 0 0 0 0 1 0 0 0 0 1

−a˜

2+i˜b2

a˜2−i˜b2 −a˜

1+i˜b1

a˜2−i˜b2 0 −a˜

1−i˜b1 a˜2−i˜b2

  . (184)

Note that B has a significant sparse structure, with at most 4r − 2 non-zero elements.

- Step 4: Let the eigenvalues of B be denoted by zt ∈ C. [24, Theorem 2] shows that the roots (which may be complex) of f′(x) = 0 are given by xt = −ilog(zt) where the complex logarithm is defined as log(z) = log |z| + i(arg(z) + 2πm),∀m ∈ Z. Therefore, the final roots are

xt = (arg(zt) + 2πm) − ilog |zt|, t = 1,2,...,2r, ∀m ∈ Z. (185) Since we are only interested in the real roots of f′(x), these real roots correspond to the eigenvalues zt lying on the unit circle. This simplifies to

xt = arg(zt) + 2πm, when |zt| = 1. (186) By taking xk modulo 2π, the final real roots can be obtained.

- Step 5: The global minimizer is the value of xt that yields the smallest f(x) among these points.


This method uses the inherent properties of trigonometric polynomials to transform the problem of finding the global minimizer of f(x) into an equivalent problem of determining all eigenvalues with modulus equal to 1 of a sparse non-Hermitian matrix B. Compared to directly using global optimization solvers (e.g., differential evolution), which are typically heuristic algorithms, this eigenvalue approach guarantees the identification of the global minimum, thereby avoiding the risk of getting trapped in local minima. Although eigenvalue problems may appear complex, in practical applications, the integer r is usually small, making it feasible to solve the eigenvalues of small matrices both efficiently and accurately.

35

