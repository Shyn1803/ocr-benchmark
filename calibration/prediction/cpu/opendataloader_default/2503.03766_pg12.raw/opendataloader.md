Now, we prove that Ψc \{(0,m) : m ≥ c} ⊂ Ψ∗c. For any 0 < p ≤ 1, consider any (p,m) ∈ Ψc and the following probability mass function for a random variable T:

Pr{T = 0} = 1 − p and Pr{T = m/p} = p.

Since m ≥ cp, we have m/p ≥ c, and so

Pr{T ≥ c} = Pr{T = m/p} = p,

and E[T] = p(m/p) = m. Therefore, (p,m) is achieved by the random variable T as constructed. Note that unless m = cp, (p,m) can always be achieved by more than one probability distribution.

It remains to prove that every ordered pair (0,m) with 0 ≤ m < c is achievable. This can be done by noting that such an ordered pair can be achieved by any random variable T with Pr{T = m} = 1. The theorem is proved. □

The region Ψc is defined by Markov’s inequality together with the constraint 0 ≤ p ≤ 1 which comes from the setup of the problem, and we have shown that for any fixed c > 0, every ordered pair in Ψc except for a region with Lebesgue measure 0 (namely the region {(0,m) : m ≥ c}) is achievable by some random variable T. Specifically:

- • When Pr{T ≥ c} > 0, Markov’s inequality, namely

E[T] ≥ c · Pr{T ≥ c}, (10)

which gives a lower bound on E[T], is the only constraint on E[T] in terms of Pr{T ≥ c}.

- • When Pr{T ≥ c} = 0, Markov’s inequality as in (10), which becomes E[T] ≥ 0, continues to be valid. However, we also have


E[T] < c. (11)

Combining (10) and (11), we have

0 ≤ E[T] < c.

11

