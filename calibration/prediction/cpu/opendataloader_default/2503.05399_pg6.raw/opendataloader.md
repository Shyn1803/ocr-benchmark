6 VEDANSH ARYA, D. DE GENNARO, AND A. KUBIN Hence we conclude that there exists σ : [0,ℓi] → R2 such that

n1 ℓi

n2 ℓi

x(s) = x(0) +

s + σ2(s), and moreover

s + σ1(s), y(s) = y(0) +

![](<2503.05399_pg6_images/imageFile1.png>)

![](<2503.05399_pg6_images/imageFile2.png>)

- (2.6) σ(s) ∞ + σ′(s) ∞ ≤ Cε0.

By the implicit function theorem (see also [22, Lemma 3.4]), the curve Γi can be parametrized as a graph over the line Li with slope n1/n2 (where Li is a line parallel to x = 0 when n2 = 0) and passing through (x(0),y(0)) with height function fi ∈ C1,21(Li) with

![](<2503.05399_pg6_images/imageFile3.png>)

- (2.7) fi C1(Li) ≤ Cε0.


Since Γi does not bound, there exists a unique Γ˜i such that Γi ∪ Γ˜i is the boundary of a connected component Ei of E. By the previous arguments, also Γ˜i is a small C1,21-deformation of a line L˜i parallel to Li. By parallel shifting the curves Γi and Γ˜i, we can ﬁnd a strip Si with boundary Li∪L˜i and |Ei| = |Si|. Thanks to (2.6), (2.7) still holds, possibly increasing C. By the area formula, it is easy to see that (see e.g. [7, Lemma 3.1])

![](<2503.05399_pg6_images/imageFile4.png>)

i) ≤ Cε20 = C κE − κ¯E 2L2(∂E).

0 ≤ P(Ei) − P(Si) ≤ C fi 2C1(L

We can then sum over all the connected components (whose number is bounded by M/2) to get the desired result. This completes the proof.

3. Asymptotic Behavior of the Mullins-Sekerka Flow

In this section we apply the quantitative Alexandrov Theorem (Theorem 1.2) to show the asymptotic of the Mullins-Sekerka ﬂow. We start by recalling the deﬁnition of ﬂat ﬂow solutions of the Mullins-Sekerka ﬂow, as given in [25, 37].

Let E ⊆ T2 be a measurable set with |E| = m, and consider the minimization problem

- (3.1) min P(F) +

h 2

![](<2503.05399_pg6_images/imageFile5.png>)

ˆ

T2

|∇UF,E|2 dx : |F| = |E| ,

where UF,E ∈ H1(T2) is the solution to

- (3.2) −∆UF,E =

1 h

![](<2503.05399_pg6_images/imageFile6.png>)

(χF − χE) in T2 with zero average. Let us set

- (3.3) D(F,E) := ˆ

T2

|∇UF,E|2 dx.

By the results of [25, 37], there exists a minimizer of (3.1), which may not be unique. Note also that, deﬁning the H−1-norm by duality as

f H−1(T2) := sup ˆ

T2

ϕf dx :  ∇ϕ L2(T2) ≤ 1 , pairing this deﬁnition with (3.2) and integrating by parts, we get

- (3.4) χF − χE 2H−1(T2) ≤ h2  ∇UF,E 2L2(T2) = h2 D(F,E).


