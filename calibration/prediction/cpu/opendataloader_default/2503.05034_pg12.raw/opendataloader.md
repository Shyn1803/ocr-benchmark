A PREPRINT - MARCH 10, 2025

Let (dn,k)n,k∈N

be an infinite lower-triangular matrix over R. If there exists a pair (d(t),h(t)) such that the (n,k)-th element of the matrix is defined as:

0

dn,k = [tn]d(t)h(t)k,

where [tn] is an operator that takes the coefficient of the term tn, then, such a matrix is called a Riordan array and we denote it as R(d(t),h(t)). If R(d(t),h(t)) and R(g(t),f(t)) are Riordan arrays, the multiplication ∗ is defined as:

R(d(t),h(t)) ∗ R(g(t),f(t)) := R(d(t)g(h(t)),f(h(t))

which is another Riordan array. Hence, the identity matrix in Riordan array form is R(1,t) while the inverse matrix of R(d(t),h(t)) is given as:

1 d(h¯(t))

,h¯(t)

R(d(t),h(t))−1 := R

where h¯(t) is the compositional inverse of h(t), that is h(h¯(t)) = h¯(h(t)) = t. Therefore, the set of Riordan arrays forms a group called the Riordan group under multiplication.

While Riordan arrays have various useful properties, we primarily utilize the following result called the fundamental theorem of Riordan arrays (FTRA):

Theorem 1 (Shapiro et al., 1991): Every combinatorial sum representable as a linear combination of the elements in the n-th row dn,k,k = 0,... of Riordan array R(d(t),h(t)) can be written down as follows:

∞

n

dn,kck = [tn]d(t)c(h(t))

dn,kck =

k=0

k=0

where c(t) = ∞i=0 citi.

The type of Riordan array used primarily in this paper is called the Exponential Riordan array, which is a generalization of the Riordan array. It is again defined using a pair of power series (d(t),h(t)), but this time exponential power series:

∞

d(t) =

i=0

∞

h(t) =

i=1

ti i!

, d0 ̸= 0, di ∈ R,

di

ti i!

, h1 ̸= 0, hi ∈ R.

hi

From here on, we denote the exponential Riordan array defined with respect to exponential power series d(t) and h(t) as Re[d(t),h(t)]. The (n,k)-th element of Re[d(t),h(t)] is defined as

h(t)k k!

tn n!

. Note that the extraction of the coefficient for the term t

d(t)

dn,k =

n

n! on an exponential power series has a nice interpretation as an operation of taking the n-th derivative of the series with respect to t followed by setting t = 0. For example, d2 = t

2! d(t) = dtd 2d(t) t=0.

2

i

The FTRA with respect to Re[d(t),h(t)] and an exponential series c(t) = ∞i=0 ci t

i! is defined as ∞

n

tn n!

d(t)c(h(t)) (3.4)

dn,kck =

dn,kck =

k=0

k=0

# 3.3 The Riordan group and the Sheffer group

The expansion of the polynomial fλ(θ;α) via the Sheffer A-type zero sequence (Sheffer, 1939) introduced in Section 3.1 is encompassed in the modern theory of umbral interpolation (Costabile et al., 2025) initiated by the work Roman and Rota (1978) and the book of Roman (1984) as the main reference for further developments. Consider a sequence of polynomials {si(θ)}∞i=0 (where si(θ) is of degree i) for a pair of characteristic exponential power series (d(t),h(t)) (overlap in notation with the previous section is intentional) with real-valued coefficients provided that d0 ̸= 0, h0 = 0

12

