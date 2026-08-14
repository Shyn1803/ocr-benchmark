# J Guarantee for UncertainStateAction

In this section, we present the main guarantee of UncertainStateAction (Algorithm 6) as a standalone algorithm; see Lemma J.1. Then, in Lemma J.2, we provide its guarantee when used as a subroutine within MTSS (Algorithm 4). For a discussion of the motivation for these results, we refer back to Section I.1.3.

Lemma J.1. Consider a call to UncertainStateActionh(C0:h−1, π1:h,Σh;a,N,N) (Algorithm 6) for some given h,C0:h−1, π1:h,Σh, a ∈ A, N, and N such that σmin(Σh) ≥ λ, for some λ ∈ (0,1). Then, for any δ′ ∈ (0,1) and ζ ∈ (0,1/2), with probability at least 1 − δ′, the output (ˆxh,aˆh) of UncertainStateAction satisfies:

- • For all ℓ ∈ [0..h − 1] and (xℓ,aℓ) ∈ Cℓ,

P π

ℓ+1:h ∥φh(xh,ah)∥2Σ−1

h

> 2 ζ ∨ ∥φh(ˆxh,aˆh)∥2Σ−1

h

| xℓ = xℓ,aℓ = aℓ ≤ max h∈[H]

4log 16H|C

h| λδ′ζ

N

, (90)

where φh(·,·) := ϕh(·,·) − ϕh(·,a).

- • Furthermore, there exists Xh,span ⊆ X such that for all ℓ ∈ [0..h − 1] and (xℓ,aℓ) ∈ Cℓ, P π


[xh ∈ Xh,span | xℓ = xℓ,aℓ = aℓ] ≥ 1 − maxh∈[H] N4 log 32HN|C

ℓ+1:h−1

h| λδ′ζ and

> 2 ζ ∨ ∥φh(ˆxh,aˆh)∥2Σ−1

h,ref(·|xh) ∥φh(xh,a)∥2Σ−1

∀xh ∈ Xh,span, Pa∼π

h

h

4log 16H|C

h| λδ′ζ

. (91)

≤ max

N

h∈[H]

Proof of Lemma J.1. Fix δ′ ∈ (0,1) and ζ ∈ (0,1/2), and let Γ := {ζ,2ζ,...,⌈ζλ4 ⌉ζ}. Further, for ℓ ∈ [0..h − 1] and (xℓ,aℓ) ∈ Cℓ, let Dℓ(xℓ,aℓ) be the dataset in Algorithm 6 when the algorithm returns. Note that Dℓ(xℓ,aℓ) consists of N i.i.d. pairs sampled from P π

[(xh,ah) = · | xℓ = xℓ,aℓ = aℓ]. Thus, by Freedman’s inequality (Lemma C.2) and the union bound over ℓ ∈ [0..h − 1], (xℓ,aℓ) ∈ Cℓ, and γ ∈ Γ, there is an event E of probability at least 1 − δ′/2 under which,

ℓ+1:h

ℓ+1:h ∥φh(xh,ah)∥2Σ−1

∀ℓ ∈ [0..h − 1],∀(xℓ,aℓ) ∈ Cℓ,∀γ ∈ Γ, P π

≥ γ | xℓ = xℓ,aℓ = aℓ ≤

h

4log(2H|Cℓ||Γ|/δ′) N

2 N

I ∥φh(x,a)∥2Σ−1

> γ +

,

h

(x,a)∈Dℓ(xℓ,aℓ)

4log 16H|C

ℓ| λδ′ζ

2 N

I ∥φh(x,a)∥2Σ−1

, (92)

≤

> γ +

N

h

(x,a)∈Dℓ(xℓ,aℓ)

where the last step follows by the facts that |Γ| ≤ ⌈ζλ4 ⌉, λ ∈ (0,1), and ζ ∈ (0,1/2). Now, since σmin(Σh) ≥ λ and sup(x,a)∈X×A ∥ϕh(·,·)∥ ≤ 1 (Assumption H.1), we have that sup(x,a)∈X×A ∥φh(x,a)∥2Σ−1

≤ λ4. Therefore, by the definition of Γ, we have that for all ℓ ∈ [0..h−1] and (xℓ,aℓ) ∈ Cℓ, there exists γℓ(xℓ,aℓ) ∈ Γ such that

h

∥φh(x,a)∥2Σ−1

≤ γℓ(xℓ,aℓ), ≤ max

max

(x,a)∈Dℓ(xℓ,aℓ)

h

∥φh(x,a)∥2Σ−1

+ ζ,

(x,a)∈Dℓ(xℓ,aℓ)

h

∥φh(x,a)∥2Σ−1

≤ 2 ζ ∨ max

,

(x,a)∈Dℓ(xℓ,aℓ)

h

≤ 2 ζ ∨ ∥φh(ˆxh,aˆh)∥2Σ−1

, (93) where the last inequality follows by the fact that

h

≤ ∥φh(ˆxh,aˆh)∥2Σ−1

∥φh(x,a)∥2Σ−1

max

max

ℓ∈[0..h−1]

(x,a)∈Dℓ(xℓ,aℓ)

h

h

## 68

