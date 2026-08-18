3. We return to the assumptions on σ and F with more details in the next subsection. See Remarks & Examples 3.1 in [ MMM11 ] for a discussion of assumptions about the cross section, and Lemma 6.1 in the same reference for the proof of statements in some cases.

Formally, passing to the limit when ε → 0 in equation ( 1.1 ), we obtain that the limit f 0 is in the kernel of Q which is spanned by the equilibrium F , which means that f 0 = ρ ( t,x ) F ( v ). Thus, it amounts to ﬁnd the equation satisﬁed by the density ρ . This question of approximation of kinetic equations by macroscopic equations has a long history, dating back to the pioneering works of E. Wigner [ WB61 ], A. Bensoussan et al. [ BLP79 ], as well as E.W. Larsen and J.B. Keller [ LK74 ]. Since then, numerous papers have addressed this topic (for further references, see the papers by C. Bardos et al. [ BSS84 ], and P. Degond et al. [ DGP00 ]). The resulting equations fall into two categories, depending on the rate of decrease in velocity of the equilibrium F . It is well-known (see [ DGP00 ] for instance) that when F decreases rapidly for large velocities (such as when F follows a Maxwellian distribution function), the distribution function f ε converges to ρ ( t,x ) F ( v ) as ε goes to 0, for the classical scaling θ ( ε ) = ε 2 , with ρ being the solution of the diﬀusion equation

$$
(DVzp) 0, (1.5)
$$

where

$$
dv.
$$

When F

$$
k F(v) ~ as (1.6)
$$

for some α > 0, the previous diﬀusion matrix D , given by ( 1.5 ) might be inﬁnite. In that case, the diﬀusion limit leading to ( 1.5 ) breaks down, which means that the choice of time scale θ ( ε ) = ε 2 was inappropriate. It has been shown in [ MMM11 ] and [ Mel10 ], using diﬀerent methods and under various assumptions, that in such cases, the appropriate time scale involves the parameter α , which appears in the equilibrium. More speciﬁcally, for θ ( ε ) = ε γ with γ depends on α , the following fractional diﬀusion equation is obtained

$$
(1.7)
$$

where the fractional Laplacian appearing in the previous equation can be deﬁned by the following singular integral γ u ( x ) − u ( y )

$$
u(s) _ u(y) : PV dy . Rd Iz Ca,d yla+7
$$

Let us now discuss in more detail the contexts of the last two references cited. In [ MMM11 ], the authors addressed the problem in the space homogeneous case (that is with σ independent of x ). They prouved that when F satisﬁes ( 1.6 ) and the collision frequency ν satisﬁes

$$
v(v) ~ as
$$

then for α > 0 and β < min( α ;2 − α ), and by taking γ := α − β 1 − β , the scaling θ ( ε ) = ε γ leads to the previous fractional diﬀusion equation. While in [ Mel10 ], the same problem has been addressed but for a cross section which depends on the position variable x but assuming that the collision frequency is bounded, more precisely

$$
v2F(v); (1.8)
$$

i.e. for β = 0 compared to the case of [ MMM11 ], which gives in particular,

$$
V2 . (1.9)
$$

