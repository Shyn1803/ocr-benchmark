and then observing that the canonical function of Y writes as k(x) = λeAx−B|x|, implying τ+−A = τ−A = λδB. The Dirac integration to which (5.25) reduces, produces

kρ(x) = λe(A2−B2)x/2 = λe−θ+θ−x/2. (5.27)

Therefore, the bilateral gamma process can be represented in law as Yt = WTt + (θ− − θ+)t/2 where L(T1) ∼ Γ(λ,θ+θ−/2). This has been known and used at least since Madan et al. (1998).

- Example 10. Subordinated representation of CTSα processes. Madan and Yor (2008) through a series of propositions covering a substantial part of the article, explain how to represent

a CTSα(R) process as a subordinated Brownian motion with drift. Based on the discussion so far, the main Proposition 2 therein trivialize. First of all notice that the assumptions in Theorem 6 are met also in the case of CTSα(R) processes with symmetric spherical part. Namely, assuming λ+ = λ− and letting again A = (θ− − θ+)/2, B = (θ− + θ−)/2, leads to k(x) = x−αeAx−B|x|, so that using the Thorin measure found in Subsection 4.3 we deduce the required density relationship τ+−A(y) = τ−A(y) = λ(y − B)α−1(Γ(α))−11{y≥B}. It then follows from Corollary 6, and with the substitution w = (s − B)√x, that

![](<2503.09574_pg27_images/imageFile1.png>)

kρ(x) =λ

exA2/2 Γ(α)

![](<2503.09574_pg27_images/imageFile2.png>)

∞

B

e−s

2x

![](<2503.09574_pg27_images/imageFile3.png>)

2 (s − B)α−1ds = λ

e(A2−B2)x/2 Γ(α)xα/2

![](<2503.09574_pg27_images/imageFile4.png>)

∞

0

e−w

2

![](<2503.09574_pg27_images/imageFile5.png>)

2 −wB√xwα−1dw

![](<2503.09574_pg27_images/imageFile6.png>)

=λ

e−θ+θ−x/2 xα/2

![](<2503.09574_pg27_images/imageFile7.png>)

H−α

θ+ + θ− 2

![](<2503.09574_pg27_images/imageFile8.png>)

√x (5.28)

![](<2503.09574_pg27_images/imageFile9.png>)

where Ha, a < 0, is the Hermite function, given by

Ha(z) =

1 Γ(−a)

![](<2503.09574_pg27_images/imageFile10.png>)

∞

0

e−x2/2−xzx−a−1dx, z > 0. (5.29)

The corresponding Le´vy density coincides with that determined in Madan and Yor (2008), Proposition 2.

- Example 11. Subordinated representation of generalized-z processes. Let µ ∈ GZDG(R) with Le´vy measure of the form (4.20), i.e. c(±1) = c± > 0, σ(±) = σ > 0 and λ(du) = λ(δ1(du) + δ−1(du)), λ > 0. We can rewrite again k(x) = eAx/σ−B|x|/σ/(1 − e−|x|/σ), A = (c− − c+)/2, B = (c− + c+)/2 so we are under the assumption of Theorem 6. Based on (4.22) and (5.25), integrating term by term the series results in


kρ(x) = λe

∞

= λ

k=0

∞

(k + B)2 2σ2

A2x 2σ2

exp −x

![](<2503.09574_pg27_images/imageFile11.png>)

![](<2503.09574_pg27_images/imageFile12.png>)

k=0

= λ

(k + c+)(k + c−) 2σ2

exp −x

![](<2503.09574_pg27_images/imageFile13.png>)

∞

k2 + 2Bk + B2 − A2 2σ2

exp −x

![](<2503.09574_pg27_images/imageFile14.png>)

k=0

. (5.30)

The subordinator is then of the form of an inﬁnite GGC convolution of gamma processes Gk = (Gkt )t≥0, k ≥ 0, L(Gk1) ∼ Γ λ, (k+c+2)(σ2k+c−) whose limit in law is not otherwise known.

![](<2503.09574_pg27_images/imageFile15.png>)

27

