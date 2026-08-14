SPLICING SKEW SHAPED POSITROIDS 9

3. Skew shaped positroid varieties

3.1. Positroid varieties. First, we recall equivalent ways of describing positroid varieties in the Grassmannian: Grassmann necklaces and bounded aﬃne permutations.

Deﬁnition 3.1.1. A (k,n)-source Grassmann necklace I = (I1,I2,... ,In) is an n-tuple of k-element subsets Ii ⊆ [n] where

- • if i ∈ Ii then there exists j ∈ [n] such that Ii−1 = (Ii \ {i}) ∪ {j}, and
- • if i  ∈ Ii then Ii = Ii−1.


We denote by GN(k,n) the set of (k,n)-Grassmann necklaces.

- Remark 3.1.2. Note that if i ∈ Ii then it may be that Ii−1 = Ii = (Ii \ {i}) ∪ {i}. Finally, note that Ii−1 \ Ii is either empty or a singleton.
- Remark 3.1.3. Grassmann necklaces were ﬁrst deﬁned in [24]. Our deﬁnition is slightly


diﬀerent, as we use Ii−1 instead of Ii+1, this diﬀerence is indicated by the word source in the name.

Deﬁnition 3.1.4 ([19]). A bijection f : Z → Z is called a (k,n)-bounded aﬃne permutation if it satisﬁes the following conditions:

- (1) f(i + n) = f(i) + n for every i ∈ Z.
- (2) For every i ∈ Z, i ≤ f(i) ≤ f(i) + n.
- (3) We have: n


(f(i) − i) = nk.

i=1

Note that, by (1), f is uniquely determined by the values f(1),... ,f(n), which are pairwise distinct modulo n. We often simply denote f = [f(1),... ,f(n)]. Note also that, upon the presence of (1) and (2), (3) is equivalent to |{i ∈ [n] : f(i) > n}| = k. We denote the set of (k,n)-bounded aﬃne permutations by BA(k,n). We say that f is a bounded n-aﬃne permutation if there exists k such that f is a (k,n)-bounded aﬃne permutation.

Lemma 3.1.5. The sets GN(k,n) and BA(k,n) are in natural bijection. In the proof, we will need the following deﬁnition.

Deﬁnition 3.1.6. We deﬁne the cyclic order ≤i on the set [n]: i <i i + 1 <i i + 2 <i ··· <i n <i 1 <i ··· <i i − 1.

Proof of Lemma 3.1.5. This is essentially a combination of [19, Corollary 3.13] and [23, Remark 2.4]. For the reader’s convenience and to ﬁx notation, we provide the bijection ϕ :

GN(k,n) → BA(k,n). Let us ﬁrst describe f¯I := ϕ(I) (mod n) through its inverse f¯I−1: we have f¯I−1(i) = i if Ii−1 = Ii, and f¯I−1(i) = j if Ii−1 \ Ii = {j}. To lift this to a bounded aﬃne permutation, we set fI(i) = i + n if Ii−1 = Ii and i ∈ Ii, and fI(i) = i if i  ∈ Ii. On the other hand, if f : Z → Z is a k-bounded aﬃne permutation, let I = {i ∈ [n] | f(i) = i + n}, and f¯ = f (mod n). Then Ii consists of I together with the elements {a ∈ [n] | a <i f¯(a)}. The collection If = (I1,... ,In) is a Grassmann necklace, and f  → If, I  → fI are inverse bijections.

Now, we associate a Grassmann necklace and a bounded aﬃne permutation to an element V in the Grassmannian Gr(k,n) following [19, 24]. We represent V by a k ×n matrix of rank k, up to row operations, and denote by v1,... ,vn ∈ Ck the columns of V . Furthermore, we deﬁne vi for all i ∈ Z by setting vi+n := (−1)k−1vi. Given an (ordered) k-element subset

