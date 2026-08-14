Let U = (P,S,M), we rewrite the system of equations (9) into the following form:

with

 



∂U ∂t

(t,x) + A(U)(t,x) = G(U)(t,x), (t,x) ∈ [0,T] × ΩR

U(t,x) = UR, (t,x) ∈ [0,T] × ∂ΩR U(0,x) = U0(x). x ∈ ΩR

(10)

A(U)(t,x) = div α⃗p(t,x)

 

  =

- g1(U)
- g2(U)
- g3(U)


G(U) =

γs(x − y)S(t,y)dy S(t,x) ,−D∆M ,

γp(x − y)P(t,y)dy P(t,x) ,div α⃗s(t,x)

ΩR

ΩR

 

 , UR = (0,SR,MR) and U0 = (P0,S0,M0).

mP(H(M) − a1λM) −ma2λMS msS(1 − M) − ηMP

# 2. Existence and uniqueness of solution

Our aim in this section is to prove the existence and uniqueness of solutions for the system outlined in equation (9). We begin by examining the local dynamics through the isolation of the convolution term and leveraging established principles from the theory of semilinear evolution equations. Following this, we integrate insights from the theory of nonlocal balance equations, as elaborated in [21] and [22], to affirm the existence and uniqueness of the solutions for the system mentioned in equation (2). Before proceeding with the existence and uniqueness proofs, we need to define the following spaces.

Let L∞(ΩR) be the space of essentially bounded measurable functions on ΩR, equipped with the norm: ∥f∥L∞(ΩR) = esssupx∈Ω

|f(x)|. Let C(ΩR) be he space of continuous functions on ΩR, with the uniform norm: ∥f∥C(ΩR) = sup

R

|f(x)|.

x∈ΩR

Let Cb1(ΩR) be the space of continuously differentiable functions on ΩR with bounded derivatives, normed by: ∥f∥C1 b(ΩR) = ∥f∥C(ΩR) + ∥∇f∥C(ΩR).

For a Banach space (X,∥.∥X), let C([0,T];X) denote the space of continuous functions from [0,T] to X, with the norm:

∥f∥C([0,T];X) = sup

∥f(t)∥X.

t∈[0,T]

Let L1([0,T];X) be the space of Bochner integrable functions from [0,T] to X, with the norm:

∥f∥L1([0,T];X) =

T

∥f(t)∥Xdt.

0

Let W2,1(ΩR) be the Sobolev space defined as: W2,1(ΩR) = {u ∈ L1(ΩR) : Dαu ∈ L1(ΩR) for all |α| ≤ 2}

2.1. Existence and uniqueness of the solution of the local system

Let wp and ws be two fixed functions belonging to C [0,T],Cb1(Rd) , and let w := (wp,ws). We consider the associated local system to (10) and written as follows:

 

∂Uw ∂t

(t,x) + Aw (Uw)(t,x) = G(Uw)(t,x), (t,x) ∈ [0,T] × ΩR

Uw(t,x) = UR, (t,x) ∈ [0,T] × ∂ΩR U(0,x) = U0(x). x ∈ ΩR



## 4

(11)

