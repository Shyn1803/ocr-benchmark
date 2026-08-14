veriﬁed that g is an eub for f ↾ αξ. But then g witnesses that αξ is good for f. Moreover, by construction, αξ ∈ C. Since C was arbitrary, we have shown that there are stationarily many elements of Sλ

+3

λ that are good for f.

By Theorem 12, it follows that there is an eub h for f such that cf(h(i)) > λ for all i < ω. Claim 14. cf(h(i)) ≥ λ+3 for all but ﬁnitely many i < ω.

Proof. If not, then there exist k ∈ {1,2} and an unbounded A ⊆ ω such that, for all i ∈ A, we have cf(h(i)) = λ+k. For each i ∈ A, let {δηi : η < λ+k} enumerate, in increasing fashion, a set of ordinals coﬁnal in h(i). For each η < λ+k, deﬁne a function hη from ω to the ordinals by letting hη(i) = δηi if i ∈ A and hη(i) = 0 otherwise. For each η < λ+k, we have hη <∗ h, so, since h is an eub for f, there is βη < λ+3 such that hη <∗ fβ

. Let γ = sup{βη : η < λ+k}. Since k < 3, we have γ < λ+3. Therefore, for all η < λ+k, we have hη <∗ fγ. Fix an unbounded B ⊆ λ+k and an n < ω such that, for all η ∈ B, we have hη <n fγ. But then, for all i ∈ A \ n, we must have fγ(i) ≥ sup{δηi : η ∈ B} = h(i), contradicting the fact that h is an upper bound for f.

η

![](<2503.06758_pg6_images/imageFile1.png>)

![](<2503.06758_pg6_images/imageFile2.png>)

![](<2503.06758_pg6_images/imageFile3.png>)

![](<2503.06758_pg6_images/imageFile4.png>)

But this claim immediately contradicts the fact that f is a sequence of functions from ω to ǫ and ǫ < λ+3. This is because, by the claim, we must have h(i) > ǫ for all but ﬁnitely many i < ω. But then the constant function, taking value ǫ, witnesses that h fails to be an eub.

![](<2503.06758_pg6_images/imageFile5.png>)

![](<2503.06758_pg6_images/imageFile6.png>)

![](<2503.06758_pg6_images/imageFile7.png>)

![](<2503.06758_pg6_images/imageFile8.png>)

The results in this section lead to the following corollary. Corollary 15. Suppose that 3 ≤ n < ω.

- 1. If η < ωn+1, then there is no strongly increasing sequence fα : α < ωn+1 of functions from ω to η.
- 2. (ℵω+1,ℵω) ։ (ℵn+1,ℵn).
- 3. There are no inner models V ⊆ W of ZFC such that (ℵω+1)V = (ℵn+1)W. It also follows that the only regular cardinals that can possibly be lengths


of strongly increasing sequences from ωω are ℵn for 0 ≤ n ≤ 3. We have seen that there are always such sequences of length ℵ0 and ℵ1. We will prove, in Section 3, the consistency of the existence of a strongly increasing sequence of length ℵ2. The question about the consistency of the existence of a strongly increasing sequence of length ℵ3 remains open.

# 3 Consistency via a Pmax variation

In this section we use a natural variation of Woodin’s partial order Pmax to produce a very strongly increasing sequence in ωω of length ω2.

We refer the reader to [14] for background on Pmax, especially Chapter 4 and Section 9.2. The article [8] may also be helpful. Conditions in our partial order P are triples (M,F,a) such that

6

