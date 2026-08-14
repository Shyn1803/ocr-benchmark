TWENTY DRY MARTINIS FOR THE UAMO 5

(4) This is the first time a DTMP is showed for (GE)CMV matrices. Some results in Baire category for certain classes of almost periodic extended CMV matrices were previously obtained by [27,41]. It is an open question whether it holds for other CMV matrices with, for example, subshift or Sturmian Verblunsky coefficients.

We base our proof on the recent understanding of Anderson localization for Diophantine frequencies obtained in [20] and techniques developed therein: the Anderson localization for the UAMO in the supercritical setting λ1 < λ2 proved in [21] is a full measure result. In [20], an arithmetic version of Anderson localization is proved, albeit for a mosaic model where every other local coin in (2.1) is trivial. However, the proof of [20] works in a straightforward way for UAMO as well, compare also [52].

Theorem 2.4. Let Φ ∈ DC(κ,τ) and λ1 < λ2. Then for each “Φ-nonresonant” θ, i.e., each θ such that

- 1

- 2τ )


|sin2π(θ + nΦ)| < exp(−|n| does not hold for infinitely many n, Wλ

1,λ2,Φ,θ admits Anderson localization.

Proof. In the case Φ ∈ R \ Q and λ1 < λ2, according to [21, Theorem 2.9], the Lyapunov exponent characterizing the (typical) decay of generalized eigenfunctions is positive:

λ2(1 + λ′1) λ1(1 + λ′

1,λ2,Φ(z) ≥ log

> 0, (2.6) with equality if and only if z ∈ Σλ

Lλ

2)

1,λ2,Φ. The rest of the proof follows the same outline as the proof of [20, Theorem 6.3]. □ Remark 2.5. This result is a full measure result in θ. It is sharp in the sense that it cannot be strengthened to all θ [18].

We shall also need the following dynamical duality formulation of Autry-Andr´e duality for the UAMO, which can be seen as the reverse statement to [21, Theorem 2.4]. As such, we expect it to be of interest beyond this paper.

Theorem 2.6 (Aubry-Andre´ Duality). Let φ = φξ = φξ,+,φξ,− ⊤, ξ ∈ T be a solution to the generalized eigenvalue equation Wλ♯

1,λ2,ξ,Φφ = zφ which has the following form

ϕ ˇ+(ξ + nΦ) ϕˇ−(ξ + nΦ)

ψ ˇ+(ξ + nΦ) + iψˇ−(ξ + nΦ) iψˇ+(ξ + nΦ) + ψˇ−(ξ + nΦ)

φξ,n+ φξ,n−

1 √2

= e2πinθ

e2πinθ

=

. Let

ϕ ˇ+ ϕˇ−

ψ ˇ+ ψˇ−

1 √2

1 −i −i 1

(2.7)

=

with n-th Fourier coefficients ψn+ and ψn−, respectively. Then ψ = [ψ+,ψ−]⊤ solves the eigenvalue equation Wλ

1,λ2,Φ,θψ = zψ.

3. Preliminaries

Our proof of Theorem 2.1 utilizes techniques from the theory of one-frequency cocycles of CMV matrices, which we hence review in this section to keep the present treatise as self-contained as possible. We first review the construction of so-called Cantero-MoralVel´azquez matrices (CMV matrices), whose intimate connection with quantum walks on

