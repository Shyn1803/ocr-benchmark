Lemma 3.1. Assume that T ∈ T h and S ∈ S h satisfy ∅   = T ∩ Γ h ⊂ S . Then we have

$$
m Ilvn IlLv(s) € Vh, Vvh
$$

where m = 0 , 1 ,... and 1 ≤ p ≤ ∞ .

We recall from [3, Theorem 5] standard interpolation error estimates for I h :

Lemma 3.2. Assume the embedding Wm,P Co holds for subsets in Then we have RN .

$$
Ilv =
$$

Estimates for ˚ I h are, however, more involved because of domain perturbation ( u = 0 on Γ does not necessarily imply ˜ u = 0 on Γ h ). We state it in the following form, whose proof is similar to that of Proposition 5.1 below (we only have to consider global Ω h and set v 2 = 0 there) and thus omitted here.

Proposition 3.1. Under the assumptions of Lemma 3.2, let m ≥ 2 and v ∈ W m,p ( ˜ Ω) satisfy v = 0 on Γ . Then we have

$$
1/p + TeTh
$$

with the obvious modiﬁcation for p = ∞ .

4 REDUCTION TO WI,1_ANALYSIS OF REGULARIZED GREEN FUNCTION

Fixing arbitrary K ∈ T h and z ∈ K , we try to bound the pointwise error ˜ u ( z ) − u h ( z ). We construct a regularized delta function; the proof is given in the appendix.

Proposition 4.1. For K ∈ T h and z ∈ K , there exists η  ∇ m η   L ∞ ( K ) ≤ Ch − N − m K ( m = 0 , 1) , and

$$
for vh = ôh 0 FK with arbitrary ôh € Pk(Â),
$$

where the constant C is independent of K , z , and h K .

Next we introduce a “dyadic decomposition” of Ω h . We set a sequence of scales:

$$
do = for j = 1,-: log 2 Lh,
$$

where L means the ratio of the “initial stride” d 0 to the “minimum scale” h . As we see later, L will be taken suﬃciently large (but independently of h ). Then we deﬁne a subset Ω h,j of Ω h —which has the scale d j in terms of the distance from K —by

$$
U{T € Tn d(T, K) < do} 2 U{T € Tn Qho Qh.j
$$

where d(T, = are compatible with a standard ball B(z;r) = {z fact, by triangle inequalities; combined with dJ 2 diam (h and diamT < Ch for T € Th, we obtain T')

$$
(2h U (disjoint union) j=0 Qho
$$

$$
=: (j 2 1) ,
$$

where Afs) We also remark 02 that large.

Now let us start the ﬁrst part of the proof of Theorem 1.1. For any v h ∈ ˚ V h we use the regularized delta function η constructed in Proposition 4.1 to get

$$
(ũ =
$$

The ﬁrst two terms on the right-hand side are bounded by C   ˜ u − v h   L ∞ ( K ) . To address the last term we deﬁne a 3 , ∞

$$
9 = 0 on
$$

where η is extended by zero outside supp η ⊂ Ω (this inclusion holds if h is small). We also utilize its ﬁnite element approximation g h ∈ ˚ V h obtained by solving

$$
€ Vh. Vvh
$$

