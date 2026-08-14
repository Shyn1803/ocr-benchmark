First- and Half-order Schemes for Regime Switching Stochastic Diﬀerential Equation with Non-diﬀerentiable Drift Coeﬃcient

Divyanshu Vashistha, Chaman Kumar∗

Indian Institute of Technology Roorkee, Haridwar, 247667, India

arXiv:2503.06658v1 [math.PR] 9 Mar 2025

![](<2503.06658_pg1_images/imageFile1.png>)

Abstract

An explicit ﬁrst-order drift-randomized Milstein scheme for a regime switching stochastic diﬀerential equation is proposed and its bi-stability and rate of strong convergence are investigated for a non-diﬀerentiable drift coeﬃcient. Precisely, drift is Lipschitz continuous while diﬀusion along with its derivative is Lipschitz continuous. Further, we explore the signiﬁcance of evaluating Brownian trajectories at every switching time of the underlying Markov chain in achieving the convergence rate 1.0 of the proposed scheme. In this context, possible variants of the scheme, namely modiﬁed randomized and reduced randomized schemes, are considered and their convergence rates are shown to be 1/2. Numerical experiments are performed to illustrate the convergence rates of these schemes along with their corresponding non-randomized versions. Further, it is illustrated that the half-order non-randomized reduced and modiﬁed schemes outperforms the classical Euler scheme.

Keywords: Randomized Milstein scheme, SDEs with Markovian switching, Bi-stability, First- and Half-order schemes, Rate of Convergence. 2020 MSC: 60H35, 65L20, 60H10, 65C30, 60J60.

![](<2503.06658_pg1_images/imageFile2.png>)

1. Introduction Let (Ω˜,F˜,P˜) be a complete probability space. Consider a d˜−dimensional standard Brownian motion

B := {B(t)}t≥0 with natural ﬁltration F˜B := {F˜tB}t≥0. Further, assume that r := {r(t)}t≥0 is a Markov chain with ﬁnite state space S := {1,...,m′} and generator Q := (qj

0k0 ≥ 0 for j0 = k0 and qj

0k0)j

0,k0∈S where qj

0k0 which implies that the transition probability matrix of r is given by,

0j0 = −

qj

k0 =j0

P˜(r(t + ∆) = k0|r(t) = j0) =

0k0∆ + o(∆), k0 = j0, 1 + qj

qj

0j0∆ + o(∆), k0 = j0,

for any t ≥ 0, j0,k0 ∈ S and ∆ > 0. The natural ﬁltration of r is denoted by F˜r := {F˜tr}t≥0. Also, consider an F˜0B-measurable random variable X0 and assume that r, B and X0 are independent. Deﬁne F˜ := {F˜t}t≥0 where F˜t := F˜tB ∨ F˜tr for t ≥ 0. For a ﬁxed T > 0, let b : [0,T] × Rd × S  → Rd and σ : [0,T] × Rd × S  → Rd×d˜ be Borel measurable functions.

Consider the following d−dimensional regime switching stochastic diﬀerential equation, also referred to as stochastic diﬀerential equation with Markovian switching (SDEwMS),

X(t) = X0 +

d˜

t

b(s,X(s),r(s))ds +

0

ℓ=1

t

σℓ(s,X(s),r(s))dBℓ(s) (1)

0

![](<2503.06658_pg1_images/imageFile3.png>)

∗Corresponding author Email addresses: dvashistha@ma.iitr.ac.in (Divyanshu Vashistha), chaman.kumar@ma.iitr.ac.in (Chaman Kumar)

