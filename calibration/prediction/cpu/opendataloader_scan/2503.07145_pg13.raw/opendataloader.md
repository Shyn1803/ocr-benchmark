Theorem 3.6. Let x   (0 ,... ,n − 1) be an irreducible score, so that C ∩ (0 , ∞ ) n × n   = ∅ . Then

$$
lim arg D(L, MO) arg minLec H(L) (3.9) k-+0 Mk minLec
$$

. It is easy to check:

h(s) < 0} is closed for all Q € R

(2) h is Legendre because

h is diﬀerentiable on idom( h );

lim t → 0+

h is strictly convex on idom( h ).

(3) h is co-ﬁnite because lim t →∞ h ( tx ) t = ∞ for all x   = 0.

Since C 1 ,C 2 ,C 3 are all aﬃne subsets, it suﬃces to apply [7, Theorem 4.3] to conclude.

See also [45] for recent development on the convergence rate of Bregman’s iteration under further technical assumptions, which we do not pursue here.

Next we propose a computational scheme inspired by Theorem 3.6. The key is to compute numerically, for each M ∈ (0 , ∞ ) n × n , its Bregman projection on C k . We distinguish three cases:

k We introduce the Lagrange   multiplier = € R" , and set Differentiating 4   with respect to these to zero; get mij we

$$
arg D(L, M) = (3.10) k=1 I<i,j<n mij mik
$$

  k = 2: The same reasoning as in the previous case yields:

$$
arg D(L, M) (3.11) k=1 I<i,j<n mij minLeC2 mkj
$$

with respect to and $ log(lij ) = and 1)lij Setting these to zero yields mij

$$
arg D(L; M) ij (3.12) I<i,j<n minLeC3
$$

where r ij is the unique positive root to the polynomial equation   n j =1 ( j − 1) m ij r j − 1 − x i = 0. Let f ( r ) :=   n j =1 ( j − 1) m ij r j − 1 − x i . It is easy to see that f is strictly increasing on [0 , ∞ ) with f (0) ≤ 0 and lim r →∞ f ( r ) = + ∞ . Thus, it is easy (and quick) to ﬁnd a numerical root of f on [0 , ∞ ) by Newton’s method.

