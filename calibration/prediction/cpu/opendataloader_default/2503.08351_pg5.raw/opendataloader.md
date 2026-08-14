The Michael Selection Theorem guarantees the existence of a continuous selection for a lower semicontinuous multimap with convex values. However, this Theorem doesn’t hold for multimap with nonconvex values. In such cases, the author of [27] introduces the concept of decomposable sets to establish the existence of a continuous selection. Let us deﬁne decomposable sets now. Formally, the concept of decomposability resembles that of convexity, and as we will see in this section, decomposable sets behave like convex sets. For this reason, decomposable sets play a central role in many applications.

Deﬁnition 2.6. A set K ⊂ L1(I,X) is said to be decomposable if for every triple (D,f1,f2) ∈ Σ×K ×K we have

χDf1 + χI\Df2 ∈ K. (2.12) We now consider the nonconvex-decomposable version of Michael’s selection theorem.

- Theorem 2.7. [28, Theorem 4.5.32] If Z is a separable metric space, X is a separable Banach space and F : Z ⊸ L1(I,X) is lower semicontinuous and has closed decomposable values, then F admits a continuous selection.

3. Navier Stokes Equations

In this section, we study the existence of local strong solutions for the nonstationary multivalued version of Navier-Stokes equations given by (1.1)-(1.4). Throughout this section, we assume that 3 < p < ∞ and 1 < q < ∞. We assume the following conditions on the multimap F. The multimap F : [0,a] × Hp ⊸ Lp(D)3 satisﬁes the following properties:

- (F1) F : [0,a] × Hp ⊸ Lp(D)3 is product measurable.
- (F2) F(t,·) : Hp ⊸ Lp(D)3 is lower semicontinuous for a.a. t ∈ [0,a].
- (F3) there exists α ∈ Lq(0,a) with α ≥ 0 for a.a. t ∈ (0,a) and a monotonically increasing function ηF : [0,∞) → [0,∞) such that


F(t,u) Lp(D)3 ≤ α(t)(1 + ηF( u H

p

)), (3.1) for a.a. t ∈ (0,a) and all u ∈ Hp.

We are now ready to prove the ﬁrst main result of this paper.

- Theorem 3.1. Let D ⊂ R3 be open, bounded and connected with ∂D ∈ C2,µ, 0 < µ < 1 and a > 0.


Also let u0 ∈ Dpq with 3 < p < ∞, 1 < q < ∞ and F : [0,a] × Hp ⊸ Lp(D)3 satisfying the assumptions (F1)-(F3). Then there exists b > 0 and

u ∈ Lq([0,b],D(Ap)) with ∂tu ∈ Lq([0,b],Hp), (3.2) p ∈ Lq([0,b],W1,p(D)3) (3.3)

such that (u,p) is a solution to the problem (1.1)-(1.4) with f ∈ Lq([0,b],Lp(D)3) with f(t) ∈ F(t,u(t)) for a.a. t ∈ [0,b].

Proof. For b > 0, we introduce the space

U(b) = {u ∈ Lq([0,b],D(Ap)) : ∂tu ∈ Lq([0,b],Hp)}. (3.4) Consider the selection multimap SF : U(b) ⊂ Lq([0,b],Hp) ⊸ Lq([0,b],Lp(D)3) as follows:

SF(u) = {f ∈ Lq([0,b],Lp(D)3) : f(t) ∈ F(t,u(t)), a.a. t ∈ [0,b]}. (3.5)

By virtue of assumption (F1), the multimap F is product measurable. Hence, the multimap t ⊸ F(t,u(t)) is closed valued and measurable for every u ∈ Lq([0,b],Hp). In accordance with the Ryll-Kurtowski

5

