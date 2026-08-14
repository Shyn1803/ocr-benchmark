H2π

- 0

(X)T belonging to the zero (C×)n-weight space are represented by log-canonical bi-vector ﬁelds, we let S(π0) = the set of all the non-zero (C×)n-weights in H2π

0

(X)T, (1.2)

and we focus on Poisson deformations of π0 of the form π = π0 +π1 +π′, where π1 is a sum of T-invariant algebraic bi-vector ﬁelds on X with (C×)n-weights in S(π0) and satisﬁes [π0,π1] = 0, and π′ is a correction term such that π is Poisson. We show in §2.2 (see Lemma 2.8 and Lemma 2.9) that the set S(π0) has the following properties:

- 1) S(π0) is a ﬁnite subset of (Z≥−1)n and each θ ∈ S(π0) has exactly two entries of −1;
- 2) For every θ ∈ S(π0), the θ-weight space of H2π


0

(X)T is 1-dimensional with a basis vector represented by a uniquely deﬁned bi-vector ﬁeld Vθ on X (see (2.19)).

For p ∈ [0,n], let Xp(X) be the space of all algebraic p-vector ﬁelds on X, and let [, ]Sch be the Schouten bracket on X(X) = ⊕np=0Xp(X). For W ⊂ Zn and p ∈ [0,n], let Xp(X)W be the direct sum of the (C×)n-weight spaces in Xp(X) with weights in W. By deﬁnition Xp(X)W = 0 if W = ∅.

For a subset S of S(π0) and m ≥ 1, let S≥m denote the set of all elements in Zn that can be written as the sum of m or more elements in S. We say that S satisﬁes Condition (W1) if

X1(X)S

≥2

= 0. Our main results in the ﬁrst part of the paper are summarized as follows. Theorem A. Let π0 be any T-log-symplectic log-canonical Poisson structure on X = Cn, and let S ⊂ S(π0).

1) (Theorem 2.21) Suppose that S is C-linearly independent. Let c = (cθ)θ∈S be a set of formal commuting parameters, and let π1S(c) = θ∈S cθVθ ∈ X2(X)S[[c]]. Then there exists (π′)S(c) ∈ X2(X)S≥2[[c]] such

πS(c) = π0 + π1S(c) + (π′)S(c) ∈ X2(X)[[c]] (1.3) satisﬁes [πS(c),πS(c)]Sch = 0. Moreover, such a πS(c) is unique up to gauge equivalence (Deﬁnition 2.19);

2) (Theorem 2.26) If S satisﬁes Condition (W1) (it is then C-linearly independent by Lemma 2.23), for any c = (cθ ∈ C×)θ∈S, there is a unique T-invariant algebraic Poisson structure πS(c) on X of the form

πS(c) = π0 + π1S(c) + (π′)S(c) ∈ X2(X), (1.4)

where π1S(c) = θ∈S cθVθ ∈ X2(X)S and (π′)S(c) ∈ X2(X)S≥2. Moreover, for any other c′ = (c′θ ∈ C×)θ∈S, the two Poisson structures πS(c) and πS(c′) coincide after a re-scaling of the coordinates (x1,...,xn).

When S(π0) is itself C-linearly independent as a subset of Cn, the T-invariant formal power series Poisson deformation πS(π

0)(c) of π0 in (1.3) is said to be maximal, and we explain in Theorem 2.22 the precise sense in which it is maximal. Similarly, if S(π0) satisﬁes Condition (W1), the T-invariant algebraic Poisson deformation πS(π

0)(c) of π0 in (1.4), for any c = (cθ ∈ C×)θ∈S(π

0), is said to be maximal, and the precise sense in which it is maximal is explained in Theorem 2.34.

We remark that the miracle that the Poisson deformations along π1S(c) as in Theorem A are unobstructed has been observed in [MPS20] in the context of complex log-symplectic manifolds. While the methods of [MPS20] heavily used the homotopy algebra techniques, such L∞-algebras, our proofs are elementary and our strategies are adopted from [MPS24] where deformations of q-symmetric algebras are studied.

- 1.3 Applications to symmetric Poisson CGL extensions


In the second part of the paper, we apply Part 2) of Theorem A to a special class of examples.

Let again T be any complex algebraic torus with Lie algebra t and character lattice X∗(T) ⊂ t∗. We deﬁne an n-dimensional T-action datum to be a pair ( , ,β), where , is a symmetric C-bilinear form on t∗, and

β = (β1, β2, ..., βn)

is a sequence of n elements in X∗(T) such that βj,βj = 0 for every j ∈ [1,n]. Given such a pair ( , ,β), let π0 be the log-canonical Poisson structure on X = Cn given by1

∂ ∂xk

∂ ∂xj

∧

π0 = −

, (1.5)

βj, βk xjxk

![](<2503.05644_pg3_images/imageFile1.png>)

![](<2503.05644_pg3_images/imageFile2.png>)

1≤j<k≤n

![](<2503.05644_pg3_images/imageFile3.png>)

1While there is no harm to remove the minus sign in the deﬁnition of π0 and adjust the results in the paper accordingly, the minus sign is there to align with the special example of standard Poisson structure on generalized Schubert cells which has appeared in a series of papers [LM17a, LM18, EL21] and has been implemented into a computer program.

3

