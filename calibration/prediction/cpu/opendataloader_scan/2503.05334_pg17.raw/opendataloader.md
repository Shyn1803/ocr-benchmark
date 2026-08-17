pendent replications, the median QMC method could achieve an error bound similar to the CBC algorithm. However, by using the median QMC method we do not need to choose the weight parameters and the weight functions as required by the CBC method, thus obviating the estimation of θ j ( n N ) in ( 2.6 ) for certain chosen ψ j .

# 4.3. Example 3: Elliptic PDE with log normal random coefficients. Consider the parametrized ODE

$$
dx
$$

= = 0 Solving this ODE we obtain

$$
dx (4.3) u8 (x,y) = a(x, y)
$$

Here we take

$$
(x,y) = exp sin(2jT2)yj j2 j=l
$$

i.i.d. with Y1, Us

N (0 , 1). We are interested in computing the expectation E y [ F ( y )], where

$$

$$

and x 0 ∈ { 1 3 , 2 3 } . According to [ 10 ], F lies in the unanchored weighted Sobolev space with

$$
(4.4) e-2_ Qj 0 2T
$$

We take s = 30 and compute the MAEs of the estimators obtained by the MC method, the randomly shifted lattice rule with the CBC algorithm, and the median QMC method. To calculate the integrals in ( 4.3 ) for any given y ∈ R s , we use the 4th-order Gauss-Legendre formula with 200 nodes. The exact value of E y [ F ( y )] are estimated by using 2 21 points from the nested scrambled Sobol’ sequence averaged over 10 independent replications. Similar to Example 2, for the median QMC method, we take the median of k = 11 independent QMC estimators, each utilizing N points, while for the MC method and the randomly shifted lattice rule with the CBC method, we use k × N points per method. Furthermore, for the CBC method, we choose the weight parameters and the weight functions as recommended in [ 10 ] . We set λ = 0 . 55 and b j = 1 j 2 for j = 1 ,...,s . For the weight functions ψ 2 j in ( 4.4 ), we take

and

$$
1 Q1 b1 + +1 = 2 2) Vb?
$$

$$
1 Qj 2 < j < s. 2 21
$$

