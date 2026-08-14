# 6 Numerical Computations

In this section, we state numerical computations that show several phenomena discussed in the introduction. In particular, we will observe a suppression of Ostwald ripening, splitting scenarios and instabilities of flat fronts and growing particles. The numerical simulations also support the sharp interface asymptotics, as we get a good agreement between phase field computations and exact solutions of the sharp interface problem. All our numerical simulations are for the quartic potential (2.7) and the interpolation functions (2.8), (2.9) and (2.10), for a fixed value rc ∈ (0,1].

## 6.1 Finite element method

We assume that Ω is a polyhedral domain and let Th be a regular triangulation of Ω into disjoint open simplices. Associated with Th is the piecewise linear finite element space

Sh = {ζ ∈ C0(Ω) : ζ|o ∈ P1(o) ∀o ∈ Th}, where we denote by P1(o) the set of all affine linear functions on o, see [13]. Let (·,·)h be the usual mass lumped L2-inner product on Ω associated with Th, and let πh : C0(Ω) → Sh be the standard interpolation operator. In addition, let τ denote a chosen uniform time step size. Then our finite element approximation of (2.1) is given as follows. Let ϕ0h ∈ Sh, e.g., ϕ0h = πhφ0 if φ0 ∈ C0(Ω). Then, for n ≥ 0, find (ϕnh+1,µnh+1) ∈ Sh × Sh such that

1 τ

(ϕnh+1 − ϕnh,χh)h + (m(ϕnh)∇µnh+1,∇χh)h = (Sε(ϕnh),χh)h ∀χh ∈ Sh, (6.1a) βε(∇ϕnh+1,∇ηh) +

β ε

(ψ′(ϕnh+1),ηh)h − (µnh+1,ηh)h = 0 ∀ηh ∈ Sh. (6.1b) We implemented the scheme (6.1) with the help of the finite element toolbox ALBERTA, see [29]. To increase computational efficiency, we employ adaptive meshes, which have a finer mesh size hf within the diffuse interfacial regions and a coarser mesh size hc away from them. In particular, we use the strategy from [5, 7], and refine an element o if ηo = |maxo |ϕnh|−1| > 0.5, unless it is already of size hf, and similarly coarsen an element o if ηo < 0.1, unless it is already of size hc. For simplicity we assume from now on that Ω = di=1(0,Li) ⊂ Rd, with L1 ≥ L2 ≥ ··· ≥Ld, and then let hf = NLd

, hc = NLd

for two chosen integer parameters Nf > Nc. Here, unless otherwise specified, for the computations with a phase field parameter ε = (2kπ)−1, k ∈ N, we choose Nf = 8Nc = 23+kLd. This ensures that the interfacial regions are accurately resolved, while using a relatively coarser mesh in the pure regions. For the time discretization we choose τ = 10−3, unless stated otherwise.

c

f

The nonlinear system of equations arising at each time level of (6.1) are solved with the help of Newton’s method. The resulting linear systems at each iteration in two spatial dimensions are solved by direct factorization using the package UMFPACK, see [15], and in three spatial dimensions with a V -cycle multigrid solver using a block Gauss–Seidel smoother.

For the initial data φ0 we in general choose a diffuse interface representation of a desired sharp interface, with signed distance function d0 : Ω → R. In particular, unless otherwise stated, we let

d0(x) ε√2

. (6.2) For the definition of S2 in (2.2), recall (2.4), we need to specify K± and L. For

φ0(x) = tanh

convenience, for the numerical simulations to follow, we will define the relations ρ± = K±

2β , 21

