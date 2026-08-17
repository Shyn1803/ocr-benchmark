Theorem 1. Deadlock-free routing can be constructed for a network G = ( V,E ) if and only if G contains two edge-disjoint directed trees rooted at the same vertex v , one tree directed into v and the other directed away from v .

Sufﬁciency of the two-tree condition of Theorem 1 for the existence of deadlockfree routing follows from the fact that given such trees, any message can be routed by ﬁrst sending it to the common root v along the ﬁrst tree, and then sending it to its target along the second tree. The two-tree condition was known to be sufﬁcient for deadlock-free routing. For

The two-tree condition was known to be sufficient for deadlock-free routing.  For example; [BS92; JMS94] established this fact; while Aba97, Section 4.4] uses such two trees to construct a deadlock-free routing for a 4x4 mesh. However; to the best of OUr knowledge; the necessity of this condition has neither been recognized nor proven

with a given deadlock-free routing. Using the result of [ DS87 ], the dependency graph induced by the deadlock-free routing is acyclic, so there is a dependency-respecting total ordering of the graph edges E such that every vertex is reachable from every other vertex through a sequence of edges that are ascending according to the total order.

Given a total ordering of the edges, we introduce three deﬁnitions: a global attractor, the attraction number and the attraction subgraph.

Deﬁnition. A vertex in a directed graph is called a global attractor if it is reachable from all other vertices.

Deﬁnition. Given a strongly connected directed graph G = ( V,E ) with a total ordering of its edges E = ( e 1 ,...,e m ) , we deﬁne its attraction number s to be the smallest integer such that there exists a vertex v ∈ V reachable from all other vertices using only the edges in the preﬁx { e 1 ,...,e s } .

The existence of such an s follows from the fact that G is strongly connected. We note that the attraction number is the minimal size of the preﬁx of the edges needed for the graph to have a global attractor. For the purpose of this deﬁnition, reachability using edges { e 1 ,...,e s } is not restricted to paths that respect the total ordering of the edges.

Deﬁnition. Given a strongly connected directed graph G = ( V,E ) with a total ordering of its edges E = ( e 1 ,...,e m ) , we deﬁne its attraction subgraph to be the subgraph G s = ( V,E s ) with the same vertices but only the ﬁrst s edges in E : E s = ( e 1 ,...,e s ) , where s is the attraction number of the graph.

By deﬁnition, the attraction subgraph has a global attractor.

Lemma 1.1. Let G = ( V,E ) be a strongly connected directed graph with a total ordering of its edges E = ( e 1 ,...,e m ) that is consistent with the dependencies induced by a deadlock-free routing. v G

If there is only a single global attractor in the attraction subgraph s , then the two-trees required by Theorem 1 exist in G .

Proof. If v is the only vertex reachable from all vertices in G s , no other vertex in G s can be reachable from it, so there are no outbound edges of v in G s . Therefore, routing

