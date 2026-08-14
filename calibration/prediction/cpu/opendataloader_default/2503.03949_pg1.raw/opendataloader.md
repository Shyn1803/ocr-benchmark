arXiv:2503.03949v1 [math.AG] 5 Mar 2025

Volumes in Calabi-Yau Complete Intersection of Products of Projective Space

Yi-Heng Tsai

Abstract. We prove that the birational automorphism group of a general Calabi-yau complete intersection X given by ample divisors in Pn1

× ··· × Pnl

is always Lorentzain. Applying the Kawamata-Morrison cone theorem on such X, we compute volX(D + sA) for any divisor D ∈ ∂Eﬀ(X) and ample divisor A when s is small. We also provide examples of volumes of certain Cartier divisors that involve the digamma function.

![](<2503.03949_pg1_images/imageFile1.png>)

# 1 Introduction

It is conjectured in [Mor93] and [Kaw97] that the movable eﬀective cone of a Calabi-Yau manifold has a rational fundamental domain under the action of the birational automorphism group.

Conjecture 1.0.1 (Kawamata-Morrison cone conjecture) Let X be a Calabi-Yau manifold. Then there exists a rational polyhedral fundamental domain Π for the action of the birational automorphism group Bir(X) on the movable eﬀective cone Move(X) in the sense that

![](<2503.03949_pg1_images/imageFile2.png>)

- (i) Move(X) = g∈Bir(X)

![](<2503.03949_pg1_images/imageFile3.png>)

g∗Π,

- (ii) int(Π) ∩ int(g∗Π) = ∅ if g∗ = id.


The conjecture has been proven in the case when X is a general Wehler N-fold i.e. a general hypersurface of multidegree (2,··· ,2) in (P1)N+1 for N ≥ 3 ([CO15, Theorem 1.3]). In [FLT23], the structure of the boundary of the pesudoeﬀective cone Eﬀ(X) has been studied. The divergent–recurrent decomposition of ∂Eﬀ(X) is proven in [FLT23, Theorem 2.4.2], and the following result on the asymptotic behavior of volume function near ∂Eﬀ(X) is derived:

![](<2503.03949_pg1_images/imageFile4.png>)

![](<2503.03949_pg1_images/imageFile5.png>)

![](<2503.03949_pg1_images/imageFile6.png>)

Theorem 1.0.2 ([FLT23, Theorem 1.3.7]) Suppose X is a general Wehler Calabi-Yau N-fold. Then, for every pseudoeﬀective R-divisor D in ∂Eﬀ(X) and suﬃciently ample divisor A, there exists an integer s(D) ∈ {0,··· ,N − 2} and a real number δ(D) ∈ [1, 21(N − s(D))] such that

![](<2503.03949_pg1_images/imageFile7.png>)

![](<2503.03949_pg1_images/imageFile8.png>)

log vol(D + sA) log s

= δ(D),

liminf

![](<2503.03949_pg1_images/imageFile9.png>)

s↓0

N − s(D) 2

log vol(D + sA) log s

limsup

=

.

![](<2503.03949_pg1_images/imageFile10.png>)

![](<2503.03949_pg1_images/imageFile11.png>)

s↓0

The fact that the birational automorphism group of a general Wehler N-fold is Lorentzian provides a hyperbolic subspace in PN1(X), and plays an important role when investigating the stucture of ∂Eﬀ(X) (see [FLT23, §2.3]). Let n = (n1,··· ,nl) ∈ N such that |n| ≥ 4 and n = (2,2). In [Ya´22], the author generalized the results in [CO15], and proved the Kawamata-Morrison cone conjecture when X is a general Calabi-Yau complete intersection in Pn := Pn1

![](<2503.03949_pg1_images/imageFile12.png>)

× ··· × Pnl given by the intersection of n ample divisors, with n ≤ min {ni}. He also conjectured that the

1

