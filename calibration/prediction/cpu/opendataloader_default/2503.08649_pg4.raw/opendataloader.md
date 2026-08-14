4 CALANCHI AND GROSSI

We observe that the results of Theorems 1.3 and 1.4 are inﬂuenced by β, even though the weights dβ ∈ A2 for all β ∈ (−1, 1). This demonstrates that the regularity of the solution to (1.2) is not solely dependent on the Muckenhoupt class, but rather on the explicit structure of the weight. Lastly, we note that our results extend to more general weights w that behave similarly near the boundary (see Remark 3.1).

The paper is organized as follows: in Section 2 we provide some additional properties of the weight dβ and recall other known results; in Section 3 we give the proof of the main estimates of Theorem 1.2, and in Section 4 we prove Theorems 1.3 and 1.4.

2. Notations and preliminary known results

In the introduction we have introduced the so called Muckenhoupt class A2, namely the class of locally integrable, nonnegative, real-valued functions w that satisfy

- (2.1) sup

B⊂Ω

1 |B| B

![](<2503.08649_pg4_images/imageFile1.png>)

w dx

1 |B| B

![](<2503.08649_pg4_images/imageFile2.png>)

w−1dx < +∞

where the supremum is taken over balls B ⊂ Ω. In [3] it was proved that that, if d is the distance function, the weight

- (2.2) w(x) := dβ(x),

belongs to A2 for β ∈ (−1, 1) (see Theorem 3.1 in [3]). Before presenting the main result, we would like to highlight some key properties of d. We denote by

- (2.3) Γσ = {x ∈ Ω : d(x) < σ} the portion in Ω of a tubular neighbourhood of ∂Ω. With an abuse of terminology, from now on we will call Γσ a neighbourhood of ∂Ω.

![](<2503.08649_pg4_images/imageFile3.png>)

![](<2503.08649_pg4_images/imageFile4.png>)

Proposition 2.1. Let Ω ⊂ RN a bounded domain with ∂Ω ∈ C2. Then there exists a small constant σ > 0 such that

- (2.4) d ∈ C2(Γ◦σ) ∩ C0(Γσ),

![](<2503.08649_pg4_images/imageFile5.png>)

- (2.5) |∇d(x)| = 1 for all x ∈ Γσ, Moreover, for every measurable nonnegative function g : (0, σ) → R
- (2.6) g ◦ d ∈ L1(Γσ) ⇐⇒ g ∈ L1(0, σ).


Proof. For (2.4) and (2.5) see e.g. [6] Appendix 14.6.

Here’s a brief outline of how to prove (2.6): from the coarea formula and (2.4) and (2.5), we have, since |∇d(x)| = 1

σ

g(t)HN−1(Γσ ∩ {d = t}) dt,

g(d(x)) dx =

0

Γσ

where HN−1 is the Hausdorﬀ measure of Γσ ∩ {d = t}. Since the ∂Ω is C2, there exist two positive constants c1 and c2 such that

c1HN−1(∂Ω) ≤ HN−1(Γσ ∩ {d = t}) ≤ c1HN−1(∂Ω) (see e.g. [9] , Appendix 2.12.3). This ends the proof.

