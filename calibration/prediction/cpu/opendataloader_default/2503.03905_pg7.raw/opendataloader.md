ON THE MINIMUM HAMMING DISTANCE BETWEEN VECTORIAL BOOLEAN AND AFFINE FUNCTIONS7

We show that σ′ is bijective on GF(2m). Let us ﬁx u, y1, y2 ∈ GF(2m), y1 = y2. There is an element v ∈ GF(2t) such that

TrGF(2t)/GF(2)(uv) = h′(y1) + h′(y2).

As τ is surjective, there is a z ∈ GF(2m) with τ(z) = v. By Lemma 7, there is x ∈ GF(2m) with y1 ⋆ x + y2 ⋆ x = z. Then

(x) = TrGF(2t)/GF(2)(uτ(y1 ⋆ x + y2 ⋆ x) + uh(y1) + uh(y2))

(x) + αy

αy

2

1

= TrGF(2t)/GF(2)(uτ(z)) + h′(y1) + h′(y2)

= TrGF(2t)/GF(2)(uv) + h′(y1) + h′(y2)

= 0. This implies αy

(x) and σ′(y1) = σ′(y2). It follows that all component functions of f are of Maiorana-McFarland type bent function. This ﬁnishes the proof of the theorem.

(x) = αy

2

1

In this paper, we do not study the question of EA-equivalence of the (2m, t)-bent functions deﬁned above. In general, this is a very diﬃcult question. We only remark that Weng, Feng and Qui [23] proved that most of the PS type bent functions, obtained from a Desarguesian spread are not EA-equivalent to any Maiorana–McFarland bent function. This leads us to conclude that, typically, for t > 1, the (2m, t)-bent functions described by (9) are generally not EA-equivalent to the other two classes, as speciﬁed in (6) and (8).

3.4. Proof of Theorem 1. Let us recall the Carlet-Ding-Yuan bound (2) for the distance between aﬃne and (n, m)-bent functions:

- 1

![](<2503.03905_pg7_images/imageFile1.png>)

- 2m


1 −

- 1

![](<2503.03905_pg7_images/imageFile2.png>)

- 2m


2n − 2n/2 ≤ dH(f, A) ≤ 1 −

2n + 2n/2 .

For an (n, m)-bent function f, the Walsh coeﬃcients are

 

±2n/2 if b = 0,

Wf(a, b) =

0 if a = 0, b = 0, 2n if a = 0, b = 0.



Hence, the Carlet-Ding-Yuan bound follows from Lemma 3 easily. The Liu-Mesnager-Chen Conjecture implies that the true value of dH(f, A) is 1 − 21m

2n − 2n/2 . Theorem 1 claims that this holds for two classes of (n, m)-bent functions.

![](<2503.03905_pg7_images/imageFile3.png>)

Proof of Theorem 1. Let Ei be the set of pairs (x, y) ∈ GF(2m)2 such that fi(x, y) = fi(0, 0), i = 1, 2. We show that |Ei| = 22m−t + 2m − 2m−t, which implies that fi has Hamming distance (1−2−t)(22m −2m) from the constant function fi(0, 0). Therefore, dH(fi, A) ≤ (1−2−t)(22m − 2m), and the theorem follows from the Carlet-Ding-Yuan bound.

Let T be the set of elements z ∈ GF(qm) with γ(z) = f1(0, 0). Since γ is balanced, |T| = 2m−t, and f1(x, y) = f1(0, 0) if and only if ⋆xy ∈ T. Moreover, since ⋆00 = 0, we have 0 ∈ T. The number of solutions of ⋆xy = 0 is 2 · 2m − 1, and the number of solutions of ⋆xy = t ∈ T \ {0} is 2m − 1. This implies

![](<2503.03905_pg7_images/imageFile4.png>)

![](<2503.03905_pg7_images/imageFile5.png>)

![](<2503.03905_pg7_images/imageFile6.png>)

![](<2503.03905_pg7_images/imageFile7.png>)

|E1| = |f1−1(f1(0, 0))| = 2 · 2m − 1 + (2m−t − 1)(2m − 1).

The same argument applies to f2. In this case, f2(0, 0) = h(0), and the number of solutions of σ(y) ⋆ x = t is 2 · 2m − 1 or 2m − 1, depending on t = 0 or t = 0.

