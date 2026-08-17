Since H 2 ( X an , O X an ) is torsion free, any torsion element of H 2 ( X ; Z ) vanishes under β . Therefore, to conclude the proof, it suffices to show α is an injection. Since H 1 ( X , O × X an ) is identified with the Picard group, to prove the desired injection, we only need to show H 1 ( X an , O X an ) = 0. Using GAGA for Deligne-Mumford stacks, [Hal11, Proposition A.4], we have H 1 ( X an , O X an ) = H 1 ( X , O X ) . Since H 1 ( X ; Q ) = 0, we also have H 1 ( X ; C ) = 0, and hence we conclude H 1 ( X , O X ) = 0 using [Sat12, Corollary 1.7], which says that the Hodge de Rham spectral sequence degenerates for smooth proper Deligne-Mumford stacks. □

7.3. Proving the stable Picard rank conjecture. We now aim to prove Theorem 7.1.1. To do this, we next compute the first two stable cohomology groups of [[ CHur G , c P 1 , n / G ] / PGL 2 ] . To do so, we need a basic lemma about the number of connected components of Hurwitz spaces.

Lemma 7.3.1. Let G be a group and c ⊂ G a conjugacy class generating G. For n sufficiently large, the set of connected components of CHur c n with boundary monodromy g ∈ G is either empty or forms a torsor under H 2 ( G , c ) ; it is nonempty if and only if the image of n in G ab (under the map Z → G ab sending the positive generator to the image of any element of c) agrees with the image of g in G ab .

Rephrasing the statement above, there are H 2 ( G , c ) many components if the image of n in G ab agrees with the image of g , and 0 components otherwise.

Proof. This essentially follows from [Woo21] as we now explain. Indeed, using [Woo21, Theorem 2.5 and Theorem 3.1] we can identify the number of components of CHur c n for n sufficiently large with the set of elements in a certain reduced Schur cover S c → G having the same image in G ab as n . Moreover, the boundary monodromy of these components is the same as their image in G under the map S c → G . The kernel of S c → G is identified with H 2 ( G , c ) and so connected components with boundary monodromy g either form a torsor under H 2 ( G , c ) when the image of n in G ab agrees with the image of g , or else there are no such connected components. □

For the next lemma and its proof, the reader may wish to recall notation from Notation 2.4.1.

Lemma 7.3.2. Let G be a group, c ⊂ G be a conjugacy class generating G, and R : = Z [ 1/2 | G | ] . For n sufficiently large depending on c and for each component   Z ⊂ [ CHur G , c P 1 , n / G ] , with corresponding component Z ⊂ [[ CHur G , c P 1 , n / G ] / PGL 2 ] , we have

$$
Hl(Ĩ;R) Hl (Z;R) 0, H2(Ĩ;R) H2(Z;R)
$$

$$
((Z/ (2n R) .
$$

  Proof. Taking g = id in Lemma 7.3.1, we obtain that for n sufficiently large, both [ CHur G , c , ∂ ∈ id n / G ] and [ CHur G , c P 1 , n / G ] have | H 2 ( G , c ) | many connected components. Indeed, the statement for [ CHur G , c , ∂ ∈ id n / G ] follows from Lemma 7.3.1 and the fact that G conjugation acts trivially on H 2 ( G , c ) as it is identified with the central kernel of S c → G by definition. Since [ CHur G , c , ∂ ∈ id n / G ] is dense open in [ CHur G , c P 1 , n / G ] , we obtain [ CHur G , c P 1 , n / G ] also has 30

