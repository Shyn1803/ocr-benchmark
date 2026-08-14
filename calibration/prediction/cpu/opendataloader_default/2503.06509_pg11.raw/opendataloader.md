/ 00 (2025) 1–33 11

∂Hj(x∗) . Since, Conv

∂Hj(x∗) and {0} are closed and convex sets

On contrary, assume that 0 Conv

j∈Λ

j∈Λ

then with the help of theorem of separation, there exists v ∈ Rn and b ∈ R such that vT0 ≥ b and vTd < b ∀d ∈ Conv

∂Hj(x∗) .

∂Hj(x∗) . Jointly both inequality contradicts (3.1). Hence, 0 ∈ Conv

j∈Λ

j∈Λ

∂Hj(x∗) , then x∗ is a Pareto critical point for H. For this

Conversely, it needs to be proven that if 0 ∈ Conv

j∈Λ

purpose, define H˘(x) = max

Hj(x) − Hj(x∗). Then, by item (ii) of Theorem 2.2, ∂H˘(x) = Conv

∂Hj(x) . Hence,

j∈Λ

i∈Λ

H˘(x). On the contrary, if x∗ is not a Pareto

∂Hj(x) , implying x∗ = argmin x∈D

the assumption leads to 0 ∈ Conv

i∈Λ

critical point, then according to Definition 2.3, there exists s ∈ D such that ∇hj(x∗,ξi)T s < 0, for all i ∈ Ij(x∗), j ∈ Λ, i.e., H′

j(x∗, s) < 0 for all j. Then there exists some η > 0 sufficiently small such that Hj(x∗ + ηs) < Hj(x∗) for all j

H˘(x). As a consequence, the assumption that x∗ is not a Pareto critical point is incorrect, and x∗ is indeed a Pareto critical point for H.

which implies H˘(x∗ + ηs) < 0 = H˘(x∗) holds for some (x∗ + ηs) ∈ D. This contradicts the fact that x∗ = argmin x∈D

<table>
  <tr>
    <td> </td>
  </tr>
</table>


Theorem 3.1. If hj(x,ξi) is continuously differentiable and convex for each j ∈ Λ and ξi ∈ U, then x∗ ∈ D is a weak efficient solution solution for OWCP(U) if and only if

0 ∈ conv ∪mj=1∂Hj(x∗) .

Proof. Let x∗ be a weak efficient solution solution for OWCP(U). It must be shown that 0 ∈ Conv∪j∈Λ∂Hj(x∗). Since given function hj(x,ξi) is continuously differentiable and convex for each j and ξi ∈ U, then hj(x,ξi) will be locally Lipschitz continuous for all i ∈ Λ¯ . Then 0 ∈ Conv{∪j∈Λ∂Hj(x∗)} (see Theorem 4.3 in [71] ). Conversely, by assumption 0 ∈ Conv{∪j∈Λ∂Hj(x∗)} it is clear that x∗ is Pareto critical point. Then for atleast one j0, it is established that H′

j0(x∗,d) ≥ 0, ∀ d ∈ D − {x∗}. Now, by using the Definition 2.2, it follows that

∇hj0(x∗,ξi)Td ≥ 0, ∀ d ∈ D, i ∈ Ij0(x∗). (3.2)

By convexity of Hj and hj(x,ξi), it is obtained that

hj0(x,ξi) ≥ hj0(x∗,ξi) + ∇hj0(x∗,ξi)T(x − x∗), ∀ i ∈ Ij0(x∗) and x, x∗ ∈ D. Since the last term of the latest inequality is positive by (3.2), it is established that

hj0(x,ξi) ≥ hj0(x∗,ξi), ∀ i ∈ Ij0(x∗), and therefore

Hj0(x) ≥ Hj0(x∗), ∀x ∈ D, i.e., x∗ is weak efficient solution.

<table>
  <tr>
    <td> </td>
  </tr>
</table>


11

