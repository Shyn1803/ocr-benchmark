HYPERSPECTRAL ANOMALY DETECTION 15

It is evident that G1 and G2 are Lipschitz continuous on any bounded set. From Lemma 2(3), we know that Wt is bounded. Hence, we obtain

Vt+1 ≤ ϖ Wt+1 −Wt , (3.33) where ϖ = maxi∈[6]{ρi +lg} and lg is the maximum Lipschitz constant of G1 and G2. □ Lemma 4 The function F(W) is a Kurdyka-Łojasiewicz (KL) function.

Proof According to [5], the Frobenius norm functions λ21∥B∥2, λ23∥H−C ×3 B−E1∥2, and λ26∥C −D∗ ZT −E2∥2 are semi-algebraic functions. The terms λ2∥E1∥11φ and λ5∥E2∥11φ are also semi-algebraic functions because they are composed of semi-algebraic operations, including the Frobenius norm,

minimum, and finite summation. Similarly, λ4∥Z∥ψF,1, which involves only the Frobenius norm and finite summation, is semi-algebraic. The functions δB(B), δC(C), and δD(D) are semi-algebraic because they are indicator functions with semi-algebraic sets [5]. Hence, F(W) is semi-algebraic because it is a finite sum of semi-algebraic functions. Additionally, since F(W) is a proper continuous function, it follows from [5, Theorem 3] that F(W) is a KL function. This completes the proof. □

Finally, we provide a theoretical guarantee for the convergence of Algorithm 1.

- Theorem 4 Consider the sequence {Wt} obtained by Algorithm 1. Assuming that either Zt or E2t is bounded, the sequence {Wt} converges to a critical point of F(W).

Proof We begin by noting that Lemma 2(3) establishes the boundedness of the sequence {Wt}. Given this boundedness, the Bolzano-Weierstrass theorem ensures the existence of a convergent subsequence. Furthermore, by exploiting the continuity of F(W), along with the results derived from Lemmas 2, 3, 4, we can rigorously establish the desired conclusion as articulated in [2, Theorem 2.9]. □

3.7. Rank reduction strategy with validation mechanism

In this subsection, we propose a rank reduction strategy to decrease r, which is related to the dimensions of D ∈ Rn1×r×b and Z ∈ Rn2×r×b, thereby reducing the complexity of Algorithm 1. Unlike most decomposition methods that set a small initial r0, we set r0 = min{n1,n2} and leverage the algorithm’s inherent capability to adaptively reduce rt. This approach is initially supported by Theorem 2. Furthermore, we present the following theorem to substantiate our proposed rank reduction strategy.

- Theorem 5 There exists t# ∈ N such that Γ(Zt) = Γ(Zt+1) for each t ≥ t#, where Γ(Z) = {j | ∥Z(:, j,:)∥ ̸= 0, j = 1,...,r}.


Proof By Lemma 2 that limt→∞∥Zt+1 − Zt∥ = 0, there exists t# ∈ N such that ∥Zt+1 − Zt∥ < min{(2λˆ4(1− p))1/(2−p),ν} for each t ≥t#. Proving by contradiction, we assume that there exists t ≥t# such that Γ(Zt) ̸= Γ(Zt+1). Then there exists j ∈ r such that (a) Zt(:, j,:) ̸= 0 and Zt+1(:, j,:) = 0, or (b) Zt(:, j,:) = 0 and Zt+1(:, j,:) ̸= 0. Hence by (3.19), we have for both cases that

Zt+1 −Zt ≥ Zt+1(:, j,:)−Zt(:, j,:) ≥ min{(2λˆ4(1− p))1/(2−p),ν}, which yields a contradiction. The proof is complete. □

