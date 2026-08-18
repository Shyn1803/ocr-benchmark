- [13] Y. S. Samoilenko , Spectral Theory of Families of Self-Adjoint Operators, vol. 57, Springer Science & Business Media, 1991.
- [14] K. Sato and R. Kawamura , Uniqueness Analysis of Controllability Scores and Their Application to Brain Networks, 2024, https://doi.org/10.48550/arXiv.2408.03023 . [15] K. Sato and A. Takeda , Controllability Maximization of Large-Scale Systems Using Projected


K. SATO AND ATAKEDA , Controllability Maximization of Large-Scale_Systems Projected Gradient Method_ IEEE Control Systems Letters, 4 (2020), pp 821826. Using

K. SATO AND STERASAKI, Controllability_Scores_for_Selecting_Control_Nodes_of Large-Scale Network Systems, IEEE Transactions on Automatic Control, 69 (2024), pp. 4673 4680

T. H. SUMMERS , F L. CORTESI AND J. LYGEROS , On Submodularity and Controllability in Complex_Dynamical_Networks, IEEE Transactions on Control   of Network Systems, (2016), pP. 91-101_

S. TERASAKI AND K SATO, Minimal Controllability Problem on Linear Structural Descriptor Systems With Forbidden Nodes, IEEE Transactions on Automatic Control, 69 (2024), pp 527 534-

N K VISHNOI, Algorithms_for_Convex_Qptimization, Cambridge University Press; 2021.

T. YAMAMOTO, On_the_Eigenvalues of Compact_ Operators in Hilbert_Space, Numerische Mathematik, 11 (1968), pP. 211 219.

K. YosIDA, Functional_Analysis, Springer Berlin Heidelberg; 2012

# Appendix A. Proof of Theorem 3.9 .

In this section, we prove Theorem 3.9 .

Deﬁne S as

$$
(A.l) S : {bi}21 0 < bi b; =
$$

  where { a i } ∞ i =1 is a sequence deﬁned in Assumption 3.6 . Then, the following lemma holds.

Lemma A.1.

Proof. Let { β ( n ) } ∞ n =1 be a sequence in S , where β ( n ) : = { b ( n ) i } ∞ i =1 ∈ S . Since 0 ≤ b ( n ) 1 ≤ a 1 holds for any n ∈ N , the sequence { b ( n ) 1 } ∞ n =1 has a convergent subsequence { b (1 n ) 1 } ∞ n =1 . Similary, since 0 ≤ b (1 n ) 2 ≤ a 2 , { b (1 n ) 2 } ∞ n =1 also has a convergent subsequence { b (2 n ) 2 } ∞ n =1 . Repeating this procedure for each coordinate and applying the diagonal argument, we obtain a subsequence { β ( n n ) } ∞ n =1 . For all i ∈ N , the sequence { b ( n n ) i } ∞ n =1 converges, and 0 ≤ b ( n n ) i ≤ a ( i ) holds. Deﬁne c i : = lim n →∞ b ( n n ) i . Since 0 ≤ b ( n n ) i ≤ a i , it follows that | b ( n n ) i − c i | ≤ a i . Moreover, since   ∞ i =1 a i < ∞ , we can apply Lebesgue convergence theorem. This yields lim n →∞   ∞ i =1 | b ( n n ) i − c i | = 0, which implies that the subsequence { β ( n n ) } ∞ n =1 converges to c with respect to ℓ 1 norm. Furthermore, it is straightforward to verify that { c i } ∞ i =1 ∈ S . Thus, { β ( n ) } ∞ n =1 has a subsequence that converges in S . Therefore, S is compact.

Lemma A.2. Under Assumption 3.6 , the feasible region F is deﬁned as

$$
(A.2)
$$

where

$$
X = {{pi}21
$$

Then F is a convex set.

Proof. Since the convexity of S is straightforward, we show the convexity of X .

