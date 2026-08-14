Conjecture 3 ([6]). For all L,C ∈ N, there exists C′ ∈ N such that if ϕ is an (L,C)quasi-isometry from a graph G to a graph H, then there is an edge-weighting function w: E(H) → N such that the same function ϕ is a (1,C′)-quasi-isometry from G to the weighted graph (H,w).

This conjecture, if true, would imply that for any class of graphs H closed under contracting edges and taking subdivisions, if a graph G is (L,C)-quasi-isometric to a graph H ∈ H, then G is (1,C′)-quasi-isometric to a graph H′ ∈ H where C′ depends only on L and C. This would be a remarkably powerful result if true.

In this paper, we disprove this conjecture by constructing explicit counterexamples demonstrating that multiplicative distortion for weighted graphs is, in fact, necessary.

Theorem 4. For every C ∈ N, there exist graphs G and H and a (2,1)-quasi-isometry ϕ: V (G) → V (H) such that, for every edge weighting w: E(H) → R+ of H, the map ϕ is not a (1,C)-quasi-isometry from G to (H,w).

Our proof for Theorem 4 is based on orientated graphs H with large girth and chromatic number. We use the orientation of the edges to split each vertex into a new edge to deﬁne our graph G (see Figure 1). Since H can be obtained from G by contracting disjoint edges, the natural map ϕ between G and H is a (2,1)-quasi-isometry. Next, we assume that H is given an edge-weighting function w: E(H) → R+. We then separate the light-weight edges from the heavy-weight edges and then ﬁnd diﬀerent types of long orientated paths within the graph. This allows us to ﬁnd in H either a long path of light-weight edges that traverse many new edges, or a long path of heavy-weight edges that avoids the new edges. Since H has large girth, such paths are geodesic which allows us to contradict ϕ being a (1,C)-quasi-isometry from G to (H,w).

# 1.1 Preliminaries

Let G be a graph. The girth of G is the length of a shortest cycle in G. For k ∈ N, a proper k-colouring of a G is a function c: V (G) → {1,...,k} such that c(u) = c(v) whenever uv ∈ E(G). The chromatic number χ(G) is the minimum k ∈ N for which G has a proper k-colouring.

Let (H,w) be a weighted graph. For a path P = (v0,v1,...,vn) in (H,w), we say that the length of P is ni=1 w(vi−1vi) and the hop-length of P is n. The path P is geodesic if it is a path of minimum length in (H,w) between v0 and vn.

An oriented graph H is a graph where each edge has a direction. The chromatic number of H is the chromatic number of H. Let Pn = (v0,v1,v2,...,vn) be an oriented path. We

3

