Our analysis is structured as follows. We introduce the correct functional analytic setup in Section 3, where we also prove the Fre´chet diﬀerentiability of J and C and give formulas for their derivatives. In Section 4 we provide the proof of Theorem 2.1.

# 3. ANALYSIS OF THE FUNCTIONAL J

In this section, we study the regularity properties of the functional F and derive and analyze its linearization. First, we introduce the underlying function spaces for functions η : S 2 → R and recall some important facts on Sobolev spaces on the sphere.

3.1. Sobolev spaces on the sphere. We denote by L 2 ( S 2 ) the space of square-integrable functions on the sphere equipped with the uniform measure d σ ( x ) = sin( θ )d ϕ d θ (which is the same as the Hausdorﬀ measure on S 2 up to a constant factor) and we write  · , ·  for the induced L 2 scalar product. m N

Our analysis is based on the fact that spherical harmonics { Y l : l ∈ 0 , − l ≤ m ≤ l } form an orthonormal eigenbasis of the Laplace–Beltrami operator on the sphere ∆ S 2 with respect to the L 2 ( S 2 ) scalar product. The corresponding eigenvalues − l ( l +1) have the multiplicity 2 l + 1. We have the expansion

$$
f = (3.1) 1=0 m=-1
$$

− for any f ∈ L 2 ( S 2 ). We recall that spherical harmonics can be expressed as

$$
Pm (cos (3.2)
$$

where c l,m =   (2 l +1) 4 π ( l − m )! ( l + m )! are positive constants and P m l are the associated Legendre polynomials. We refer the reader e.g. to [44] for background reading. β S 2 2 S 2

For β > 0, with

$$
IlfllẺ? (s2) (1 + 0O. 7)28
$$

− These spaces can be equivalently deﬁned via smooth charts [27], and thus, they arise as the trace spaces of H β + 1 2 ( B 1 (0)), cf. (3.8). For integer exponents β ∈ N , they coincide with the classical Sobolev spaces deﬁned via diﬀerentiation on the manifold. β S 2

For notational convenience, we introduce a subspace of H ( ) that reﬂects the symmetric setting we restrict to in (1.23).

Deﬁnition 3.1. Let β ≥ 0. We deﬁne

$$
Hsym (S2) (2 -0) = f (2+0)}
$$

the subspace of all axisymmetric functions in H β ( S 2 ), which are symmetric in x 3 .

The following characterization will be beneﬁcial for our analysis.

Lemma 3.2. For all β ≥ 0 we have

$$
(3.3)
$$

