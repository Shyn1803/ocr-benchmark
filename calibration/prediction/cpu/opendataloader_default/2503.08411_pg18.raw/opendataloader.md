Before turning to the proof of Theorem 3.15, we gather a few facts relating hyperplanes and relative contact complexes.

Proposition 3.17. Let X be a quasi-median graph and G be a collection of gated subgraphs. For a finite collection of hyperplanes J of X, the following statements are equivalent:

- • J is a simplex of Cont△(X,G);
- • there exists Y ∈ G and x ∈ Y ∩ J∈J N(J) such that Y contains the clique of J containing x for each J ∈ J .


Moreover, if G is a star-covering collection of gated subgraphs, the above statements are equivalent to:

• for every x ∈ J∈J N(J), there exists Y ∈ G that contains the clique of J containing x for each J ∈ J .

Proof. Suppose J = {J1,...,Jn} is a simplex of Cont△(X,G). Then there exists Y ∈ G such that {N(J1),...,N(Jn)} ∪ {Y } is a collection of pairwise intersecting gated subgraphs, and the Helly property implies that Y ∩ ni=1 N(Ji) is non-empty. Let x ∈ Y ∩ ni=1 N(Ji). Since Ji crosses Y , the clique of Ji containing x is contained in Y by Corollary 2.6. That the second and third statements imply the first one follows directly from the definitions.

Let us prove that the first statement implies the third one assuming that G is starcovering. Let J = {J1,...,Jn} be a simplex of Cont△(X,G) and x ∈ J∈J N(J). The hyperplanes in J are pairwise in contact, and there exists Z ∈ G such that each J ∈ J crosses Z. If x ∈ Z ∩ ni=1 N(J), then Corollary 2.6 implies that the clique of J containing x is contained in Z for each J ∈ J ; in this case, it suffices to set Y := Z. Suppose that x ̸∈ Z ∩ ni=1 N(Ji) and let J be a hyperplane separating x from Z, which we can choose to be tangent to x. Let C be the clique of J containing x. Since G is star-covering, there exists Y ∈ G containing all the prisms that contain C. For every 1 ≤ i ≤ n, let Ci be the clique of Ji containing x. Since J is necessarily transverse to Ji, Proposition 2.10 implies that C and Ci span a prism containing x, and hence Ci is contained in Y .

<table>
  <tr>
    <td> </td>
  </tr>
</table>


The rest of the section is dedicated to the proof of Theorem 3.15. We fix a quasi-median graph X and a collection G of gated subgraphs. The equivalence of the two statements of Theorem 3.15 will be proven in Lemma 3.20 by showing that for each vertex x ∈ X, sLG(x) is homotopy equivalent to LG(x).

Let X⊙ be the perforation of X, i.e. the space obtained from the prism-completion X□ of X by removing a small open ball around each vertex of a fixed radius ϵ < 1/2, if we endow X□ with a length metric that extends the Euclidean metrics on its prisms. Given a vertex x ∈ X, the sphere S(x,ϵ) can be identified with the link of x in the prismcompletion X□. In other words, we can think of S(x,ϵ) as the simplicial complex whose vertices are the edges of X containing x and whose simplices are given by collections of edges contained in a common prism of X.

When G is prism-covering, the complex LG(x) naturally contains S(x,ϵ) as a subcomplex, which allows us to define

XG := X⊙ ∪

x∈X

where each LG(x) is glued to X⊙ over S(x,ϵ).

LG(x)

18

