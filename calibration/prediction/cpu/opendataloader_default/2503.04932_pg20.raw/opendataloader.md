20 Joseph Nakao, Gianluca Ceruti, Lukas Einkemmer

![](<2503.04932_pg20_images/imageFile1.png>)

![](<2503.04932_pg20_images/imageFile2.png>)

Fig. 2: Error plot for (66) with initial condition

(67) using backward Euler, DIRK2 and DIRK3.

Fig. 3: Error plot for (69) with initial condition u0(x,y,z,) = 2k=1 sin(kx)sin(ky)sin(kz) using IMEX111, IMEX222 and IMEX443.

![](<2503.04932_pg20_images/imageFile3.png>)

![](<2503.04932_pg20_images/imageFile4.png>)

![](<2503.04932_pg20_images/imageFile5.png>)

Fig. 4: The multilinear rank (r1,r2,r3) and average of the multilinear rank (r1+r2+r3)/3 of the solution to (66) with initial condition (67) using backward Euler (left), DIRK2 (middle) and DIRK3 (right).

As seen in Figure 3, the expected accuracies are observed for the RAIL scheme when using IMEX111, IMEX222 and IMEX443. We used a mesh size N = 80, tolerance ε = 10−6, final time Tf = 0.3, and λ ranging from 0.1 to 1. Despite observing the expected accuracy, the L1 error for the first-order scheme (and even the second-order scheme) is quite large. However, recall that we do not scale the L1 error by the measure of the domain, which in this case would be |Ω| = (2π)3; scaling by the measure of the domain would provide a better comparison against the L∞ error which is not as large.

# Example 3 (Rigid body rotation with diffusion, about zˆ)

ut − yux + xuy = d(uxx + uyy + uzz) + c(x,y,z,t), x,y,z ∈ (−2π,2π) (71)

where the flow field describes rotation about the vector zˆ. To test the accuracy of the scheme, we use the manufactured solution u(x,y,z,t) = exp(−(x2 +2y2 +3z2 +3dt)) with d = 1/3, for which the source term c(x,y,z,t) offsets the rotation and is

2+2y2+3z2+3dt) − 2xy − d(−9 + 4x2 + 16y2 + 36z2) . (72)

c(x,y,z,t) = e−(x

As seen in Figure 5, the expected accuracies are observed for the RAIL scheme when using IMEX111, IMEX222 and IMEX443. We used a mesh size N = 80, tolerance ε = 10−8, final time Tf = 0.3, and λ ranging from 0.5 to 2. When a low-rank source term is involved, we must express it in a Tucker tensor format. By inspection, it is straightforward for one to write down a Tucker decomposition of (72).

To test the rank of the solution, we set d = 1/12, c(x,y,z,t) = 0, double the speed of the rotation,

ut − 2yux + 2xuy =

1 12

(uxx + uyy + uzz), x,y,z ∈ (−2π,2π) (73)

and set the initial condition to u0(x,y,z) = exp(−(x2 +9y2 +z2)). The solution rotates counterclockwise about the positive z-axis while slowly diffusing. Theoretically, the exact multilinear rank should be

