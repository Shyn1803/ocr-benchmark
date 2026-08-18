Step 1: regularizing coeﬃcients of A : We follow [AN24]. Let θ ∈ D ( R ) a nonnegative function with ´ R θ ( t )d t = 1 . For all p ≥ 1 , let θ p ( t ) = pθ ( pt ) be the associated mollifying sequence. We set A p ( t,x ) := ( θ p ⋆ A ( · ,x ))( t ) , i.e. , we mollify the matrix-valued function A in the time variable only. For all p ≥ 1 and t ∈ R , we set

$$
1 Ap(t, )V Rn p
$$

We check easily that (Rn) In

$$
d0p zull2, t _ sl Re(BP(u, u)) , dt L1 (R)
$$

    where ˙ θ is the derivative of θ . For all p ≥ 1 , we set U p ( t ) := Γ p ( t,s ) f where Γ p is the fundamental solution of the parabolic operator associated to the family ( B p t ) t ∈ R . Combining [Kat61, Theorem III] with uniqueness in in L 2 (( s, T ); H 1 ω ( R n )) for any T > s , we have for all p ≥ 1 , U p : ( s, ∞ ) → L 2 ω ( R n ) is strongly diﬀerentiable. Note that U p is a real-valued function by the same argument as we did for U . Since ∇ x U p ( t ) ∈ L 2 ω ( R n ) , we have ∂ t | U p ( t ) | , ∇ x | U p ( t ) | ∈ L 2 ω ( R n ) with

$$
if Up(t) > 0, VzUp(t) if Up(t) > 0, 0 |Up(t)| = if Up(t) < 0, and JUp(t)| = {~v8,) if Up(t) < 0.
$$

Using this, we have

$$
~2(0 (Up(t) = |Up(t)l) , Up(t) = |Up(t)l)2, dt =4 Rn
$$

Integrating from s to t in this inequality, we see that t  →   U p ( t ) − | U p function. Since it vanishes at t = s , we have for all t > s , U p ( t ) = Γ ( t,s ) f , hence Γ ( t,s ) is a nonnegative operator.

| p | p Step 2: passing to the limit: using uniqueness in L 2 (( s, T ); H 1 ω ( R n )) for any T > s combined with the boundedness of ( U p ) p ≥ 1 in L 2 (( s, T ); H 1 ω ( R n )) provided by the energy equality, it is easy to check that, up to extracting a sub-sequence, ( U p ) p ≥ 1 converges weakly to U when p → ∞ in L 2 (( s, T ); L 2 ( R n )) for any T > s , and therefore U ( t ) is nonnegative for all t s .  

Combining Caccioppoli inequality in Lemma 4.4, a weighted Sobolev inequality [HKM18, Theorem 15.26] and the Moser’s iteration principle, we have the following L ∞ -estimate on nonnegative local weak solutions. For a proof, one can follow the classical scheme or see [Ish99, Proposition 2.1] with lower order coeﬃcients equal to zero.

Lemma 6.2. If u is is a nonnegative local weak solution of Hu = 0 in 0

$$
1/2 ess sup U = dp
$$

where B = B ( n,D,M,ν ) > 0 is a constant. The same estimate holds for nonnegative local weak solution of H ⋆ v = 0 .

By combining Lemma 6.2 above, Lemma 6.1 and Proposition 5.12, we obtain the following result.

Proposition 6.3. The operator H admits a nonnegative generalized fundamental with, for all t > s , almost everywhere pointwise Gaussian upper bound, that is, 2

$$
Ko (6.4) e Vwt-s ($) Wt-s
$$

    for almost every ( x,y ) ∈ R 2 n , where K 0 = K 0 ( n,D,M,ν ) > 0 and k 0 = k 0 ( M,ν ) > 0 are constants.

