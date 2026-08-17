By isometry we conclude that Hn = F'(Zn) is a Cauchy sequence converging to some H € = Zn = ZI = 0 and therefore I(H) = Z.

Equation ( 3.11 ) is evident in the case that 𝛾 is a simple function. For general 𝛾∈𝐿 𝑡 (𝑋,𝑑 ′ ) , choose a sequence of simple 𝛾 (𝑛) with ‖𝛾 (𝑛) −𝛾‖ 2 →0 . By ( 3.9 ) and It ¯ o’s isometry we have

$$
Y(n)(s) dX(s) = 0 Y(n)(s) dY(s) = Y(s) dY(s)| ~ 0
$$

‖ 0 0 ‖ ‖ 0 0 ‖ as 𝑛→∞ . The claim then follows because the continuity of the operator 𝐼 𝑡 yields

$$
lim I Y(n)(s) dX(s) = lim Y(n)(s) dY(s) n->0 n->0
$$

# 4 Filtering, smoothing, and prediction

This section is devoted to optimal linear filtering, prediction and smoothing of partially observed polynomial processes. We let either I : = N or I : = R+ and fix a probability space = we assume Xa(t) are observable whereas X  (t), Xm(t) are not. We let the subscript 0 stand for the observable part of a vector x € Rd and let H = = Hx = (xm+1, For 2 € we set := ZHT = Z1:d, m+l:d, Zo, = HZHT = Zm+l:d, m+l:d. The subscript u standing for the unobservable part of a vector is treated in the same manner: R+, Rdxd 2:,0

𝔼(‖𝑋(𝑡)‖ 2 )<∞ 𝑡∈𝐼 problem for fixed 𝑡∈𝐼 . The goal is to minimise the mean square error 𝔼(‖𝑋(𝑡) −𝑌‖ 2 ) over all random variables 𝑌 that are measurable with respect to the observable information

$$
=0 Xo(s) s € I, $ <t}) (4.1)
$$

We call the minimiser of ( 4.1 ) the optimal filter for . Regardless of any specific model the optimal filter is then given by the conditional mean

# 4.1 Discrete-time linear filtering problems

Let 𝐼=ℕ . For Gaussian state space models, the optimal filter can be computed recursively:

Proposition 4.1 (Kálmán filter) . Suppose that 𝑋 is a linear Gaussian state space model as in Definition 3.1 and set 𝐶(𝑡) ∶=𝐵(𝑡)𝐵(𝑡) ⊤ . Let ̂ 𝑋(0,−1) ∶=𝔼(𝑋(0)) , ̂ Σ(0,−1) ∶= Cov(𝑋(0)) and

$$

$$

$$
Ê(t + 1,t) := A(t + 1)Ê(t,t)A(t + 1)T + C(t + 1)
$$

