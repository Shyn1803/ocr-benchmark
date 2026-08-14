for some 0 < ω0 < ω˜ and suﬃciently small ǫ ∈ R. The spectral structure in combination with resolvent bounds proven uniformly in the parameter imply

Sǫ(τ)(I − Pǫ)u s,k e−ω

0τ (I − Pǫ)u s,k ,

and Pǫ Sǫ(τ) = eτ Pǫ for Pǫ denoting the spectral projection onto the eigenspace spanned by gǫ, see [30], Theorem A.1. For the nonlinearity Nǫ, we establish Lipschitz bounds by imposing again the above assumptions (1.19) on the Sobolev exponents and apply the estimates of Appendix A. With these results at hand we construct in Section 4.2 global, exponentially decaying strong Hrs,k-solutions of Eq. (1.20). For this, we use the standard approach and ﬁrst suppress the exponential growth induced by the symmetry eigenvalue λ = 1 by a correction with values in ranPǫ. In a second step we account for this using the T−dependence of the initial condition to determine the suitable blowup time Tǫ. In Proposition 4.10 we upgrade the constructed strong solutions to classical ones. By deﬁning

1 T − t

x T − t

vǫT(t, x) :=

, ψǫ(ξ) := |ξ|−1fǫ(|ξ|) (1.21) for x ∈ Rn and t ∈ [0, T) we get the following result. Theorem 1.6. Let n ≥ 5 and choose ǫ∗ > 0 as in Theorem 1.2. For ǫ ∈ R, |ǫ| ≤ ǫ∗, let vǫT be deﬁned as in Eq. (1.21) and let (s, k) ∈ R × N satisfy

ψǫ

![](<2503.04425_pg8_images/imageFile1.png>)

![](<2503.04425_pg8_images/imageFile2.png>)

n 2 − 1 +

- 1

![](<2503.04425_pg8_images/imageFile3.png>)

- 2n − 2


n 2 − 1 < s ≤

, k > n. (1.22)

![](<2503.04425_pg8_images/imageFile4.png>)

![](<2503.04425_pg8_images/imageFile5.png>)

Then there exist ω > 0 and 0 < ǫ ≤ ǫ∗ such that for every ǫ ∈ R, |ǫ| ≤ ǫ there are δ > 0 and M > 1 such that the following holds: For any pair of radial, real-valued functions ϕ0, ϕ1 ∈ S(Rn) satisfying

![](<2503.04425_pg8_images/imageFile6.png>)

![](<2503.04425_pg8_images/imageFile7.png>)

δ M

(ϕ0, ϕ1) H ˙ s∩H˙ k(Rn)×H˙ s−1∩H˙ k−1(Rn) <

, (1.23)

![](<2503.04425_pg8_images/imageFile8.png>)

there exists T = Tǫ ∈ [1 − δ, 1 + δ] and a unique radial solution v ∈ C∞([0, T) × Rn) to Eq. (1.14) with

v(0, ·) = vǫ1(0, ·) + ϕ0, ∂tv(0, ·) = ∂tvǫ1(0, ·) + ϕ1. Moreover, v blows up at (T, 0) and can be decomposed as

1 T − t

x T − t

T T − t

v(t, x) = vǫT(t, x) +

,

ϕ log

![](<2503.04425_pg8_images/imageFile9.png>)

![](<2503.04425_pg8_images/imageFile10.png>)

![](<2503.04425_pg8_images/imageFile11.png>)

for all (t, x) ∈ [0, T) × Rn, where ϕ ∈ C∞([0, T) × Rn) is radially symmetric and satisﬁes

ϕ(−log(T − t) + log T, ·) H ˙ r(Rn) δ(T − t)ω (1.24) for all r ∈ [s, k]. Furthermore,

(∂0 + Λ + 1)ϕ(−log(T − t) + log T, ·) H ˙ r−1(Rn) δ(T − t)ω. (1.25)

Finally, we rephrase the results of Theorem 1.6 in terms of normal coordinates using the equivalence of norms of corotational maps and their radial proﬁles, see [23], to obtain Theorem 1.3.

8

