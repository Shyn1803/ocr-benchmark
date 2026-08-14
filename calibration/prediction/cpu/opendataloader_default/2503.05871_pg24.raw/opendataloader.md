Φ(t,x,y), and pressure perturbation δP(t,x,y), viz.

- ux = U(y) + ∂yΦ(t,x,y), (A.2)
- uy = 0 − ∂xΦ(t,x,y), (A.3)
- uz = 0, (A.4) P = −2νρx + δP(t,x,y), (A.5)


where U(y) = 1 − y2. The perturbed flow is incompressible, ∇⃗ · ⃗u = 0, and we impose no-slip boundary conditions Φ(t,±1) = ∂yΦ(t,±1) = 0. In order to correctly account for energy in the system we work to second order in perturbation theory,

δP = ϵP(1)(t,x,y) + ϵ2P(2)(t,x,y) + O(ϵ)3 (A.6) Φ = ϵΦ(1)(t,x,y) + ϵ2Φ(2)(t,x,y) + O(ϵ)3, (A.7)

where ϵ is a formal parameter counting orders in the expansion. Let us consider each order in turn.

At O(ϵ) we take a real perturbation formed as follows: Φ(1)(t,x,y) = ϕ(t,y)eiαx + ϕ(t,y)e−iαx (A.8)

with wavenumber α ̸= 0. P(1) is determined algebraically by the x-component of (A.1) at order ϵ. The y component of (A.1), after inserting P(1), gives the Orr-Sommerfeld equation (2.1), where the Orr-Sommerfeld operator is

OOS = −∆−2 1 (iαRe)−1∆22 − U(y)∆2 + U′′(y) , (A.9)

with Reynolds number Re = ν−1, and where ∆2 = ∂y2 − α2 is the spatial Laplacian for the x,y-plane.

At O(ϵ)2 we have perturbations sourced by O(ϵ) terms. These take the form, Φ(2)(t,x,y) = δϕ0(t,y) +

δϕ±α(t,y)e±i2αx. (A.10)

±

The zero-momentum piece ∂yδϕ0 obeys the following diffusion equation,

∂t − ν∂y2 ∂yδϕ0 = iα∂y ϕ∂yϕ − ϕ∂yϕ , (A.11) with viscosity ν serving as the diffusivity, and a current source term coming from the O(ϵ) perturbations. P(2), δϕ±α(t,y) are determined by other differential equations but we will not need them here.

To O(ϵ)2 the energy of the perturbed flow evaluates to

E =

1

dy dxu · u = volx

−1

16 15

+ 2ϵ2

+ 2ϵ2

1

|∂yϕ|2 + α2|ϕ|2 dy (A.12)

−1

1

(1 − y2)∂yδϕ0 dy + O(ϵ)3 . (A.13)

−1

– 23 –

