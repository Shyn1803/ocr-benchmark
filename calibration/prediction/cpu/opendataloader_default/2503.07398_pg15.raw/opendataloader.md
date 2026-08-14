CATEGORICAL APPROACH TO RIGIDITY OF ROE-LIKE ALGEBRAS OF COARSE SPACES 15

Proof. The result follows from the observation that rk( C

0⊕C1

A ) = rk( C

A ⊕ C

A ) ≥ rk( C

A ), for any measurable subset A of X.

0

1

0

Observe that Aκ(X) does not necessarily contains a faithful X-module. For instance, if X has ℵ1 coarsely connected components, no coarse X-module of rank ℵ0 can be faithful. However, it is possible to fully characterise the cardinals for which the approximable category contains a faithful module.

- Lemma 2.10. Let X be a LFCM space with an inﬁnite discrete partition. For any two discrete

partitions {Ai}i∈I and {Bj}j∈J, the cardinalities of I and J are equal. Moreover, for an inﬁnite cardinal κ, the following statements are equivalent:

- (1) κ is greater than or equal to the cardinality of a discrete partition of X;
- (2) Aκ(X) contains a faithful X-module;
- (3) Aκ(X) contains an ample X-module.


Proof. Since {Ai}i∈I is a discrete partition of X, for each j ∈ J, there exist only ﬁnitely many i ∈ I such that Bj ∩ Ai = ∅. Consequently, |J| ≤ |I| × ℵ0. Similarly, one has |I| ≤ |J| × ℵ0. Note that if X admits an inﬁnite discrete partition, then any discrete partition of X must also be inﬁnite. It follows that

|I| = |I| × ℵ0 = |J| × ℵ0 = |J|. For the second part of the statement, note that every ample X-module is necessarily faithful. Conversely, given a faithful X-module C, let H be a separable, inﬁnite-dimensional Hilbert space. Deﬁne the X-module C ⊗ H, where the underlying Hilbert space is HC ⊗ H and the representation •C⊗H is given by AC⊗H = CA ⊗ idH for all subsets A. It is straightforward to verify that C ⊗ H is an ample X-module with the same rank as C.

It remains to establish the equivalence of (1) and (2). If κ exceeds the cardinality of the discrete partition, then the module constructed in Example 2.1 is a faithful X-module of rank |I|. Conversely, suppose C is a faithful X-module of rank κ. Deﬁne IC = {i ∈ I | Ai ∩ dom1(C) = ∅} ⊆ I. By discretising X and dom1(C), there exists a gauge E ∈ EI such that

I = E[IC] =

i∈IC

E[{i}].

It follows that the cardinality of I is given by |IC| × supi∈I

C

|E[{i}]|. Since |E[{i}]| is ﬁnite for all i ∈ I, we deduce |I| = |IC|.

We shall focus on the case of countably generated LFCM spaces. Accordingly, we aim to determine the cardinals κ for which the approximable category Aκ(X) contains a faithful X-module. The following lemma addresses this question in the connected case.

- Lemma 2.11. If X is a countably generated LFCM space with a countable number of connected


(X) contains a faithful X-module.

components, then Aℵ

0

Proof. Let {Ai}i∈I be a discrete partition of X. By considering the discretisation I = (I,EI,P(I)) of X, as in Proposition 1.9, we obtain a locally ﬁnite, countably generated coarse space. We may select a generating set {En}n∈N for I satisfying the following conditions:

- (1) For every n ∈ N, the inclusion En ⊂ En+1 holds;
- (2) For every n ∈ N, the entourage En is a gauge;
- (3) For every entourage F ∈ EI, there exists n ∈ N such that F ⊂ En.


Since I has a countable amount of connected components, there exists a sequence {ik}k∈N ⊂ I such that for every j ∈ J there are n,k ∈ N such that (ik,j) ∈ En. As I is locally ﬁnite, the sets En[ik] are ﬁnite for all n,k ∈ N. Hence,

I =

En[ik]

k∈N n∈N

is at most countable. Consequently, X admits a countable discrete partition. By Lemma 2.10, the approximable category Aℵ

(X) contains a faithful X-module.

0

In the case where X has an uncountable number of connected components, the theorem above does not hold. For instance, consider an uncountable disjoint union of copies of N, equipped with an extended metric

d(n,m) =

|n − m|, if n,m belong to the same copy of N; ∞, otherwise.

