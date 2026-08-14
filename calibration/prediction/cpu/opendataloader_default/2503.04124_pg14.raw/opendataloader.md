whose center vertex is x, by adding an edge vx and a pendent 4-cycle at vertex v. In that case,

- by Proposition 2.6, there is a hop dominating set S of H, such that x ∈ S and |S| ≤ 2(n5−4), which implies that S ∪ {v} is a hop dominating set S of G, a contradiction. Thus such a path P exists. Note that k ≥ 2. Claim 3.10. k ∈ {2,3}

Proof. Suppose that k ≥ 4. Let G′ = (G−xx1)+x1x4. Note that x1x2x3x4v1 is a pendent 4-cycle at x4 in G′. Note that |V (G′)| = n, |E(G′)| = |E(G)|, and G′ has more pendent 4-cycles than G.

Suppose that degG(x) ≥ 3. Then δ(G′) ≥ 2 and G′ has no connected component in B. There is a minimum hop dominating set S′ of G′ such that x4,v,x ∈ S′ and NG(x4) ∩ S′ ̸= ∅ by Proposition 2.7. By the choice of G, |S′| ≤ 25n. Thus S′ is a hop dominating set of G, which is a contradiction.

Suppose that degG(x) = 2. Then let H be the connected component of G′ containing x4. Note that |V (H)| ≤ n − 5. There is a minimum hop dominating set S′ of G′ such that x4 ∈ S′, NG′(x4)∩S′ ̸= ∅ by Proposition 2.7. If S′ contains x1, then we replace x1 with x3 so that S′ does not have x1. Then S′ ∪ {v,x} is a minimum hop dominating set of G, a contradiction.

<table>
  <tr>
    <td> </td>
  </tr>
</table>


Let G′ = G − {x1,...,xk−1}. Suppose that degG(x) ≥ 3. Then δ(G′) ≥ 2. If G′ has no connected component in B, then take a minimum hop dominating set S′ of G′ such that v,x ∈ S′

- by Proposition 2.7, which implies that S′ is a minimum hop dominating set of G, a contradiction. Thus, G′ has two connected components D1 and D2. We may assume that D1 ̸∈ B and D2 ∈ B.


There is a hop dominating set S1 of D1 such that v,x ∈ S1 and |S1| ≤ 2|V(D

1)|

5 by Proposition 2.7. If k = 3 or D2 ̸= C8, then by (3.1), there is a minimum hop dominating set S2 of D2 such that |S2| ≤ 2|V(D

2)|+2(k−1)

5 . If k = 2 and D2 = C8, then we take a minimum hop dominating set S2 of a path D2 − x2 such that |S2| = 3 ≤ 2|V(D

2)|+2(k−1)

5 . Note that S1 ∪ S2 is a hop dominating set of G. Then

2|V (D1)| + 2|V (D2)| + 2(k − 1) 5

2n 5

|S1 ∪ S2| ≤

, which is a contradiction.

=

Suppose that degG(x) = 2. Let H be the connected component containing xk. Then |V (H)| ≤ n − 6. If H ̸= C8, then for a minimum hop dominating set S of H, we have |S| ≤ 2(n−56)+2 by (3.1), and so S ∪ {v,x} is a hop dominating set of G whose size is at most 25n, a contradiction. Thus H = C8. Then G is one of the last two graphs in Figure 6, which shows that γh(G) ≤ 25n. This completes the proof of our main theorem.

# 4 An open problem

It would be a natural extension to consider giving a sharp upper bound on the hop domination number for a graph with a large girth. So we propose the following open problem.

14

