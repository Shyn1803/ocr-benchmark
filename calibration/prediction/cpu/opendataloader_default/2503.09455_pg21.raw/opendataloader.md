SHELUKHIN’S QUASIMORPHISM AND REZNIKOV’S CLASS 21

Proposition 5.1. Let (M,ω) be a closed symplectic manifold. Assume that Shelukhin’s quasimorphism SM on Hamc(M,ω) is not extendable to Sympc0(M,ω). Then R0 ∈ H2(Sympc0(M,ω)) is non-zero. In particular, the Reznikov class R ∈ H2(Sympc(M,ω)) is non-zero.

Before proving the proposition, we discuss the vanishing of the Reznikov class in a more general setting. Let M be a closed symplectic manifold. Let G be a subgroup of Sympc0(M,ω) which contains Hamc(M,ω) and set G = p( G), where p: Sympc0(M,ω) → Sympc0(M,ω) is the universal covering map. Consider the following commutative diagram:

Hamc(M,ω) i0

# G i1

# Sympc0(M,ω)

p

p

p

Hamc(M,ω) i0 G i1 Sympc0(M,ω). Here i0, i1,i0 and i1 are the inclusions. Lemma 5.2. The following are equivalent.

- (1) i∗1R0 ∈ H2(G) is zero.
- (2) There exists ϕ ∈ Q(G) such that i0∗p∗ϕ = SM.


Proof. To prove that (1) implies (2), we assume that i∗1R0 = 0. Recall that bJ is a cocycle representing the Reznikov class. Then there exists u ∈ C1(G) such that i∗1bJ = δu. Since bJ is a bounded cocycle, u is a quasimorphism. Recall from (2.4) that −δνJ = p∗i∗0i∗1bJ. Hence we have

−δνJ = p∗i∗0δu = δ(p∗i∗0u) = δ( i0∗p∗u). This implies that νJ + i0∗p∗u: Hamc(M,ω) → R is a homomorphism. Because Hamc(M,ω) is perfect ([Ban78]), we have νJ = − i0∗p∗u. Let ϕ be the homogenization of −u. Then we have SM = i0∗p∗ϕ.

To prove that (2) implies (1), we assume (2) and take ϕ ∈ Q(G) satisfying i0∗p∗ϕ = SM. Since SM is the homogenization of νJ, there exists a bounded function v: Hamc(M,ω) → R such that SM = νJ + v. Then we have

−δνJ = −δ(SM − v) = δv − δ i0∗p∗ϕ = δv − p∗i∗0δϕ. Together with −δνJ = p∗i∗0i∗1bJ, we have

p∗i∗0(i∗1bJ + δϕ) = δv. Note that i∗1bJ +δϕ is a bounded cocycle on G. Since v is a bounded function, the second bounded cohomology class p∗i∗0[i∗1bJ +δϕ] of Hamc(M,ω) is zero. Since G/Hamc(M,ω) is abelian, the bounded cohomology H2b(G/Hamc(M,ω)) is zero. In particular, the map i∗0: H2b(G) → H2b(Hamc(M,ω)) is injective by (2.2). Moreover, since p: Hamc(M,ω) → Hamc(M,ω) is surjective, the map

