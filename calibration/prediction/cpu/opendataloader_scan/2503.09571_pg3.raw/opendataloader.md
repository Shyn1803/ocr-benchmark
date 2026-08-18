# 2 The Mandelstam Region

symmetric n × n matrix S = [ s ij ] of rank r is said to be a Mandelstam matrix if

the diagonal entries are non-negative, s ii ≥ 0 for i = 1 ,...,n ; and

it has precisely one positive eigenvalue and r − 1 negative eigenvalues.

We denote the set of all Mandelstam matrices of rank r by M n,r . This is a semialgebraic set in R ( n +1 2 ) , the space of all symmetric matrices. The following is the Mandelstam analogue of the familiar characterization of positive semidefinite matrices in terms of principal minors.

Lemma 2.1. A symmetric n × n matrix S is Mandelstam if and only if

$$
(~1)/-1 det(S1) 0
$$

where det( S I ) are the principal minors of S .

Proof. This follows from the general results in [ 6 ]. We refer to Baker’s exposition in [ 3 ]. The key step is Cauchy’s interlacing theorem [ 12 ]. This states that the eigenvalues of S I interlace the eigenvalues of S J whenever I ⊂ J . Hence, if S I has at most one positive eigenvalue then so does S J . But S J cannot have all negative eigenvalues because its trace is non-negative.

The name of our matrices refers to the physicist Stanley Mandelstam (1928–2016) who is credited for introducing the variables s ij in the context of scattering amplitudes. In [ 14 ] the role of M n,r as a kinematic space is recognized. A term more familiar to mathematicians might be “Lorentzian matrices.” These encode Lorentzian quadratic forms [ 5 , 6 ]. We here use the term Lorentzian matrix for a Mandelstam matrix whose entries s ij are all non-negative.

Mandelstam matrices arise as Gram matrices of momentum vectors in R 1+ d with the Lorentzian inner product. A non-zero momentum vector is any vector p ∈ R 1+ d of the form

$$
p (5)
$$

for some scalar λ ̸ = 0, and x = ( x 1 ,...,x d ) in the closed unit ball B d = { x ∈ R d : || x || ≤ Given n momentum vectors, p ( i ) , their Gram matrix S = [ s ij ] has entries s ij = p ( i ) · This is the matrix in ( 1 ). The entries of S may now be written as

$$
Sij (6)
$$

Here · is the Lorentz inner product on R 1+ d and ⟨ , ⟩ is the Euclidean inner product on R d .

Lemma 2.2. A symmetric n × n matrix S is Mandelstam, i.e. S lies in the region M n, ≤ 1+ d , if and only if it is the Gram matrix of n momentum vectors in (1+ d ) -dimensional spacetime.

Proof. Assume that S has no zero rows or columns. For the only-if direction, take a Mandelstam matrix S . By Lemma 2.1 and diagonalization of symmetric matrices, it can be factorized as in ( 1 ). Namely, we write S = MDM T , where D = diag(1 , − 1 , − 1 ,..., − 1). Let the

