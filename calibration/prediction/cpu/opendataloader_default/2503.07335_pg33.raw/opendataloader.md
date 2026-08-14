The sum ij1=i

0+1 11{j ∈ BC} is thus stochastically dominated by a sum of independent {0,1}random variables

imax−1

ω

Zh(i),

Z =

i=0

h=1

where Pr(Zh(i) = 1) = (1 + o(1)) 1 − 23ti for all h = 1,2,...,ω, uniformly in i. We compute

imax−1

- 2ti

- 3


1 −

E[Z] = (1 + o(1))ω

i=0

imax−1

- 2

- 3 ·


i0 + iω n

1 −

= (1 + o(1))ω

i=0

imax−1

2i0 3n −

2ω 3n

= (1 + o(1))ωimax 1 −

i

i=0

i2max 2

2ω 3n

= (1 + o(1)) n −

- 2n

- 3


= (1 + o(1))

.

It follows from Proposition 1.5 that Z ≤ (1+o(1))E[Z] = (1+o(1))23n a.a.s. Since Z stochastically dominates |BC|, we may conclude 21|BC| ≤ (1 + o(1))n3 a.a.s., completing the proof.

<table>
  <tr>
    <td> </td>
  </tr>
</table>


# 7. Conclusion

In this paper, we have shown that s(Gn,3) ≤ (1 + o(1))n3 a.a.s., and have additionally made

the conjecture that s(Gn,3) = (1 + o(1))n4 a.a.s., which is (asymptotically) smallest possible for cubic graphs on n vertices. Resolving this conjecture is an interesting direction for future research.

Another one is to study s(Gn,d) for d ≥ 4—a problem which at present appears challenging.

We considered the following crude technique for upper bounding the Sudoku number of a graph G with chromatic number k. Start with any k-coloring of G using colour classes {1,2,...,k}. Iteratively move vertices from class k to another available class until every remaining vertex has a neighbour in each class i for i = 1,...,k −1. Then the union of classes 1 through k −1 is a Sudoku set for G, and we have the bound

s(G) ≤ (χ(G) − 1)α(G), (38) where α(G) is the size of the largest independent set in G.

Using the best available bound α(Gn,4) ≤ 0.41635 a.a.s. (see [23]) and the fact that χ(Gn,4) = 3 a.a.s. ([26]), (38) gives s(Gn,4) ≤ 0.8327n a.a.s. The next value of d for which χ(Gn,d) is known explicitly is d = 6, where we have χ(Gn,d) = 4 a.a.s. [27]. However, it has been shown that Gn,6 has an independent set of size at least 0.33296n a.a.s. [8], meaning that any bound using (38) for d = 6 will be very close to n. In fact, currently available upper bounds, such as 0.35799n, are well above n/3 (see for instance [8]) and thus, are far from providing any useful bound on s(Gn,6). For large d, (38) is too weak to say anything nontrivial about s(Gn,d). Indeed, for d → ∞ sufficiently slowly with respect to n, it is known that χ(Gn,d) = (1 + o(1))α(Gn

n,d) = (1 + o(1))2 logd d a.a.s. [10].

33

