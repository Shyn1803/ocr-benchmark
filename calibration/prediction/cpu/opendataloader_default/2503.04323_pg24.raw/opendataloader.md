Observe that I : L2 → L2 is a monotone operator as soon as h is a nondecreasing map, since ⟨I(u) − I(v),u − v⟩ =

T

1 k(T)

E (h(ZTu) − h(ZTv))

G(T − t)(ut − vt)dt

0

1 k(T)

E (h(ZTu) − h(ZTv))(ZTu − ZTv) ≥ 0, u,v ∈ L2. Then, applying Fubini’s Theorem we get

=

T

dgt k(t)

(h′(Ztu) − h′(Ztv))(Ztu − Ztv)

, u,v ∈ L2,

⟨III(u) − III(v),u − v⟩ = −E

0

so that the monotonicity of the operator III may not true in general and depends on the dynamics of the endogenous signal g. The particular case where dgt = g′(t)dt with g′ ≥ 0 (i.e., g is a nondecreasing input curve) and h′ is nonincreasing (i.e., the impact function h is concave on the real line) would yield the monotonicity of III, but such assumptions may be too restrictive.

Furthermore, verifying the monotonicity property of the operators II and IV in general is not obvious and depends on the form of the kernel G and its first-argument derivative ∂xG.

Case of one exponential for the impact decay. For this reason, in what follows we assume (i) h to be nondecreasing and we restrict our attention to the exponential Volterra kernel, i.e.,

G(t,s) = {t≥s}ae−b(t−s), t,s ∈ [0,T], a > 0, b ≥ 0, to study the monotonicity property of the operator V := II + IV. In this way, we conveniently use the relation ∂xG(t,s) = −bG(t,s), for 0 ≤ s < t ≤ T, and the fact that k ≡ a. Specifically, by Fubini’s Theorem and straightforward calculus, we get for any u, v ∈ L2

b a ⟨h(Zu) − h(Zv), Zu − Zv⟩

⟨V(u) − V(v),u − v⟩ =

b a ⟨Zuh′(Zu) − Zvh′(Zv),Zu − Zv⟩

+

T

b a

gt(h′(Ztu) − h′(Ztv))(Ztu − Ztv)dt .

E

−

0

Concluding on the nonnegativity of the above quantity in general depends on the endogenous signal g as was the case for III. But if we additionally assume that (ii) g ≡ 0 and (iii) x  → xh′(x) is nondecreasing, then clearly V is monotone, which proves Proposition 2.8.

Case of a sum of exponential time scales for the impact decay. More generally, one may wonder whether we could derive in a similar way sufficient conditions to get the monotonicity property of the operator V:L2 → L2 in the case of a Volterra kernel given by a finite sum of exponentials, i.e.,

n

aie−b

i(t−s), t,s ∈ [0,T], ai > 0, bi ≥ 0, i ∈ {1,···,n}, n ∈ N.

G(t,s) = {t≥s}

i=1

The answer turns out to be negative. Indeed, assume without loss of generality that the mean– reversion speeds (bi)i differ from one another. Then, in this case, k ≡ Ni=1 ai =: A and

n

∂xG(t,s) = −

aibi exp{−bi(t − s)}, 0 ≤ s < t ≤ T.

i=1

For any i = 1,...,n, we also define the Volterra kernels Gi(t,s) = {t≥s}aie−b

i(t−s), so that

G(t,s) = ni=1 Gi(t,s), s,t ∈ [0,T], and ∂xG(t,s) = − ni=1 biGi(t,s), 0 < s < t < T. Considering the initial input curve g ≡ 0, we can write

n

n

Zu =

Zi,u, u ∈ L2.

Giu =:

i=1

i=1

24

