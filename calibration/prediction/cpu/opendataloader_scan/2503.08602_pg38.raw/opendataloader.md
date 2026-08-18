We start by defining so-called ‘off-shell’ Bethe vectors: fix some 0 ≤ k ≤ n and let 1 ,...,x k be pairwise commuting indeterminates. Then we set

$$
(8.31) (~xk)v; t1o (
$$

where v o is the highest weight vector (8.29). (For k = 0 we shall simply take v o instead.) The following is a restatement of [GK17, Prop 4.3] which gives the expansion of the off-shell Bethe vectors in the spin basis v λ = v i n ⊗ ··· ⊗ v i 1 where I = i 1 ...i n is the unique 01-word corresponding to λ :

Proposition 8.12. We have the expansion

$$
11
$$

is the with Jx € {1, n} being the positions of 0-letters in the 01-word corresponding to X.

Using the commutation relations from Lemma 8.2 one now shows by a standard computation in the literature on quantum integrable systems (see e.g. [Fad90]) that the Bethe vectors are eigenvectors of the images of the elements t ( z ) in the evaluation module V w provided the indeterminates x i satisfy the so-called Bethe ansatz equations,

$$
(8.33) II( i = 1, k j=1 j#i
$$

The solutions of these equations are called ‘Bethe roots’ and the Bethe vectors evaluated on the Bethe roots are called ‘on-shell’. (Physically, the Bethe roots are the momenta of quasi-particles in the associated quantum spin chain.) The statement which in is general difficult to prove is that all eigenvectors are obtained this way and that they from an eigenbasis in each subspace V k,n = span { v λ : λ ⊂ ( n − k ) k } ⊂ V w . Expanding the Bethe roots as power series in q both statements have been proven in [GK17, Lemma 4.6 and Theorem 4.8]. In particular, each solution x λ = ( x λ 1 ,...,x λ k ) with λ ⊂ ( n − k ) k is uniquely identified by its formal limit q → 0 where it coincides with ε λ .

Theorem 8.1. The ‘on-shell’ Bethe vectors { b λ = b ( x λ 1 ,...,x λ k ) : λ ⊂ ( n − provide an eigenbasis in each subspace V k,n and we have the eigenvalue equations

$$
(8.34) t(z)bx k bx
$$

N.B. the eigenvalues are polynomial in z because of the Bethe ansatz equations. In fact, one verifies that the condition that the residues at z = − x i vanish for i = 1 ,...,k is equivalent to the Bethe ansatz equations (8.33). The polynomial form of the eigenvalues can be made explicit using the so-called level-rank duality which we discuss next.

