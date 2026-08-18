therefore, X1(B-woC') = (V1(B); (B is asserting that 2/1 < X1 (B WoC*) . However, the arguments in Lemmas 4 and 5, that apply to C* (since C* WC*) is a and that the linear  function 2/1 This violates the strict inequality in: X1 (B woC') = 2/1 X1 (B WoC*) < 2/1

Let S denote the two dimensional subspace spanned by V1(B) and V and C's denote the restriction of C' to this subspace (i.e., Cs agrees with C' for any vector in this subspace and assigns 0 to any element outside) . Also V1 (B woC') € S by the definition of V and X1 (B woCs) = X1 (B

Since C To satisfy the Proposition 3 establishes C* 1 Cs, relationship that applies to all w € [0, 2], that guarantees:

$$
X1 (B WoC*) < X1 (B This is in contradiction with the strict inequality X1 (BWoC*) > X1(B = woC' ) .
$$

Proof of Theorem 1. Theorem 2 implies λ 1 ( B ⋆ − ω C ⋆ ) = λ 1 ( B − ω C ⋆ ) ≤ λ 1 ( B − ω C ) for ω ∈ [0 , 2] that establishes C ( ω ) ≥ λ max ( A ( ω )) based on (14). The covariance Σ k converges to 0 according to the rate given by λ max ( A ( ω )) and the expected error at each step is the trace of Σ k : E   ∥ ε k ∥ 2   = tr Σ k . When i is drawn independently and identically distributed at each step of (1), the geometric rate of convergence is bound by C ( ω ) for every ω ∈ [0 , 2].

# 4.4 Perron-Frobenius Theory For Positive Linear Maps

The superoperator A defined in (7) plays the role of the iteration matrix whose spectrum provides convergence analysis in classical iterative methods [Saad, 2003] for randomized iterations. In this section we discuss the theoretical foundations that provide necessary properties on the spectrum of A in the covariance analysis we have seen.

Recall the superoperator A , for a fixed ω , denotes a linear map over the space of n × n matrices as:

$$
A(X) = (I =wPi)X(I wPi) i=1
$$

Since orthogonal projection is a symmetric operator, for any symmetric positive semi-definite matrix X the operation ( I − ω P i ) X ( I − ω P i ) preserves its positivity [Bhatia, 2009]. Hence the superoperator A is a positive linear map , leaving the cone of symmetric positive semi-definite matrices invariant.

The spectra of positive linear maps on general (noncommutative) matrix algebras was studied in [Evans and Høegh-Krohn, 1978] that generalized the Perron-Frobenius theorem to this context. The spectral radius of a positive linear map is attained by an eigenvalue for which there exists an eigenvector that is positive semi-definite (see Theorem 6.5 in [Wolf, 2012]). The notion of irreducibility for positive linear maps guarantees that the eigenvalue is simple and the corresponding eigenvector is well-defined (up to a sign). What is more is that the eigenvector can be chosen to be a positive definite matrix. This guarantees that the power iterations in (7) converge along this positive definite matrix with the corresponding simple eigenvalue giving the rate of convergence. For a system of equations in A x = b , we examine the irreducibility of its corresponding superoperator

A for any given relaxation value ω . The criteria for irreducibility of positive linear maps was developed in [Farenick, 1996] and involve invariant subspaces. A collection S of (closed) subspaces of the vector space of n × n matrices is called trivial if it only contains { 0 } and the space itself. Given a bounded linear operator M , let Lat( M ) denote the invariant subspace lattice of M . The following theorem is a specialization of a more general result in [Farenick, 1996] (see Theorem 2) to our superoperator.

Theorem 3 (Irreducibility of the superoperator A ) . The positive linear map A is irreducible if and only if,   m i =1 Lat( I − ω P i ) is trivial.

Based on this theorem, we establish the equivalence of the irreducibility of A , in the sense of positive linear maps, to a geometric notion of irreducibility defined for alternating projections (2) that is inherently a geometric approach to solving a system of equations A x = b . We recall the Frobenius notion of irreducibility for symmetric matrices. Such a matrix M is called irreducible if it can not be transformed to block diagonal form by a permutation matrix Π :

$$
M M = II II-1 , 0 M" |
$$

