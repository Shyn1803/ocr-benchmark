# 4.1 Entanglement temperatures

Let a general multi-interval region in d = 2 (at the line t = 0) be A = ∪Ni=1(li,ri). In a CFT the modular Hamiltonian K of the vacuum is non local except for the case of a single interval. However, it was conjectured in [9, 10] that for multi-intervals there is a local term in K having the same universal structure for any CFT. This writes

Kloc = dxβ(x)T00(x), (4.1) where the “local inverse temperatures” are

2π

. (4.2)

β(x) =

n i=1

1

x−li − x−1r

i

The modular Hamiltonian for multi-interval regions in d = 2 is known explicitly for free massless scalar and fermions [24, 25], and the local term agrees with (4.1).

A clear operational definition of these entanglement temperatures is that they measure the ratio between the expectation value of the modular Hamiltonian and the energy for very localized high energy excitations:

⟨ψ|K|ψ⟩ ⟨ψ|H|ψ⟩

β(x) = lim

. (4.3)

E→∞ ,∆x→0

Here |ψ⟩ is an excitation above the vacuum localized in ∆x around the point x and has energy E. This limit can be argued to exist based on monotonicity of the relative entropy [9].

We will now show the universality of these entanglement temperatures in a more formal way. To test the entanglement temperatures we will be using a chiral field operator acting on the vacuum as the excited state probe. We would like to compute (for a real chiral field ϕ)

⟨0|ϕ(x)Kϕ(y)|0⟩ ⟨0|ϕ(x)Hϕ(y)|0⟩

β(x) = lim

. (4.4)

y→x

This measures the ratio between the modular energy K and the ordinary energy H. As a regularization we set x ̸= y and take the limit x → y.7 The modular operator K can be obtained from the modular flow ∆i τ = e−iKτ with K = −log ∆. We get the entanglement temperature as a limit of a modular evolved correlator

∂τ⟨0|ϕ(x)∆iτϕ(y)|0⟩ ∂y0⟨0|ϕ(x)ϕ(y)|0⟩

−

. (4.5)

β(x) = lim

lim

y→x

τ→0

For a general chiral field ϕ in a CFT, S. Hollands obtained a general structure of the modular evolved correlator [26]. From a clever use of the KMS condition for the modular flow and analyticity in the Euclidean plane Hollands maps the problem into a Riemann-Hilbert problem in the plane with a cut at A. His expression will be enough to get the entanglement temperatures by the limit (4.5).

Take a chiral field ϕ of dimension h. By locality h is a half integer number. The field is normalized such that

e−iπh

⟨0|ϕ(x)ϕ(y)|0⟩ =

(x − y − i0+)−2h . (4.6) Defining

Πl(x) =

N

(x − lj), Πr(x) ≡

j=1

N

(x − ri), Z(x) =

i=1

- 1

- 2π


ln(−Πl(x)/Πr(x)), (4.7)

7The structure of the singularity turns out to be the same in numerator and denominator, so we can equivalently take fields smeared in a short interval around a point.

## 18

