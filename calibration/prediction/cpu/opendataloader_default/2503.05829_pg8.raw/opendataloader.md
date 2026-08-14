# 2 Results

In this section, we introduce the deﬁnition of the model of interest along with the relevant notation. We then proceed to state the main results of this work.

## 2.1 Deﬁnition of the model

Throughout, we use the notation N := {1, 2, . . .}, N0 := N∪{0} and [n] := {1, . . ., n} for each n ∈ N. We consider a labeled directed graph (V, E) with vertex set V = [n] for some n ∈ N and edge set E ⊂ {(v, w): v, w ∈ V }. The natural number representing a vertex is then referred to as its label. In such a graph, a sequence of vertices (v1, v2, . . ., vk+1) is a directed path of length k ∈ N if

∀i ∈ [k]: (vi, vi+1) ∈ E

and an undirected path of length k ∈ N if

∀i ∈ [k]: (vi, vi+1) ∈ E ∨ (vi+1, vi) ∈ E.

A labeled directed graph is called

- • connected if, for each pair of vertices, there is an undirected path joining those vertices,
- • acyclic if it does not contain any directed cycles, i.e. directed paths that visit the same vertex more than once,
- • increasing if the labels are decreasing along all directed paths.


We observe that if a graph is increasing, then it is acyclic in particular. For v ∈ V , we call a vertex w ∈ V an out-neighbor if (v, w) ∈ E and an in-neighbor if (w, v) ∈ E. Then, the number of out-neighbors of v is denoted by outdeg(v). On the other hand, we call the number of in-neighbors of v the degree of vertex v, denoted by dV (v). For all n, m ∈ N we deﬁne In(m) to be the set of increasing directed graphs on [n] satisfying the condition

∀v ∈ [n]: outdeg(v) = m ∧ (v − 1). (2.1)

Now, we are ready to formally deﬁne RRDAGs.

8

