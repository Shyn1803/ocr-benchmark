For the Fourier expansion, we use the same truncation mode for both the bundle and the manifold, as we can always take the maximum between the two when needed. The coefficients used in these computations are available in the GitHub repository associated with this paper [38].

The zero-finding problems (27), (44), and (61) define well-conditioned maps that can be used with root-finding algorithms to refine numerical approximations. In practice, after obtaining an approximate solution, we apply Newton’s method to these maps to improve the accuracy of our numerical approximations. The required level of accuracy varies depending on the proof. In some cases, smaller residuals are necessary, while in others, lower accuracy suffices.

Our proof consists of three stages: the proof of the tangent bundle, the proof of the stable manifold attached to the periodic orbit and the validation of the solution of the soliton boundary value problem. We begin by obtaining a solution to the bundle problem. Our numerical approximation x¯

F ∈ X

of the bundle problem satisfies that λ¯ < 0 and the coefficients of v¯ satisfy the symmetry condition

F

v¯k(i) = [¯v−(ik) ]∗, for i = 1,2, k ∈ Z. (72) Observe that this condition can be explicitly enforced in our computational implementation. We fix a norm weight ν = 1.05 for the norm in (15), and a scaling factor l = 0.5 for the phase condition

) = 2.6879100002352747 × 10−13, Z1(¯x

) = 0.3465291783592818, and Z2(¯x

(26). The computable bounds Y (¯x

F

F

) = 14.980732463866438, defined in (32), (33), and (41), satisfy the following inequalities:

F

Z1(¯x

) < 1 and Z2(¯x

) <

F

F

))2 2Y (¯x

(1 − Z1(¯x

F

.

)

F

Applying Theorem 7, we obtain a unique zero of the validation map (27), x

def= (λ,v(1),v(2)), within the ball BX

F

= 4.122891017172993 × 10−13. This zero corresponds to a solution

(¯x

,r

) with radius r

F

F

F

F

(λ,v(1),v(2),0,0) ∈ R × S4

,

F

which satisfies the sequence equation (23) and represents a real solution of (11). With this result, we can now evaluate the validation map and its derivative for the parameterization of the stable manifold attached to the periodic orbit described by (44).

The second stage of our proof corresponds to the construction of this parameterization. We have that in this case, for r∗

= 10−3 , the bounds Y ( ¯w,r

) = 6.327932449800631 × 10−9, Z1( ¯w,x¯

) = 0.9583731072113382, and Z2( ¯w,r∗

F

F

TF

) = 104.77593347038471 defined in (48), (50), and (53) satisfy

TF

) < 1 and Z2( ¯w,r∗

Z1( ¯w,x¯

) < min

F

TF

))2 2Y ( ¯w,r

(1 − Z1( ¯w,x¯

,r∗

F

TF

)

F

.

TF ∈ X

with a radius r

Therefore, we use Theorem 11 to validate our paramaterization of the manifold x

TF

= 1.5204458252945915 × 10−7. The resulting stable manifold is represented in orange in Figure 1. Once we obtain the stable manifold via the W parameterization, we compute a numerical approxi-

TF

mation to the corresponding boundary value problem. In this case, setting θ = 1 and L = 1 + 2π in (57), we obtain

σ¯ = 0.927447198734628. Next, in a manner analogous to the previous stages, we fix a norm weight ω = 1.05 in (15) and

compute the following bounds: Y (¯x

) = 7.814019760054922 × 10−7, Z1( ¯w,x¯

,r

) = 0.9076283031949424 and Z2(¯x

C

TF

F

,r∗

) = 372.96640912543626,

C

TF

26

