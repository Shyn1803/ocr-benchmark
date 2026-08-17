4.2.2. Bratu problem. We use lrAA to solve the non-linear Bratu problem

$$
(x,y) € [0, 1] x [0, 1], Uxr
$$

with λ = 1 and homogeneous Dirichlet boundary conditions. To ﬁnd the approximate solution we discretize this equation using standard second order ﬁnite diﬀerence approximations for the x and y derivatives. Given an approximation X ( i,j ) ≈ u ( x i ,y j ) this results in a function G B ( i,j ; X ) describing the equation

$$
1 GB(i,j;X) = (X(i + 1,j) = 2X(i,j) + X(i _ 1,j)) h2 (4.2) 1 4 h2
$$

Near the boundaries some of the terms in this expression will be set to zero to account for the homogeneous Dirichlet boundary conditions. In the numerical examples below we take the mesh to be x i = ih x , h x = 1 m +1 and y j = jh y , h y = 1 n +1 with m = n = 200, making the setup the same as in [52]. The ﬁxed point function G ( i,j ) is obtained by applying the preconditioned Richardson iteration. We

The fixed function G(i,j) is obtained by applying the preconditioned Richardson iteration. We point have

$$
'(i,j) = G(i,j;Xk,0) = Xk+1 , Xk (
$$

We test lrAA with no preconditioner and with the ES preconditioner (corresponding to Rel1_x_n10.1E10 ) described above. The lrAA parameters used are the following TOL = 10 − 6 , ˆ m = 5 ,θ = 0 . 9 ,α = 0 . 125 h 2 x (un-preconditioned case) and α = 0 . 1 (preconditioned case, no scheduling is used). In all experiments we use a rank 1 matrix with Frobenius norm around 1.

The results in Figure 11 display the numerical solutions obtained by lrAA methods with and without the ES preconditioner. In particular, both methods obtain visually similar numerical results in terms of solution contours and column and row index section for the ﬁnal iterates. The un-preconditioned lrAA gives a montonically increasing intermediate ranks. The ES-preconditioned lrAA converges very rapidly in 8 iterations.

0.4

0.2

10

0.2

0.4

0.6

0.8

![](<2503.03909_pg14_images/imageFile1.png>)

-0.01

- -0.02
- -0.03


-0.04

- -0.05
- -0.06


10 2

10 0

10 -2 k

10

10

10 0

preconditioner

no

Preconditioned

10

preconditioner

no

preconditioned

10 -5

100

preconditioner

no

preconditioned

200

300

400

# iteration

500

100

200

300

400

# iteration

500

Fig. 11 . Bratu problem solved by lrAA. The top left ﬁgure displays the contour levels of the converged solution along with markers at the intersection points of the ﬁnal index sets I and J (for both lrAA with and without ES preconditioner). The top right ﬁgure displays the singular values from lrAA solutions with and without the ES preconditioner. The bottom left ﬁgure and right ﬁgures display the rank evolution and the decay of the residual throughout the lrAA iterations for lrAA with and without the ES preconditioner.

