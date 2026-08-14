INVASION DYNAMICS OF SUPER INVADERS 21

- 3.3. Global existence. Theorem 3.10. Assuming that (3.2) and (3.3) are satisfied, then the conclusions in Theorem 3.4 hold for any T > 0.

Proof. By Theorem 3.4, we may assume that (3.1) has a unique solution (u,g,h) defined on some maximal time interval (0,Tm) with Tm ∈ (0,∞], and

h,g ∈ C1+

β

2 ((0,Tm)), u ∈ C1+

β

2,2+β(ΩTm),

where ΩTm := {(t,x) : t ∈ (0,Tm),x ∈ [g(t),h(t)]}. To complete the proof, we must demonstrate that Tm = ∞. Suppose Tm < ∞. Then, by the proof of Theorem 3.4, along with Lemmas 3.8 and 3.9, there exist positive constants C1,C2 = C2(Tm), such that for t ∈ [0,Tm) and x ∈ [g(t),h(t)],

0 ≤ u(x,t) ≤ C1, |h′(t)| + |g′(t)| ≤ C2, |h(t)|,|g(t)| ≤ C2t + h0. For any small constant ε > 0, it follows from the proof of Theorem 3.4 and Lemmas 3.8 and 3.9 that u,v ∈ C1+β,1+2β (ΩTm−ε). Thus, as in Step 4 of the proof of Theorem 3.4, applying Schauder’s estimates, for any fixed 0 < T0 < Tm − ε, we obtain ∥u∥

C2+β,1+

β 2 (ΩTm−ε\ΩT0)

≤ Q∗, where Q∗ depends on T0, Tm,

and Ci for i = 1,2, but is independent of ε. Since ε > 0 can be made arbitrarily small, it follows that for any t ∈ [T0,Tm),

∥u(t,·)∥C2+β([g(t),h(t)]) ≤ Q∗.

By repeating the arguments used in the proof of Theorem 3.4, we can conclude that there exists T > 0 small, depending on Q∗ and Ci (i = 1,2), such that the solution to (3.1) with initial time Tm − T2 can be extended uniquely to t = Tm − T2 + T > Tm, a contradiction to the definition that Tm is the maximal time interval for the solution. Thus, we must have Tm = ∞. □

- 3.4. Proof of Theorem 3.1. Let us first note that f(t,x,1) ≡ 0 and f(t,x,u) ≤ f¯(u) < 0 for u > 1 imply f¯(1) = 0. Let M0 = max{∥u0∥∞,1} and v(t) be the solution of


v′ = f¯(v), v(0) = M0.

Since f¯(v) < 0 for v > 1, we clearly have 1 ≤ v(t) ≤ M0 and v(t) → 1 as t → ∞. Since f(t,x,u) ≤ f¯(u) for u ≥ 1, we obtain

vt − dvxx = f¯(v) ≥ f(t,x,v) for t > 0,x ∈ [g(t),h(t)].

We also have v ≥ 1 > δ = u for x ∈ {g(t),h(t)} and v(0) = M0 ≥ u(0,x) for x ∈ [−h0,h0]. Therefore the standard comparison principle over the region {(t,x) : t > 0,x ∈ [g(t),h(t)]} infers u(t,x) ≤ v(t) in this region. It follows that

- (3.31) limsup t→∞

u(t,x) ≤ lim

t→∞

v(t) = 1 uniformly for x ∈ [g(t),h(t)]. To bound u(t,x) from below, we first make use of (3.4) to show that there exists T0 > 0 such that

- (3.32) u(t,x) ≥ δ for t ≥ T0 and x ∈ [g(t),h(t)]. Similar to the proof of Theorem 1.1, since f satisfies (fA), we are able to choose a function fˆ ∈ C1 sufficiently close to f in L∞ such that fˆ(s) ≤ f(s) for s ≥ 0, and fˆ satisfies (Fb) with (P,Q) = (θ,δˆ ) for some θˆ ∈ [θ,δ) ∩ (0,δ). Then, by Lemma 2.1, the traveling wave problem (2.4) has a solution pair


(c,q) = (c0,q0) with c0 > 0 and q0(·) strictly increasing. The same reasoning as in the proof of Theorem 1.1 shows that for some L > 0 sufficiently large,

u(t,x) := max{q0(ct − x − L),q0(ct + x − L)} satisfies (in the weak sense)

ut ≤ duxx + f(u) ≤ f(t,x,u) for t > 0, x ∈ R. Additionally,

0 ≤ u(t,x) ≤ δ ≤ u(t,x) for t > 0, x ∈ {g(t),h(t)}, and

u(0,x) ≤ u0(x) for x ∈ [−h0,h0]. Therefore we can apply the standard comparison principle over {(t,x) : t > 0,x ∈ [g(t),h(t)]} to deduce u(t,x) ≥ u(t,x) in this region.

Moreover, using

∥u(t,·) − δ∥L∞(R) = 0,

lim

t→∞

