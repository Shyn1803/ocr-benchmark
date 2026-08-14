Since H2(Xan,OXan) is torsion free, any torsion element of H2(X;Z) vanishes under β. Therefore, to conclude the proof, it suffices to show α is an injection. Since H1(X,OX×an) is identified with the Picard group, to prove the desired injection, we only need to show H1(Xan,OXan) = 0. Using GAGA for Deligne-Mumford stacks, [Hal11, Proposition A.4], we have H1(Xan,OXan) = H1(X,OX). Since H1(X;Q) = 0, we also have H1(X;C) = 0, and hence we conclude H1(X,OX) = 0 using [Sat12, Corollary 1.7], which says that the Hodge de Rham spectral sequence degenerates for smooth proper Deligne-Mumford stacks. □

7.3. Proving the stable Picard rank conjecture. We now aim to prove Theorem 7.1.1. To do this, we next compute the first two stable cohomology groups of [[CHurPG1,c,n /G]/ PGL2]. To do so, we need a basic lemma about the number of connected components of Hurwitz spaces.

- Lemma 7.3.1. Let G be a group and c ⊂ G a conjugacy class generating G. For n sufficiently large, the set of connected components of CHurcn with boundary monodromy g ∈ G is either empty or forms a torsor under H2(G, c); it is nonempty if and only if the image of n in Gab (under the map Z → Gab sending the positive generator to the image of any element of c) agrees with the image of g in Gab.

Rephrasing the statement above, there are H2(G, c) many components if the image of n in Gab agrees with the image of g, and 0 components otherwise.

Proof. This essentially follows from [Woo21] as we now explain. Indeed, using [Woo21, Theorem 2.5 and Theorem 3.1] we can identify the number of components of CHurcn for n sufficiently large with the set of elements in a certain reduced Schur cover Sc → G having the same image in Gab as n. Moreover, the boundary monodromy of these components is the same as their image in G under the map Sc → G. The kernel of Sc → G is identified with H2(G, c) and so connected components with boundary monodromy g either form a torsor under H2(G, c) when the image of n in Gab agrees with the image of g, or else there are no such connected components. □

For the next lemma and its proof, the reader may wish to recall notation from Notation 2.4.1.

- Lemma 7.3.2. Let G be a group, c ⊂ G be a conjugacy class generating G, and R := Z[1/2|G|]. For n sufficiently large depending on c and for each component Z ⊂ [CHurPG1,c,n /G], with corresponding component Z ⊂ [[CHurPG1,c,n /G]/ PGL2], we have


- H1(Z; R) = H1(Z; R) = 0,
- H2( Z; R) = H2(Z; R) = ((Z/(2n − 2)Z) ⊗ R) .


Proof. Taking g = id in Lemma 7.3.1, we obtain that for n sufficiently large, both [CHurG,c,∂∈id

n /G]

and [CHurPG1,c,n /G] have |H2(G, c)| many connected components. Indeed, the statement for [CHurG,c,∂∈id

n /G] follows from Lemma 7.3.1 and the fact that G conjugation acts trivially on H2(G, c) as it is identified with the central kernel of Sc → G by definition. Since [CHurG,c,∂∈id

n /G] is dense open in [CHurPG1,c,n /G], we obtain [CHurPG1,c,n /G] also has

30

