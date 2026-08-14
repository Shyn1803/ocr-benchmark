- 1) Ω(t,t)=id, Ω(t,t0)= Ω(t,s)Ω(s,t0) for all t, s, t0 ∈[τ,∞);
- 2) and for almost all t,s ∈ [τ,∞) it holds that ∂


Ω(t,s) = A(t)Ω(t,s),

![](<2503.09471_pg2_images/imageFile1.png>)

∂t

(3)

∂ ∂s

Ω(t,s) = −A(s)Ω(t,s).

![](<2503.09471_pg2_images/imageFile2.png>)

A non-empty, closed, convex subset K ⊂ H is called a cone, if R+K ⊂ K and K (−K) = {0} hold. A cone K is called generating if any x ∈ H can be written as x = x+ − x− for some x± ∈ K. In a Hilbert space any generating cone is nonﬂat, that is there exists a constant aK > 0, independent on x, such that in the representation x = x+ −x− the vectors x± can be chosen so that

x± ≤ aK x . (4)

The set K∗ = {f ∈ L(H ;R) : f(K) ⊂ R+} ⊂ H ∗ = H is called adjoint cone. If K is generating, then K∗ is normal, i.e., there is a constant bK > 0 such that x ∈ K, y−x ∈ K imply

x ≤ bK y . A cone K is called selfadjoint if K∗ = K. In a Hilbert space any selfadjoint cone is normal [13].

- Deﬁnition 1: Let K be a generating and selfadjoint cone in H . System (1) is called Wazewski [14] with respect to K (also called monotone [15]) if its evolution operator Ω satisﬁes Ω(t,s)K ⊂ K for all t ≥ s ≥ τ.
- Deﬁnition 2: We say that (1) is stable in K if for any ε > 0 and any t0 ≥ τ there is a δ = δ(ε,t0) > 0 such that x0 ∈ Bδ∩K =⇒ x(t;t0,x0) <ε, t ≥t0; if, in addition, the δ can be chosen independent on t0, then (1) is called uniformly stable in K;


asymptotically stable in K if it is stable in K and there is η = η(t0) > 0 such that x0 ∈ Bη ∩ K =⇒ limt→∞ x(t;t0,x0) = 0; if, in addition, η can be chosen independent on t0, then (1) is called uniformly asymptotically stable in K.

If any of the above properties holds with H on the place of K, then we drop ”in K” in their deﬁnitions. Let system (1) be decomposed in two subsystems as follows

x˙i = Aii(t)xi +Aij(t)xj, i = j, i, j = 1,2, (5)

with xi ∈ Hi, Aij ∈ L(Hj,Hi) for i, j = 1,2. Let Ki be a solid selfadjoint cone in Hi, then K = K1 K2 is a solid and selfadjoint cone in H .

Let Ωi ∈ C([τ,∞) × [τ,∞);L(Hi)) denote the evolution operator of the decoupled subsystem

y˙i = Aii(t)yi, yi ∈ Hi, i = 1,2 (6) It can be veriﬁed by deﬁnition that (1), written as (5), is

a Wazewski system for the cone K, if and only if

Ωi(t,s)Ki ⊂ Ki and Aij(t)Kj ⊂ Ki, t ≥ s ≥ τ. (7)

Deﬁnition 3: An operator O ∈ L(Hj;Hi) is called positive, if it satisﬁes OKj ⊂ Ki and it is denoted by O ≥ 0. For the evolution operator Ωi of (6) let αi, βi, γi, δi ∈ C([τ,∞);R>0) be such that

Ωi(t,s) ≤ αi(t)βi(s), t ≥ s ≥ τ, Ωi(t,s) ≤ (γi(t))−1(δi(s))−1, s ≥ t ≥ τ,

(8)

for example we can ﬁx any p ∈ (s,t) and take αi(t) = Ωi(t, p) , βi(s) = Ωi(p,s) due to Ωi(t,s) = Ωi(t, p)Ωi(p,s).

Let qi ∈C([τ,∞);R>0) be suitable weight functions guaranteeing convergence of the next integrals for t ∈ [τ,∞)

φi(t) := γi2(t)

t

gi(t) := βi2(t)

t

∞

qi(s)δi2(s)ds,

∞

qi(s)αi2(s)ds.

(9)

III. MAIN RESULTS

For simplicity and clearness in this work we consider the case of r = 2 interconnected subsystems in (5). An extension for r ∈ N will developed elsewhere. We introduce the following notation for 1 ≤ i = j ≤ 2: linear weighted integral gains for the interconnection (5) are deﬁned as

ωi(t)βi2(t)

πii(t0) = 2sup t≥t0

∞

∞

αi(p)αj(p) Aij(p) ωi(p)

αi(s) Aji(s) βj(s)

dpds,

×

![](<2503.09471_pg2_images/imageFile3.png>)

s

t

(10)

ωi(t)βi2(t)

πji(t0) = 2sup t≥t0

∞

∞

αi(p)αj(p) Aji(p) ωj(p)

αi(s) Aji(s) βj(s)

×

dpds,

![](<2503.09471_pg2_images/imageFile4.png>)

t

s

(11)

where ωi are suitable weight functions, which can help to enable convergence of the integrals. Also for f ∈ C([t0,T];L(Hi)) we introduce the weighted norm

ωi(t) f(t) . (12)

f ωi,T := max

t∈[t0,T]

Theorem 1: Let (1) be a Wazewski system with respect to a selfadjoint solid cone K and written as (5) with r = 2. Let αi,βi,γi,δi be as in (8) and φi,gi,qi,ωi,πij as in (9),(10),(11). If the spectral radius of the matrix Π(t0) ∈ R2×2 deﬁned by the weighted integral gains πij(t0) satisﬁes

rσ(Π(t0)) < 1 (13)

then solutions to (1) satisfy the estimate

t

![](<2503.09471_pg2_images/imageFile5.png>)

q(s) 2h(s,t0)

h(t0,t0) φ(t)

exp −

ds x0 ,

x(t;t0,x0) ≤ 2aK

![](<2503.09471_pg2_images/imageFile6.png>)

![](<2503.09471_pg2_images/imageFile7.png>)

t0

(14) where aK is from (4), q(t) := min{q1(t),q2(t)}, φ(t) := min{φ1(t),φ2(t)} and h(t,t0) := max{h11(t,t0) +

