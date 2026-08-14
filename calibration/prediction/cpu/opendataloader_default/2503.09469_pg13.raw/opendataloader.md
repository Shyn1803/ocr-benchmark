therefore, λ1(B−ω0C′) = ⟨V 1(B), (B − ω0C′) (V 1(B))⟩ = 2µ1−ω0ξ since C′ ∈ C. So the strict inequality is asserting that 2µ1 − ω0ξ < λ1(B − ω0C⋆). However, the arguments in Lemmas 4 and 5, that apply to C⋆ (since C⋆ ∈ C), show that λ1(B − ωC⋆) is a concave function of ω and that the linear function 2µ1 − ωξ is an upper bound for it. This violates the strict inequality in: λ1(B − ω0C′) = 2µ1 − ω0ξ < λ1(B − ω0C⋆) ≤ 2µ1 − ω0ξ.

Let S denote the two dimensional subspace spanned by V 1(B) and V and C′S denote the restriction of C′ to this subspace (i.e., C′S agrees with C′ for any vector in this subspace and assigns 0 to any element outside). Also V 1(B − ω0C′) ∈ S by the definition of V and λ1(B − ω0C′S) = λ1(B − ω0C′).

Since C′ ∈ C, its restriction to S satisfies ⟨V 1(B), C′S(V 1(B))⟩ = ξ. Also, C′S ≼ B/2 since C′ ≼ B/2. To satisfy the kissing constraint in Properties 2, we can add a component along V : C′′S := C′S+δV ⊗V ∈ C for some δ ≥ 0. Since C′′S ≽ C′S we have λ1(B−ω0C′′S) ≤ λ1(B−ω0C′S). Proposition 3 establishes C⋆ ↑ C′′S, a relationship that applies to all ω ∈ [0, 2], that guarantees:

λ1(B − ω0C⋆) ≤ λ1(B − ω0C′′S) ≤ λ1(B − ω0C′S). This is in contradiction with the strict inequality λ1(B − ω0C⋆) > λ1(B − ω0C′).

<table>
  <tr>
    <td> </td>
  </tr>
</table>


Proof of Theorem 1. Theorem 2 implies λ1(B⋆ − ωC⋆) = λ1(B − ωC⋆) ≤ λ1(B − ωC) for ω ∈ [0, 2] that establishes C(ω) ≥ λmax(A(ω)) based on (14). The covariance Σk converges to 0 according to the rate given by λmax(A(ω)) and the expected error at each step is the trace of Σk: E ∥εk∥2 = tr Σk. When i is drawn independently and identically distributed at each step of (1), the geometric rate of convergence is bound by C(ω) for every ω ∈ [0, 2].

<table>
  <tr>
    <td> </td>
  </tr>
</table>


# 4.4 Perron-Frobenius Theory For Positive Linear Maps

The superoperator A defined in (7) plays the role of the iteration matrix — whose spectrum provides convergence analysis in classical iterative methods [Saad, 2003] — for randomized iterations. In this section we discuss the theoretical foundations that provide necessary properties on the spectrum of A in the covariance analysis we have seen.

Recall the superoperator A, for a fixed ω, denotes a linear map over the space of n × n matrices as:

m

1 m

A(X) =

(I − ωPi)X(I − ωPi).

i=1

Since orthogonal projection is a symmetric operator, for any symmetric positive semi-definite matrix X the operation (I − ωPi)X(I − ωPi) preserves its positivity [Bhatia, 2009]. Hence the superoperator A is a positive linear map, leaving the cone of symmetric positive semi-definite matrices invariant.

The spectra of positive linear maps on general (noncommutative) matrix algebras was studied in [Evans and Høegh-Krohn, 1978] that generalized the Perron-Frobenius theorem to this context. The spectral radius of a positive linear map is attained by an eigenvalue for which there exists an eigenvector that is positive semi-definite (see Theorem 6.5 in [Wolf, 2012]). The notion of irreducibility for positive linear maps guarantees that the eigenvalue is simple and the corresponding eigenvector is well-defined (up to a sign). What is more is that the eigenvector can be chosen to be a positive definite matrix. This guarantees that the power iterations in (7) converge along this positive definite matrix with the corresponding simple eigenvalue giving the rate of convergence.

For a system of equations in Ax = b, we examine the irreducibility of its corresponding superoperator A for any given relaxation value ω. The criteria for irreducibility of positive linear maps was developed in [Farenick, 1996] and involve invariant subspaces. A collection S of (closed) subspaces of the vector space of n × n matrices is called trivial if it only contains {0} and the space itself. Given a bounded linear operator M, let Lat(M) denote the invariant subspace lattice of M. The following theorem is a specialization of a more general result in [Farenick, 1996] (see Theorem 2) to our superoperator.

Theorem 3 (Irreducibility of the superoperator A). The positive linear map A is irreducible if and only if, mi=1 Lat(I − ωPi) is trivial.

Based on this theorem, we establish the equivalence of the irreducibility of A, in the sense of positive linear maps, to a geometric notion of irreducibility defined for alternating projections (2) that is inherently a geometric approach to solving a system of equations Ax = b. We recall the Frobenius notion of irreducibility for symmetric matrices. Such a matrix M is called irreducible if it can not be transformed to block diagonal form by a permutation matrix Π:

M = Π

M′ 0 0 M′′

Π−1,

13

