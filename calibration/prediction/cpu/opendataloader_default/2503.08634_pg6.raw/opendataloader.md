- [Case i] The following error bounds hold true for some M > 0.

- (i-1) 0 ≤ E[h(ˆxη)] − h∗ ≤ Errη + ηM.
- (i-2) µ2f E[∥xˆη − x∗∥2] − ∥∇f(x∗)∥E[dist(ˆxη,Xh∗)] ≤ E[f(ˆxη)] − f∗ ≤ η1Errη.

- (i-3) If µf > 0, then E[∥xˆη − x∗∥2] ≤ µ2


f

∥∇f(x∗)∥E[dist(ˆxη,Xh∗)] + η1Errη .

- [Case ii] Suppose Xh∗ is α-weak sharp with order κ ≥ 1. Then, the following holds for some M > 0.

- (ii-1) 0 ≤ E[h(ˆxη)] − h∗ ≤ Errη + ηM.
- (ii-2) µ2f E[∥xˆη − x∗∥2] − ∥∇f(x∗)∥ κ α1 (Errη + ηM) ≤ E[f(ˆxη)] − f∗ ≤ η1Errη.


- (i-3) If µf > 0, then E[∥xˆη − x∗∥2] ≤ µ2

f

∥∇f(x∗)∥ κ α1 (Errη + ηM) + η1Errη . [Case iii] If Xh∗ is α-weak sharp with order κ = 1 and η ≤ 2∥∇fα(x∗)∥, then the following holds.

- (iii-1) 0 ≤ E[h(ˆxη)] − h∗ ≤ 2Errη.
- (iii-2) µ2f E[∥xˆη − x∗∥2] − 2∥∇fα(x∗)∥ Errη ≤ E[f(ˆxη)] − f∗ ≤ η1Errη.

- (iii-3) If µf > 0, then E[∥xˆη − x∗∥2] ≤ ηµ2


f

Errη.

Proof. (i-1) In view of the definition of Errη and fη, we have E[h(ˆxη) + ηf(ˆxη)] − fη∗ ≤ Errη. Also, from the definition of fη∗, we have fη∗ ≤ fη(x∗) = h∗ + ηf∗. From the preceding two relations, we obtain

E[h(ˆxη)] − h∗ + η(E[f(ˆxη)] − f∗) ≤ Errη. (2)

By invoking Assumption 1, we have E[f(ˆxη)] > −∞. Therefore, there exists some M > 0 such that f∗ − E[f(ˆxη)] < M. As a result, we obtain E[h(ˆxη)] − h∗ ≤ Errη + ηM. From xˆη ∈ X, we also have E[h(ˆxη)] − h∗ ≥ 0. This completes the proof of (i-1).

- (i-2) The upper bound holds in view of (2) and that E[h(ˆxη)] − h∗ ≥ 0. To show the lower bound, from the convexity of f, we may write

µf

2 E[∥xˆη − x∗∥2] + ∇f(x∗)⊤E[(ˆxη − x∗)] ≤ E[f(ˆxη)] − f∗,

where the expectation is taken with respect to the random variables generated in the method M. Note that ∇f(x∗)⊤E[(ˆxη − x∗)] is not necessarily nonnegative. We may write

µf

2 E[∥xˆη − x∗∥2] + ∇f(x∗)⊤E[(ˆxη − ΠX∗

h

[ˆxη] + ΠX∗

h

[ˆxη] − x∗)] ≤ E[f(ˆxη)] − f∗.

In view of ΠX∗

h

[ˆxη] ∈ Xh∗, we have ∇f(x∗)⊤E ΠX∗

h

[ˆxη] − x∗ ≥ 0. We obtain

µf

2 E[∥xˆη − x∗∥2] + ∇f(x∗)⊤E x ˆη − ΠX∗

h

[ˆxη] ≤ E[f(ˆxη)] − f∗ Invoking the Cauchy-Schwarz inequality, we obtain

µf

2 E[∥xˆη − x∗∥2] − ∥∇f(x∗)∥ E x ˆη − ΠX∗

h

[ˆxη] ≤ E[f(ˆxη)] − f∗. Invoking the Jensen’s inequality, we obtain

µf

2 E[∥xˆη − x∗∥2] − ∥∇f(x∗)∥E x ˆη − ΠX∗

h

[ˆxη] ≤ E[f(ˆxη)] − f∗.

Noting that E[dist(ˆxη,Xh∗)] = E x ˆη − ΠX∗

h

[ˆxη] , we obtain the lower bound in (i-2).

- (i-3) This result follows directly from (i-2).


- (ii-1) This result is identical to (i-1).




6

