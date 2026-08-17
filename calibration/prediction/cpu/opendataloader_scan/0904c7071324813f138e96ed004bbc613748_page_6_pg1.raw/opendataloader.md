If we assume that l ρ ≈ l v then

$$
X (1 +y) 7 lp (24)
$$

In this case the linear approximation to 1 / ( ρ ( r A ) | Δ | r A ) is

$$
lp (1 = y + xJ) _ (25)
$$

Here J is a factor which measures the relative importance of the non-uniformity of the ﬂow to that of density and it is deﬁned as

$$
J = 26
$$

With all terms approximated linearly, the approximation of the damping rate, γ , becomes

$$
T (pi Pe)? Wk 8 p(rA) pi 8pipe 2p; 1+x +Jl (27) pi +pe Ui
$$

If we repeat the analysis for the backward wave we obtain the same expression with a change in the sign in front of x . The ﬁnal expression for the damping rates of the two waves

(forward and backward propagating) using the sinusoidal proﬁle of density and velocity reduces to

$$
Y = Uk 4 R (p; + pe) kvi 8piPe pi =Pe (pi 1+ (28) pi +pe (pi =pe)
$$

The ± sign corresponds to forward and backward propagating waves respectively. When the ﬂow is zero, the second term inside the curly brackets vanishes and we recover the formula of the damping in the static equilibrium (see for example Ruderman & Roberts 2002 ). In the non-static case since we have assumed that l ρ ≈ l v ( l ≈ l   ) the last two terms inside the square brackets are of the same order and we see that the imaginary part of the frequency linearly decreases with the ﬂow for the forward propagating wave and increases for the backward wave. Using the linear approximation to the frequency (Eq. ( 17 )) and damping rate (Eq. ( 28 )) it is straight forward to calculate the damping per period. The results are represented in Fig. 3 (see dashed lines). We see that the analytical approximations agree very well with the full solution based on the calculation of r A and the evaluation of Eq. ( 1 ) and Eq. ( 8 ). Note that the dependence of the damping rate on the spatial variation of the ﬂow across the loop boundary, l   , is present in Eq. ( 28 ). In Fig. 4 we have plotted the results using this expression (see dashed lines). Again, we ﬁnd an excellent agreement between the two curves for both the forward and backward waves.  

For the regime l   l it is possible to derive useful information from the linear approximation.Using the assumption l v   l ρ it is easy to see that the damping rate of the resonance inside the velocity layer (for both the forward and backward waves) is proportional to l   , which means, as we have already anticipated in Sect. 3.1 , that the contribution of this resonance to the total damping tends to zero (damping time tending to inﬁnity) for a purely discontinuous velocity proﬁle. This is the behaviour already found in Fig. 4 for the backward wave. Moreover, we can estimate the total damping of the two regular resonances of

the forward wave (see Fig. 5 ) by adding the individual damping rates. It turns out that the total damping rate for the forward wave is simply

$$
pe Y = 1 8piPe pi Pe (29) Wk pi + pe Wk
$$

This is the asymptotic value for the forward wave when l   tends to zero. Note that this is twice the damping rate of the situation with a very smooth velocity proﬁle (see Eq. ( 28 ) when l     l ) indicating a more e ﬃ cient attenuation (half the damping time).

# 3.3. Beyond the TTTB approximation: full resistive eigenvalue problem

The results of the previous Sections are based on the TT approximation. It is known that without ﬂows this approximation works very well even for thick layers. However it remains to be conﬁrmed whether this assumption is still valid in the presence of ﬂows. For this reason, we go beyond the TTTB approximation. In this case we solve the full problem numerically. We follow the approach of Terradas et al. ( 2006 ). To study the quasimode properties, the eigenvalue problemgiven by Eqs. (1)–(5)in Terradas et al. ( 2006 ), plus the additional terms due to the ﬂow, is solved. A time dependence of the form e i ω t is assumed and the problem is solved numerically using a code based on ﬁnite elements. As boundary conditions we impose that the velocity components are zero for r → ∞ . In practice, the condition is applied at r = r max , and then it is necessary to check that the results do not depend on this parameter. On the other hand, at r = 0 it is imposed that ∂v r /∂ r = 0, i.e., we select the regular solution at the origin, while the rest of the variables are extrapolated. All the variables and the eigenfrequency are assumed to be complex numbers, since we are interested in resonantly damped modes. We include resistivity to avoid the singular behaviour of the ideal MHD equations at the resonances. The resistive eigenvalueproblem is solved and we obtain the real and the imaginary part of the frequency which must be independent of the magnetic Reynolds number that we use in the computations( Poedts & Kerner 1991 ). The results of the calculations for l     l are plotted in Fig. 3

(shown by dots). The agreement with the analytical calculations, using the TTTB approximation, is remarkable. The numerical curves almost overlap with the analytical ones. In Fig. 4 (shown by dots) we represent the damping per period as a function of l   and ﬁnd the same behaviour as in the analytical expression. With these results we are even more conﬁdent about the method used in Sect. 3.1 and about the analytical expressions derived in Sect. 3.2 .  

For the regime l   l the numerical method we are using fails since the thinner the layer (in density or velocity) the larger the Reynolds number required for the damping time to be independent of the dissipation. A method based on the application of the jump conditions at the resonance or resonances, used for example by Tirry et al. ( 1998 ) or Andries et al. ( 2000 ); Andries & Goossens ( 2001 ), is more appropriate but since this is not the main focus of this paper it will not be further investigated here.

# 3.4. The standing wave problem

The results presented in the previous sections correspond to two propagating waves, one propagating in the direction of the ﬂow, ω f + , and the other travelling in the opposite direction, ω f − . In

