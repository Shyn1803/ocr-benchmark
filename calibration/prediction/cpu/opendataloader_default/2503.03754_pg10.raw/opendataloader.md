- [20] P. Skrzypczyk, N. Brunner, and S. Popescu, “Emergence of quantum correlations from nonlocality swapping,” Physical Review Letters, vol. 102, no. 11, p. 110402, 2009.
- [21] A. J. Short, S. Popescu, and N. Gisin, “Entanglement swapping for generalized nonlocal correlations,” Physical Review A—Atomic, Molecular, and Optical Physics, vol. 73, no. 1, p. 012101, 2006.
- [22] J. Barrett, “Information processing in generalized probabilistic theories,” Physical Review A—Atomic, Molecular, and Optical Physics, vol. 75, no. 3, p. 032304, 2007.


# A Proof of Theorem 3

We prove the second part of the theorem first. Take some arbitrary Φ in F2. We can represent a Z-channel source as follows

1 − s 0 sd s(1 − d)

PXY =

where s,d ∈ [0,1]. Let u = fX(0) and v = fX(1) for some u,v ≥ 0. Assume that E[f] = m = (1−s)u+sv. Then u = m1−−svs . One can verify directly that

HΦ(E[f|Y ]) HΦ(f)

g(v,m) :=

(1 − s(1 − d))Φ 1−s 1(1−s−d)u + 1−ssd(1−d)v + s(1 − d)Φ(v) − Φ((1 − s)u + sv) (1 − s)Φ(u) + sΦ(v) − Φ((1 − s)u + sv)

=

(13)

(1 − s(1 − d))Φ m1−−ss(1(1−−dd))v + s(1 − d)Φ(v) − Φ(m) (1 − s)Φ m1−−svs + sΦ(v) − Φ(m)

. (14)

=

Then, we claim that if (10) holds, then g(v,m) is decreasing in v for every fixed m. Therefore, the maximum of g(v,m) would occur when v = 0. This would complete the proof. Taking the partial derivative of log(g(v,m)) with respect to v, we need to show that

sΦ′(v) − sΦ′ m1−−svs (1 − s)Φ m1−−svs + sΦ(v) − Φ(m)

≥

For any t ∈ [0,1], define

s(1 − d)Φ′(v) − s(1 − d)Φ′ m1−−ss(1(1−−dd))v (1 − s(1 − d))Φ m1−−ss(1(1−−dd))v + s(1 − d)Φ(v) − Φ(m)

. (15)

stΦ′(v) − stΦ′ m1−−svtst (1 − st)Φ m1−−svtst + stΦ(v) − Φ(m)

(16)

k(t) =

Φ′(v) − Φ′ m1−−svtst (st1 − 1)Φ m1−−svtst + Φ(v) − st1 Φ(m)

. (17)

=

Then, (15) can be written as k(1) ≥ k(1−d). We would be done if we can show that k(t) is an increasing function. Showing k′(t) ≥ 0 is equivalent with

m − svt 1 − st

(m − v)st 1 − st

m − svt 1 − st

m − svt 1 − st −Φ

1 st2

Φ′

Φ′(v) − Φ′

C(t) = −

+

+ Φ(m)

s(m − v) (1 − st)2

1 − st st

m − svt 1 − st −

m − svt 1 − st

1 st

Φ′′

−

Φ(m) ≥ 0.

Φ(v) +

Φ

Let x1 = v, x2 = m1−−svtst . Then we can compute s from x1 and x2 as follows:

m − x2 t(x1 − x2)

s =

.

10

