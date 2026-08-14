where n is the outward normal to ∂D. Denote PL as the orthogonal projection of L2(D)2 onto H. The space of vector ﬁelds whose gradients are integrable in L2(D)2 is also relevant and we deﬁne

V := {u ∈ H1(D)2 : ∇ · u = 0, u|∂D = 0}. We denote the norms associated to H and V respectively as | · | and · .

The Stokes operator is deﬁned as Au = −PL∆u, for any vector ﬁeld u ∈ V ∩ H2(D)2. Since A is self-adjoint with a compact inverse, we infer that A admits an increasing sequence of eigenvalues λk ∼ k diverging to inﬁnity with the corresponding eigenvectors ek forming a complete orthonormal basis for H. We denote by PN and QN the projection onto HN = span {ek : k = 1,... ,N} and its orthogonal complement, respectively. Recall the generalized Poincare´ inequalities

PNu 2 ≤ λN|PNu|2, |QNu|2 ≤ λ−N1 QNu 2 (3.6) hold for all suﬃciently smooth u and any N ≥ 1.

We make the following Hypotheses:

- H1. The function σ = (σ1,... ,σm) is bounded and Lipschitz, i.e., there exist constants B0,L > such that

|σ(u)|2 =

m

k=1

|σk(u)|2 ≤ B0, for all u ∈ H;

|σ(u) − σ(v)|2 =

m

k=1

|σk(u) − σk(v)|2 ≤ L|u − v|2, for all u,v ∈ H.

- H2. There exists N ∈ N such that PNH ⊂ Range (σ(u)), for all u ∈ H.

Moreover, the corresponding pseudo-inverse operators σk−1 : PNH → H are uniformly bounded, i.e., there exists a constant C0 such that

|σ(u)−1(PNw)| ≤ C0|PNw|, for all u,w ∈ H.

- H3. Finally, we assume that N is suﬃciently large such that


L ν

+

λN >

![](<2503.09285_pg9_images/imageFile1.png>)

CD2 ν3

B0. (3.7)

![](<2503.09285_pg9_images/imageFile2.png>)

The existence of a unique strong solution to equation (3.5) is standard, see e.g. [28]. Furthermore, as the energy estimates and Feller property can be obtained directly, we prove these two parts ﬁrst.

Energy estimates Proposition 3.3. Assume H1. Then

E|u|2 ≤ e−2νt|x|2 +

B0 2ν

. (3.8)

![](<2503.09285_pg9_images/imageFile3.png>)

9

