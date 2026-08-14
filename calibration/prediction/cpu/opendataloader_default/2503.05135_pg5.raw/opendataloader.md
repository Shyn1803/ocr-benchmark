We have the following subsequent corollary.

Corollary 1. Let Cσ be an unbalanced signed cycle, then p+(Cσ) ≥ 2. Yu et al. [18] calculated the positive inertia of signed path Pnσ.

- Lemma 6. Let Pnσ be a signed path of order n, then p+(Pnσ) = ⌊n2⌋. Yu et al. [4, Theorem 3.1] characterized all connected signed graph Gσ with p+(Gσ) = 1.

- Lemma 7. Let Gσ be a connected signed graph. Then p+(Gσ) = 1 if and only if Gσ is a balanced complete multipartite signed graph.

The length of a signed path (or simply a path) Pσ refers to the total number of edges in Pσ. For any two vertices y and z, the distance between them, denoted by d(y,z), is defined as the length of the shortest path between y and z.

- Lemma 8. Let Gσ be a connected signed graph with girth gr and let Cσ be a shortest cycle in Gσ. If y,y′ ∈ V (Cσ) and there exists a path Pσ of length k from y to y′ satisfying (V (Pσ)\{y,y′})∩V (Cσ) = ∅,

then

gr 2 ≤ k.

Proof. Remember that Cσ have two different paths from y to y′. The total length of both the paths equals the length of Cσ, i.e., gr. Thus, the shorter length of these paths is at most g2 . The shorter of these two paths from y to y′, followed by the path Pσ, forms a cycle of length at most g2r + k. Therefore, we obtain:

gr 2

+ k ≥ gr, and consequently

gr 2 ≤ k.

This concludes the proof.

<table>
  <tr>
    <td> </td>
  </tr>
</table>


Let Gσ[Hσ] be a subgraph of Gσ induced by Hσ, and let x be a vertex outside Hσ. We denote the distance between x and Gσ[Hσ] as: d(x,Gσ[Hσ]) = min{d(x,y) | y ∈ Hσ}. Next, we define Nj(Gσ[Hσ]) as:

Nj(Gσ[Hσ]) = {x ∈ V (Gσ) \ Hσ | d(x,Gσ[Hσ]) = j, j = 1,2,...,n}. The number of vertices in Nj(Gσ[Hσ]) is denoted by |Nj(Gσ[Hσ])|.

- Lemma 9. Let Gσ be a connected signed graph with girth gr, and let Cσ be a shortest cycle in Gσ. If p+(Cσ) = p+(Gσ), then Nj(Cσ) = ∅ for j ≥ 2.

Proof. Indeed, we only need to establish that N2(Cσ) = ∅. Suppose, for the sake of contradiction, that N2(Cσ) ̸= ∅. Let y′ ∈ N2(Cσ) and y′ ∼ y ∈ N1(Cσ). Then, y′ is a pendant vertex of Gσ[V (Cσ) ∪ {y,y′}]. Consequently,

p+(Gσ) ≥ p+(Gσ[V (Cσ) ∪ {y,y′}]) = p+(Cσ) + 1 > p+(Cσ),

by Lemmas 1 and 2, which contradicts the assumption that p+(Cσ) = p+(Gσ). Hence, N2(Cσ) = ∅, and therefore, Nj(Cσ) = ∅ for j ≥ 3. This completes the proof.

<table>
  <tr>
    <td> </td>
  </tr>
</table>


Smith [6] showed the following characterization.

- Lemma 10. A graph has precisely one positive eigenvalue if and only if the set of its non-isolated vertices constitute a complete multipartite graph.


5

