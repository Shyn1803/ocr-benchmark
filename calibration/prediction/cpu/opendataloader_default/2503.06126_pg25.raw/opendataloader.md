LIMIT OF QUASILINEAR EQUATIONS AND RELATED EXTREMAL PROBLEMS 25

One implication of this Gamma convergence is that: if un minimizes E˜n over g + W1,n (Ω), then any cluster point, say u, of un should minnimize E˜∞, i.e.

 ∇w L∞ .

u = arg min

w∈g+W01,∞(Ω)

Hence u is inﬁnity harmonic, i.e. the Gamma convergence of E˜n echoes the convergence of un. This can be regarded as an alternative proof for the classical result that −∆p is approximately an inﬁnity Laplacian when the constant exponent p is large.

Coming back to the Orlicz setting, in general, we cannot simply replace  ∇u Ln

with  ∇u LΦn(·) and expect a clean analogy for the above to hold. One reason is that the Luxemburg norm of an Orlicz space is not a complete parallel for the

usual Lp space. For example, Φ(x,s) = sp (p 1) a generalized Φ-function, its Luxemburg norm  · LΦ(·) is equivalent but not equal to  · Lp. Some scalings are needed to make them agree. For detailed dicussions of the scalings of generalized Orlicz spaces and its consequences on Luxemburg norms, we refer to [HH19, Section 3.4]. That being said, there are some situations where such analogy exists.

Theorem 11. Assume that Φn satisﬁes (4.3) and the unit normalization condition

- (6.4). Assume in addition that (a stronger version of (4.4)holds, i.e.)

lim

n→∞

p−n = ∞ and lim

n→∞

p+n p−n

![](<2503.06126_pg25_images/imageFile1.png>)

= 1. Let

E˜n : L1 (Ω)  →

| ∇u |LΦn(·) , u ∈ W1,Φ

n(·) (Ω); ∞, otherwise,

and

E˜∞ : L1 (Ω)  →

 ∇u L∞ , u ∈ W1,∞ (Ω); ∞, otherwise.

Then Γ L1 (Ω) - lim

n→∞

E˜n = E˜∞.

This can be proved by similar arguments as [BM15, Theorem 2]. We omit the details.

7. Comparison Principle and Uniqueness of the Limit Equation

Let un be the sequence of the unique continuous weak solution for equation (5.3). In Theorem 8 or Theorem 10, we have established that { ∇un Lm : p−n m} is bounded for all m > d and there is a subsequence of un which converges uniformly to the following limit equation

- (7.1)


−∆∞,Λu = 0, x ∈ Ω; u = g, x ∈ ∂Ω,

where

−∆∞,Λu = −∆∞u − |∇u| Λ (x,|∇u|),∇u . Remark 7. We shall show that the equation (7.1) has a unique continuous viscosity solution. Since un is continuous and { ∇un Lm : p−n m} is bounded for all m > d, the uniform convergence limit of every subsequence of un is again continuous. Hence the uniqueness result indicates that the whole sequence un, not just a subsequence, converges uniformly to the unique continuous viscosity solution of (7.1).

