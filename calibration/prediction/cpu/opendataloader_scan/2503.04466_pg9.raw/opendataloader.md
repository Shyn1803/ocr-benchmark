# 2 Optimal control of second-order systems

The optimal control problem for second-order systems, under suﬃcient diﬀerentiability conditions can be treated exactly as in Eq. (3). There, the augmented running cost featured inside the integral was a function on T ∗ M ⊕ M E . In the second-order case, this naturally leads to an augmented running cost on T ∗ T Q ⊕ T Q E . Assuming adapted local coordinates ( q,v,λ q ,λ v ) on T ∗ T Q , and a generic controlled SODE X = v ∂ q + f ( q,v,u ) ∂ v , Eq. (3) transforms into

$$
+
$$

We refer to this as the ﬁrst-order version of the optimal control problem since the controlled SODE appears as a ﬁrst order system.

The second-order constraint, i.e. ˙ q = v , may be added implicitly, leading to a new augmented cost function

$$
8
$$

Here, the curve y = ( q,κ ) is a curve on T ∗ Q . One must also understand u to denote the curve deﬁned on the ﬁbers along the tangent lift of q , i.e. ( q ( t ) , ˙ q ( t ) ,u ( t )) ∈ E . The remaining constraint is now to be (2)

interpreted as a function on T Q ⊕ T Q E . Taking variations we ﬁnd that the necessary conditions for optimality provided by ˜ J 1 are

(state dynamics) ˙ q ( t ) = v ( t ),

(maximization) 0 = D 3 C ( q ( t ) ,v ( t ) ,u ( t )) −

$$

$$

while those provided by ˜ J 2 are

=

$$

$$

$$
transversality) K(T)T k(T)T = +
$$

These, lead to the following easy to check

Theorem 2.1. The necessary optimality conditions provided by ˜ J 1 and ˜ J 2 are equivalent under the identiﬁcation λ v = κ .

