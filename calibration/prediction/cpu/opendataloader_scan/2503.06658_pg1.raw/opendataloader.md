# Firstand Half-order Schemes for Regime Switching Stochastic Diﬀerential Equation with Non-diﬀerentiable Drift Coeﬃcient

Indian Institute of Technology Roorkee, Haridwar, 247667, India

# Abstract

An explicit ﬁrst-order drift-randomized Milstein scheme for a regime switching stochastic diﬀerential equation is proposed and its bi-stability and rate of strong convergence are investigated for a non-diﬀerentiable drift coeﬃcient. Precisely, drift is Lipschitz continuous while diﬀusion along with its derivative is Lipschitz continuous. Further, we explore the signiﬁcance of evaluating Brownian trajectories at every switching time of the underlying Markov chain in achieving the convergence rate 1 . 0 of the proposed scheme. In this context, possible variants of the scheme, namely modiﬁed randomized and reduced randomized schemes, are considered and their convergence rates are shown to be 1 / 2. Numerical experiments are performed to illustrate the convergence rates of these schemes along with their corresponding non-randomized versions. Further, it is illustrated that the half-order non-randomized reduced and modiﬁed schemes outperforms the classical Euler scheme.

Keywords: Randomized Milstein scheme, SDEs with Markovian switching, Bi-stability, Firstand Half-order schemes, Rate of Convergence. 2020 MSC: 60H35, 65L20, 60H10, 65C30, 60J60.

2020 MSC: 60H35 , 65L20, 6OH10, 65C3o, 60J60.

# Introduction

Let ( ˜ Ω , ˜ F , ˜ P ) be a complete probability space. Consider a ˜ d − dimensional standard Brownian motion B := { B ( t ) } t ≥ 0 with natural ﬁltration ˜ F B := { ˜ F B t } t ≥ 0 . Further, assume that r := { r ( t ) } t ≥ 0 is a Markov chain with ﬁnite state space S := { 1 ,...,m ′ } and generator Q := ( q j 0 k 0 ) j 0 ,k 0 ∈ S where q j 0 k 0 ≥ 0 for j 0   = k 0 and q j 0 j 0 = −   k 0   = j 0 q j 0 k 0 which implies that the transition probability matrix of r is given by,

$$
= kolr(t) = jo) = qjoko A + 0(4), ko # jo, 1 + qjojoA + 0(4), ko = jo,
$$

for any t ≥ 0, j 0 ,k 0 ∈ S and ∆ > 0. The natural ﬁltration of r is denoted by ˜ F r := { ˜ F r t } t ≥ 0 . Also, consider an ˜ F B 0 -measurable random variable X 0 and assume that r , B and X 0 are independent. Deﬁne ˜ F := { ˜ F t } t ≥ 0 where ˜ F t := ˜ F B t ∨ ˜ F r t for t ≥ 0. For a ﬁxed T > 0, let b : [0 ,T ] × R d × S  → R d and σ : [0 ,T ] × R d × S  → R d × ˜ d be Borel measurable functions.

Consider the following d − dimensional regime switching stochastic diﬀerential equation, also referred to as stochastic diﬀerential equation with Markovian switching (SDEwMS),

$$
X(t) = Xo + b(s, X(s);r(s))ds +
$$

∗ Corresponding author Email addresses:

dvashistha@ma.iitr.ac.in (Divyanshu Vashistha), chaman.kumar@ma.iitr.ac.in (Chaman Kumar)

