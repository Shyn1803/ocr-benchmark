# (7) and (9) gives

u(1)n = u(1)n−3 + u(2)n−7 + u(3)n−11 + u(2)n−8 + u(3)n−12

= u(1)n−3 + u(2)n−7 + u(2)n−8 + u(1)n−5 − u(1)n−8

= u(1)n−3 + u(1)n−5 − u(1)n−8 + u(2)n−7 + u(2)n−8 (10) and (6) and (7) gives

u(2)n = u(1)n−1 + u(2)n−6 + u(3)n−10

= u(1)n−1 + u(2)n−6 + u(2)n−5 − u(1)n−6

= u(1)n−1 − u(1)n−6 + u(2)n−5 + u(2)n−6. (11) Finally, (10) and (11) gives

u(1)n =u(1)n−3 + u(1)n−5 − u(1)n−8 + u(1)n−8 − u(1)n−13 + u(2)n−12

+ u(2)n−13 + u(2)n−9 − u(1)n−14 + u(1)n−13 + u(2)n−14

=u(1)n−3 + u(1)n−5 + u(1)n−9 − u(1)n−13 − u14n−1 + u(1)n−5 − u(1)n−8 − u(1)n−10 + u(1)n−13 + u(1)n−6 − u(1)n−9 − u(1)n−11 + u(1)n−14

=u(1)n−3 + 2u(1)n−5 + u(1)n−6 − u(1)n−8 − u(1)n−10 − u(1)n−11

which gives us a universal characteristic polynomial x11−x8−2x6−x5+x3+x+1. However, it factorizes as

x11 −x8 −2x6 −x5 +x3 +x+1 = (x−1)(x4 +x3 +x2 +x+1)(x6 −x3 −x−1), and we can check whether some proper divisor is also a universal characteristic polynomial. Specifically, we can let j ∈ {1,...,13} and set u(3j) = 1 and u(3i) = 0 for i ̸= j. We set the initial values for n = k, as (1) is only defined for n ≥ k. It turns out that u(13i) − u(10i) − u(8i) − u(7i) = 0 for all i ∈ {1,...,13} regardless of j. By Lemma 3.2, we then have u(ni) − un(i−) 3 − un(i−) 5 − un(i−) 6 = 0 for all n ≥ 13 for all i, and since any set of initial values is a linear combination of the ones we have tried out, x6 − x3 − x − 1 is a universal characteristic polynomial on (ξ,I3). Since it is irreducible and ξ is nontrivial, it must be minimal.

As an example of an execution of the flowchart in Algorithm 1, let v = (4,16,{(L2,L3),(R1,R2)}). The subgraph ρ(v) ⊂ σ3 consists of the SCCs

9

