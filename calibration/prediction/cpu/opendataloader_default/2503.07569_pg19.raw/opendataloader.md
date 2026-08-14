FUNDAMENTAL SOLUTION AND GAUSSIAN BOUNDS 19

- Step 1: regularizing coeﬃcients of A: We follow [AN24]. Let θ ∈ D(R) a nonnegative function

with

´

R θ(t)dt = 1. For all p ≥ 1, let θp(t) = pθ(pt) be the associated mollifying sequence. We set Ap(t,x) := (θp ⋆ A(·,x))(t), i.e., we mollify the matrix-valued function A in the time variable only. For all p ≥ 1 and t ∈ R, we set

Btp(u,v) := ˆ

Rn

ω−1Ap(t,·)∇xu · ∇xv dω +

![](<2503.07569_pg19_images/imageFile1.png>)

1 p

![](<2503.07569_pg19_images/imageFile2.png>)

u,v 2,ω.

We check easily that min(1/l,ν) u 2H1

ω(Rn) ≤ Re(Btp(u,u)) and Im(Btp(u,u)) ≤ Mν Re(Btp(u,u)). In particular, the quadratic form of Re(Btp(·,·)) is closed. Moreover, we have

![](<2503.07569_pg19_images/imageFile3.png>)

|Btp(u,u) − Bsp(u,u)| ≤ M

dθp dt L1(R) |t − s| ∇xu 22,ω ≤

![](<2503.07569_pg19_images/imageFile4.png>)

pM θ ˙ L1(R) ν |t − s|Re(Btp(u,u)),

![](<2503.07569_pg19_images/imageFile5.png>)

where θ˙ is the derivative of θ. For all p ≥ 1, we set Up(t) := Γp(t,s)f where Γp is the fundamental solution of the parabolic operator associated to the family (Btp)t∈R. Combining [Kat61, Theorem III] with uniqueness in in L2((s,T);Hω1(Rn)) for any T > s, we have for all p ≥ 1, Up : (s,∞) → L2ω(Rn) is strongly diﬀerentiable. Note that Up is a real-valued function by the same argument as we did for U. Since ∇xUp(t) ∈ L2ω(Rn), we have ∂t |Up(t)| ,∇x |Up(t)| ∈ L2ω(Rn) with

∂t |Up(t)| =

∂tUp(t) if Up(t) ≥ 0, −∂tUp(t) if Up(t) < 0,

and ∇x |Up(t)| = ∇xUp(t) if Up(t) ≥ 0,

−∇xUp(t) if Up(t) < 0. Using this, we have

−

d dt

![](<2503.07569_pg19_images/imageFile6.png>)

Up(t) − |Up(t)| ,Up(t) − |Up(t)| 2,ω = −2 ∂t (Up(t) − |Up(t)|) ,Up(t) − |Up(t)| 2,ω

= −4 ∂tUp(t),Up(t) − |Up(t)| 2,ω

= 4ˆ

Rn

ω−1A(t,·)∇xUp(t) · ∇x(Up(t) − |Up(t)|) dω ≥ 0.

Integrating from s to t in this inequality, we see that t  → Up(t) − |Up(t)| 22,ω is a non-increasing function. Since it vanishes at t = s, we have for all t > s, Up(t) = |Up(t)|, that is Γp(t,s)f = |Γp(t,s)f|, hence Γp(t,s) is a nonnegative operator.

- Step 2: passing to the limit: using uniqueness in L2((s,T);Hω1(Rn)) for any T > s combined with the boundedness of (Up)p≥1 in L2((s,T);Hω1(Rn)) provided by the energy equality, it is easy to check that, up to extracting a sub-sequence, (Up)p≥1 converges weakly to U when p → ∞ in L2((s,T);L2ω(Rn)) for any T > s, and therefore U(t) is nonnegative for all t ≥ s.


Combining Caccioppoli inequality in Lemma 4.4, a weighted Sobolev inequality [HKM18, Theorem 15.26] and the Moser’s iteration principle, we have the following L∞-estimate on nonnegative local weak solutions. For a proof, one can follow the classical scheme or see [Ish99, Proposition 2.1] with lower order coeﬃcients equal to zero.

Lemma 6.2. Let (t0,x0) ∈ R1+n and R > 0. If u is is a nonnegative local weak solution of Hu = 0 in a neighborhood of Q2R(t0,x0), then

1/2

1 µ(Q2R(t0,x0))

ˆ

u2 dµ

esssup

u = u L∞(QR(t0,x0)) ≤ B

![](<2503.07569_pg19_images/imageFile7.png>)

Q2R(t0,x0)

QR(t0,x0)

where B = B(n,D,M,ν) > 0 is a constant. The same estimate holds for nonnegative local weak solution of H⋆v = 0.

By combining Lemma 6.2 above, Lemma 6.1 and Proposition 5.12, we obtain the following result.

Proposition 6.3. The operator H admits a nonnegative generalized fundamental solution Γ(t,x;s,y) with, for all t > s, almost everywhere pointwise Gaussian upper bound, that is,

|x−y|2

K0 ωt−s(x) ωt−s(y)

e−k0

(6.4) 0 ≤ Γ(t,x;s,y) ≤

t−s ,

![](<2503.07569_pg19_images/imageFile8.png>)

![](<2503.07569_pg19_images/imageFile9.png>)

![](<2503.07569_pg19_images/imageFile10.png>)

![](<2503.07569_pg19_images/imageFile11.png>)

for almost every (x,y) ∈ R2n, where K0 = K0(n,D,M,ν) > 0 and k0 = k0(M,ν) > 0 are constants.

