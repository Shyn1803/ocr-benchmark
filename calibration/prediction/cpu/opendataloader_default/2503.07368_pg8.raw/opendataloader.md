# 8 Modules via graphcodes

If M is an interval module, then, when viewed as a persistence module of one-parameter persistence modules, every slice M( ,i) is either zero or a single one-parameter interval (see Figure 2). This is a direct consequence of the definition of an interval module as an indecomposable thin persistence module supported on a convex connected subset of G(m,n). Since there is at most one non-zero morphism between two one-parameter interval modules, id = (id,...,id) is the only barcode basis for an interval module.

▶ Proposition 7. For an interval module M, GCid(M) is a directed path.

Proof. By construction of GCid(M) = GC(M), the vertices at every height of GC(M) correspond to the intervals in M( ,i). Since M is an interval module, there is at most one vertex at every height. Since M is indecomposable all these vertices have to be connected. Otherwise Proposition 2 and 4 would imply that M is decomposable. Since there are only edges between vertices at consecutive height levels in a graphcode, GC(M) is a directed path. ◀

Compressed graphcodes. A disadvantage of graphcodes is that every bar of every barcode is represented by a vertex, leading to a high number of vertices and therefore a large graph. However, in practical situations, the barcodes of consecutive slices often do not differ from each other, and the question is how to compress the information of a graphcode without losing any information. The following definition prepares our approach by relaxing the condition that graphcodes only connect bars on consecutive slices.

▶ Definition 8 (generalized Graphcode). A directed graph G = (V,E,c) with vertex labels

c: V → {1,...,m} × {1,...,m + 1} × {1,...,n} is called a generalized graphcode if:

- 1. for all v ∈ V with c(v) = (b,d,h), we have b < d
- 2. for all v ∈ V and all (v,w),(v,w′) ∈ E, we have h(w) = h(w′)
- 3. for all (v,w) ∈ E with c(v) = (b1,d1,h1) and c(w) = (b2,d2,h2), we have [b2,d2) ◁ [b1,d1).


Note that graphcodes are generalized graphcodes where h(w) = h(v) + 1 for all edges (v,w) ∈ V . The condition that all out-neighbors of a vertex are on the same height will be convenient in the next section where we generate a minimal presentation out of a generalized graphcode.

We call a vertex w in a generalized graphcode G superfluous if w has exactly one incoming edge (v,w), v and w have the same birth and death values (i.e., with c(v) = (b1,d1,h1) and c(w) = (b2,d2,h2), we have b1 = b2 and d1 = d2), w has at least one outgoing edge, and v has no further outgoing edge. In that case, writing (w,x1),...,(w,xs) for the outgoing edges of w, we define G′ as the graph obtained from G by removing w and all incident edges, and adding the edges (v,x1),...,(v,xs) instead. It is simple to verify that G′ is a generalized graphcode as well. Moreover, the property of being superfluous does not change when eliminating other superfluous vertices in the graphcode. We call a generalized graphcode G′ a compression of a graphcode G if G′ is obtained from G by removing superfluous vertices. We call G′ fully compressed if it does not contain any superfluous vertex. Figure 3 shows an example.

A generalized graphcode also induces a two-parameter persistence module: For a generalized graphcode G, we define its expansion Exp(G) as follows: if a vertex v with c(v) = (b,d,h) has all its outgoing neighbors w1,...,ws at height h′ with h′ − h ≥ 2, remove all edges (v,wi), introduce vertices vh+1,...,vh′ 1 with c(vh+i) := (b,d,h + i) and add edges

