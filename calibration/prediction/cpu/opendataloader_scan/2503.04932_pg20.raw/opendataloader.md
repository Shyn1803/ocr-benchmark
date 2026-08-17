![](<2503.04932_pg20_images/imageFile1.png>)

10-1

10-?

10-3

10 4

bEuler

DIRK2

10-5

DIRK3

Order

Order 2

Order

10-6

2.5

0.5

1.5

Fig. 2: Error plot for ( 66 ) with initial condition ( 67 ) using backward Euler, DIRK2 and DIRK3.

![](<2503.04932_pg20_images/imageFile2.png>)

10

100

10

- 10-2
- 10-3


IMEX111

10 4

IMEX222

IMEX443

Order

Order 2

Order 3

100

10-1

3: Error plot for (69) with initial condition Uo IMEXIlI, IMEX222 and IMEX443. using

![](<2503.04932_pg20_images/imageFile3.png>)

Fig. 4: The multilinear rank ( r 1 ,r 2 ,r 3 ) and average of the multilinear rank ( r 1 + r 2 + r 3 ) / 3 of the solution to ( 66 ) with initial condition ( 67 ) using backward Euler (left) , DIRK2 (middle) and DIRK3 (right) .

As seen in Figure 3 , the expected accuracies are observed for the RAIL scheme when using IMEX111, IMEX222 and IMEX443. We used a mesh size N = 80, tolerance ε = 10 − 6 , final time T f = 0 . 3, and λ ranging from 0.1 to 1. Despite observing the expected accuracy, the L 1 error for the first-order scheme (and even the second-order scheme) is quite large. However, recall that we do not scale the L 1 error by the measure of the domain, which in this case would be | Ω | = (2 π ) 3 ; scaling by the measure of the domain would provide a better comparison against the L ∞ error which is not as large.

# Example 3 (Rigid body rotation with diffusion, about ˆ z )

$$
Ut = (71
$$

where the flow field describes rotation about the vector ˆ z . To test the accuracy of the scheme, we use the manufactured solution u ( x,y,z,t ) = exp( − ( x 2 +2 y 2 +3 z 2 +3 dt )) with d = 1 / 3, for which the source term c ( x,y,z,t ) offsets the rotation and is

$$
+322+3dt) = d(-9+ 422 + 16y2 + 3622) ) . (72) e-(r2+2y? 2xy
$$

As seen in Figure 5 , the expected accuracies are observed for the RAIL scheme when using IMEX111, IMEX222 and IMEX443. We used a mesh size N = 80, tolerance ε = 10 − 8 , final time T f = 0 . 3, and λ ranging from 0.5 to 2. When a low-rank source term is involved, we must express it in a Tucker tensor format. By inspection, it is straightforward for one to write down a Tucker decomposition of ( 72 ). To test the rank of the solution, we set d = 1 / 12, c ( x,y,z,t ) = 0, double the speed of the rotation,

$$
Ut 2yuz + (73) 12 2xUy (Uzz
$$

exp(-(r2+9y? +22)). The solution rotates counterclockwise about the positive z-axis multilinear rank should be

