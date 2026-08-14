38 VASSILY GORBOUNOV, CHRISTIAN KORFF, AND LEONARDO C. MIHALCEA

We start by defining so-called ‘off-shell’ Bethe vectors: fix some 0 ≤ k ≤ n and let x1,...,xk be pairwise commuting indeterminates. Then we set

- (8.31) b(x1,...,xk) = t10(−x1)···t10(−xk)vo,

where vo is the highest weight vector (8.29). (For k = 0 we shall simply take vo instead.) The following is a restatement of [GK17, Prop 4.3] which gives the expansion of the off-shell Bethe vectors in the spin basis vλ = vi

n ⊗ ··· ⊗ vi

1

where I = i1 ...in is the

unique 01-word corresponding to λ: Proposition 8.12. We have the expansion

- (8.32) b(x1,...,xk) = x1 ···xk

λ

ε−λ1Gλ∨(1−x1,...,1−xk|1−ε−w(1n),...,1−ε−w(1)1 )vλ,

where the sum runs over all λ ⊂ (n−k)k, λ∨ denotes the partition whose Young diagram is the complement of the one of λ in the k × (n − k) bounding box and ελ = j∈J

λ

εw(j) with Jλ ⊂ {1,...,n} being the positions of 0-letters in the 01-word corresponding to λ.

Using the commutation relations from Lemma 8.2 one now shows by a standard computation in the literature on quantum integrable systems (see e.g. [Fad90]) that the Bethe vectors are eigenvectors of the images of the elements t(z) in the evaluation module Vw provided the indeterminates xi satisfy the so-called Bethe ansatz equations,

- (8.33)

n

j=1

(1 − xi/εj)

k

j̸=i

(xj/xi) + (−1)kq = 0, i = 1,...,k .

The solutions of these equations are called ‘Bethe roots’ and the Bethe vectors evaluated on the Bethe roots are called ‘on-shell’. (Physically, the Bethe roots are the momenta of quasi-particles in the associated quantum spin chain.) The statement which in is general difficult to prove is that all eigenvectors are obtained this way and that they from an eigenbasis in each subspace Vk,n = span{vλ : λ ⊂ (n − k)k} ⊂ Vw. Expanding the Bethe roots as power series in q both statements have been proven in [GK17, Lemma 4.6 and Theorem 4.8]. In particular, each solution xλ = (xλ1,...,xλk) with λ ⊂ (n − k)k is uniquely identified by its formal limit q → 0 where it coincides with ελ.

Theorem 8.1. The ‘on-shell’ Bethe vectors {bλ = b(xλ1,...,xλk) : λ ⊂ (n − k)k} provide an eigenbasis in each subspace Vk,n and we have the eigenvalue equations

- (8.34) t(z)bλ =


n

- j=1(1 + z/εj)

- k


q

+

k

i=1(1 + z/xλi )

i=1(1 + xλi /z)

bλ .

N.B. the eigenvalues are polynomial in z because of the Bethe ansatz equations. In fact, one verifies that the condition that the residues at z = −xi vanish for i = 1,...,k is equivalent to the Bethe ansatz equations (8.33). The polynomial form of the eigenvalues can be made explicit using the so-called level-rank duality which we discuss next.

