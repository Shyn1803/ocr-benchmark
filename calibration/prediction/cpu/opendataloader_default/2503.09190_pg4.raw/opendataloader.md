L∞-ERROR ESTIMATE FOR ISOPARAMETRIC FEM 4

- Lemma 3.1. Assume that T ∈ Th and S ∈ Sh satisfy ∅ = T ∩ Γh ⊂ S. Then we have

 ∇m(vh − ˚Ihvh) Lp(T) ≤ ChT1/p−m vh Lp(S) ∀vh ∈ Vh, where m = 0,1,... and 1 ≤ p ≤ ∞.

We recall from [3, Theorem 5] standard interpolation error estimates for Ih:

- Lemma 3.2. Let l,m ∈ N satisfy 0 ≤ l ≤ m ≤ k + 1 and p ∈ [1,∞]. Assume the embedding Wm,p ֒→ C0 holds for subsets in RN. Then we have


v − Ihv Wl,p(T) ≤ Chm−l v Wm,p(T) (T ∈ Th, v ∈ Wm,p(T)).

Estimates for ˚Ih are, however, more involved because of domain perturbation (u = 0 on Γ does not necessarily imply u˜ = 0 on Γh). We state it in the following form, whose proof is similar to that of Proposition 5.1 below (we only have to consider global Ωh and set v2 = 0 there) and thus omitted here.

- Proposition 3.1. Under the assumptions of Lemma 3.2, let m ≥ 2 and v ∈ Wm,p(Ω)˜ satisfy v = 0 on Γ. Then we have

T∈Th

 ∇l(v − ˚Ihv) pLp(T)

1/p

≤ Chm−l v Wm,p(Ωh) + Chk+1−l ∇2v Lp(Γ(δ)), with the obvious modiﬁcation for p = ∞.

4. Reduction to W1,1-analysis of a regularized Green function

Fixing arbitrary K ∈ Th and z ∈ K, we try to bound the pointwise error u˜(z)−uh(z). We construct a regularized delta function; the proof is given in the appendix.

- Proposition 4.1. For K ∈ Th and z ∈ K, there exists η = ηK,z ∈ C0∞(K) such that dist(suppη,∂K) ≥ ChK,  ∇mη L∞(K) ≤ ChK−N−m (m = 0,1), and


(vh,η)K = vh(z) for vh = vˆh ◦ FK−1 with arbitrary vˆh ∈ Pk(Tˆ), where the constant C is independent of K, z, and hK.

Next we introduce a “dyadic decomposition” of Ωh. We set a sequence of scales: d0 = Lh, dj = 2jd0 for j = 1,...,J :=

log(diamΩh/d0) log 2

,

![](<2503.09190_pg4_images/imageFile1.png>)

where L means the ratio of the “initial stride” d0 to the “minimum scale” h. As we see later, L will be taken suﬃciently large (but independently of h). Then we deﬁne a subset Ωh,j of Ωh—which has the scale dj in terms of the distance from K—by

Ωh0 = {T ∈ Th | d(T,K) ≤ d0}, Ωh,j = {T ∈ Th | dj−1 < d(T,K) ≤ dj} (j = 1,...,J),

where d(T,T′) = min{|x−x′| | x ∈ T,x′ ∈ T′} denotes a distance function between two elements T,T′ ∈ Th. They are compatible with a standard ball B(z;r) = {x | |x − z| ≤ r} and annulus A(z;r,R) = {x | r ≤ |x − z| ≤ R}. In fact, by triangle inequalities, combined with dJ ≥ diamΩh and diamT ≤ Ch for T ∈ Th, we obtain

J

Ωh,j (disjoint union), Ωh0 ⊂ Ωh ∩ B(z;2d0),

Ωh =

j=0

Ωh,j ⊂ Ωh ∩ A(js) ⊂ Ωh,j−1 ∪ Ωh,j ∪ Ωh,j+1 =: Ω′h,j (j ≥ 1),

where A(js) := A(z;(1 − s2)dj−1,(1 + s)dj) for all s ∈ (0,1), provided that L is suﬃciently large. We also remark that ℓ

![](<2503.09190_pg4_images/imageFile2.png>)

j=ℓ1 dαj is bounded by Cdαℓ

if α < 0, by C|log d0| if α = 0, and by Cdαℓ

if α > 0, for 0 ≤ ℓ1 ≤ ℓ2 ≤ J.

2

1

2

Now let us start the ﬁrst part of the proof of Theorem 1.1. For any vh ∈ V˚h we use the regularized delta function η constructed in Proposition 4.1 to get

(˜u − uh)(z) = (˜u − vh)(z) + (vh − u,η˜ )Ω

+ (˜u − uh,η)Ω

.

h

h

The ﬁrst two terms on the right-hand side are bounded by C u ˜ − vh L∞(K). To address the last term we deﬁne a regularized Green function g ∈ W3,∞(Ω) by solving

−∆g = η in Ω, g = 0 on Γ, where η is extended by zero outside suppη ⊂ Ω (this inclusion holds if h is small). We also utilize its ﬁnite element approximation gh ∈ V˚h obtained by solving

h ∀vh ∈ V˚h.

ah(vh,gh) = (∇vh,∇gh)Ω

= (vh,η)Ω

h

