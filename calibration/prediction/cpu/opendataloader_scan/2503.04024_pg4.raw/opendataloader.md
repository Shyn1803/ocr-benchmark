we introduce the PG-VarMiON emulating the optimal Petrov-Galerkin formulation, describe the training procedure, and present an analysis of the generalization error. Numerical results are presented in Section 4 for the diffusion and advection-diffusion equations in one dimension, and the advection-diffusion problem in two dimensions. We end with concluding remarks in Section 5.

# 2 Problem Formulation

Let Ω ∈ R d be an open, bounded domain with piecewise smooth boundary Γ. The boundary is further split into the Dirichlet boundary Γ D and natural boundary Γ η , with Γ = Γ D ∪ Γ η . Define the space H r D (Ω) = { u ∈ H r (Ω) : u   Γ D = 0 } . We consider the following scalar elliptic boundary value problem

$$
(2.1) u(x) = 0
$$

where L is a linear elliptic PDE operator and B is the natural boundary operator, both parametrized by a set of functions g ∈ G . Also, f ∈ F ⊆ L 2 (Ω) is the source term, and η ∈ H ⊆ L 2 (Γ η ). The solution u := H r (Ω), where r depends on the order of the operator .

particular example of (2.1) is the steady advection-diffusion equation with

$$
K(z)Vu(z) n = (2.2) u(2) = 0
$$

Here K € kmin a.e . diffusion coefficient, while c € We will use (2.2) as a canonical example for the numerical results in Section 4.-

# 2.1 Variational form and symmetrization

The variational formulation of (2.1) is given by: find u ∈ V such that

$$
V w € V, (2.3)
$$

Γ η η associated bilinear form parameterized by g . We also assume that the bilinear form is coercive, which requires additional conditions on g . With this assumption, a unique solution of (2.3) exists, as guaranteed by the Lax-Milgram theorem [10, 9].

For the particular case of the advection-diffusion equation, we have

$$
(2.4)
$$

