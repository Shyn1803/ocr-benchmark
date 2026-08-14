14 D. APPELO¨ AND Y. CHENG 4.2.2. Bratu problem. We use lrAA to solve the non-linear Bratu problem uxx + uyy + λeu = 0, (x,y) ∈ [0,1] × [0,1],

with λ = 1 and homogeneous Dirichlet boundary conditions. To ﬁnd the approximate solution we discretize this equation using standard second order ﬁnite diﬀerence approximations for the x and y derivatives. Given an approximation X(i,j) ≈ u(xi,yj) this results in a function GB(i,j;X) describing the equation

1 h2x

(X(i + 1,j) − 2X(i,j) + X(i − 1,j))

GB(i,j;X) =

![](<2503.03909_pg14_images/imageFile1.png>)

(4.2)

1 h2x

(X(i,j + 1) − 2X(i,j) + X(i,j − 1)) + λeX(i,j).

+

![](<2503.03909_pg14_images/imageFile2.png>)

Near the boundaries some of the terms in this expression will be set to zero to account for the homogeneous Dirichlet boundary conditions. In the numerical examples below we take the mesh to be xi = ihx, hx = m1+1 and yj = jhy, hy = n+11 with m = n = 200, making the setup the same as in [52].

![](<2503.03909_pg14_images/imageFile3.png>)

![](<2503.03909_pg14_images/imageFile4.png>)

The ﬁxed point function G(i,j) is obtained by applying the preconditioned Richardson iteration. We have

Xk+1(i,j) = G(i,j;Xk,α) ≡ Xk(i,j) + αM(GB(i,j;Xk)). We test lrAA with no preconditioner and with the ES preconditioner (corresponding to Rel1_x_n10.1E10) described above. The lrAA parameters used are the following TOL = 10−6,mˆ = 5,θ = 0.9,α = 0.125h2x (un-preconditioned case) and α = 0.1 (preconditioned case, no scheduling is used). In all experiments we use a rank 1 matrix with Frobenius norm around 1.

The results in Figure 11 display the numerical solutions obtained by lrAA methods with and without the ES preconditioner. In particular, both methods obtain visually similar numerical results in terms of solution contours and column and row index section for the ﬁnal iterates. The un-preconditioned lrAA gives a montonically increasing intermediate ranks. The ES-preconditioned lrAA converges very rapidly in 8 iterations.

0

<table>
  <tr>
    <td> </td>
  </tr>
</table>


![](<2503.03909_pg14_images/imageFile5.png>)

102

<table>
  <tr>
    <td><table>
  <tr>
    <td>no preconditioner<br><br>Preconditioned</td>
  </tr>
</table>
</td>
  </tr>
</table>


-0.01

0.8

100

-0.02

0.6

-0.03

y

10-2

k

0.4

-0.04

10-4

0.2

-0.05

10-6

-0.06

0.2 0.4 0.6 0.8

0 2 4 6 8 10

x

k

100

<table>
  <tr>
    <td> </td>
  </tr>
  <tr>
    <td> </td>
  </tr>
  <tr>
    <td><table>
  <tr>
    <td>no preconditioner<br><br>preconditioned</td>
  </tr>
</table>
</td>
  </tr>
</table>


<table>
  <tr>
    <td><table>
  <tr>
    <td>no preconditioner<br><br>preconditioned</td>
  </tr>
</table>
</td>
  </tr>
</table>


10

8

residual

6

rank

10-5

4

2

0

0 100 200 300 400 500

0 100 200 300 400 500

# iteration

# iteration

Fig. 11. Bratu problem solved by lrAA. The top left ﬁgure displays the contour levels of the converged solution along with markers at the intersection points of the ﬁnal index sets I and J (for both lrAA with and without ES preconditioner). The top right ﬁgure displays the singular values from lrAA solutions with and without the ES preconditioner. The bottom left ﬁgure and right ﬁgures display the rank evolution and the decay of the residual throughout the lrAA iterations for lrAA with and without the ES preconditioner.

