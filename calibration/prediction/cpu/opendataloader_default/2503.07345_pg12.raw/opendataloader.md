12 J. LUHRMANN,¨ W. SCHLAG, AND S. SHAHSHAHANI

Proof. These operators are limit point at both end points r = 0, and r = ∞. Indeed, any solution of Lf = 0 or Ljf = 0 is asymptotic to a linear combination of r32,r−12 as r → 0+, so no boundary condition is needed at r = 0. The other endpoint r = ∞ is standard, see [53, Theorem X.8]. The claim about essential self-adjointness is [53, Theorem X.7]. See [30, Section 4] for the Bessel operator L0 and its domain. The Kato-Rellich theorem applies to L,L1,L2, which are relatively bounded perturbations of L0, see [17, Section 1.4] (in fact, these operators are perturbations of L0 by bounded operators). The Weyl criterium, see [54, Theorem XIII.14], implies that specess(L0) = specess(L1) = [0,∞). If λ ∈ spec(L1) for some λ < 0, then there exists a ground state of negative energy, i.e., L1ϕ = λ0ϕ for some λ0 < 0 and ϕ ∈ D with ϕ > 0 (in fact, ϕ is smooth and ϕ(r) ∼ cr32 as r → 0+ for some constant c). Let χ(r) = 1 for 0 ≤ r ≤ 1, χ ∈ C∞([0,∞)) with compact support, and set χb(r) = χ(r/b) with b ≥ 1. Then

⟨L1ϕ,χb(r)r12ρ1⟩ = λ0⟨ϕ,χb(r)r21ρ1⟩ Integrating by parts on the left-hand side and sending b → ∞ now leads to a contradiction because of the vanishing L1(r12ρ1) = 0. Hence L1 > 0 as stated (note that L1 cannot have a zero energy eigenfunction because the unique 0-energy solution is not in X0). Pure a.c. spectrum is a consequence of the construction of the Weyl, Titchmarsh m-function for these operators, see [30,40].

The essential spectrum of L2 follows from the Weyl criterium as before. Since L2 = L1 +2ρ21 > 0, we conclude that the discrete spectrum of L2 – if it exists – is strictly positive. □ Remark 2.3. The exact value of c0 > 0 is not known, but the approximate value c0 ≈ 1.3326 is obtained in [51] via a numerically assisted argument. Moreover, [51] shows that L2 has infinitely many eigenvalues in (c0,2) and that 2 is a resonance.

Next, we determine the spectrum of iL and define the evolution etL using the Hille-Yosida theorem. As we do not have a selfadjoint reference operator available as required for the standard version of Weyl’s theorem as in [54, Theorem XIII.14], we need to proceed differently. To this end we first obtain a proper understanding of the resolvent (iL0 − z)−1 of the free operator

0 −∂r2 + 43r2 − −∂r2 + 43r2 + 2 0

L0 :=

.

Let p˜+(ζ) denote the modified Hankel function

p˜+(ζ) := ζH1(1)(ζ) = ζ J1(ζ) + iY1(ζ) , and let q˜+(ζ) denote the modified Bessel function

q˜+(ζ) := ζJ1(ζ).

Here H1(1), J1, and Y1 denote the order one Hankel function, Bessel function of the first kind, and Bessel function of the second kind respectively. p˜+ and q˜+ satisfy the ODE

d2 dζ2

d2 dζ2

- 3

- 4ζ2


- 3

- 4ζ2


−

p˜+(ζ) = p˜+(ζ), −

q˜+(ζ) = q˜+(ζ). Then by direct inspection, the vectors

p˜+(ζ) +

q˜+(ζ) +

ψ˜1(r,z) :=

ψ˜3(r,z) :=

ik1(z)2 z p˜+(k1(z)r) p˜+(k1(z)r)

ik1(z)2 z q˜+(k1(z)r) q˜+(k1(z)r)

, ψ˜2(r,z) :=

, ψ˜4(r,z) :=

ik2(z)2 z p˜+(k2(z)r) p˜+(k2(z)r)

ik2(z)2 z q˜+(k2(z)r) q˜+(k2(z)r)

,

,

