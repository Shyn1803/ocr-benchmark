8 ZDENĚK MIHULA

Lorentz spaces Lp,q(R,µ) are an important generalization of Lebesgue spaces, where either p ∈ (1,∞) and q ∈ [1,∞] or p = q = 1 or p = q = ∞. The corresponding r.i. function norm · Lp,q(R,µ) is deﬁned as

p−q1 f∗(t) Lq(0,∞), f ∈ M+(R,µ).

1

f Lp,q(R,µ) = t

![](<2503.05922_pg8_images/imageFile1.png>)

![](<2503.05922_pg8_images/imageFile2.png>)

However, one needs to be more careful here. The functional · Lp,q(R,µ) is not an r.i. function norm when 1 < p < q ≤ ∞, because it is not subadditive. When

1 < p < q ≤ ∞, the functional · Lp,q(R,µ) is merely equivalent to an r.i. function norm. More precisely, the functional

f L(p,q)(R,µ) = f∗∗ Lp,q(0,∞), f ∈ M+(R,µ), is an r.i. function norm, and there are positive constants C1 and C2 such that

C1 f L(p,q)(R,µ) ≤ f Lp,q(R,µ) ≤ C2 f L(p,q)(R,µ) for every f ∈ M+(R,µ), provided that either p ∈ (1,∞) and q ∈ [1,∞] or p = q = ∞. The interested reader can ﬁnd more information in [6, Chapter 4, Section 4] or [33]. In view of that, we will consider Lp,q(R,µ) an r.i. space even when 1 < p < q ≤ ∞. Note that

· Lp(R,µ) = · Lp,p(R,µ) for every p ∈ [1,∞].

Furthermore, when p ∈ (1,∞) and 1 ≤ q1 < q2 ≤ ∞, we have Lp,q

(R,µ) Lp,q

(R,µ),

2

1

regardless of whether µ(R) < ∞ or not. Orlicz spaces LA(R,µ) are another very important generalization of Lebesgue spaces. The corresponding r.i. function norm

· LA(R,µ) is deﬁned as

f LA(R,µ) = inf λ > 0 :

A

R

|f(x)| λ

![](<2503.05922_pg8_images/imageFile3.png>)

dµ(x) ≤ 1 , f ∈ M+(R,µ),

where A: [0,∞] → [0,∞] is a Young function. A function A: [0,∞] → [0,∞] is called a Young function if it is convex, left-continuous, vanishing at 0, and not constant on the entire interval (0,∞). For example, when p ∈ [1,∞), we have  · Lp(R,µ) =  · LA(R,µ) with A(t) = tp, t ≥ 0. We also have  · L∞(R,µ) =  · LA(R,µ) with A(t) = ∞ · χ(1,∞](t), t ≥ 0. Besides the classical textbooks [6, 53], the interested reader can ﬁnd more information on the contemporary theory of Orlicz spaces and in particular Orlicz–Sobolev spaces in [16, 46].

An analogue of Fatou’s lemma is at our disposal in the framework of r.i. spaces. More precisely, if M(R,µ) ∋ fk → f pointwise µ-a.e., then

- (2.1) f X(R,µ) ≤ lim inf k→∞

fk X(R,µ).

With any r.i. function norm · X(R,µ), there is associated another r.i. function norm, · X′(R,µ), deﬁned for g ∈ M+(R,µ) as

- (2.2) g X′(R,µ) = sup f X(R,µ)≤1 R

|f(x)||g(x)|dµ(x), g ∈ M+(R,µ).

The r.i. function norm · X′(R,µ) is called the associate norm of · X(R,µ). The resulting r.i. space X′(R,µ) is called the associate space. The deﬁnition of  · X′(R,µ) immediately gives us that the Hölder inequality

- (2.3)


|f||g|dµ ≤ f X(R,µ) g X′(R,µ) for all f,g ∈ M(R,µ)

R

