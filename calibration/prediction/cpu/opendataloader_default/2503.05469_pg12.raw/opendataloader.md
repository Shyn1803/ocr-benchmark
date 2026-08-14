By construction the output sets Y1,... ,Yd are pairwise disjoint and ui is connected to

Yi by edges in U . Also, for every i ∈ {1,... ,d} the algorithm adds at most a2u−ρ− + 1 vertices to the graph U , so that its output U satisﬁes

![](<2503.05469_pg12_images/imageFile1.png>)

|U | ≤ |U ′| + d a2u−ρ− + 1 ≤ a(m/u)ρ− uρ− + 21 + a1uρ− ≤ a(m/u)ρ−,

![](<2503.05469_pg12_images/imageFile2.png>)

![](<2503.05469_pg12_images/imageFile3.png>)

![](<2503.05469_pg12_images/imageFile4.png>)

for all 0 < u < u0 by choice of u0. In the following we show how the algorithm can be used to construct a suitably large subgraph of Gm.

We run the algorithm with parameter (˜π,u,m) for an intensity measure with a slightly decreased density parameter 0 < β˜ < β, 0 < u < u0 and some large m. This leads to a slightly smaller value of ρ− which is referred to as ρ in the statement of Proposition 2. The next lemma shows that the probability of edges inserted by the algorithm is bounded from above by the edge probabilities in Gm.

Lemma 2.3. There exists m(u) ∈ N such that, for all m ≥ m(u), for all m ≥ s,r ≥ bum with s = r the probability that a particle v in location V (v) with πm(V (v)) = r has an oﬀspring y with location V (y) satisfying πm(V (y)) = s is at most

β(r ∧ s)−γ(r ∨ s)γ−1.

Proof. For a ﬁxed particle v in location V (v) with πm(V (v)) = r the probability that it has an oﬀspring y with location V (y) satisfying πm(V (y)) = s equals

m

1 − exp − π˜ −

k=s

m

1 k

− V (v),−

![](<2503.05469_pg12_images/imageFile5.png>)

k=s+1

1 k

− V (v) . (4)

![](<2503.05469_pg12_images/imageFile6.png>)

As πm(V (v)) = r we have

m

1 k

−

![](<2503.05469_pg12_images/imageFile7.png>)

k=r

m

1 k

< V (v) ≤ −

.

![](<2503.05469_pg12_images/imageFile8.png>)

k=r+1

The probability in (4) is therefore largest when V (v) = − mk=r k1. It therefore remains to show that, for bum ≤ s < r, we have

![](<2503.05469_pg12_images/imageFile9.png>)

r−1

1 − exp − π˜ −

k=s

and, for bum ≤ r < s, we have

r−1

1 k

1 k

,−

![](<2503.05469_pg12_images/imageFile10.png>)

![](<2503.05469_pg12_images/imageFile11.png>)

k=s+1

≤ βs−γrγ−1, (5)

1 − exp − π˜

s−1

1 k

,

![](<2503.05469_pg12_images/imageFile12.png>)

k=r

s

1 k

![](<2503.05469_pg12_images/imageFile13.png>)

k=r

≤ βsγ−1r−γ. (6)

For (5) we ﬁnd that, for some constant C > 0, if m ≥ m(u) for a suitable m(u) ∈ N,

r−1

π˜ −

k=s

r−1

1 k

1 k

,−

![](<2503.05469_pg12_images/imageFile14.png>)

![](<2503.05469_pg12_images/imageFile15.png>)

k=s+1

r−1

β˜ 1 − γ

1 k

1−γ

exp −(1 − γ)

s+1 − 1)

=

(e

![](<2503.05469_pg12_images/imageFile16.png>)

![](<2503.05469_pg12_images/imageFile17.png>)

![](<2503.05469_pg12_images/imageFile18.png>)

k=s

β ˜ s + 1

C (bum)2

exp − (1 − γ)(log rs−−11 − bumC ) ≤ βs−γrγ−1.

≤

+

![](<2503.05469_pg12_images/imageFile19.png>)

![](<2503.05469_pg12_images/imageFile20.png>)

![](<2503.05469_pg12_images/imageFile21.png>)

![](<2503.05469_pg12_images/imageFile22.png>)

Hence, using that 1 − e−x ≤ x, we get (5).

12

