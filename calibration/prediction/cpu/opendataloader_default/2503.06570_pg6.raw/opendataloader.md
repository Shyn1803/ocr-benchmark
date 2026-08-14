Continuous and Discrete Asymptotic Behaviours of the J-function 5

defined by the formal sum

⟨α,β,ϕℓ⟩0,3,d ϕℓ e⟨τ,d⟩ (⋄)

α ⋆τ β = α ∪ β +

d∈Eff̸=0, 0≤ℓ≤N−1

where Eff ⊆ H2(X,Z) is the set of effective curve classes.

The quantum product reduces to the classical cup product when ⟨τ,d⟩ → −∞ for non-zero effective class d ∈ Eff̸=0. When X is Fano, the degree axiom of Gromov-Witten invariants [12] implies that ⟨α,β,γ⟩0,3,d = 0 when deg α+deg β+ deg γ ̸= ⟨c1,d⟩. Therefore, the sum on the right-hand side of (⋄) is finite.

All the genus-0 Gromov-Witten invariants can be encoded within a connection, known as the Dubrovin conenction.

Definition 2.3 (Quantum Differential Equations [2, Chapter 10]). Let X be a Fano manifold. Let B be the trivial vector bundle with fibre H∗(X) over H2(X)× C×. Set the coordinate (τ,z) = ( b

2(X)

j=1 tjϕj,z) ∈ H2(X) × C×. The Dubrovin connection on B can be defined by:

1 z

∇∂tj

ϕj ⋆τ φ, ∇z∂z

φ =

1 z

φ = −

c1(X) ⋆τ φ + µ(φ),

where µ : H∗(X) → H∗(X); the Hodge grading operator, is a linear map defined by

- 1

- 2


(deg ϕℓ − dimX)ϕℓ, and φ ∈ H∗(X) is regarded as a constant section of the trivial bundle.

µ(ϕℓ) =

The Dubrovin connection is a flat connection. Its fundamental solution along the τ-direction, i.e., sections satisfying ∇∂tj

L(τ,z)α = 0 for all j = 1,...,b2(X), can be given by

L(τ,z)α := e−τ/zα −

ϕℓ,

d∈Eff̸=0 0≤ℓ≤dim H∗(X)−1

e−τ/zα z + ψ

e⟨τ,d⟩ϕℓ,

0,2,d

where the second argument of the coefficients is expanded as

1 z + ψ

∞

(−1)k z−(k+1) ψk.

=

k=0

By the linearilty of the Gromov-Witten invariants, the coefficients are a sum of the Gromov-Witten invariants with gravitational descendants.

