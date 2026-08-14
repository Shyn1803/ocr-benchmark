10 Billey and Ryan

The decaf order has many nice properties. It is the product of Bruhat order for Sk and the poset determined by pushbacks on the subset {w ∈ Wn,k | π(w) = id}. The decaf order is a ranked poset on Wn,k, and its rank generating function is the same as the Poincaré polynomial in (1.4). The medium roast and espresso orders are not ranked posets in general. For n ≥ 5 and most values of k, there are covering relations in the medium roast Fubini-Bruhat order (Wn,k, ≤) with a dimension difference of 2 or more, causing the medium roast Fubini-Bruhat order to be unranked in general. For example, in W5,4, 44312 covers 41321, but 44312 has dimension 1, and 41321 has dimension 3.

- Theorem 4.2. The Superpushback Rule. Suppose w ∈ Wn,k, i ∈ [k − 1], and j ∈ [n] such that wj = πi is a redundant letter in w. If i + p ≤ k and v is obtained from w by replacing wj by πi+p(w), then v ⇀ w and this is a covering relation in both espresso and medium roast orders.
- Theorem 4.3. The Lifting Property. Suppose v, w ∈ Wn,k, i ∈ [k − 1], αi+1(v) < αi(v), and αi+1(w) < αi(w). If v ≤ w in medium roast Fubini-Bruhat order, then siv ≤ siw. Furthermore, if v ⇀ w, then siv ⇀ siw.


# 5 Essential Sets

We extend the notion of a Rothe diagram from Definition 2.1 to Fubini words. This allows us to define the essential set for a Fubini word. We then show the essential set determines a minimal set of rank equations on the corresponding PR variety, generalizing Fulton’s essential set for permutations and Schubert varieties [7]. This leads to an essential set characterization of v ≤ w in medium roast order.

- Definition 5.1. [16] A Fubini word w ∈ Wn,k is called convex if h < j and wh = wj implies that wi = wj for every i such that h < i < j. Then the convexification of w, denoted by conv(w), is the unique convex word such that π(conv(w)) = π(w) and the content of w and

conv(w) are the same as multisets. The standardization of w, denoted std(w) ∈ Sn, is obtained by replacing the n − k redundant letters of w with k + 1, k + 2, . . . , n from left to right.

Deduce from Definition 5.1 that two Fubini words v, w ∈ Wn,k have the same convexification, conv(v) = conv(w), if and only if π(v) = π(w) and they have the same multiset of letters.

- Definition 5.2. Given Fubini word w ∈ Wn,k, define the diagram of w to be D(std(conv(w))).


One can observe that D(std(conv(w))) ⊂ [k] × [n], as none of the bottom n − k rows will contribute any elements to D(std(conv(w))). Thus, the diagram of a Fubini word in Wn,k can be drawn as a k × n grid of dots. For example, the convexification of w = 44253136541 ∈ W11,6 is 44425533116, and std(44425533116) = [4,7,8,2,5,9,3,10,1,11,6]. So the diagram for w is D([4,7,8,2,5,9,3,10,1,11,6]). See Figure 1.

