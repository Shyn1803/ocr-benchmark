Example 6.2. Consider the two-dimensional semilinear parabolic problem

∂u ∂t

(t,x,y) −

![](<2503.04674_pg19_images/imageFile1.png>)

∂2u ∂x2

(t,x,y) −

![](<2503.04674_pg19_images/imageFile2.png>)

∂2u ∂y2

1 1 + u(t,x,y)2

(t,x,y) =

+

![](<2503.04674_pg19_images/imageFile3.png>)

![](<2503.04674_pg19_images/imageFile4.png>)

1 1 + u(2t − 21,x,y)2

, (6.63)

![](<2503.04674_pg19_images/imageFile5.png>)

![](<2503.04674_pg19_images/imageFile6.png>)

![](<2503.04674_pg19_images/imageFile7.png>)

for (x,y) ∈ [0,1]2 and t ∈ [0,3], subject to homogeneous Dirichlet boundary conditions. The initial condition is given by φ(t,x,y) = e−tx(1 − x)y(1 − y) for t ∈ [−21,0].

![](<2503.04674_pg19_images/imageFile8.png>)

We apply standard ﬁnite diﬀerences with n = 200 grid points to discretize the problem in each spatial direction. In this example the exact solution is unknown. The reference solution is computed by the ERKC-C method with Gauss collocation points (s = 3) using the constant step size h = 2−11. The errors of the ERKC-I and ERKC-C methods in the L∞(Ω) and the L2(Ω) norm at ﬁnal time T = 3 are presented in Figures 3 and 4. The ﬁgures conﬁrm the theoretical analysis. Moreover, a comparison of computational cost of the ERKC methods with Gauss collocation points (s = 3) is presented in Table 1. For step sizes h = 2−k with k = 3,4,...,9, the ERKC-I method consistently reduces the CPU time by approximately 12% compared to the ERKC-C method, demonstrating its computational eﬃciency across a range of step sizes.

10-6

10-6

<table>
  <tr>
    <td>Gauss (s=1)<br><br>Radau IIA (s=2)<br><br>Gauss (s=2)<br><br>Radau IIA (s=3)<br><br><br>Gauss (s=3)<br><br><br></td>
  </tr>
</table>


<table>
  <tr>
    <td>Gauss (s=1)<br><br>Radau IIA (s=2)<br><br>Gauss (s=2)<br><br>Radau IIA (s=3)<br><br><br>Gauss (s=3)<br><br><br></td>
  </tr>
</table>


L Error of ERKC-C Methods

L Error of ERKC-I Methods

10-8

10-8

10-10

10-10

10-12

10-12

10-14

10-14

<table>
  <tr>
    <td>slope = 2<br><br>slope = 3<br><br>slope = 4<br></td>
  </tr>
</table>


<table>
  <tr>
    <td>slope = 2<br><br>slope = 3<br><br>slope = 4<br></td>
  </tr>
</table>


10-16

10-16

10-2 10-1

10-2 10-1

h

h

Figure 3: The convergence rates of ERKC-I methods (in the left panel) and ERKC-C methods (in the right panel) for (6.63). The errors are measured at T = 3 in the L∞(Ω) norm.

19

