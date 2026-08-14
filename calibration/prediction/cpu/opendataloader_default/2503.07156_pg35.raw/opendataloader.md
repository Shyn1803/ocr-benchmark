Finally, we deﬁne the nonlinear mapping FM : R3 → R3 as FM(U) := (faM(U) + ε−1QM(U),fbM(U) − ε−1QM(U),fvM).

Note that the functions fνM,ψM,φM are globally Lipschitz and bounded. Therefore, FM is globally Lipschitz, bounded and

FM(U) := (fa(U) + ε−1Q(U),fb(U) − ε−1Q(U),fv(U)), if |U| ≤ M . Given p ∈ (1,+∞), we consider the operator Ap on Xp := (Lp(Ω))3 deﬁned by

D(Ap) = Dp3 (see (2.1)) ApU = (da∆ua,db∆ub,dv∆v) for U ∈ D(Ap),

(A.1)

and the abstract initial value problem

U′(t) = ApU(t) + FM(U(t)), t > 0 , U(0) = Uin := (uina ,uinb ,vin). (A.2) We will solve (A.1),(A.2) and then we will get rid of the truncation. The main in-

gredient is that Ap:D(Ap)⊂Xp → Xp is a sectorial operator ([21], Theorem 3.1.3). Hence it generates in Xp an analytic semigroup denoted (etA

)t≥0 ([21], Chapter 2). Moreover, Ap is closed so that D(Ap), endowed with the graph norm, is a Banach space. D(Ap) being also dense in Xp, the semigroup is strongly continuous, i.e. limt→0 etA

p

U = U, for all U ∈ Xp. Furthermore, there exists Kp > 0 and ωp ∈ R such that (see [21], Proposition 2.1.1)

p

etA L(X

p) ≤ Kpeω

p t , ∀ t ≥ 0 . (A.3)

First step: well-posedness of (A.1),(A.2). Let · p denote the usual norm in Xp. We start proving that (A.1),(A.2) has a unique mild solution, i.e. a unique function U ∈ C([0,∞),Xp) such that

U(t) = etAUin +

t

e(t−s)AFM(U(s))ds , ∀ t ≥ 0 . (A.4)

0

It is easily seen that FM maps Xp into Xp and FM(U) p ≤ FM(0) p+LM U p = LM U p , ∀ U ∈ Xp . (A.5)

Therefore, (A.4) makes sense since, by assumption (2.3), Uin ∈ Xp and, for all U ∈ C([0,∞),Xp) and all t > 0, FM(U(·)) ∈ L1((0,t);Xp). Moreover, the Lipschitz property of FM together with (A.3) and Gronwall’s Lemma gives us the uniqueness of (A.4). The same ingredients give us the continuous dependence of U with respect to Uin. Therefore, it remains to prove the existence of U and that U belongs to C1([0,∞);Xp) ∩ C([0,∞);Dp(A)) for all p ∈ (1,+∞).

Let θ > 0 be such that ωp+θ > 0. The existence is proved using the contraction mapping principle in the space

E := {U ∈ C([0,∞),Xp) : U E = sup t≥0

e−(ω

p+θ)t U(t) p < ∞} ,

that is a Banach space when endowed with the norm U E. Hence, given U ∈ E, we set

t

Φ(U)(t) = etAUin +

e(t−s)AFM(U(s))ds , ∀t ≥ 0 .

0

35

