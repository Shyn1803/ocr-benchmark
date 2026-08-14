6

However, in our work, we are interested in heat kernels on Lie groups. To make sense of the heat equation on a Lie group, the proper Riemannian structure needs to be chosen. For compact semi-simple Lie group G, the Riemannian structure (G,g) can be defined via Ad-invariant positive definite inner product (·,·) stemming from the Killing form 2.

Notice that although the group U(d) is compact, it is not semi-simple. Hence, the metric tensor stemming from the Killing form is only positive semi-definite. Indeed, one can check that such a metric tensor for U(1) ∼= S1 is identically zero, so it does not equip S1 with the Riemannian structure. This is in contrast with the construction from Example 1.

Of course, general Lie groups are not commutative. Hence, in order to study the heat equation on a compact Lie group G, non-commutative Fourier/harmonic analysis is needed. Fourier coefficients on a compact Lie group are calculated with respect to the irreducible representations (irreps) of the group. Generally, the object being transformed is the regular Borel measure on G. However, we focus on the related case of integrable functions f. In this case (see e.g. [34]), the Fourier coefficient fˆ(λ) is the operator in End(Vπ

) defined via

λ

fˆ(λ) =

π(g−1)f(g)dµ(g), (22)

G

where by Vπ

) with the norm √dλ|| · ||HS, where dλ := dim (Vπ

we denote the representation space of irrep πλ with highest weight λ. Equipping the space End(Vπ

λ

λ

) and the Hilbert-Schmidt norm ||u||2HS = Tr(uu∗), one can show that such the Fourier transform is an isomorphism of Hilbert spaces

λ

L2(G) ∼=

End(Vπ

), (23)

λ

π∈Gˆ

where Gˆ is the set of equivalence classes of irreps of G. Namely, we obtain a generalisation of the Plancherel’s theorem

dλ||fˆ(λ)||2HS. (24)

||f||22 =

|f(g)|2dµ(g) =

G

λ∈Gˆ

This is a consequence of the Peter-Weyl theorem.

Remark 1. The transform (22) is a generalization of the Fourier series. Indeed, suppose a compact group G is additionally abelian and connected (so is a torus). Take one-dimensional torus U(1) ∼= S1 for example. The unitary irreps πλ of U(1) are the homomorphisms U(1) → U(1) so they are of the form eiϕ  → eiλϕ for some integer λ. All irreps are one-dimensional and Sˆ1 ∼= Z. The Fourier coefficients of a function f : U(1) → C are

- 1

- 2π


π

fˆ(λ) =

e−iλϕf(eiϕ)dϕ, (25)

−π

which coincides with the Fourier coefficients of the corresponding 2π-periodic complex-valued function f˜ : R → C, f˜(x) = f(eix). Similarly, other results such as the completeness, orthogonality relations and Plancherel’s theorem generalise to the non-abelian case via the Peter-Weyl theorems and representation theory.

Heat kernels on simply-connected compact semi-simple Lie groups were studied in Ref. [32], together with a useful Poisson form. In Section IV we show how to apply those results for PU(d), which is not simply-connected.

# III. MAIN RESULTS AND APPLICATIONS

Below we summarise the main results of this paper and outline some of their applications.

Result 1. The main technical result of the paper is the construction of the polynomial approximation to the Dirac delta function HP(t)(·,σ) on PU(d), together with some of its properties. This allows us to summarise the key properties of the family of polynomial approximations of Dirac delta based on the trimmed heat kernels (see Theorem 3 for a precise statement.

2 Taking the negative of the negative-definite Killing form leads to the positive-definite scalar product.

