whose center vertex is x , by adding an edge vx and a pendent 4-cycle at vertex v . In that case, by Proposition 2.6, there is a hop dominating set S of H , such that x ∈ S and | S | ≤ 2( n − 4) 5 , which implies that S ∪ { v } is a hop dominating set S of G , a contradiction. Thus such a path P exists. Note that k ≥ 2.

# Claim 3.10. k ∈ { 2 , 3 }

Proof. Suppose that k ≥ 4. Let G ′ at x 4 in G ′ . Note that | V ( G ′ ) | = n ,

| | | | Suppose that deg G ( x ) ≥ 3. Then δ ( G ′ ) ≥ 2 and G ′ has no connected component in B . There is a minimum hop dominating set S ′ of G ′ such that x 4 ,v,x ∈ S ′ and N G ( x 4 ) ∩ S ′ ̸ = ∅ by Proposition 2.7. By the choice of G , | S ′ | ≤ 2 n 5 . Thus S ′ is a hop dominating set of G , which is a contradiction.

Suppose that deg G ( x ) = 2. Then let H be the connected component of G ′ containing x 4 . Note that | V ( H ) | ≤ n − 5. There is a minimum hop dominating set S ′ of G ′ such that x 4 ∈ S ′ , N G ′ ( x 4 ) ∩ S ′ ̸ = ∅ by Proposition 2.7. If S ′ contains x 1 , then we replace x 1 with x 3 so that S ′ does not have x 1 . Then S ′ ∪ { v,x } is a minimum hop dominating set of G , a contradiction.

Let G ′ = G − { x 1 ,...,x k − 1 } . Suppose that deg G ( x ) ≥ 3. Then δ ( G ′ ) ≥ 2. If G ′ has no connected component in B , then take a minimum hop dominating set S ′ of G ′ such that v,x ∈ S ′ by Proposition 2.7, which implies that S ′ is a minimum hop dominating set of G , a contradiction. Thus, G ′ has two connected components D 1 and D 2 . We may assume that D 1 ̸∈ B and D 2 ∈ B . There is a hop dominating set S 1 of D 1 such that v,x ∈ S 1 and | S 1 | ≤ 2 | V ( D 1 ) | 5 by Proposition 2.7. If k = 3 or D 2 ̸ = C 8 , then by (3.1), there is a minimum hop dominating set S 2 of D 2 such that | S 2 | ≤ 2 | V ( D 2 ) | +2( k − 1) 5 . If k = 2 and D 2 = C 8 , then we take a minimum hop dominating set S 2 of a path D 2 − x 2 such that | S 2 | = 3 ≤ 2 | V ( D 2 ) | +2( k − 1) 5 . Note that S 1 ∪ S 2 is a hop dominating set of G . Then 2 V ( D ) + 2 V ( D ) + 2( k 1) 2 n

$$
2n 1S1 U S2| 5 5
$$

which is a contradiction.

Suppose that deg G ( x ) = 2. Let H be the connected component containing x k . Then | V ( H ) | ≤ n − 6. If H ̸ = C 8 , then for a minimum hop dominating set S of H , we have | S | ≤ 2( n − 6)+2 5 by (3.1), and so S ∪ { v,x } is a hop dominating set of G whose size is at most 2 n 5 , a contradiction. Thus H = C 8 . Then G is one of the last two graphs in Figure 6, which shows that γ h ( G ) ≤ 2 n 5 . This completes the proof of our main theorem.

# An open problem

It would be a natural extension to consider giving a sharp upper bound on the hop domination number for a graph with a large girth. So we propose the following open problem.

