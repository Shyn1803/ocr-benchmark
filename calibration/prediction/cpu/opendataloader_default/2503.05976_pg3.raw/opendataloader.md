HERMITIAN RANK IN IDEAL POWERS 3

We note that the above is the most general statement of this result possible in the sense that no hypothesis can be dropped, and the bound is sharp. Firstly, the bound is sharp as equality occurs if Q is a nonzero constant, and it trivially fails if Q ≡ 0.

Less trivially, the conclusion fails if P has no zero set: For d > 0, P = 1 + ∥z∥2, and

Q = P1d, we get that P has no zero set, and rank of Pd is n+dd > 1, but rank of QPd is 1. More generally, the conclusion fails simply if Q is not defined in a neighborhood

of any point on the zero set of P: For d > 0, P = 1 − ∥z∥2, and Q = P1d, the rank of Pd is

n+d d > 1, but rank of QPd is 1. The conclusion may also fail if the bidegree of P is bigger than (1,1): For d = 1,

√

√

2|z1|2|z2|2 + |z2|4, and Q = |z1|4 +

n = 2, P = |z1|4 −

2|z1|2|z2|2 + |z2|4, we get that P is of bidegree (2,2) and rank of Pd is 3, but rank of QPd = |z1|8 + |z2|8 is 2. The proof of [4, Proposition 4.1] generalizes this to a family of examples with d a power of 2.

The key idea in the proof is to reduce to the case when P is of the form

(7) w + w¯ + ∥z∥2 + bidegree-(1,1) terms involving w or w¯

where we split the variables to z ∈ Cn−1 and w ∈ C. The combinatorics of the bound on the rank in the case considered in [5] turns out to be somewhat straightforward once the problem is viewed in the correct context; one bounds the rank of the matrix by considering the number of nonzero entries on an extremal superdiagonal (or subdiagonal), and the count reduces to what could be termed a “monomial version” of the problem. In the presence of the linear terms w + w¯ , we can no longer reduce to a single superdiagonal (a monomial version), and the combinatorics required for the degree bound are significantly more difficult. If Q were a polynomial, then one could work in projective space and get rid of the linear terms by an automorphism of Pn. However, if Q is a real-analytic function, then such a change of coordinates is unavailable. The idea of the proof is that both the matrix of coefficients of Pd and a certain submatrix of the matrix of coefficients of QPd in the reduced case have enough zero entries to allow row reduction preserving certain nonzero entries. These nonzero entries raise diagonal submatrices of full rank in the row echelon form.

2. Preliminaries

This section establishes the fundamental definitions and notations for the (hermitian) rank of real-analytic functions. These concepts form the basis of our result. In this section, we write z = (z1,...,zn) and ζ = (ζ1,...,ζn) for the coordinates in Cn, where ζ is used for polarization.

Notation 1. For any positive integer k, denote by [k] the set {1,...,k} of integers from 1 to k. For convenience, we will let [0] denote the empty set, and [∞] denote the natural numbers N. We will use this notation extensively to index terms in sums.

Definition 2.1. Let U ⊂ Cn be a domain, and R: U → C a real-analytic function. We define the rank of R at p ∈ U to be the smallest r ∈ {0}∪N∪{∞} such that there exists

