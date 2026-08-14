4 Improved Adaptive Orthogonal Basis Method for Multiple Solutions with the homogeneous Neumann boundary condition, it is known that u has exactly a single peak (i.e. local maximum of u). Moreover, if the single peak is on the boundary of Ω, then it is located at the point where the mean curvature of the boundary ∂Ω reaches its maximum value. These results have not been numerically verified, which limits the further application of multiple-solution analysis.

The rest of this paper is organized as follows. In section 2, we describe the spectral Legendre–Fourier scheme we used to discretize equation (1.1) defined in an elliptic geometry. The IAOBDM is designed and presented in section 3. In section 4, ample numerical experiments are carried out to demonstrate the efficiency of this method, and to show the effect of varying geometry Ω on multiple solutions of (1.1). Finally, we end the paper with some remarks in section 5.

# 2. A Legendre–Fourier scheme for elliptic equations in an elliptic domain

To numerically study the effect of varying geometry Ω on multiple solutions of (1.1), the first step is to provide an efficient discretization scheme. Here, we adopt a Legendre–Fourier scheme for (1.1) in an elliptic domain. Let

2

2

a2 + y

Ω = (x,y) : x

b2 ≤ 1 . (2.1)

The weak formulation of (1.1) with homogeneous Dirichlet boundary condition and ε = 1 is to find u ∈ H01(Ω) such that

∇u∇vdxdy =

Ω

f(x,u)vdxdy, ∀v ∈ H01(Ω), (2.2)

Ω

where x = (x,y). We use polar transformation x = ar cosθ,y = br sinθ to transform the Dirichlet problem into polar coordinate form:

 

1 r2

1 r

(ω3uθ + ω2uθθ) + f(r,θ,u) = 0, in Ω = (0,1) × [0,2π), u(1,θ) = 0, u periodic in θ,

(ω2ur − ω3urθ) +

ω1urr +



(2.3) where

sin2 θ b2

sin2 θ a2

cos2 θ a2

cos2 θ b2

1 a2 −

1 b2

). (2.4) The corresponding weak formulation (2.2) becomes

ω1 =

+

, ω2 =

+

, ω3 = sin2θ(

L(u,v) :=

+

(ω3uθvr − ω2urv − ω1(urv + rurvr))drdθ

Ω

1 r

fvdrdθ, ∀v ∈ H01(Ω).

uθ(ω3v − ω2vθ)drdθ =

Ω

Ω

(2.5)

Obviously, from (2.3) or (2.5), we can find that a singularity point appears at r = 0, indicating that additional polar conditions should be proposed to obtain the desired solution regularity at

