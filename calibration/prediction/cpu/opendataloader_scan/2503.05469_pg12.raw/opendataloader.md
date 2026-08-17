By construction the output sets Y 1 ,... , Y d are pairwise disjoint and u i is connected to Y i by edges in U . Also, for every i ∈ { 1 ,... ,d } the algorithm adds at most a 2 u − ρ − + 1 vertices to the graph U , so that its output U satisﬁes

$$

$$

        for all 0 < u < u 0 by choice of u 0 . In the following we show how the algorithm can be used to construct a suitably large subgraph of G m .

We run the algorithm with parameter (˜ π,u,m ) for an intensity measure with a slightly decreased density parameter 0 < ˜ β < β , 0 < u < u 0 and some large m . This leads to a slightly smaller value of ρ − which is referred to as ρ in the statement of Proposition 2. The next lemma shows that the probability of edges inserted by the algorithm is bounded from above by the edge probabilities in G m .

Lemma 2.3. There exists m ( u ) ∈ N such that, for all m ≥ m ( u ) , for all m ≥ s,r ≥ bum with s   = r the probability that a particle v in location V ( v ) with π m ( V ( v )) = r has an oﬀspring y with location V ( y ) satisfying π m ( V ( y )) = s is at most

$$

$$

Proof. For a ﬁxed particle v in location V ( v ) with π m ( V ( v )) = r the probability that it has an oﬀspring y with location V ( y ) satisfying π m ( V ( y )) = s equals

$$
m 1 exp k=s k=s+1
$$

As π m ( V ( v )) = r we have

$$
m 1 k=r k=r+l
$$

m It therefore remains to show that, for bum < s < r, we have

$$
1 exp 4]) k=s k=s+1
$$

$$
1 exp 6) k=r k=r
$$

For (5) we

$$
(-2 k exp =1) k=s k=s+1 k=s 8 + 1 exp @um))
$$

Hence, using that 1 − e − x ≤ x , we get (5).

