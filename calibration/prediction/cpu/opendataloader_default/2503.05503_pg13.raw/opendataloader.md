STEADY BUBBLES AND DROPS IN INVISCID FLUIDS 13

Our analysis is structured as follows. We introduce the correct functional analytic setup in Section 3, where we also prove the Fre´chet diﬀerentiability of J and C and give formulas for their derivatives. In Section 4 we provide the proof of Theorem 2.1.

3. Analysis of the functional F

In this section, we study the regularity properties of the functional F and derive and analyze its linearization. First, we introduce the underlying function spaces for functions η: S2 → R and recall some important facts on Sobolev spaces on the sphere.

3.1. Sobolev spaces on the sphere. We denote by L2(S2) the space of square-integrable functions on the sphere equipped with the uniform measure dσ(x) = sin(θ)dϕdθ (which is the same as the Hausdorﬀ measure on S2 up to a constant factor) and we write  ·,·  for the induced L2 scalar product.

Our analysis is based on the fact that spherical harmonics {Ylm : l ∈ N0, −l ≤ m ≤ l} form an orthonormal eigenbasis of the Laplace–Beltrami operator on the sphere ∆S2 with respect to the L2(S2) scalar product. The corresponding eigenvalues −l(l +1) have the multiplicity 2l + 1. We have the expansion

l

∞

f,Ylm Ylm, (3.1)

f =

m=−l

l=0

for any f ∈ L2(S2). We recall that spherical harmonics can be expressed as Ylm(θ,ϕ) = cl,mPlm(cos θ)eimϕ, (3.2)

![](<2503.05503_pg13_images/imageFile1.png>)

where cl,m = (2l4+1)π ((ll−+mm)!)! are positive constants and Plm are the associated Legendre polynomials. We refer the reader e.g. to [44] for background reading.

![](<2503.05503_pg13_images/imageFile2.png>)

![](<2503.05503_pg13_images/imageFile3.png>)

For β > 0, we deﬁne the Sobolev space Hβ(S2) as the space of all functions f ∈ L2(S2) with

l

∞

(1 + l)2β | f,Ylm |2 < ∞.

f 2Hβ(S2) =

m=−l

l=0

These spaces can be equivalently deﬁned via smooth charts [27], and thus, they arise as the trace spaces of Hβ+12(B1(0)), cf. (3.8). For integer exponents β ∈ N, they coincide with the classical Sobolev spaces deﬁned via diﬀerentiation on the manifold.

![](<2503.05503_pg13_images/imageFile4.png>)

For notational convenience, we introduce a subspace of Hβ(S2) that reﬂects the symmetric setting we restrict to in (1.23). Deﬁnition 3.1. Let β ≥ 0. We deﬁne

π 2 − θ = f

π 2

Hβsym(S2) := f ∈ Hβ(S2) : f = f(θ) with f

+ θ , the subspace of all axisymmetric functions in Hβ(S2), which are symmetric in x3.

![](<2503.05503_pg13_images/imageFile5.png>)

![](<2503.05503_pg13_images/imageFile6.png>)

The following characterization will be beneﬁcial for our analysis. Lemma 3.2. For all β ≥ 0 we have

Hβsym(S2) := f ∈ Hβ(S2) : f,Ylm = 0 if l is odd or m = 0 . (3.3)

