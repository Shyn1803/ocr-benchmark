vil

v x

C

v1′ x′1

P

v′ x′

(a) Another shortest path P from v′ to x′

vil

v x

y

v1′ x′1

v′ x′

(b) vil is incident to exactly one chord in C

Figure 12: The cycle C created by two distinct paths from v′ to x′

to it in C. Let vi

y be one such chord; then we show that y lies in P(v1′, x′1) in the next

l

claim. Claim 6.6. y lies in P(v1′, x′1). Proof. If y does not lie in P(v1′, x′1), then y must lie in the path between vi

and x′1 (or the path between vi

l

and v1′). If it lies on the path between vi

and x′1 (resp. between vi

l

l

l

and v1′), then we have a path from vi

and v′) which has length smaller than d(vi

to x′ (resp. between vi

l

l

, x′) (resp. d(vi

, v′)), which is a contradiction. Hence, y lies in P(v1′, x′1)

l

l

(refer to Figure 12b). Note that d(x′1, y) ≥ d(x′1, vi

![](<2503.06086_pg17_images/imageFile1.png>)

![](<2503.06086_pg17_images/imageFile2.png>)

![](<2503.06086_pg17_images/imageFile3.png>)

![](<2503.06086_pg17_images/imageFile4.png>)

) and d(v1′, y) ≥ d(v1′, vi

). If not, then there exists a shorter or equal length path from v′ to vi

l

l

v (resp. vi

(from x′ to vi

) that bypasses the edge vi

l

l

l

, x′) monitors the edge vi

x), which is a contradiction to the fact that the pair vi

, v′ (resp. vi

l

l

l

x). Hence dP(x′1, v1′) = d(x′1, y) + d(y, v1′) ≥ d(v1′, vi

), implying dP(x′1, v1′) = d(v1′, vi

v (resp. vi

) + d(x′1, vi

l

l

l

l

) and d(v1′, y) = d(v1′, vi

). This implies that d(x′1, y) = d(x′1, vi

) + d(x′1, vi

l

l

l

), which implies that the vertex y is unique in P(v1′, x′1). This fact together with Claim 6.6 implies that in C, vi

l

is incident to exactly one chord. Now note that if v and y are not adjacent, then the induced 2-path yvi

l

v is part of a chordless cycle of length at least 4, which is a contradiction. Hence vy ∈ E(Gk+1). Similarly, it can be shown that xy ∈ E(Gk+1). Hence vvi

l

x is part of a 4-cycle vvi

xyv, which leads to a contradiction. Hence v′ and x′ monitor vvi

l

l

.

l

Hence, until now, we showed that all edges in El can be monitored by the vertices of Man(Gk) \ {vi

l}. Hence, combining this fact with Claim 6.1 and 6.3, we can conclude that Man(Gk+1) forms an optimal MEG set of Gk+1. Hence, meg(G) = |Man(G)| for every strongly chordal graph G.

![](<2503.06086_pg17_images/imageFile5.png>)

![](<2503.06086_pg17_images/imageFile6.png>)

![](<2503.06086_pg17_images/imageFile7.png>)

![](<2503.06086_pg17_images/imageFile8.png>)

7. Conclusion and future aspects

In this paper, we solved the complexity status of the MIN-MEG problem for some well-known graph classes. Next, it will be interesting to address the following questions:

17

