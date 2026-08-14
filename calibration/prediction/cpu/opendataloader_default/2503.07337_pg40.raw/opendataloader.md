Proposition A.2. Let q > n, let Ω ⊂ Rn be an open bounded connected set, and let u ∈ W3,q(Ω) be a function such that for some positive constant k

|∇u|(x) ≥ k, ∀x ∈ u−1(0).

Assume in addition that d(u−1(0),∂Ω) > 0. Let uj ∈ C2,α(Ω) be a sequence of functions such that

−−−−−→2,q(Ω) u.

uj W

Then for every j large enough u−j 1(0) is a C1,s hypersurface, with s = 1−n/q, and there exist deformations Φj ∈ W2,q(Ω;Rn) such that

- (i) Φj are orthogonal to u−1(0);
- (ii) u−j 1(0) = (Id +Φj)(u−1(0));
- (iii) lim


Φj 2,q = 0

j

Proof. • Step 1: we ﬁrst notice that for every ε > 0 there exists t0 such that if |t| ≤ t0 then u−1(t) ⊆ (u−1(0))ε,

where we use the notation (K)t = { p ∈ Rn | d(p,K) ≤ t }, for the outer parallel set. Indeed, let us assume by contradiction that there exist ε0 > 0 and points yk ∈ u−1(tk) with limk tk = 0 such that

∀k ∈ N, d(yk,u−1(0)) > ε0.

![](<2503.07337_pg40_images/imageFile1.png>)

As Ω is bounded, up to a subsequence, we may assume that yk converge to some point y¯ ∈ Ω. The continuity of u gives u(¯y) = 0, so that y¯ ∈ u−1(0). On the other hand,

d(¯y,u−1(0)) ≥ ε0, which is a contradiction.

• Step 2: We now want to extend the non-degeneracy property of the gradient of u to the functions uj on their level sets u−j 1(0). We notice that by uniform convergence and by the previous step, for every ε > 0 there exist t0 > 0 and j0 such that

∀j ≥ j0, u−j 1(0) ⊂ u−1((−t0,t0)) ⊂ (u−1(0))ε. (A.2) On the other hand, ∇u is uniformly continuous in Ω so there exists α0 > 0 such that

k 4

∀(x,z) ∈ Ω s.t. |z − x| ≤ α0, |∇u(z) − ∇u(x)| ≤

.

![](<2503.07337_pg40_images/imageFile2.png>)

In particular,

k 2

∀x ∈ (u−1(0))α0, |∇u(x)| ≥

. Also, ∇uj uniformly converge to ∇u, so for j large enough

![](<2503.07337_pg40_images/imageFile3.png>)

k 8

|∇uj(x) − ∇u(x)| ≤

![](<2503.07337_pg40_images/imageFile4.png>)

∀x ∈ Ω.

From the previous estimates, we get |∇uj|(x) > 0 for every x ∈ u−j 1(0) and j large enough, which implies that the sets u−j 1(0) are C1,s hypersurfaces.

40

