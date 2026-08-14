we introduce the PG-VarMiON emulating the optimal Petrov-Galerkin formulation, describe the training procedure, and present an analysis of the generalization error. Numerical results are presented in Section 4 for the diffusion and advection-diffusion equations in one dimension, and the advection-diffusion problem in two dimensions. We end with concluding remarks in Section 5.

# 2 Problem Formulation

Let Ω ∈ Rd be an open, bounded domain with piecewise smooth boundary Γ. The boundary is further split into the Dirichlet boundary ΓD and natural boundary Γη, with Γ = ΓD ∪ Γη. Define the space HDr (Ω) = {u ∈ Hr(Ω) : u Γ

= 0}. We consider the following scalar elliptic boundary value problem

D

L(u(x);g(x)) = f(x) ∀ x ∈ Ω, B(u(x);g(x)) = η(x) ∀ x ∈ Γη,

(2.1)

u(x) = 0 ∀ x ∈ ΓD,

where L is a linear elliptic PDE operator and B is the natural boundary operator, both parametrized by a set of functions g ∈ G. Also, f ∈ F ⊆ L2(Ω) is the source term, and η ∈ H ⊆ L2(Γη). The solution u ∈ V := HDr (Ω), where r depends on the order of the operator L.

A particular example of (2.1) is the steady advection-diffusion equation with −∇ · (κ(x)∇u(x)) + c(x) · ∇u(x) = f(x) ∀ x ∈ Ω, κ(x)∇u(x) · n = η(x) ∀ x ∈ Γη, u(x) = 0 ∀ x ∈ ΓD,

(2.2)

where V = HD1 (Ω), n is the unit outward normal on Γη and the set of parametrizing functions are g = [κ,c]. Here κ ∈ L∞(Ω) ∪ {κ | κ(x) ≥ κmin a.e. x ∈ Ω} for some (fixed) scalar κmin > 0 is the diffusion coefficient, while c ∈ Hdiv1 (Ω) = {c ∈ [L2(Ω)]2 | ∇ · c ∈ L2(Ω)} is the velocity field. We will use (2.2) as a canonical example for the numerical results in Section 4.

## 2.1 Variational form and symmetrization

The variational formulation of (2.1) is given by: find u ∈ V such that a(u,w;g) = (f,w) + (η,w)Γη ∀ w ∈ V, (2.3)

where (.,.) is the L2(Ω) inner-product, (.,.)Γη is the L2(Γη) inner-product, while a(u,w;g) is the associated bilinear form parameterized by g. We also assume that the bilinear form is coercive, which requires additional conditions on g. With this assumption, a unique solution of (2.3) exists, as guaranteed by the Lax-Milgram theorem [10, 9].

For the particular case of the advection-diffusion equation, we have a(u,w;κ,c) := (κ∇u,∇w) + c · ∇u,w (2.4) 4

