MEDIAN QMC METHOD IN UNANCHORED WEIGHTED SOBOLEV SPACES 17

pendent replications, the median QMC method could achieve an error bound similar to the CBC algorithm. However, by using the median QMC method we do not need to choose the weight parameters and the weight functions as required by the CBC method, thus obviating the estimation of θj(Nn ) in (2.6) for certain chosen ψj.

4.3. Example 3: Elliptic PDE with log normal random coefficients. Consider the parametrized ODE

dus(x,y) dx

d dx

(as(x,y)

−

) = 1,

with homogeneous Dirichlet boundary conditions, us(0,y) = us(1,y) = 0. Solving this ODE we obtain

- (4.3) us(x,y) =

x

0

c − t a(t,y)

dt, c =

1

0

xdx a(x,y)

1

0

dx a(x,y)

.

Here we take

as(x,y) = exp

 

s

j=1

1 j2

sin(2jπx)yj

 ,

with y1,...,ys i.i.d.∼ N(0,1). We are interested in computing the expectation Ey[F(y)], where

F(y) = G(us(·,y)) = us(x0,y),

and x0 ∈ {31, 23}. According to [10], F lies in the unanchored weighted Sobolev space with

- (4.4) ϕ(x) =


1 √2π

x2

e−

2 , ψj2(x) = e−2α

j|x|, αj > 0.

We take s = 30 and compute the MAEs of the estimators obtained by the MC method, the randomly shifted lattice rule with the CBC algorithm, and the median QMC method. To calculate the integrals in (4.3) for any given y ∈ Rs, we use the 4th-order Gauss-Legendre formula with 200 nodes. The exact value of Ey[F(y)] are estimated by using 221 points from the nested scrambled Sobol’ sequence averaged over 10 independent replications. Similar to Example 2, for the median QMC method, we take the median of k = 11 independent QMC estimators, each utilizing N points, while for the MC method and the randomly shifted lattice rule with the CBC method, we use k × N points per method. Furthermore, for the CBC method, we choose the weight parameters and the weight functions as recommended in [10] . We set λ = 0.55 and bj = j12 for j = 1,...,s. For the weight functions ψj2 in (4.4), we take

- 1

- 2


α1 =

- 1

- 2λ


b1 + b21 + 1 −

,

and

- 1

- 2


αj =

- 1

- 2λ


b2 + b22 + 1 −

, 2 ≤ j ≤ s.

