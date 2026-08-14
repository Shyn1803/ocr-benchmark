Subscripts t and xx represent the ﬁrst time derivative and second position derivative of the function f. The factor α in the equation is called the diﬀusivity which is deﬁned by the system under investigation. The Schrödinger equation (in dimensionless units) using the same notation as in equation (29) becomes

- 1

![](<a2b1ca3482f994a59aa8308dec03cd8156fef7fe6aa811ef9a2339068d51dc35_images/imageFile1.png>)

- 2


iΨt = −

Ψxx. (30)

Except for the imaginary number i, the equation (30) is identical to (29). Therefore, it is mathematically correct to proceed to solve (30) with the complex extension of the same tools used in the numerical method for the Diﬀusion Equation. Numerical methods13 solve the PDE by transforming the integral problem into an algebraic one that is computationally accessible. The Crank-Nicholson method is the preferred numerical algorithm used to solve the Schrödinger equation as a diﬀusion type equation. It is an implicit algorithm valid through second order in both space and time coordinates, so it is very stable13.

To make that equation equivalent to the escape problem, it is necessary to employ the mathematical concepts of TBCs. The discretized domain of the solution is constructed using the following ﬁnite diﬀerence grids

<table>
  <tr>
    <th>xi = (i − 1) △x</th>
    <th>(31)</th>
  </tr>
  <tr>
    <td>tn = n△t (△tconstant)</td>
    <td>(32)</td>
  </tr>
</table>


with i = 0, 1, 2, . . ., imax and n = 1, 2, . . ., nmax . The domain D (x, t) is from 0 to L on the x − axis and the solution is marching in a positive time direction on the y − axis. We introduce the following notation in the context of the ﬁnite diﬀerence method grid point (i, t) → (xi, tn) , function f (xi, tn) → fin, ﬁrst time derivative ∂f

n i

∂t → ft|ni , and second space derivative ∂

![](<a2b1ca3482f994a59aa8308dec03cd8156fef7fe6aa811ef9a2339068d51dc35_images/imageFile2.png>)

2fin

∂t2 → fxx|ni . The 2nd Order Central Space approximation of the second derivative is:

![](<a2b1ca3482f994a59aa8308dec03cd8156fef7fe6aa811ef9a2339068d51dc35_images/imageFile3.png>)

fin+1 − 2fin + fin−1 △x2

fxx|ni =

![](<a2b1ca3482f994a59aa8308dec03cd8156fef7fe6aa811ef9a2339068d51dc35_images/imageFile4.png>)

(33)

To obtain second order precision in the time, a key point of the method is to estimate derivatives at half integral time steps. The 2nd Order Central Time approximation of the

9

