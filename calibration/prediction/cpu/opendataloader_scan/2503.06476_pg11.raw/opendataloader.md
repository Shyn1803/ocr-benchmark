which implies

$$
Qk 0(2k) 0 k=0
$$

Since the right-hand side of the above inequality is ﬁnite and inequality holds for any positive integer N , then we get ∞ k 2

$$
Qk + k=0
$$

The above inequality implies the result of this lemma.

Theorem 4.1. Suppose that Φ is convex in component-wise sense (i.e., Φ is R m − convex) and the Assumption 1 holds. Then any sequence produced by Algorithm 3.1 converges to a WPOS x ∗ ∈ R n .

Proof. Since by Algorithm 3.1 , { Φ( x k ) } is a component-wise decreasing sequence, then by assumption, there exists ˜ x ∈ R n such that

It is observed that 0 < α k ≤ 1 for all k, so

$$
(4.18)
$$

$$
= for all k = 0,1,2, Qk for all k = 0,1, 2, ( Qk 2k+1 2k
$$

Therefore, by above inequality, ( 4.18 ), and Lemma ( 4.5 ) we obtained

Thus,

$$
= k=0 k=0 = xk|l2 < % 4.19) k=0 Ilzk+1
$$

Let us deﬁne ˜ L = { x ∈ R n : Φ( x ) ≤ Φ( x k ) , k of Φ and Lemma 4.3 , for any x ∈ ˜ L we have

$$
Ilz for all k = 0,1,2
$$

As L is non empty because ˜ x ∈ L , by ( 4.19 ) and the above inequality, it follows that { x } is quasi-Fejer convergent to the set ˜ L. Then by Theorem 2.4 , { x k } is bounded and hence { x k } has an accumulation point. Let x ∗ be one of them. Then by Lemma 4.4 , x ∗ ∈ ˜ L. Then by Theorem 2.4 , we observe that { x k } converges to x ∗ . Therefore, by Theorem 3.3 , x ∗ is a critical point, and hence R m − convexity implies that x ∗ is a weak Pareto optimal solution for Φ .

