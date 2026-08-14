Optimal Space-Variant Anisotropic Tikhonov Regularization Gholami and Gazzola A PREPRINT

![](<2503.08187_pg4_images/imageFile1.png>)

where α > 0. The FWI problem in equation 7 ensures that the estimated model, while satisfying the data (and the wave equation), is smooth along the direction θ.

Figure 1, top row, shows the anisotropic regularization balls for only one term of the regularizer equation 4 and for different values of [σ]i = σ and [θ]i = θ. We observe that for σ = 0.5, the anisotropic regularization becomes equivalent to the standard isotropic regularization. When the value of σ increases, reaching the maximum considered value of 0.9, the degree of regularization applied in the direction θ and its normal is maximally different, resulting in a needle-shaped ellipse. This shape favors models with elongated features aligned with θ, while allowing variations in the normal direction to it, as illustrated in the bottom row.

3 Algorithm

The augmented Lagrangian function of equation 7 is L(θ,σ,us,m,λ,ν) =

ns

- 1

![](<2503.08187_pg4_images/imageFile2.png>)

- 2


Pus − ds 22 + αR(m,θ,σ)

s=1

ns

µ 2

A(m)us − bs 22 − λTs (A(m)us − bs)

+

![](<2503.08187_pg4_images/imageFile3.png>)

s=1

τ 2

θ − z 22 − νT(θ − z),

+

![](<2503.08187_pg4_images/imageFile4.png>)

where z(θ) = min(max(θ,−π2), π2), λs and ν are Lagrange multipliers associated to the constraints, and µ > 0 and τ > 0 are the penalty parameters. The regularization parameter α > 0 is given, being typically determined by the

![](<2503.08187_pg4_images/imageFile5.png>)

![](<2503.08187_pg4_images/imageFile6.png>)

discrepancy principle.

This problem can be efﬁciently solved using the alternating direction method of multipliers (ADMM, [15]), resulting in the following iterative procedure starting from initial guess m (typically encoding some prior information), (spatially invariant) σ = 0.5 and initial multipliers λs = ν = 0:

θ+ = argmin

L(θ,σ,us,m,λ,ν) (8a) σ+ = argmin

θ

L(θ+,σ,us,m,λ,ν) (8b) u+s = arg min

σ

L(θ+,σ+,u,m,λ,ν) (8c) m+ = arg min

u

L(θ+,σ+,u+s ,m,λ,ν) (8d)

m

λ+s = λs − µ(A(m+)u+s − bs) (8e) ν+ = ν − τ(θ+ − z+). (8f)

Here, the updated variables at each iteration are denoted by a superscript “+”. Each step of the algorithm addresses a speciﬁc subproblem, as described more in details below.

- Subproblem equation 8a involves minimizing the regularization function R, as deﬁned in equation 4, with respect to θ, given the current values of m and σ. This can can be efﬁciently achieved using a single iteration of the Gauss-Newton method. To ensure the stability of the θ update, it is essential to incorporate a smoothing term, as suggested by [11].
- Subproblem equation 8b involves minimizing R with respect to σ, resulting in:


[gz′]2i [gx′]2i + [gz′]2i

[σ]i =

, (9)

![](<2503.08187_pg4_images/imageFile7.png>)

where ([gx′]i,[gz′]i)T = R([θ]i)[∇m]i represent the rotated gradient of the current model at the ith pixel. This expression for equation 9 is justiﬁed by considering that, when [θ]i corresponds to the correct orientation angle, we typically expect |[gx′]i| ≪ |[gz′]i|. In this case, directly minimizing [gx′]2i + [gz′]2i would heavily penalize [gz′]i, which is undesirable because we aim to apply more smoothing along the direction deﬁned by [θ]i. The weights [σ]i in equation 9 balance the contributions of gradient components in the weighted sum [σ]2i [gx′]2i + (1 − [σ]i)2[gz′]2i , ensuring that the magnitudes of both terms are approximately equal before penalization. This adaptive weighting mechanism effectively enhances smoothing along the structural direction [θ]i while allowing variations across it, eventually enabling the recovery of dominating structures and details in the model m. To maintain stability during the σ update, the computed weights are smoothed using a convolution with a 5 × 5 averaging ﬁlter; alternatively, one could incorporate a smoothing term.

A comprehensive analysis of the methods for solving subproblems equation 8c and equation 8d can be found in [14].

4

