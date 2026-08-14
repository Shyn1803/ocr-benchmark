for the Dirichlet form associated to sticky Brownian motion. Denoting a0 = 2+1ωL and b0 = ωa0, for all s > 0 we have

f2 dµ = a0(f(0)2 + f(L)2) + b0

L

f2 dx,

0

- ≤ a0(f(0)2 + f(L)2) + b0s

L

0

(f′)2 dx + b0β(s)

L

0

|f|dx

2

,

- ≤ b0s


L

(f′)2 dx + b0 max(b−0 2,a−0 1)β(s) |f|dµ

0

2

.

Therefore the sticky Brownian satisfies a super Poincaré inequality. Then by [Wan00, Th. 5.1], it has an empty essential spectrum. Now, by [BGL14, Th. A.6.4], the resolvent is compact and thus the generator has discrete spectrum.

<table>
  <tr>
    <td> </td>
  </tr>
</table>


Corollary 19. Choosing T = m−1/2, the transition semigroup of the RTP process is exponentially contractive in T-average with rate

ν = Ω

ω 1 + (ωL)2

.

Note that the relaxation time corresponding to this decay rate is of the same order as the mixing time obtained in [GHM24]. It reveals the existence of two regimes controlled by the parameter ωL. In the ballistic regime ωL ≪ 1, velocity flips are rare, leading to a fast exploration of the position space S and a comparatively slow exploration of the velocity space V. This results in the scaling ν ∝ ω. On the contrary, in the diffusive regime ωL ≫ 1, the high frequency of velocity flips makes the exploration of V faster than the exploration of S. This leads to the scaling ν ∝ ω−1L−2.

Proof. We begin by verifying Assumption (A). Recall that Dom(LC0) is a core of L by Theorem 7. For all f ∈ Dom(LC0) we have Lˆv(f ◦ π) = 0 hence Lˆtr is a lift of L by Remark 8. Furthermore, for f ∈ Dom(LC0) one has

Lˆ∗tr(f ◦ π)(x,v) = −v1{0<x<L}f′(x) = −Lˆtr(f ◦ π)(x,v). A straightforward computation yields

Lˆvf(x,v)dκx(v) = 0 for all x ∈ S and f ∈ Dom(Lˆ).

V

Finally, we prove ∥f − Πvf∥2L2(ˆµ) ≤ m1

Ev(f) with mv = 2. Define the matrices

v

 

 , Q =

 

 ,

−2 2 0 1 −2 1 0 2 −2

1/4 0 0 0 1/2 0 0 0 1/4

S =

as well as the scalar product ⟨x,y⟩S = x⊤Sy and let Π be the orthogonal projection on the kernel of Q with respect to ⟨·,·⟩S. The matrix Q is symmetric w.r.t. the scalar

26

