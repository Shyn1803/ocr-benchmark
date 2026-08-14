The LVPP saddle point subproblem (3.6) can be discretized with many other techniques. We also provide results where the subproblem (3.6) is discretized with a coefficient-based Zernike sparse spectral method [39, 109, 130, 106] and a five-point stencil finite difference method. For the finite difference scheme, we change the domain to the square Ω = (−1,1)2. Here, we again use the double-exponential update rule

- (3.8) for αk. We terminate once ∥uk − uk−1∥ℓ2 < 10−9 where uk is the discrete coefficient vector for u at iteration k. The results are provided in Figure 2c where we observe h- and p-independent iteration counts for the proximal finite difference and spectral methods, respectively. Further numerical experiments with the obstacle problem can be found in [85, 62, 108].

3.2. Example 2: The Signorini problem. We now consider the classical Signorini problem. This problem demonstrates for the first time an extension of LVPP to pointwise bound constraints acting solely on the boundary of a computational domain Ω ⊂ R3. In this problem, we separate the boundary ∂Ω = ΓD ∪ ΓT into disjoint measurable subsets for imposing displacement and traction boundary conditions.

The Signorini problem, posed by Signorini in 1959 [123] and analyzed by Fichera in 1963 [59], is the essential first problem in contact mechanics. It models the deformation of a linear elastic body in the presence of a contact boundary constraint. The problem is posed on

- (3.9) V = u ∈ H1(Ω,R3) | u = g on ΓD , and involves the minimization of the strain energy function
- (3.10) J(u) =

- 1

- 2 Ω


(Cϵ(u)) : ϵ(u)dx −

Ω

f · udx,

over the feasible set

- (3.11) K = u ∈ V | u · n˜ ≤ ϕ1 on ΓT .


Here, ϵ : H1(Ω,R3) → L2(Ω,R3sym×3), ϵ := (∇+∇⊤)/2 denotes the symmetric gradient, C: R3sym×3 → R3sym×3 denotes the symmetric positive-definite elasticity tensor, f : Ω → R3 is an internal body force density, ϕ1: ΓT → R+ is a prescribed gap function, and n˜: ΓT → R3 is a prescribed vector field. For simplicity of presentation, we assume that the displacement boundary conditions are homogeneous (g = 0) in the formulation below.

Notice that K is obtained from the general feasible set (2.1) by choosing V as in (3.9), B = −γ(·) · n˜, Ωd = ΓT, and C(x) = [ϕ1(x),∞). Applying LVPP with the Legendre function (3.4), the resulting saddle-point formulation (2.7) is: for ψ0 = 0, find (uk,ψk) ∈ V × L∞(ΓT) satisfying

= (αkf,v) − (ψk−1,v · n˜)Γ

(αk Cϵ(uk),ϵ(v)) − (ψk,v · n˜)Γ

(3.12a) , (uk · n,w˜ )Γ

T

T

+ (expψk,w)Γ

(3.12b) , for all (v,w) ∈ V × L∞(ΓT), where (·,·)Γ

= (ϕ1,w)Γ

T

T

T

denotes the L2(ΓT)-inner product.

T

As for the obstacle problem in Subsection 3.1, we use equal-order continuous Lagrange spaces for the displacement and latent variable. Note that the spaces arising in (3.12) are defined on manifolds of differing dimensions. This is inherited in the discretization, and hence, the two discrete subspaces are not the same. We use the mixed-dimensional assembly routines in DOLFINx [23, 49] to solve the coupled problem. The discrete problem is solved for a half sphere with a fixed displacement on

9

