Let the function µr(t) be:

µr(t) =

t

λr(v)dv = (1 + r

0

γ ρ

) ln(1 + ρ t). (A.3)

It can be seen from Eq. (A.3) that µ′r(t) = λr(t) and µr(0) = 0 ∀r ≥ 0. We now define the auxiliary function

γ ρ

µ∆(t) = µr+1(t) − µr(t) =

ln(1 + ρ t), (A.4)

which does not depend on r. Note that µ∆(0) = 0. It is a fact that the following equality holds:

(γρ + r ) r + 1

t

λr(x) eµ

∆(x) (eµ

∆(x) − 1)r dx =

0

(eµ

∆(t) − 1)r+1. (A.5)

The proof can be done by differentiating the right side of Eq. (A.5) to show it’s indeed a primitive of the left side’s integrand. Since the functions are also equal on t = 0, fundamental theorem of calculus yields that the equalty is valid for every t.

Considering the initial condition P0(0) = 1 (the beginning population is 0), the probability mass functions are given by:

Γ(γρ + r) r! Γ(γρ)

Pr(t) =

e−(µ

r(t)−µ0(0)) (eµ

∆(t) − 1)r. (A.6)

This is demonstrated by induction over r, using Eq. (A.6) as inductive hypothesis and P0(t) from Eq. (A.1). In fact,

t

e−(µ

r+1(t)−µr+1(x))λr(x)Pr(x)dx

Pr+1(t) =

0

Γ(γρ + r) r! Γ(γρ)

t

e−(µ

r+1(t)−µ0(0))

λr(x)eµ

∆(x)(eµ

∆(x) − 1)r(x)dx

=

0

Γ(γρ + r) r! Γ(γρ)

r+1(t)−µ0(0)) (γρ + r ) r + 1

e−(µ

(eµ

∆(t) − 1)r+1.

=

We can rewrite Eq. (A.6) as:

Γ(γρ + r) r! Γ(γρ)

e−(µ

Pr(t) =

r(t)−µ0(0)−rµ∆(t)) (1 − e−µ

∆(t))r. (A.7)

25

