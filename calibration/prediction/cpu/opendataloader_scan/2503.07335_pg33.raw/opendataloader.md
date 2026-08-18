The sum   i 1 j = i 0 +1 11 { j ∈ B C } is thus stochastically dominated by a sum of independent { 0 , 1 } random variables i max 1 ω

$$
Z i=0 h=l imax
$$

where for all h = 1,2, W uniformly in i. We compute

$$
=1 E[Z] = (1 + 0(1))w (1 _ 3 i=0 2 io + i) i=0 imax 2i0 2w = (1 + 0(1 ))wimax ) 3n 3n i=0 2w i 2ax = (1 + 0(1)) n 3n 2 2n (1 + 0(1))3 imax
$$

It follows from Proposition 1.5 that Z ≤ (1+ o (1)) E [ Z ] = (1+ o (1)) 2 n 3 a.a.s. Since Z stochastically dominates |B C | , we may conclude 1 2 |B C | ≤ (1 + o (1)) n 3 a.a.s., completing the proof.

# 7. Conclusion

In this paper, we have shown that s ( G n, 3 ) ≤ (1 + o (1)) n 3 a.a.s., and have additionally made the conjecture that s ( G n, 3 ) = (1 + o (1)) n 4 a.a.s., which is (asymptotically) smallest possible for cubic graphs on n vertices. Resolving this conjecture is an interesting direction for future research. Another one is to study s ( G n,d ) for d ≥ 4—a problem which at present appears challenging. We considered the following crude technique for upper bounding the Sudoku number of a graph

G with chromatic number k . Start with any k -coloring of G using colour classes { 1 , 2 ,...,k } . Iteratively move vertices from class k to another available class until every remaining vertex has a neighbour in each class i for i = 1 ,...,k − 1. Then the union of classes 1 through k − 1 is a Sudoku set for G , and we have the bound

$$
s(G) < (x(G) = 1)a(G) (38
$$

where α ( G ) is the size of the largest independent set in G .

Using the best available bound α ( G n, 4 ) ≤ 0 . 41635 a.a.s. (see [23]) and the fact that χ ( G n, 4 ) = 3 a.a.s. ([26]), (38) gives s ( G n, 4 ) ≤ 0 . 8327 n a.a.s. The next value of d for which χ ( G n,d ) is known explicitly is d = 6, where we have χ ( G n,d ) = 4 a.a.s. [27]. However, it has been shown that G n, 6 has an independent set of size at least 0 . 33296 n a.a.s. [8], meaning that any bound using (38) for d = 6 will be very close to n . In fact, currently available upper bounds, such as 0 . 35799 n , are well above n/ 3 (see for instance [8]) and thus, are far from providing any useful bound on s ( G n, 6 ). For large d , (38) is too weak to say anything nontrivial about s ( G n,d ). Indeed, for d → ∞ sufficiently slowly with respect to n , it is known that χ ( G n,d ) = (1 + o (1)) n α ( G n,d ) = (1 + o (1)) d 2 log d a.a.s. [10].

