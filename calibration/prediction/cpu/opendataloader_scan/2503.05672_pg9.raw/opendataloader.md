The LVPP saddle point subproblem (3.6) can be discretized with many other techniques. We also provide results where the subproblem (3.6) is discretized with a coefficient-based Zernike sparse spectral method [ 39 , 109 , 130 , 106 ] and a five-point stencil finite difference method. For the finite difference scheme, we change the domain to the square Ω = ( − 1 , 1) 2 . Here, we again use the double-exponential update rule (3.8) for α k . We terminate once ∥ u k − u k − 1 ∥ ℓ 2 < 10 − 9 where u k is the discrete coefficient vector for u at iteration k . The results are provided in Figure 2c where we observe h and p -independent iteration counts for the proximal finite difference and spectral methods, respectively. Further numerical experiments with the obstacle problem can be found in [ 85 , 62 , 108 ].

3.2. Example 2: The Signorini problem. We now consider the classical Signorini problem. This problem demonstrates for the first time an extension of LVPP to pointwise bound constraints acting solely on the boundary of a computational domain Ω ⊂ R 3 . In this problem, we separate the boundary ∂ Ω = Γ D ∪ Γ T into disjoint measurable subsets for imposing displacement and traction boundary conditions.

The Signorini problem, posed by Signorini in 1959 [ 123 ] and analyzed by Fichera in 1963 [ 59 ], is the essential first problem in contact mechanics. It models the deformation of a linear elastic body in the presence of a contact boundary constraint. The problem is posed on

$$
(3.9)
$$

and involves the minimization of the strain energy function

$$
(3.10) J(u) = Jf udz
$$

over the feasible set

$$
(3.11)
$$

VT)/2 denotes the symmetric gradient, C: sym is an internal body density; 01 : FT is a prescribed gap function; and For simplicity of presentation; we assume that the displacement   boundary conditions are homogeneous (g = 0) in the formulation below_ R3x3 R3x3 force

Notice that K is obtained from the general feasible set (2.1) by choosing V as in (3.9) , B = − γ ( · ) · ˜ n , Ω d = Γ T , and C ( x ) = [ ϕ 1 ( x ) , ∞ ). Applying LVPP with the Legendre function (3.4) , the resulting saddle-point formulation (2.7) is: for ψ 0 = 0, find ( u k ,ψ k ) ∈ V × L ∞ (Γ T ) satisfying

$$
(3.12a) u
$$

$$
(3.12b) (uk (exp%k , w)Fr (01, w)Fr ,
$$

∈ × T · · Γ T T As for the obstacle problem in Subsection 3.1 , we use equal-order continuous Lagrange spaces for the displacement and latent variable. Note that the spaces arising in (3.12) are defined on manifolds of differing dimensions. This is inherited in the discretization, and hence, the two discrete subspaces are not the same. We use the mixed-dimensional assembly routines in DOLFINx [ 23 , 49 ] to solve the coupled problem. The discrete problem is solved for a half sphere with a fixed displacement on

