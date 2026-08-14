E     A             13 We ﬁnally show that the set AC is contained within a neighborhood of size N−le−M

![](<2503.06110_pg13_images/imageFile1.png>)

around a hyperplane in Fq((X−1))n. For any x ∈ C, deﬁne y = e(n+1)lM(x−x0) in ZnO, so that

gtux = uygtux0.

Consider a linear functional φt,C of norm 1 that is zero on the hyperplane Ht,C = gtux0HC. Then, we have

d([e1],gtuxHC) = d([e1],uyHt,C) ≍ d([u−ye1],Ht,C) ≍ φt,C(u−ye1). Thus, if x ∈ AC, we obtain φt,C(u−ye1) e−M, implying that y lies within a neighborhood of size O(e−Mn ) of the aﬃne hyperplane in Fq((X−1))n deﬁned by

![](<2503.06110_pg13_images/imageFile2.png>)

φt,C(e1 − y1e2 − ··· − ynen+1) = 0. This means that x lies in a neighborhood of size O(N−le−M) around an aﬃne hyperplane in Fq((X−1))n. The number of subcubes of C that intersect this neighborhood is bounded by

n Nne−M, and thus we obtain

1

card Kl(C) ≥ Nn(1 − On(e−M)) = Nn − On(Nn−

n+1).

![](<2503.06110_pg13_images/imageFile3.png>)

Now, we proceed to the proof of Theorem 1.1.

Proof of Theorem 1.1. To obtain a lower bound for the Hausdorﬀ dimension of K∞, we apply the Mass Distribution Principle. This argument follows identically from the work of [BdS23], but we include the proof here for the sake of completeness.

For l ≥ 1, deﬁne

⌊Nn(1 − R3e−Mn )⌋ if lk+−1 < l ≤ lk− 1 if lk− < l ≤ lk+.

![](<2503.06110_pg13_images/imageFile4.png>)

bl =

We also replace K∞ by a Cantor subset F∞ that is more regular in nature. Removing some cubes in Kl at each step, we obtain the subset F∞ ⊂ K∞ given as

F∞ =

Fl,

l≥1

where each cube C in Fl−1 contains exactly bl subcubes in Fl. As stated in Proposition 1.7 of [Fal90], there is a probability measure µ that is supported on F∞, and for each cube C at level l (with C ⊂ Fl), we have the relationship

1 b1b2 ... bl

µ(C) =

. We propose that if α is smaller than the limit inferior

![](<2503.06110_pg13_images/imageFile5.png>)

log(b1b2 ... bl) l log N

lim inf

,

![](<2503.06110_pg13_images/imageFile6.png>)

l→∞

then there exists a constant C = Cn,N,α such that for every x ∈ Fq((X−1)) and for all radii r > 0,

µ(B(x,r)) ≤ Crα. To justify this, choose l such that N−l < r ≤ N−l+1. The ball B(x,r) can intersect no more than (3N)n cubes from Fl. Hence, we have

µ(B(x,r)) ≤ (3N)n · (b1b2 ... bl)−1 ≤ (3N)nN−lα ≤ (3N)nrα

