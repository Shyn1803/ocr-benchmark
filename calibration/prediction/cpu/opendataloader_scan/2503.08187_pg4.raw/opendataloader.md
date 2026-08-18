where α > 0 . The FWI problem in equation 7 ensures that the estimated model, while satisfying the data (and the wave equation), is smooth along the direction θ .

Figure 1 , top row, shows the anisotropic regularization balls for only one term of the regularizer equation 4 and for different values of [ σ ] i = σ and [ θ ] i = θ . We observe that for σ = 0 . 5 , the anisotropic regularization becomes equivalent to the standard isotropic regularization. When the value of σ increases, reaching the maximum considered value of 0.9, the degree of regularization applied in the direction θ and its normal is maximally different, resulting in a needle-shaped ellipse. This shape favors models with elongated features aligned with θ , while allowing variations in the normal direction to it, as illustrated in the bottom row.

# 3 Algorithm

The augmented Lagrangian function of equation 7 is

$$

$$

$$
ns Pus 2 IA(m)us bs) 2 =
$$

2 where z ( θ ) = min(max( θ, − π 2 ) , π 2 ) , λ s and ν are Lagrange multipliers associated to the constraints, and µ > 0 and τ > 0 are the penalty parameters. The regularization parameter α > 0 is given, being typically determined by the discrepancy principle.

This problem can be efﬁciently solved using the alternating direction method of multipliers (ADMM, [ 15 ]), resulting in the following iterative procedure starting from initial guess m (typically encoding some prior information), (spatially invariant) σ = 0 . 5 and initial multipliers λ s = ν = 0 : +

$$
0+ = 8a)
$$

$$
arg min L(0+,0, m, X,v) Us ,
$$

$$
U 8c) , 0 +
$$

$$
m + arg min L(0+_ 8d) , 0+ .
$$

$$
bs) 8e)
$$

$$
=v _ T(0+ _ 2+). (8f)
$$

Here, the updated variables at each iteration are denoted by a superscript “+”. Each step of the algorithm addresses a speciﬁc subproblem, as described more in details below.

Subproblem equation 8a involves minimizing the regularization function R , as deﬁned in equation 4 , with respect to θ , given the current values of m and σ . This can can be efﬁciently achieved using a single iteration of the Gauss-Newton method. To ensure the stability of the θ update, it is essential to incorporate a smoothing term, as suggested by [ 11 ].

Subproblem equation 8b involves minimizing R with respect to σ , resulting in: 2

$$
[gz']2 [ơ]
$$

where ([ g x ′ ] i , [ g z ′ ] i ) T = R ([ θ ] i )[ ∇ m ] i represent the rotated gradient of the current model at the i th pixel. This expression for equation 9 is justiﬁed by considering that, when [ θ ] i corresponds to the correct orientation angle, we typically expect | [ g x ′ ] i | ≪ | [ g z ′ ] i | . In this case, directly minimizing [ g x ′ ] 2 i + [ g z ′ ] 2 i would heavily penalize [ g z ′ ] i , which is undesirable because we aim to apply more smoothing along the direction deﬁned by [ θ ] i . The weights [ σ ] i in equation 9 balance the contributions of gradient components in the weighted sum [ σ ] 2 i [ g x ′ ] 2 i + (1 − [ σ ] i ) 2 [ g z ′ ] 2 i , ensuring that the magnitudes of both terms are approximately equal before penalization. This adaptive weighting mechanism effectively enhances smoothing along the structural direction [ θ ] i while allowing variations across it, eventually enabling the recovery of dominating structures and details in the model m . To maintain stability during the σ update, the computed weights are smoothed using a convolution with a 5 × 5 averaging ﬁlter; alternatively, one could incorporate a smoothing term.

A comprehensive analysis of the methods for solving subproblems equation 8c and equation 8d can be found in [ 14 ].

