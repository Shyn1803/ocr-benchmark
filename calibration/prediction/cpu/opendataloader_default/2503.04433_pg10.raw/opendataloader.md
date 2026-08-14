- Equation (36) is a special form, for the zero structural damping case d = 0, of the following: amq¨ + (ρVb + d)q˙ + ρV2c + e q = 0 (37)

where am is the mass, or inertia, matrix, b is the aerodynamic damping matrix, c is the aerodynamic stiffness matrix, d is the structural damping and e is the stiffness matrix. Now, considering the availability of modal data and assuming that the measured damping is dependent solely on the structure itself, d can be built from the uncoupled modal damping assumption in [52]:

d = ϕ−Tdnϕ−1 for dn = 2ζnωnan (38)

where the subscript n identifies the uncoupled matrix, ωn the natural frequency, ζn the damping ratio and ϕ the mode shape. Hence, Equations (36) and (38) can be combined to assemble Equation (37). Given full knowledge of the wing

geometric characteristics, three properties remain to be defined: Mθ˙, EI, and GJ. Mθ˙ is the unsteady aerodynamics term and it is defined from oscillatory aerodynamics [49]:

Mθ˙ = 2π −

k 2

- 1

- 2 − a + kF a +


- 1

- 2


- 1

- 2 − a + +


G k

- 1

- 2


+ a (39)

where fk is the reduced frequency, a is the ratio between c and the flexural axis position, and F and G are, respectively, the real and imaginary part of Theodorsen’s function, C(fk), such that:

C(fk) = F(fk) + jG(fk) =

H1(2)(fk) H1(2)(fk) + jH1(2)(fk)

(40)

where Hn(2)(fk) are Hankel functions of the second kind and j is the imaginary number. Concerning the bending and torsional stiffness, EI and GJ, let us consider the still air case where b and c are zero.

- Equation (37) then becomes a simple mass-spring-damper system:


# amq¨ + dq˙ + eq˙ = 0 (41)

The natural frequencies can then be easily extracted through eigenanalysis. Hence, by having a set of experimental ωn it is possible to define the EI and GJ of the equivalent system by minimising its squared difference to the experimental ωn. Thus, by using this and the identified ζn for Equation (38), an aeroelastic model can be defined starting from experimental data. To study the system stability, the eigenanalysis of Equation (41) can be solved iteratively with the well-known p-k method [53] to find the divergence and flutter onset speeds. The p-k method is based on the hypothesis that pure harmonic aerodynamics can be used as a good approximation for lightly damped harmonic motions. This allows the computation of the aerodynamic transfer matrix at a complex frequency p = δ ± jk, such that p ≈ jk. In simple terms, the real part, i.e. the damping, is neglected. A widely accepted workflow of the p-k method [49] can be summarised as follow:

- 1. Initiate an estimation, usually the still air value, of p, said p0 = δ ± jk0
- 2. Evaluate the aerodynamics, in our case Mθ˙
- 3. Solve the eigenvalue (λ) problem for Equation (37) and obtain a new set of λ, p1 = δ ± jk1
- 4. Iterate between 2 and 3 until kn ≈ kn−1


From the λ obtained after convergence, it is possible to build ωn, ζn, real(λ) and imag(λ) vs air-speed (U∞) plots, which can be used to graphically portray divergence or flutter speed, whichever is detected first. Particularly, critical speeds are identified for ζn approaching zero or for real(λ) zero crossings, since both cases are interpreted as instability in the system. Particularly, for flutter, only the real(λ) zero crossing condition needs to be satisfied, while for divergence, imag(λ) must be zero.

10

