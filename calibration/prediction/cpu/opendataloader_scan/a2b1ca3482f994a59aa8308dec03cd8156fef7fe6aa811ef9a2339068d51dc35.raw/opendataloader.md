function f . The factor α in the equation is called the diﬀusivity which is deﬁned by the system under investigation. The Schrödinger equation (in dimensionless units) using the same notation as in equation (29) becomes

$$
(30) 2
$$

Except for the imaginary number i , the equation (30) is identical to (29). Therefore, it is mathematically correct to proceed to solve (30) with the complex extension of the same tools used in the numerical method for the Diﬀusion Equation. Numerical methods 13 solve the PDE by transforming the integral problem into an algebraic one that is computationally accessible. The Crank-Nicholson method is the preferred numerical algorithm used to solve the Schrödinger equation as a diﬀusion type equation. It is an implicit algorithm valid through second order in both space and time coordinates, so it is very stable 13 .

To make that equation equivalent to the escape problem, it is necessary to employ the mathematical concepts of TBCs . The discretized domain of the solution is constructed using the following ﬁnite diﬀerence grids

$$
Ti (i _ 1) Az (31)
$$

$$
tn = nAt (At constant) (32)
$$

with i = 0 , 1 , 2 , . . ., imax and n = 1 , 2 , . . ., nmax . The domain D ( x, t ) is from 0 to L on the x − axis and the solution is marching in a positive time direction on the y − axis. We introduce the following notation in the context of the ﬁnite diﬀerence method grid point ( i, t ) → ( x i , t n ) , function f ( x i , t n ) → f n i , ﬁrst time derivative ∂f n i ∂t → f t | n i , and second space derivative ∂ 2 f n i ∂t 2 → f xx | n i .

The 2nd Order Central Space approximation of the second derivative is:

$$
2fn + fn-1 (33)
$$

To obtain second order precision in the time, a key point of the method is to estimate derivatives at half integral time steps. The 2nd Order Central Time approximation of the

