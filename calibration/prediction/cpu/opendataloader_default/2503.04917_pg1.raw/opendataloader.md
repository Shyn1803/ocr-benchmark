arXiv:2503.04917v1 [math.AP] 6 Mar 2025

WAVE DECAY WITH SINGULAR DAMPING

HANS CHRISTIANSON, EMMANUEL SCHENCK, AND MICHAEL TAYLOR

Abstract. We consider the stabilization problem on a manifold with boundary for a wave equation with measure-valued linear damping. For a wide class of measures, containing Dirac masses on hypersurfaces as well as measures with fractal support, we establish an abstract energy decay result.

1. Introduction

In this paper, we consider a damped wave equation with measure-valued damping on a compact Riemannian manifold (Ω, g) with non-empty smooth boundary. If the measure is the Dirac mass on a hypersurface, then this problem has been considered on an interval in [BRT82,JTZ98] and on bounded domains in R2, provided the hypersurface stays away from the boundary. In particular, in [JTZ98], it is shown that generically for curved hypersurfaces, the energy of corresponding solutions decays to 0. However, if the domain is strictly convex, the existence of whispering gallery modes highly concentrated along the boundary [Ral69] shows that the decay rate is not uniform.

In this paper, we develop a functional analysis approach, assuming that the measure has good mapping properties between (generalized) Sobolev spaces. The novelty here is that the class of measures considered here is much wider than restrictions of the Riemannian volume to hypersurfaces (see Section 2). This mapping assumption allows us to prove an abstract energy decay result rather directly, in any dimension n 2.

Let −∆g be the (positive) Laplace-Beltrami operator on Ω. Let dVg denote the Riemannian volume element, and let  ·, · L2(Ω) denote the L2 inner product with respect to dVg, with the convention that it is linear in the ﬁrst argument. Since the boundary of Ω is non-empty, we prescribe Dirichlet boundary conditions to −∆g, so that the domain is

D(−∆g) = H2(Ω) ∩ H01(Ω). Here H01(Ω) is the completion of Cc∞(Ω) with respect to the homogeneous norm u H1 0(Ω) =  ∇u, ∇u 1L/22(Ω) . We observe that the Dirichlet boundary conditions imply that for u ∈ Cc∞(Ω), 0 = u 2H1

0(Ω) =  ∇u, ∇u L2(Ω) ⇔ u is constant, so this is a norm. In fact, we have

u 2H1

0(Ω) =  −∆u, u L2(Ω) λ0 u 2L2(Ω),

1

