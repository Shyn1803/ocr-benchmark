Finally, we deﬁne the nonlinear mapping F M : R 3 → R 3 as

$$

$$

Note that the functions f M ν ,ψ M ,φ M are globally Lipschitz and bounded. Therefore, F M is globally Lipschitz, bounded and

Given consider the operator Ap on p € we

$$
if JU| < M .
$$

$$
(see (2.1)) (A.l) for U € D(Ap) ,
$$

and the abstract initial value problem

$$
t > 0 , U(0) = Uin (A.2)
$$

We will solve ( A.1 ),( A.2 ) and then we will get rid of the truncation. The main ingredient is that A p : D ( A p ) ⊂ X p → X p is a sectorial operator ([ 21 ], Theorem 3.1.3). Hence it generates in X p an analytic semigroup denoted ( e tA p ) t ≥ 0 ([ 21 ], Chapter 2). Moreover, A p is closed so that D ( A p ), endowed with the graph norm, is a Banach space. D ( A p ) being also dense in X p , the semigroup is strongly continuous, i.e. lim t → 0 e tA p U = U , for all U ∈ X p . Furthermore, there exists K p > 0 and ω p ∈ R such that (see [ 21 ], Proposition 2.1.1)

$$
< Kpe"p (A.3) 'IlL(xp)
$$

First step: well-posedness of ( A.1 ) , ( A.2 ). Let   ·   p denote the usual norm in X p . We start proving that ( A.1 ),( A.2 ) has a unique mild solution, i.e. a unique function U ∈ C ([0 , ∞ ) ,X p ) such that

$$
U(t) = etAUin + e(t-s)AFM (U(s)) ds , V t 2 0 . (A.4)
$$

It is easily seen that F M maps X p into X p and

$$
IJFM (U)llp < V U € Xp (A.5) IlFM
$$

Therefore, ( A.4 ) makes sense since, by assumption ( 2.3 ), U in ∈ X p and, for all U ∈ C ([0 , ∞ ) ,X p ) and all t > 0, F M ( U ( · )) ∈ L 1 ((0 ,t ); X p ). Moreover, the Lipschitz property of F M together with ( A.3 ) and Gronwall’s Lemma gives us the uniqueness of ( A.4 ). The same ingredients give us the continuous dependence of U with respect to U in . Therefore, it remains to prove the existence of U and that U belongs to C 1 ([0 , ∞ ); X ) ∩ C ([0 , ∞ ); D ( A )) for all p ∈ (1 , + ∞ ).

p p Let θ > 0 be such that ω p + θ > 0. The existence is proved using the contraction mapping principle in the space

$$
E := {U € C([0,%), Xp) IJUIlE sup e +0U (t)llp t20
$$

that is a Banach space when endowed with the norm   U   E . Hence, given U ∈ E , we set t

$$
4(U)(t) = etAUin + e(t-s)AFM (U(s)) ds , Vt > 0 .
$$

