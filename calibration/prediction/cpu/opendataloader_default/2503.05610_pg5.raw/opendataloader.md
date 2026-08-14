# 3.1 Zero Infimum Spacing

The next theorem gives a condition under which the infimum spacing is zero. Here our main result is Theorem 2, where we show that the existence of a nonzero repulsive fixed point of the spectral decimation function with multiplier, larger than the zero fixed point indicates zero infimum spacing in the spectrum.

Theorem 2. Assume ∆ admits spectral decimation with spectral decimation function R and suppose 0,ζ > 0 are fixed point of R with |R′(ζ)| > R′(0) > 1. Then inf{|λ − λ′| : λ ̸= λ′,λ,λ′ ∈ σ(∆)} = 0.

Proof. Let ϕζ be the inverse branch of R with ζ in it’s range. Note that ζ is in the Julia set of R and is an attracting fixed point of ϕζ and hence we may choose n, and x1,x2 ∈ σ(∆n) so that ϕmζ (xj) → ζ,j = 1,2 [HSTZ11]. Therefore, we have,

ϕmζ (x1) − ϕmζ (x2) = (ϕmζ (γm))′ |x1 − x2|

= ϕ′ζ(ϕmζ −1(γm)) ... ϕ′ζ(γm) |x1 − x2|

Note that ϕζ is a continuous injective map and hence monotone. Therefore, it is no loss to assume, ϕkζ(x1) ≤ ϕkζ(γm) ≤ ϕkζ(x2),∀k.

Thus, ϕkζ(γm) − ζ ≤ maxj∈{1,2} ϕkζ(xj) − ζ Hence, by continuity of R′, given δ > 0 there is N so that m ≥ k ≥ N =⇒ R′(ζ) − δ ≤ R′(ϕkζ(γm) . Thus,

1 R′(ϕkζ(γm))

≤ (R′(ζ1)−δ),∀k ≥ N. So for m > N, we have,

1 R′(ϕmζ (γm))

1 R′(ϕζ(γm)) |x1 − x2|

ϕmζ (x1) − ϕmζ (x2) ≤

...

1 (R′(ζ) − δ)m−N

1 R′(ϕNζ (γm))

1

≤

R′(ϕζ(γm))|x1 − x2|. Now note that

...

c∆n+j+mϕj0ϕmζ (x1) − cn∆+j+mϕj0ϕmζ (x2) = cn∆·cj∆ (ϕj0)′(γj) ·cm∆ ϕmζ (x1) − ϕmζ (x2) .

for some γj lying between ϕmζ (x1) and ϕmζ (x2). Choose δ so that R′(0) < R′(ζ) − δ and observe that cm∆ ϕmζ (x1) − ϕmζ (x2) → 0 as m → ∞.

Hence by [Shi96, Proposition 3.1], it remains to show that cj∆ (ϕj0)′(γj) converges to a finite number as j → ∞.

5

