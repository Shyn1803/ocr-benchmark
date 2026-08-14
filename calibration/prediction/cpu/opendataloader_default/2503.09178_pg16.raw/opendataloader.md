polynomial degree N at M = 11, while Figure 3(b) displays the L2-errors with respect to the angular discretization number M + 1 at N = 30.

100

10-5

10-10

10-15

3 4 5 6 7 8

10-5

10-10

10-15

2 4 6 8 10 12 14

(a) Numerical errors u − uMN L2 vs. N (M = 11).

(b) Numerical errors u−uMN L2 vs. M+1 (N = 30).

Figure 3: The L2-errors versus N and M + 1 of Example 1 using the spectral method.

From Figure 3(a), it is evident that the proposed method exhibits spectral accuracy concerning the polynomial degree N. As the degree N increases to 6, the L2-errors approach the machine epsilon, indicating the convergence of the numerical solution to the exact solution. Similarly, in Figure 3(b), it can be observed that when the angular discretization number M +1 is small (e.g., M = 1), the L2-errors also approach the machine epsilon. This occurs because the exact solution is a sixth-degree polynomial solely in the spatial variable x and is entirely independent of the angular variable µ. As a result, selecting N = 6 and M = 1 enables the L2-error to reach machine epsilon.

Furthermore, by comparing Figure 2(b) and Figure 3(a), it is evident that for problems with a higher regularity of the exact solution, the spectral method requires fewer degrees of freedom compared to the Hermite WENO fast sweeping method to achieve the same level of accuracy.

# 5.2 Example 2

In this test, we solve the absorbing-scattering transfer problem described by the equation (1.1) with

Σt = 22000, Σs = 1, s(x,µ) = −4πµ3 cos3 πxsin πx + Σt(µ2 cos4 πx + const) − Σs(const +

cos4 πx 3

).

![](<2503.09178_pg16_images/imageFile1.png>)

Here const = 10−14 is a small positive constant which is used to ensure the source term to be nonnegative. The computational domain is D = (0,1). The boundary condition is given as follows

- ϕ(0,µ) = µ2 + const, if µ > 0,
- ϕ(1,µ) = µ2 + const, if µ < 0.


For this problem, we have the exact solution given as [25] ϕ(x,µ) = µ2 cos4 πx + const. 16

