Equation ( 36 ) is a special form, for the zero structural damping case d = 0, of the following:

$$
am9 + (pVb + d) 9 + (37)
$$

where a m is the mass, or inertia, matrix, b is the aerodynamic damping matrix, c is the aerodynamic sti ff ness matrix, d is the structural damping and e is the sti ff ness matrix. Now, considering the availability of modal data and assuming that the measured damping is dependent solely on the structure itself, d can be built from the uncoupled modal damping assumption in [ 52 ]:

$$
(38)
$$

where the subscript n identifies the uncoupled matrix, ω n the natural frequency, ζ n the damping ratio and ϕ the mode shape. Hence, Equations ( 36 ) and ( 38 ) can be combined to assemble Equation ( 37 ). Given full knowledge of the wing geometric characteristics, three properties remain to be defined: M ˙ θ , EI , and GJ . M ˙ θ is the unsteady aerodynamics term and it is defined from oscillatory aerodynamics [ 49 ]:

$$
+kF (a + (39)
$$

where f k is the reduced frequency, a is the ratio between c and the flexural axis position, and F and G are, respectively, the real and imaginary part of Theodorsen’s function, C ( f k ), such that:

$$
(40) jH{2) (fk)
$$

n k Concerning the bending and torsional sti ff ness, EI and GJ , let us consider the still air case where b and c are zero. Equation ( 37 ) then becomes a simple mass-spring-damper system:

$$
(41)
$$

The natural frequencies can then be easily extracted through eigenanalysis. Hence, by having a set of experimental ω n it is possible to define the EI and GJ of the equivalent system by minimising its squared di ff erence to the experimental ω n . Thus, by using this and the identified ζ n for Equation ( 38 ), an aeroelastic model can be defined starting from experimental data. To study the system stability, the eigenanalysis of Equation ( 41 ) can be solved iteratively with the well-known p k method [ 53 ] to find the divergence and flutter onset speeds. The p k method is based on the hypothesis that pure harmonic aerodynamics can be used as a good approximation for lightly damped harmonic motions. This allows the computation of the aerodynamic transfer matrix at a complex frequency p = δ ± jk , such that p ≈ jk . In simple terms, the real part, i.e. the damping, is neglected. A widely accepted workflow of the p k method [ 49 ] can be summarised as follow:

- 1. Initiate an estimation, usually the still air value, of p , said p 0 = δ ± jk 0
- 2. Evaluate the aerodynamics, in our case M ˙ θ
- 3. Solve the eigenvalue ( λ ) problem for Equation ( 37 ) and obtain a new set of λ , p 1 = δ ± jk 1
- 4. Iterate between 2 and 3 until k n ≈ k n − 1


From the λ obtained after convergence, it is possible to build ω n , ζ n , real( λ ) and imag( λ ) vs air-speed ( U ∞ ) plots, which can be used to graphically portray divergence or flutter speed, whichever is detected first. Particularly, critical speeds are identified for ζ n approaching zero or for real( λ ) zero crossings, since both cases are interpreted as instability in the system. Particularly, for flutter, only the real( λ ) zero crossing condition needs to be satisfied, while for divergence, imag( λ ) must be zero.

