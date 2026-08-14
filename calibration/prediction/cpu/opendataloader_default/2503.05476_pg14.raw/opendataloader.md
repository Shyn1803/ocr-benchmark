14 GEROLD ALSMEYER, KONRAD KOLESKO, MATTHIAS MEINERS, AND JAKOB STONNER

Deﬁne a0 := ∞, an := k≥n µ−+1(δk)/k for n ∈ N, and the function ψ by ψ(t) :=

δn (a

n+1,an](t), t ≥ 0.

n∈N0

Then

δ 4(2 + δ)

µ−+1(1).

F(t) ≤ ψ(4t) for all t ≤ t0 :=

![](<2503.05476_pg14_images/imageFile1.png>)

Proof. The assumptions imply that µ+ is continuous and strictly increasing and hence is the cumulative mass function of a continuous measure on [0,∞). Moreover, µ+ is a bijection of [0,∞), and its generalized inverse µ−+1 is simply the inverse function. Let ψ0 = ψ, and for n ∈ N, deﬁne ψn recursively by

ψn+1(t) := 1 − exp − ψn(t) −

t/4

ψn(t − 4x)µ+(dx) , t ≥ 0.

0

Denote by T denoting the smoothing transform associated with the Poisson point process with intensity measure µ = δ0 + µ+ as given by (3.2) and its representation (5.1). By induction, we observe that

1 − ψn(4t) = Tn 1 − ψ(4(·)) (t), t ≥ 0. Thus, by Theorem 3.4(b), we infer that ψn(4t) → F(t) as n → ∞ for all t > 0.

To complete the proof, it remains to show that ψn(t) ≤ ψ(t) holds for all t ≤ 4t0 and n ∈ N0. We will prove the slightly stronger statement ψn(t) ≤ ψ(t) for all t ≤ ak

via induction on n, where k0 ∈ N0 is chosen such that

0

. (5.3)

ak

0+1 < 4t0 ≤ ak

0

For n = 0, the claim is trivially true (base case). For the inductive step, assume ψn(t) ≤ ψ(t) for all t ≤ ak

and some n ∈ N0. We will show that ψn+1(t) ≤ ψ(t) for all t ∈ (ak+1,ak] and k ≥ k0. If k0 = 0, for t > a1 we clearly have ψ(t) = 1 ≥ ψn+1(t). Thus we can assume k ≥ k0 ∨ 1. Let t ∈ (ak+1,ak] for k ≥ k0 ∨ 1. Then we have

0

ak/4

ψn+1(t) ≤ ψn+1(ak) = 1 − exp − ψn(ak) −

ψn(ak − 4x)µ+(dx)

0

ak/4

≤ 1 − exp − ψ(ak) −

ψ(ak − 4x)µ+(dx)

0

= 1 − exp − (ψ(t) + Ik) where Ik represents the integral in the exponent. To estimate Ik, we ﬁrst note that

ak/4

ψ(ak − 4x)µ+(dx) =

Ik =

ψ(ak − 4x)µ+(dx)

0

j≥k [ak−aj,ak−aj+1)/4

ak − aj 4

ak − aj+1 4

δj µ+

− µ+

=

![](<2503.05476_pg14_images/imageFile2.png>)

![](<2503.05476_pg14_images/imageFile3.png>)

j≥k

∞

ak − ak+j+1 4

ak − ak+j 4

δj µ+

= δk

− µ+

![](<2503.05476_pg14_images/imageFile4.png>)

![](<2503.05476_pg14_images/imageFile5.png>)

j=0

∞

ak − ak+j+1 4

δj(1 − δ)µ+

= ψ(t)

,

![](<2503.05476_pg14_images/imageFile6.png>)

j=0

