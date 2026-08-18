for some almost surely finite random variable O

Remark 6.8. Under the assumption that liminf i →∞ d ( i ) ≥ R we can adapt the proof of ( 6.23 ) (and by using ( 6.1 ) rather than ( 6.2 )) to show that for any ε > 0 there exists p > 0 such that

$$
cont R lim Ps Vs € [(1 _ p)t, (1 + p)t] 1.
$$

It yields a weaker bound on O cont s ,

Remark 6.9. When setting s = t in ( 6.23 ) and ( 6.24 ), the quantity in the absolute values converges to zero in probability. Though in some cases where K grows sufficiently fast it may be possible to strengthen the convergence in probability to almost sure convergence, we are unable to derive the stronger bounds due to the use of ( 6.18 ) and ( 6.19 ) in Corollary 6.6 . Stronger versions of these results would be required to improve to almost sure convergence. ◀

Remark 6.10. Proposition 6.7 provides the main step in proving the asymptotic behaviour of O n , as presented in Theorems 2.3 through 2.10 . It remains to translate the asymptotic behaviour of O cont t into the asymptotic behaviour of O n , which is carried out in Section 9 . ◀

Intuitively, an individual born at time T < t survives up to time t with probability P ( L > t − T ), independently of all other individuals. At the same time, the number of individuals born around time T is roughly e λ ∗ T by Proposition 6.5 . The proof uses first and second moment bounds to establish the optimal choice of T such that no individuals born before T are alive at time t , whereas many individuals born after T are alive at time t .

Proof. We first prove ( 6.23 ). Fix K,p > 0 and define

$$
R R R t = K log t, Ut := t + K log t, t, (6.26) À* + R À* + R À* + R
$$

and

$$

$$

− We then observe that O cont t is increasing in t , so that

$$
R Ps Ocont t| K t for all s € +R (6.27) log
$$

(6.27) We thus aim to bound the probabilities on the right-hand side from above, starting with the leftmost one. For any δ > 0, recalling that A cont t denotes the set of alive individuals at time t ,

$$
Ps (6.28) P(S) 4 P ) ]
$$

The second probability in the brackets converges to zero by Corollary 6.6 (with r = 0 ,s = ℓ t , and u = δ log t ). Furthermore, lifetimes among individuals are i.i.d. and each individual born before time ℓ t needs to live for at least r ( t ) − ℓ t time to be alive at time r ( t ). Hence, by a union bound and using the upper bound in ( 6.2 ) of Lemma 6.1 , we arrive for some large constant C > 0 at the upper bound

$$
(6.29) log log tP(L
$$

By the definition of ℓ t and r ( t ), this equals

$$
exp
$$

Hence, for any K larger than K 0 := C ( λ ∗ + R ) − 1 , we can choose δ and p sufficiently small so that the terms in the square brackets are negative. As a result, the upper bound in ( 6.29 ) tends to zero with t for these choices of K,p , and δ .

