which implies

N

tk 2 2

αk |Θ(xk)| +

![](<2503.06476_pg11_images/imageFile1.png>)

k=0

1 β

(Φj(x0) − yˆj), ∵ θ(xk) < 0.

≤

![](<2503.06476_pg11_images/imageFile2.png>)

Since the right-hand side of the above inequality is ﬁnite and inequality holds for any positive integer N, then we get

∞

tk 2 2

αk |Θ(xk)| +

< ∞.

![](<2503.06476_pg11_images/imageFile3.png>)

k=0

The above inequality implies the result of this lemma.

![](<2503.06476_pg11_images/imageFile4.png>)

![](<2503.06476_pg11_images/imageFile5.png>)

![](<2503.06476_pg11_images/imageFile6.png>)

![](<2503.06476_pg11_images/imageFile7.png>)

Theorem 4.1. Suppose that Φ is convex in component-wise sense (i.e., Φ is Rm− convex) and the Assumption 1 holds. Then any sequence produced by Algorithm 3.1 converges to a WPOS x∗ ∈ Rn.

Proof. Since by Algorithm 3.1, {Φ(xk)} is a component-wise decreasing sequence, then by assumption, there exists x˜ ∈ Rn such that

Φ(˜x) ≤ Φ(xk) for all k = 0,1,2... . (4.18)

It is observed that 0 < αk ≤ 1 for all k, so

1 αk

xk+1 − xk 2 ≤

![](<2503.06476_pg11_images/imageFile8.png>)

1 αk

≤

![](<2503.06476_pg11_images/imageFile9.png>)

xk+1 − xk 2 for all k = 0,1,2,...

αktk 2 = αk tk 2 for all k = 0,1,2,... (∵ xk+1 = xk + αktk).

Therefore, by above inequality, (4.18), and Lemma (4.5) we obtained

∞

k=0

∞

αk tk 2 < ∞.

xk+1 − xk 2 ≤

k=0

Thus,

∞

k=0

xk+1 − xk 2 < ∞. (4.19)

Let us deﬁne L˜ = {x ∈ Rn : Φ(x) ≤ Φ(xk), k = 0,1,2,...}. By the component-wise convexity of Φ and Lemma 4.3, for any x ∈ L˜ we have

x − xk+1 2 ≤ x − xk 2 + xk − xk+1 2 for all k = 0,1,2... .

As L˜ is non empty because x˜ ∈ L˜, by (4.19) and the above inequality, it follows that {xk} is quasi-Fejer convergent to the set L.˜ Then by Theorem 2.4, {xk} is bounded and hence {xk} has an accumulation point. Let x∗ be one of them. Then by Lemma 4.4, x∗ ∈ L.˜ Then by Theorem 2.4, we observe that {xk} converges to x∗. Therefore, by Theorem 3.3, x∗ is a critical point, and hence Rm− convexity implies that x∗ is a weak Pareto optimal solution for Φ.

![](<2503.06476_pg11_images/imageFile10.png>)

![](<2503.06476_pg11_images/imageFile11.png>)

![](<2503.06476_pg11_images/imageFile12.png>)

![](<2503.06476_pg11_images/imageFile13.png>)

11

