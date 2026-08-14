Using the universal property of THH(k) as a commutative algebra, we find that k⊗k⊗THH(k) k ≃ THH(k) ⊗ (k ⊗THH(k) k), and using now Bökstedt’s equivalence THH(k) ≃ k[ΩS3], we find k ⊗THH(k) k ≃ k[S3], so that, in total,

(Ω2nk ⊕ Ω2n+3k)

mapk⊗THH(k)(k,k) ≃

n

To get k-linear endomorphisms of HHk, one simply adjoins [S1] to this. ◁ Remark 3.4. In the previous examples, it is not clear to the author what the extra operations “do”. Similarly to the situation in Remark 2.15, we do not know how to “name” them, and it would probably be worthwhile to spend time figuring out what these operations do, or are. ◁

# 4 Operations on THH of O-algebras

The goal of this section is to initiate the study of endomorphisms of THH viewed as a functor AlgO(Catperf) → Sp, that is, to study the extra operations that arise on THH(C) when C has a particular kind of multiplicative structure encoded by a one-colored ∞-operad O. Our main result in this section is Theorem B.

As is clear from the statement of Theorem B, the case of endomorphisms of THH viewed as a functor on AlgO(Catperf) is more subtle.

We first describe the general approach to this question, and then specialize to get the precise results that we claimed.

We let U : AlgO(Catperf) → Catperf denote the forgetful functor, with a left adjoint F such that UF ≃ n(O(n) ⊗ (−)⊗n)hΣ

[Lur12, Proposition 3.1.3.13]. The idea now is that by general adjunction nonsense,

n

O(Catperf),Sp)(THH ◦ U,THH ◦ U) ≃ MapFun(Catperf,Sp)(THH,THH ◦ UF) and so we are “left with” understanding THH ◦ UF.

MapFun(Alg

For this, we compute each of the individual terms of THH ◦ UF =

THH((O(n) ⊗ (−)⊗n)hΣ

)

n

n

Proposition 4.1. Let O be a space with a Σn-action. There is an equivalence, natural in C ∈ Catperf:

(Oσ ⊗ THH(C)⊗n(σ))hC(σ)

THH((O ⊗ C⊗n)hΣ

) ≃

n

σ∈Σn/conj

where for σ ∈ Σn, n(σ) is the number of cycles appearing in σ, C(σ) is the centralizer of σ in Σn and Oσ = L(OhΣ

) ×LBΣn {σ} with its residual C(σ)-action13.

n

13Here, L denotes the free loop space, i.e. Map(S1, −).

16

