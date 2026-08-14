Therefore,

+∞

1 (2π)3 S2

IE(z) =

0

= F−1F[J]

= J(z), z ∈ R3. The proof is complete.

F[J](kxˆ)eikxˆ·zk2dkdsxˆ

<table>
  <tr>
    <td> </td>
  </tr>
</table>


Note that, different from the acoustic and elastic source scattering problems, there exists nonradiating sources for the electromagnetic waves. Precisely, the electromagnetic far field patterns may vanish for the sources J satisfying divJ ̸= 0. We refer to [7, 17] for more details on the non-radiating electromagnetic sources. Physically, ρ := iω1 divJ is the charge density. We define

√µ 2π2 S2

+∞

H∞(ˆx,k)eikxˆ·zk2dkdsxˆ, z ∈ R3, (3.18)

IH(z) :=

0

+∞

ωF[ρ](kxˆ) − 4πi√εE∞(ˆx,k) eikxˆ·zkdkdsxˆ, z ∈ R3. (3.19)

1 (2π)3 S2

Iρ(z) :=

0

Following the arguments in the proof of Theorem 3.1, we obtain the following theorem. To avoid repetition, we omit the proof.

Theorem 3.2. For J ∈ H1(R3) 3, we have

IH = curlJ. If we know the charge density ρ ∈ L2(R3) in advance, we have Iρ = J.

We finally remark that, without any a priori information on the charge density, we can always reconstruct curlJ from the magnetic far field patterns.

# 4 Stability estimates for the discrete indicators

Definitely, the theorems in the previous two sections show that the indicators If,Ip,Is,IE and IH can be used to determine the full or partial information of unknown sources. In practice, the far field patterns are taken for finitely many observation directions and frequencies. Therefore, we have to consider the indicators in the form of a finite sum. In this section, we derive the stability analyses for such indicators.

We begin with the elastic source reconstructions in R2. The observation direction set is defined by

2lπ L

2lπ L

,sin

ΘL := cos

T

l = 0,1,··· ,L − 1 .

We take the circular frequencies ωm = m∆ω, m = 1,2,··· ,Λ. 8

