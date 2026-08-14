Finally, we proceed to the main result of this section. We show that if G is a nontrivial (k,g,s)-multipole with s ≤ (k − 2)g, then it cannot happen that |G| ≤ b1(k,g,s). Thus, we obtain a nontrivial lower bound on the size of G.

Theorem 9. Let G be a nontrivial (k,g,s)-multipole for some k ≥ 3, g ≥ 5 and s ≤ (k − 2)g. Then

- 1

- 2


|G| ≥ b2(k,g,s) ≥

M(k,g).

Proof. Note that b2(k,g,s) ≥ 12M(k,g). It is easy to check that the statement is true for k = 3 and g ≤ 8 (see Table 1), for other values we can use Lemma 7 and it is sufficient to prove

|G| ≥ b2(k,g,(k − 2)g) which is equivalent to |G| > b1(k,g,(k − 2)g). This is clearly true for s = 0. We will proceed by induction as follows. Let G be a nontrivial (k,g,s)-multipole of order n with 0 < s ≤ (k−2)g and assume that Theorem 9 holds for all nontrivial (k′,g′,s′)-multipoles of order n′ with s′ ≤ (k′ − 2)g′ where (k′,g′,s′,n′) is lexicographically smaller than (k,g,s,n). By Lemma 3 we also assume that G contains no vertex with inner degree 1.

# Case 1: G contains a vertex v with inner degree 2

If k ≥ 4, then let G′ = G − v. Clearly, G′ is a (k,g,s − (k − 4))-multipole of order n − 1. Graph G′ cannot be trivial, otherwise either G would be trivial, or it would have girth less than g (≥ 5). But then G′ fulfils the theorem condition and as (k,g,s − (k − 4),n − 1) is lexicographically smaller than (k,g,s,n) we have |G′| ≥ b2(k,g,s − (k − 4)). By Lemma 7, |G′| ≥ b2(k,g,(k − 2)g)) and then |G| ≥ b2(k,g,(k − 2)g) + 1. Thus, k = 3.

For k = 3 we already resolved the cases when g ≤ 8. Thus, we may assume g ≥ 9. We remove the vertex v from G and join the two links formerly incident with v to produce one new link. The constructed multipole G′ is clearly a nontrivial (3,g − 1,s − 1)-multipole with s − 1 ≤ (k − 2)(g − 1). By the induction hypothesis and Lemma 7 we have |G| ≥ b2(3,g − 1,s − 1) ≥ b2(3,g − 1,g − 1). So it is sufficient to show that

b2(3,g − 1,g − 1) > b1(3,g,g)

We manually checked that this is true for all g < 14. For g ≥ 14, by Proposition 8 it is sufficient to show

(g − 1)2 2

M(3,g − 1) −

g2 2

, or equivalently, M(3,g − 1) > g2 − g +

>

- 1

- 2


. (8)

For g = 2d + 1, Inequality (8) is equivalent to

M(k,2d) = 2 · 2d − 2 > 4d2 + 2d +

which is true for g ≥ 7. For g = 2d + 2, Inequality (8) is equivalent to

- 1

- 2


, (9)

M(3,2d + 1) = 3 · 2d − 2 > 4d2 + 6d +

which holds for d ≥ 6, thus g ≥ 14.

11 2

, (10)

11

