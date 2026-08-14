are central in the rest of this paper. It holds that

w⊥T Aw⊥ ≥ ρΛw⊥T Mw⊥ for all w⊥ ∈ E⊥≤ρΛ (4.1)

![](<2503.08465_pg8_images/imageFile1.png>)

![](<2503.08465_pg8_images/imageFile2.png>)

Let W⊥ be the basis matrix of E⊥≤ρΛ. Note that W can be obtained by solving few lowest eigenmodes of the pencil (A,M), whereas W⊥ is large, dense, and never available in a practical computation. In the following, we use the notation

![](<2503.08465_pg8_images/imageFile3.png>)

![](<2503.08465_pg8_images/imageFile4.png>)

B⊥ := W⊥TBW⊥, ∀B ∈ Rn×n. (4.2) We proceed to split eigenvectors of (1.1) as the sum of a component in E≤ρΛ and a

![](<2503.08465_pg8_images/imageFile5.png>)

correction term in E⊥≤ρΛ. A suitable splitting is given in Lemma 4.2 after a technical result.

![](<2503.08465_pg8_images/imageFile6.png>)

- Lemma 4.1. Assume that A : S → S++n×n is spectrally equivalent to A as in (3.1) with constants α and β. Let Λ > 0 and ρ be such that αρ > 1 and ρ > 1. Then the matrix A⊥(σ) − tM⊥ is positive deﬁnite for all (σ,t) ∈ S × (0;Λ). Proof. For all (σ,t) ∈ S × (0;Λ) and w⊥ ∈ E⊥≤ρΛ\{0}, from the spectral equivalence of A(σ) with A, we get

![](<2503.08465_pg8_images/imageFile7.png>)

![](<2503.08465_pg8_images/imageFile8.png>)

![](<2503.08465_pg8_images/imageFile9.png>)

w⊥T A(σ)w⊥ − tw⊥Mw⊥ ≥ αw⊥T Aw⊥ − tw⊥Mw⊥ ≥ (αρΛ − t) w⊥ 2M > 0 (4.3) as w⊥ ∈ E⊥≤ρΛ.

![](<2503.08465_pg8_images/imageFile10.png>)

![](<2503.08465_pg8_images/imageFile11.png>)

![](<2503.08465_pg8_images/imageFile12.png>)

![](<2503.08465_pg8_images/imageFile13.png>)

![](<2503.08465_pg8_images/imageFile14.png>)

![](<2503.08465_pg8_images/imageFile15.png>)

- Lemma 4.2. Make the same assumptions as in Lemma 4.1. Let σ ∈ S and (λ(σ),x(σ)) ∈


(0;Λ) × Rn \ {0} be a solution to (1.1). In addition, let W⊥ be a basis matrix of E⊥≤ρΛ. Then there holds that

![](<2503.08465_pg8_images/imageFile16.png>)

x(σ) = x(σ) + Z(σ,λ(σ))x(σ), (4.4) for x(σ) ∈ E≤ρΛ and correction operator Z(σ,t) : S × (0,Λ)  → Rn×n deﬁned as

![](<2503.08465_pg8_images/imageFile17.png>)

![](<2503.08465_pg8_images/imageFile18.png>)

![](<2503.08465_pg8_images/imageFile19.png>)

![](<2503.08465_pg8_images/imageFile20.png>)

Z(σ,t) = W⊥(W⊥T(A(σ) − tM)W⊥)−1W⊥TδA(σ) (4.5)

![](<2503.08465_pg8_images/imageFile21.png>)

with δA(σ) = A(σ) − A. Proof. Let σ ∈ S and split x(σ) = x(σ) + r(σ) with x(σ) ∈ E≤ρΛ and r(σ) = W⊥γ(σ) ∈ E⊥≤ρΛ. Then as (λ(σ),x(σ)) ∈ (0;Λ) × Rn is a solution of (1.1), we get

![](<2503.08465_pg8_images/imageFile22.png>)

![](<2503.08465_pg8_images/imageFile23.png>)

![](<2503.08465_pg8_images/imageFile24.png>)

![](<2503.08465_pg8_images/imageFile25.png>)

(A(σ) − λ(σ)M)x(σ) = −(A(σ) − λ(σ)M)W⊥γ(σ). (4.6)

![](<2503.08465_pg8_images/imageFile26.png>)

By orthogonality, we ﬁrst observe that W⊥TMx(σ) = 0 and W⊥TAx(σ) = 0. By multiplication with basis matrix W⊥T and using these identities gives

![](<2503.08465_pg8_images/imageFile27.png>)

![](<2503.08465_pg8_images/imageFile28.png>)

![](<2503.08465_pg8_images/imageFile29.png>)

W⊥T(A(σ) − A)x(σ) = −W⊥T(A(σ) − λ(σ)M)W⊥γ(σ). (4.7)

![](<2503.08465_pg8_images/imageFile30.png>)

![](<2503.08465_pg8_images/imageFile31.png>)

Then from Lemma 4.1, matrix in the right-hand side of equation (4.7) is invertible and we obtain −W⊥(W⊥T(A(σ) − λ(σ)M)W⊥)−1W⊥TδA(σ)x(σ) = W⊥γ(σ).

![](<2503.08465_pg8_images/imageFile32.png>)

![](<2503.08465_pg8_images/imageFile33.png>)

![](<2503.08465_pg8_images/imageFile34.png>)

![](<2503.08465_pg8_images/imageFile35.png>)

![](<2503.08465_pg8_images/imageFile36.png>)

![](<2503.08465_pg8_images/imageFile37.png>)

It is straightforward to estimate the A-norm of x(σ) appearing in (4.4). Recall that x(σ)TAW⊥ = 0 and using spectral equivalence (3.1) gives

![](<2503.08465_pg8_images/imageFile38.png>)

![](<2503.08465_pg8_images/imageFile39.png>)

![](<2503.08465_pg8_images/imageFile40.png>)

1 α

x(σ) A(σ). (4.8) As x(σ) is an eigenvector of the pencil (A(σ),M) corresponding to an eigenvalue on (0,Λ) and

x(σ) A ≤ x(σ) A ≤

![](<2503.08465_pg8_images/imageFile41.png>)

![](<2503.08465_pg8_images/imageFile42.png>)

![](<2503.08465_pg8_images/imageFile43.png>)

![](<2503.08465_pg8_images/imageFile44.png>)

x(σ) M = 1, it follows that

x(σ) A(σ) ≤ Λ1/2 and thus x(σ) A ≤

![](<2503.08465_pg8_images/imageFile45.png>)

![](<2503.08465_pg8_images/imageFile46.png>)

1 α

Λ1/2. (4.9)

![](<2503.08465_pg8_images/imageFile47.png>)

8

