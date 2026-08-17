Example 6.2. Consider the two-dimensional semilinear parabolic problem

$$
Ou 02u (6.63) 1 + u(t,2,9)2
$$

for ( x,y ) ∈ [0 , 1] 2 and t ∈ [0 , 3], subject to homogeneous Dirichlet boundary conditions. The initial condition is given by φ ( t,x,y ) = e − t x (1 − x ) y (1 − y ) for t ∈ [ − 1 2 , 0].

We apply standard ﬁnite diﬀerences with n = 200 grid points to discretize the problem in each spatial direction. In this example the exact solution is unknown. The reference solution is computed by the ERKC-C method with Gauss collocation points ( s = 3) using the constant step size h = 2 − 11 . The errors of the ERKC-I and ERKC-C methods in the L ∞ (Ω) and the L 2 (Ω) norm at ﬁnal time T = 3 are presented in Figures 3 and 4. The ﬁgures conﬁrm the theoretical analysis. Moreover, a comparison of computational cost of the ERKC methods with Gauss collocation points ( s = 3) is presented in Table 1. For step sizes h = 2 − k with k = 3 , 4 ,..., 9, the ERKC-I method consistently reduces the CPU time by approximately 12% compared to the ERKC-C method, demonstrating its computational eﬃciency across a range of step sizes.

![](<2503.04674_pg19_images/imageFile1.png>)

10

10

Radau IIA (s-2

Radau IIA (s-2

Gauss (s-2)

Gauss

(s=3)

10 -8

10 -8

Radau IIA (s-3

Radau IIA (s-3

Gauss (s-3)

Gauss

010-10

10-10

10 -14 L

10 -14 L

slope

slope

slope =

slope =

slope

slope

10 -16

10 -16

10 -2

10 -1

10 -2

10 -1

Figure 3: The convergence rates of ERKC-I methods (in the left panel) and ERKC-C methods (in the right panel) for (6.63). The errors are measured at T = 3 in the L ∞ (Ω) norm.

