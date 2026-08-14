4 ANNE BOUTET DE MONVEL, KIRAN KUMAR A.S., MOSTAFA SABRI

dynamical delocalization result. However, assumption (1.3) is stronger than simply assuming the spectrum is AC, and this stronger assumption seems to be essentially necessary for ergodicity, see [7, Prp. 1.5] for a related result.

Some basic examples were given in [2, §3.2]: if ν = 1, i.e. the fundamental cell is simply one vertex, then the limiting measure is uniform. This covers the continuous quantum walk eitA on Zd and the triangular lattice for example. The same property is true for the hexagonal lattice and the infinite ladder, both of which have ν = 2. It was also shown that in the cases where Γ is a 1d strip of width 3, or a cylinder Z□C4, then the limiting distribution is not uniform.

1.2. Main results. In this note we analyze further families of graphs which satisfy our assumptions, and compute the limiting average ⟨a⟩p explicitly.

We first give the following result, extracted from [7].

Proposition 1.2 (Case of Cartesian and Tensor Products). Suppose Γ0 is a periodic graph with ν = 1 (for example Γ0 = Zd or the triangular lattice), and let GF be any finite graph with νF = |GF| vertices. Let Γ1 = Γ0 □GF be the Cartesian product , Γ2 = Γ0×GF be the tensor product and Γ3 = Γ0 ⊠ GF be the strong product of Γ0 and GF. Let EΓ0(θ) be the band function of Γ0, (wj) an orthonormal eigenbasis of AGF and (µj) the corresponding eigenvalues, j ≤ νF. Then

- (1) The band functions of AΓ1 are given by Ej(θ) = EΓ0(θ) + µj.
- (2) The band functions of AΓ2 are given by Ej(θ) = µjEΓ0(θ).
- (3) The band functions of AΓ3 are given by Ej(θ) = (1 + µj)EΓ0(θ) + µj.
- (4) Assumption (1.3) is satisfied for AΓ1 but not necessarily for AΓ2 or AΓ3.
- (5) For each of AΓ1,AΓ2 and AΓ3, we have


νF′

νF

|Pµs(vp,vq)|2 ,

⟨a⟩p =

⟨a(· + vq)⟩

q=1

s=1

j=µs wj(vp)wj(vq) is the (kernel) of the orthogonal projection for the distinct eigenvalues of the finite graph.

where Pµs(vp,vq) = j µ

For example, if Γ0 = Zd, then EΓ0(θ) = 2 di=1 cos2πθi and if Γ0 is the triangular lattice, then EΓ0(θ) = 2cos2πθ1 + 2cos2πθ2 + 2cos2π(θ1 + θ2), for θi ∈ [0,1). Here Γ1,2,3 are viewed as periodic graphs with fundamental domain containing νF vertices, cf. [7, Lemma 3.1, §3.4], with (vi) the vertices of GF.

Arguing as before, we get for these more special graphs that

ν′

1 Nd

1 Nd

|Pµs(vp,vq)|2 =:

(1.6) µNT,vp+na(ka + vq) ≈

d(p,q).

s=1

whenever (1.3) is satisfied. This gives a more satisfactory concept of a quantum limiting distribution than in [7] where quantum ergodicity was assessed by the behaviour of eigenvector bases, and it was shown in [7, §4.5] that such a limiting distribution depends on the eigenvector basis. In contrast, here the RHS of (1.6) depends only on the graph.

Our main target now is to compute the weights d(p,q) for specific finite graphs GF. Because of point (4) above, the theorems are illustrated only for the Cartesian product, but some hold more generally. For definiteness, the reader can assume Γ0 = Z in all these results, which is already interesting. However, nothing changes for any Γ0 having a single vertex in its fundamental domain, such as Zd and the triangular lattice.

A nice simplification in the family of Cartesian products is that the limiting weight d(p,q) in (1.6) depends only on the finite graph GF, compared to the general case (1.5), where the weight depends on the full Floquet matrix and computations become more daunting. Still, as we will see, Cartesian products already offer interesting contrasting

