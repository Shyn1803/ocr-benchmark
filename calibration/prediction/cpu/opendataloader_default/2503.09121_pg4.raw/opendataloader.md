Theorem 1.9. Given integers ∆ 1 and n 2∆. There exist A,B ⊆ Z, |A| = |B| = n and a relation R ⊆ A × B with bounded degree ∆ from B such that

|A +R B| = |A| + |B| − 1 −

5∆ 2

![](<2503.09121_pg4_images/imageFile1.png>)

.

We believe the above theorem is tight, which suggests Theorem 1.5(i) could potentially be strength-

ened to |A +R B| |A| + |B| − 1 − 5∆2 . It is worth noting that any improvement of the −3∆ term in Theorem 1.5(i) would directly lead to a strengthening of Theorem 1.6(i), with the same parameters

![](<2503.09121_pg4_images/imageFile2.png>)

cε,p0 unchanged. The bottleneck of the current method for potential improvement of Theorem 1.6(i) lies in the case A,B ⊆ Z after applying the rectiﬁability argument. The remaining part of the proof would remain valid without any modiﬁcation.

Conjecture 1.10. Suppose ∆ 1 is an integer, A,B ⊆ Z satisﬁes |B| |A|, and R ⊆ A × B is a binary relation between A and B. If the maximum degree of R on B is at most ∆, we have

|A +R B| |A| + |B| − 1 −

5∆ 2

![](<2503.09121_pg4_images/imageFile3.png>)

.

The second part of this paper presents two examples. The ﬁrst explans why the additional requirement |B| = Oε(p) is necessary for Corollary 1.8(i) to hold. The second demonstrates why a stronger assumption |A|+|B| (1+δ)p is required for Conjecture 1.2 to hold in order to prove |A+RB| p−2, even in the case where |B| εp.

Theorem 1.11(i) restates an example originally given by Lev [Lev00b]. We reformulated it here for consistency with the notation and style used throughout this paper. Theorem 1.11(ii) was inspired from the same paper.

Theorem 1.11. Suppose p is a prime number.

- (i) For any integer k 1 and 1 ℓ ⌊p2−kk−−11⌋, there exist subsets A,B ⊆ Fp and a function

![](<2503.09121_pg4_images/imageFile4.png>)

R: B → A such that |A| = p − (k − 1)ℓ − k + 1, |B| = kℓ + 2 and |A +R B| = p − k.

- (ii) For any prime number p, there exists a subset A ⊆ Fp and a symmetric relation R ⊆ A × A

with maximum degree 1, such that |A| = 6⌊11p ⌋ − 3 and |A +R A| = p − 3.

![](<2503.09121_pg4_images/imageFile5.png>)

- (iii) For any ε > 0, there exists δ > 0 such that for any suﬃciently large prime number p, there


exist A,B ⊆ Fp with |A| + |B| > (1 + δ)p − O(1), |B| εp, and a relation R ⊆ A × B with maximum degree 1, such that |A +R B| = p − 3.

Plugging ℓ = ⌊p2−kk−−11⌋ and ℓ = 1 into Theorem 1.11(i), we have the following. Corollary 1.12. Suppose p is a prime number.

![](<2503.09121_pg4_images/imageFile6.png>)

- (i) For any integer k 1, there exist subsets A,B ⊆ Fp and a function R: B → A such that

- |A| = p − (k − 1)⌊p2−kk−−11⌋ − k + 1, |B| = k⌊p2−kk−−11⌋ + 2 and |A +R B| = p − k.

![](<2503.09121_pg4_images/imageFile7.png>)

![](<2503.09121_pg4_images/imageFile8.png>)

(ii) For any ε > 0, there exist A,B ⊆ Fp and a function R: B → A such that |A| = (1−2ε)p+O(1),

- |B| = εp+O(1) and |A+R B| = |A|+|B|−4, where the value of the O(1) term within the expressions of |A| and |B| are smaller than 3.




Thus, for potential extensions of Corollary 1.8(i), in the regime where |A|+|B| p, it is necessary

to assume at least |A|+|B| p−k+⌊p2−kk−−11⌋+4 > 2k2−k1p−k+2 in order to establish |A+RB| p−k+1. In the regime |A| + |B| (1 − ε)p, an additional assumption |B| εp is required.

![](<2503.09121_pg4_images/imageFile9.png>)

![](<2503.09121_pg4_images/imageFile10.png>)

Combining Corollary 1.8(i) and the examples above, we propose the following conjecture. The main obstacle in proving this conjecture lies in the fact that, in Theorem 1.6, the parameter cε is not linear in ε. So it remains unclear how to prove |A +R B| |A| + |B| − 3 under assumptions such as |A| + c|B| < p for any constant c.

Conjecture 1.13. Suppose p is a prime number, A,B ⊆ Fp with |B| |A|. Let R: B → A be an arbitrary function from B to A. If |A| + 2|B| p, then |A +R B| |A| + |B| − 3.

4

