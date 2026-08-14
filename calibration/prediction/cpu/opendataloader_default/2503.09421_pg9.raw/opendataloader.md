where the constant c is independent of A and n (but does depend on the dimension of Ran(P)). We use that 1 ∞ ts−2 dt < ∞ for s < 1 to bound the second term. Thus, there exists a constant C(s) such that

n+1

∥(A + x)−1∥s dx ≤ C(s) for all maximally dissipative A, where C(s) is independent of n and Ran(P). Using that

n

1

1+(|n|−1)2 < ∞, we can therefore bound the right hand side of (9) for all |z| > 1.

n∈Z

If |z| < 1, we drop a minus sign in both norms in (9) and use that i Fz and i Fz−1 are dissipative. Repeating the arguments from above yields the bound for all |z| < 1.

The case x(i) = y(j) is significantly easier: We can directly take α = ωx and do not need β. The operators Fz and Fz act on C3, while all other estimates still hold. The integrals in (9) can be similarly bounded by Lemma 1.

<table>
  <tr>
    <td> </td>
  </tr>
</table>


We state a simplified version of Lemma 3.1 from [3], which we use to bound the integrals in the proof of Theorem 2.

Lemma 1. Let H be a separable Hilbert space, A be a maximally dissipative operator with strictly positive imaginary part and M1,M2 : H → H be Hilbert-Schmidt operators. Then there exists a constant c independent of A, M1 and M2 such that for any t > 0:

1 t

| x ∈ Rs.t. ∥M1 (A + x)−1 M2∥ > t | ≤ c∥M1∥HS ∥M2∥HS

, where | · | denotes the Lebesgue measure.

# 4.2 The boundary of a box

We want to define a ”box” ΛL for any size L ∈ N2, whose sides have lengths L1 and L2, such that the Quantum Walker is unable to cross the boundary of ΛL. Restricting the Walker to some box ΛL is achieved by changing the coin matrix at specific lattice sites on the boundary of ΛL. In other words, we want to obtain unitary operators Uω(L) = UωΛL ⊕ UΛ

C

ω L and subspaces HL ⊕ HLC = H such that HL, respectively HLC, are invariant under UωΛL, respectively UΛ

C

ωL. Note that we call a subspace H′ ⊂ H invariant under U if UH′ ⊂ H′. Recalling the definition of Hj,k (4), we use that C0 induces a fully localized Quantum Walk, see section 2, and define the invariant subspaces:

Hj,k, HLC = H \ HL.

HL =

−L1≤j≤L1−1 −L2≤k≤L2−1 j+k>−L1−L2

The choice j+k > −L1−L2 is not necessary, but simplifies the structure of ΛL, see Figure

3. We call the number of ΓA-vertices in ΛL the volume of ΛL, that is:

vol(ΛL) = 4L1L2 − 1 and |L| = L21 + L22. (10) To obtain a Quantum Walk such that these two subspaces are invariant, we need to change the coin matrix at specific lattice sites from C to C0. In particular, we use the coin matrix C0 at all ΓB sites in

Γ(CL)

= |j,k⟩ ⊗

0

- 0
- 1


s.t. − L1 ≤ j ≤ L1 − 1,k = L2 − 1 or

− L1 + 1 ≤ j ≤ L1,k = −L2 − 1 or j = L1,−L2 ≤ k ≤ L2 − 2 or j = −L1,−L2 ≤ k ≤ L2 − 2 .

## 9

