where the first inequalities are ensured by Theorem 2 . However, the irreducibility condition (H κ irr ) is not satisfied by κ red , so uniqueness is not ensured and Proposition 1 does not apply to guarantee that N red 1 and N red 2 are non-zero. Adapting the proof of Proposition 1 to each of the strongly connected components of the graph of κ , simply reduced to { v 1 } and { v 2 } , shows that for each i ∈ { 1 , 2 } , N red i is either zero everywhere or positive on ( b 2 , + ∞ ) . The normalization condition

$$
ie{1,2}
$$

implies that at least for one i ∈ { 1 , 2 } , N red i is non-zero. Both N red 1 and N red 2 cannot be non-zero, otherwise Lemma 2 would work (in equality ( 14 ), we need the existence of i ̸ = j such that N red i ̸ = 0 and N red j ̸ = 0 ) and we could use it to prove the long-time convergence of system ( 20 ) towards a stationary sate (fourth step of Theorem 4 ). That would contradict [ 6 ]. The only possibility is that N red 1 ≡ 0 and N red 2 ( x ) > 0 for x ≥ b 2 or the opposite and then λ = λ 2 or λ = λ 1 respectively.

In the mixing case, the equations of system (GF t,v ) are coupled through their source term:

$$
471 (22)n1 (t, 22) ,
$$

and the irreducibility condition (H κ irr ) , missing in the non-mixing case, is now satisfied. We can thus apply successively Theorem 3 , Proposition 1 and Theorem 4 to get eigenelements ( λ irr ,N irr ,ϕ irr ) such that

$$
irrt 0 R+ i=1
$$

0 on (0 , + ∞ ) .

These two simple cases illustrate that the existence result (Theorem 3 ) holds for every probability matrix κ , in particular reducible ones. The irreducibility condition on κ comes into play to characterize the functions canceling the dissipation of entropy (Lemma 2 ), which then proves crucial to establish uniqueness of the steady state and convergence towards it.

# 3.2 Numerical illustration

Similarly to the previous subsection, we focus here on the special case of linear growth rates to illustrate the convergence result of Theorem 4 . We numerically approximate and compare the long-time asymptotics in the presence and absence of mixing in feature.

We choose M = 3 different features, namely V = { 1 , 2 , 3 } , and approximate on the grid

$$
mN Im := 2 k m € {0, 2N} k = 200, N = 2501,
$$

the time-evolution of the following initial data (taken identical for all features)

$$
nin a = 30. b = 60, C S.t. 1,
$$

