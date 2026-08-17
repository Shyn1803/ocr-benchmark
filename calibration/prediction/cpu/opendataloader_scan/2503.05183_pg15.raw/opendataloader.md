It is evident that G 1 and G 2 are Lipschitz continuous on any bounded set. From Lemma 2 (3), we know that W t is bounded. Hence, we obtain

where ϖ

$$
(3.33)
$$

Lemma 4 The function F ( W ) is a Kurdyka-Łojasiewicz (KL) function.

Proof According to [ 5 ], the Frobenius norm functions λ 1 2 ∥ B ∥ 2 , λ 3 2 ∥H−C × 3 B −E 1 ∥ 2 , and λ 6 2 ∥C −D∗ Z T −E 2 ∥ 2 are semi-algebraic functions. The terms λ 2 ∥E 1 ∥ 11 φ and λ 5 ∥E 2 ∥ 11 φ are also semi-algebraic functions because they are composed of semi-algebraic operations, including the Frobenius norm, minimum, and finite summation. Similarly, λ 4 ∥Z∥ ψ F , 1 , which involves only the Frobenius norm and finite summation, is semi-algebraic. The functions δ B ( B ) , δ C ( C ) , and δ D ( D ) are semi-algebraic because they are indicator functions with semi-algebraic sets [ 5 ]. Hence, F ( W ) is semi-algebraic because it is a finite sum of semi-algebraic functions. Additionally, since F ( W ) is a proper continuous function, it follows from [ 5 , Theorem 3] that F ( W ) is a KL function. This completes the proof. □

Finally, we provide a theoretical guarantee for the convergence of Algorithm 1 .

Theorem 4 Consider the sequence {W t } obtained by Algorithm 1 . Assuming that either Z t or E t 2 is bounded, the sequence {W t } converges to a critical point of F ( W ) .

Proof We begin by noting that Lemma 2 (3) establishes the boundedness of the sequence {W t } . Given this boundedness, the Bolzano-Weierstrass theorem ensures the existence of a convergent subsequence. Furthermore, by exploiting the continuity of F ( W ) , along with the results derived from Lemmas 2 , 3 , 4 , we can rigorously establish the desired conclusion as articulated in [ 2 , Theorem 2.9]. □

# 3.7. Rank reduction strategy with validation mechanism

In this subsection, we propose a rank reduction strategy to decrease r , which is related to the dimensions of D ∈ R n 1 × r × b and Z ∈ R n 2 × r × b , thereby reducing the complexity of Algorithm 1 . Unlike most decomposition methods that set a small initial r 0 , we set r 0 = min { n 1 , n 2 } and leverage the algorithm’s inherent capability to adaptively reduce r t . This approach is initially supported by Theorem 2 . Furthermore, we present the following theorem to substantiate our proposed rank reduction strategy.

Theorem 5 There exists t# € N such 2 t# where T(Z)

z' || =0 Or have for both cases that 1lz'+1 2t# 2'+1( we

      which yields a contradiction. The proof is complete.

$$
,V}
$$

