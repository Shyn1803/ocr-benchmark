where we define

$$
0 for k = 0 ãk and = ~akk, for k = 1,2, (181) bkk , for k = 1,2,-
$$

It is assumed that both a r and b r are nonzero; otherwise, they should be removed, and r should be reduced.

Step 2: Define the coefficients h j as

$$
4 hj 2ão, (182) ãj-r j =r + 1,r + 2, 2r
$$

Since ˜ a 0 = 0, it follows that h r = 0.

Step 3: Next, define a 2 r × 2 r matrix B with entries B kj as

$$
for k = 1,2, 2r 1 hj-1 (183) for k = 2r, ãr ibr Bkj
$$

where δ k,j − 1 is the Kronecker delta function. For example, when r = 2, the matrix B is explicitly 0 1 0 0

$$
0 B= 0 (184) 0 ã2 ã2 -ib2 ã2 -ib2
$$

− − − Note that B has a significant sparse structure, with at most 4 r − 2 non-zero elements.

Step 4: Let the eigenvalues of B be denoted by z t ∈ C . [ 24 , Theorem 2] shows that the roots (which may be complex) of f ′ ( x ) = 0 are given by x t = − i log( z t ) where the complex logarithm is defined as log( z ) = log | z | + i (arg( z ) + 2 πm ) , ∀ m ∈ Z . Therefore, the final roots are

$$
It = (arg(zt) + 2Tm) = i Izt| t =1,2, 2r , Vm € Z. (185 _ log
$$

Since we are only interested in the real roots of f ′ ( x ), these real roots correspond to the eigenvalues z t lying on the unit circle. This simplifies to

$$
when (186)
$$

By

Step 5:

This method uses the inherent properties of trigonometric polynomials to transform the problem of finding the global minimizer of f ( x ) into an equivalent problem of determining all eigenvalues with modulus equal to 1 of a sparse non-Hermitian matrix B . Compared to directly using global optimization solvers (e.g., differential evolution), which are typically heuristic algorithms, this eigenvalue approach guarantees the identification of the global minimum, thereby avoiding the risk of getting trapped in local minima. Although eigenvalue problems may appear complex, in practical applications, the integer r is usually small, making it feasible to solve the eigenvalues of small matrices both efficiently and accurately.

