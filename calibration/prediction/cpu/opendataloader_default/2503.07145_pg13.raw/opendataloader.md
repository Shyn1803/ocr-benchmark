13

Theorem 3.6. Let x (0,... ,n − 1) be an irreducible score, so that C ∩ (0,∞)n×n = ∅. Then

Mk = arg minL∈C D(L,M0) = arg minL∈C H(L). (3.9)

lim

k→∞

Proof. Note that dom(h) = R+, idom(h) = (0,∞) and bdom(h) = {0}. It is easy to check:

- (1) h is a proper convex function. Moreover, h is closed because {x ∈ dom(h) : h(x) ≤ α} is closed for all α ∈ R.
- (2) h is Legendre because

- • h is diﬀerentiable on idom(h);
- • limt→0+ h′(x + t(y − x))(y − x) = −∞ for all x ∈ bdom(f) and y ∈ idom(h);
- • h is strictly convex on idom(h).


- (3) h is co-ﬁnite because limt→∞ h(txt ) = ∞ for all x = 0.

![](<2503.07145_pg13_images/imageFile1.png>)

- (4) h is very strictly convex because h′′(x) > 0 for all x ∈ idom(h).


Since C1,C2,C3 are all aﬃne subsets, it suﬃces to apply [7, Theorem 4.3] to conclude. See also [45] for recent development on the convergence rate of Bregman’s iteration under further technical assumptions, which we do not pursue here.

Next we propose a computational scheme inspired by Theorem 3.6. The key is to compute

numerically, for each M ∈ (0,∞)n×n, its Bregman projection on Ck. We distinguish three cases:

- • k = 1: We introduce the Lagrange multiplier λ = (λ1,... ,λn) ∈ Rn, and set Φ(L,λ) := D(L,M) + ni=1 λi nj=1 lij − 1 . Diﬀerentiating Φ with respect to

mij and λi yields ∂lijΦ = log(lij)−log(mij)+λi and ∂λiΦ = nj=1 lij −1. By setting these to zero, we get

arg minL∈C1 D(L,M) =

mij

![](<2503.07145_pg13_images/imageFile2.png>)

n k=1 mik 1≤i,j≤n

. (3.10)

- • k = 2: The same reasoning as in the previous case yields:

arg minL∈C2 D(L,M) =

mij

![](<2503.07145_pg13_images/imageFile3.png>)

n k=1 mkj 1≤i,j≤n

. (3.11)

- • k = 3: Deﬁne Φ(L,λ) := D(L,M)+ ni=1 λi nj=1(j − 1)lij − xi , and diﬀerentiate Φ with respect to mij and λi yields ∂lijΦ = log(lij) − log(mij) + λi(j − 1) and ∂λiΦ = nj=1(j − 1)lij − xi. Setting these to zero yields


arg minL∈C3 D(L,M) = mijrijj−1

, (3.12)

1≤i,j≤n

where rij is the unique positive root to the polynomial equation nj=1(j−1)mijrj−1− xi = 0. Let f(r) := nj=1(j − 1)mijrj−1 − xi. It is easy to see that f is strictly increasing on [0,∞) with f(0) ≤ 0 and limr→∞ f(r) = +∞. Thus, it is easy (and quick) to ﬁnd a numerical root of f on [0,∞) by Newton’s method.

