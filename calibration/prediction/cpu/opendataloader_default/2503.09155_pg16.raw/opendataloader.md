of system (29) we can see that en is a real and positive root of the polynomial

Q(s) := αsm+1 + αs − 1, (30) and, in view of Descartes’ rule of signs, there is a unique such en. Then

ej =

αk en, for all j ∈ [n − 1], (31)

k≥j+1

and hence e ∈ int (BG) is unique.

Several studies (see e.g. Sanchez (2009b) and the references therein) derived conditions guaranteeing that the equilibrium e ∈ int (BG) is globally asymptotically stable. Tyson (1975) analyzed the special case of (29) with n = 3. He noted that if e is locally asymptotically stable, then one may expect that all solutions converge to e, and proved that system (29) admits a periodic solution whenever e is unstable. For n = 3, the model can also be studied using the theory of competitive dynamical systems (Smith, 1995). The case n = 3 has also been analyzed using the theory of Hopf bifurcations (Woller et al., 2014). For a general n, the analysis using Hopf bifurcations becomes highly non-trivial and results exist only for special cases, e. g. under the additional assumption that all the αi’s are equal, see Invernizzi and Treu (1991). Hastings et al. (1977) studied the general n-dimensional case and proved that, if the Jacobian of the vector ﬁeld at the equilibrium has no repeated eigenvalues and at least one eigenvalue with a positive real part, then the system admits a non-trivial periodic orbit; the proof relies on the Brouwer ﬁxed point theorem.

Our Theorem 2 allows us to prove the following result.

Corollary 3 Consider the n-dimensional Goodwin model (29) with n ≥ 3, and let e denote the unique equilibrium in int (BG). Let J : Rn≥0 → Rn×n denote the Jacobian of the vector ﬁeld of the Goodwin model. Suppose that J(e) has at least one eigenvalue with a positive real part. Then, for any initial condition a ∈ Rn≥0 \ {e} such that s−(a − e) ≤ 1, the solution x(t, a) of (29) converges to a (non-trivial) periodic orbit as t → ∞.

PROOF. The Jacobian of (29)





- m−1
- n


−α1 0 0 . . . 0 − mx

![](<2503.09155_pg16_images/imageFile1.png>)

(1+xmn )2

1 −α2 0 . . . 0 0 0 1 −α3 . . . 0 0 . . .

J(x) =

... . . 0 0 0 . . . −αn−1 0 0 0 0 . . . 1 −αn

 

 

has the sign pattern A¯2 in (3) for all x ∈ Rn≥0, hence the system is 2-cooperative on Rn≥0. We

16

