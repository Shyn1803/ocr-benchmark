New Lagrangian approach to optimal control of SODEs

![](<2503.04466_pg9_images/imageFile1.png>)

# 2 Optimal control of second-order systems

The optimal control problem for second-order systems, under suﬃcient diﬀerentiability conditions can be treated exactly as in Eq. (3). There, the augmented running cost featured inside the integral was a function on T∗M ⊕M E. In the second-order case, this naturally leads to an augmented running cost on T∗TQ ⊕TQ E. Assuming adapted local coordinates (q,v,λq,λv) on T∗TQ, and a generic controlled SODE X = v ∂q + f(q,v,u)∂v, Eq. (3) transforms into

J˜1(x,λ,u) = φ(q(T),v(T)) (7)

T

C(q(t),v(t),u(t)) + (λq(t),λv(t)),( ˙q(t) − v(t),v˙(t) − f(q(t),v(t),u(t))) TQ dt.

+

0

We refer to this as the ﬁrst-order version of the optimal control problem since the controlled SODE appears as a ﬁrst order system. The second-order constraint, i.e. q˙ = v, may be added implicitly, leading to a new augmented cost function

J˜2(y,u) = φ(q(T),q˙(T)) +

T

0

C(q(t),q˙(t),u(t)) + κ(t)⊤(¨q(t) − f(q(t),q˙(t),u(t))) dt. (8)

Here, the curve y = (q,κ) is a curve on T∗Q. One must also understand u to denote the curve deﬁned on the ﬁbers along the tangent lift of q, i.e. (q(t),q˙(t),u(t)) ∈ E. The remaining constraint is now to be interpreted as a function on T(2)Q ⊕TQ E. Taking variations we ﬁnd that the necessary conditions for optimality provided by J˜1 are

- • (state dynamics) q˙(t) = v(t), v˙(t) = f(x(t),v(t),u(t)),
- • (adjoint dynamics) λ˙q(t)⊤ = D1C(q(t),v(t),u(t)) − λv(t)⊤ D1f(q(t),v(t),u(t)), λ˙v(t)⊤ = D2C(q(t),v(t),u(t)) − λv(t)⊤ D2f(q(t),v(t),u(t)) − λq(t)⊤,
- • (maximization) 0 = D3C(q(t),v(t),u(t)) − λv(t)⊤ D3f(q(t),v(t),u(t)),
- • (transversality) λq(T)⊤ = −D1φ(q(T),v(T)), λv(T)⊤ = −D2φ(q(T),v(T));


while those provided by J˜2 are

- • (state dynamics) q¨(t) = f(q(t),q˙(t),u(t)),
- • (adjoint dynamics) κ¨(t)⊤ = dtd D2C(q(t),q˙(t),u(t)) − κ(t)⊤D2f(q(t),q˙(t),u(t)) − D1C(q(t),q˙(t),u(t)) + κ(t)⊤ D1f(q(t),q˙(t),u(t)),

![](<2503.04466_pg9_images/imageFile2.png>)

- • (maximization) 0 = D3C(q(t),q˙(t),u(t)) − κ(t)⊤ D3f(q(t),q˙(t),u(t)),
- • (transversality) κ(T)⊤ = −D2φ(q(T),q˙(T)), κ˙(T)⊤ = D1φ(q(T),q˙(T))


+ D2C(q(T),q˙(T),u(T)) + D2φ(q(T),q˙(T))D2f(q(T),q˙(T),u(T)). These, lead to the following easy to check Theorem 2.1. The necessary optimality conditions provided by J˜1 and J˜2 are equivalent under the identiﬁcation λv = κ.

![](<2503.04466_pg9_images/imageFile3.png>)

March 7, 2025 9

