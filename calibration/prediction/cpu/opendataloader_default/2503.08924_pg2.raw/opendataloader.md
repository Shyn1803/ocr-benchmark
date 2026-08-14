quadric. In Section 2, the definition of the cutcurve with its characterization is introduced. In Section 2.1, we study the relationship between the resultant, the first subresultant and the cutcurve. In Section 3, we explore the relationship between the singularities of the cutcurve and those of the intersection curve. In Section 4 we present the expression of the cutcurve in terms of the coefficients of the implicit equation of the quadric, its relation with the silhouette curves of the torus and the quadric, and a characterization of the cutcurve singularities. Section 5 is dedicated to presenting examples which illustrate the results presented in the paper.

Through the paper, we will assume that the quadric is irreducible, i.e. neither the square of a plane nor the union of two planes.

# 1 Resultants and subresultants

Resultants and subresultants are the algebraic tools used to determine both the projection of the intersection curve between the considered surfaces and its lifting from the plane to the 3D space, because they provide a very easy and compact way of characterizing the greatest common divisor of two polynomials when they involve parameters.

The concept of polynomial determinant associated to a matrix provides one of the usual ways to define Subresultant polynomials. Let ∆ be a m × n matrix with m ≤ n. The determinant polynomial of ∆, detpol(∆), is defined as:

n−m

det(∆k)xn−m−k

detpol(∆) =

k=0

where ∆k is the square submatrix of ∆ consisting of the first m−1 columns and the (k +m)–th column. Definition 1.1. Let

m

n

aixi and B(x) =

bixi

A(x) =

i=0

i=0

be two polynomials with coefficients in a field (Q or R in our case). The i–th Subresultant polynomial of A and B, denoted by Sresi(A,B), is defined as the determinant polynomial of the following submatrix of Sylvester matrix of A and B:

n+m−i





 

am ... a0 ...

... am ... a0

n − i



 

bn ... b0 ...

 

 

... bn ... b0

m − i



and we define the i–th subresultant coefficient of A and B with respect to x, sresi(A,B;x), as the coefficient of xi in Sresi(A,B;x). Moreover, sresi,j denotes the coefficient of xj in the polynomial Sresi(A,B;x) for j < i. Observe that the resultant of A and B with respect to x is Sres0(A,B;x) = sres0(A,B;x).

There are many ways of defining and computing subresultants: for a short introduction, see [15] and the references cited therein. Subresultants allow an easy characterization of the degree of the greatest common divisor of two univariate polynomials whose coefficients depend on one or several parameters. More generally, the determinants sresi(A,B;x), which are the formal leading coefficients of the subresultant sequence for A and B, can be used to compute the greatest common divisor of A and B, owing to the following equivalence:

Sresi(A,B;x) = gcd(A,B) ⇐⇒

sres0(A,B;x) = ... = sresi−1(A,B;x) = 0 sresi(A,B;x) ̸= 0

(1)

Suppose now that the torus and the quadric are defined respectively as follows, T = {(x,y,z) ∈ R3 : T(x,y,z) = 0} and Q = {(x,y,z) ∈ R3 : Q(x,y,z) = 0},

2

