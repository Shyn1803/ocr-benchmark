Proof. If λ ∈/ σ(D|J ) the resolvent R = (D − λI|J )−1 has the form Rx = ℓ(x)φλ + V (I − λV )−1x, with ℓ a continuous linear functional on C∞(D). Since Wϕ(λ) = 0 it follows that ϕλ(x) = ϕ(V (I − λV )−1x) = ϕ(Rx) = 0, for all x ∈ J . By the form of ϕ it follows easily that ϕλ has order N − 1 if N > 0. Moreover, Wϕλ(z) = ϕ(V (I − λV )−1φz)# = ϕ((z − λ)−1(φz − φλ))# = Wϕ(z) z − λ

![](<2503.08443_pg27_images/imageFile1.png>)

![](<2503.08443_pg27_images/imageFile2.png>)

![](<2503.08443_pg27_images/imageFile3.png>)

![](<2503.08443_pg27_images/imageFile4.png>)

![](<2503.08443_pg27_images/imageFile5.png>)

![](<2503.08443_pg27_images/imageFile6.png>)

![](<2503.08443_pg27_images/imageFile7.png>)

. (ii) follows by a repeated application of (i).

![](<2503.08443_pg27_images/imageFile8.png>)

![](<2503.08443_pg27_images/imageFile9.png>)

![](<2503.08443_pg27_images/imageFile10.png>)

![](<2503.08443_pg27_images/imageFile11.png>)

![](<2503.08443_pg27_images/imageFile12.png>)

![](<2503.08443_pg27_images/imageFile13.png>)

6.3 Residual subspaces and their annihilators

As pointed out before, we are especially interested in D−invariant subspaces J with σ(D|J ) = ∅. Such subspaces will be called residual. They possess an alternative characterization based on the following simple observation.

Lemma 3. If J ∈ J and p is a polynomial then p(D)J is closed. Proof. It suﬃces to show that (D − λI)J , λ ∈ C is closed. Let (xk) be a sequence in J such that (D − λI)xk → y ∈ H. Then there is a sequence (ck) in C such that

V (I − λV )−1(D − λI)xk = xk − ckφλ → V (I − λV )−1y, (30)

when k → ∞. If φλ ∈ J , it follows that (xk) converges to x ∈ J and y = (D − λI)x ∈ (D − λI)J . If φλ ∈/ J , let ϕ be a continuous linear functional in J ⊥ with ϕ(φλ) = 1. Then applying ϕ to both sides of (30) we obtain that (ck) converges and as above, we obtain that (xk) converges to x ∈ J and y = (D − λI)x ∈ (D − λI)J .

![](<2503.08443_pg27_images/imageFile14.png>)

![](<2503.08443_pg27_images/imageFile15.png>)

![](<2503.08443_pg27_images/imageFile16.png>)

![](<2503.08443_pg27_images/imageFile17.png>)

With the lemma in hand, the characterization of residual subspaces is as follows. Proposition 12. A subspace J ∈ J is residual if and only if

J = {p(D)J : p polynomial}.

Proof. If σ(D|J ) = ∅ we have (D − λ)J = J for all λ and the equality in the statement holds. Conversely, if the equality holds, then (D − λI)J = J for each λ. Suppose for a contradiction that D − λ0I is not injective for some λ0. Then for each j ≥ 0 there exists a nonzero xj ∈ J , such that (D − λ0)jxj = φλ

. From this it follows that Vλj

0 ∈ J for all j ≥ 0, and J = C∞(D) by Proposition 8 (ii).

φλ

0

0

![](<2503.08443_pg27_images/imageFile18.png>)

![](<2503.08443_pg27_images/imageFile19.png>)

![](<2503.08443_pg27_images/imageFile20.png>)

![](<2503.08443_pg27_images/imageFile21.png>)

Note that for every subspace J ∈ J we can consider its residual part

Jres = {p(D)J : p polynomial}. By the above proposition this is a closed residual subspace of J

Let us now turn to annihilators of residual subspaces. It turns out that these spaces can be described using the generalized Fourier transform W. To state our result we use the same notation as in Theorem 8, that is WH = e−iαzH(E), with α ∈ R.

27

