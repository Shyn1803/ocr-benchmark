![](<2503.03948_pg3_images/imageFile1.png>)

(a) (c)

(b)

a

Local Gap μ(x,0,E) 0 0.3

ζE = sign[Pf(L)] −1 0 1

y

t1 ieiϕt2

![](<2503.03948_pg3_images/imageFile2.png>)

<table>
  <tr>
    <td> </td>
  </tr>
</table>


x

![](<2503.03948_pg3_images/imageFile3.png>)

![](<2503.03948_pg3_images/imageFile4.png>)

![](<2503.03948_pg3_images/imageFile5.png>)

![](<2503.03948_pg3_images/imageFile6.png>)

2

Closing

1

Energy E

Egap

0

Closing

- −2

−1

3

- −3 Γ K M


−xm 0 xm Brillouin Zone

0 0.3 Local Gap μ(0,0,E)

Position x

FIG. 1. (a) Bulk band structure for the C2T -symmetric TBG model. Inset diagrams this lattice model. (b) The local gap µ(x,y,E) for x and E at y = 0. Position x is scaled in terms of the lattice constant a and xm denotes the length of the edge from the origin. (c) µ(x,y,E) for E at the center of rotation denoted by blue dotted line in panel (b). The energy-resolved invariant ζE is shown by the green dots, where κ = 0.1t/a for all calculations.

Specifically, when perturbing the system H → H + δH, ζE is guaranteed by Weyl’s inequality to be preserved so long as ∥δH∥ < µ(0,0,E)(X,Y,H) [60, 61]. In addition, as locations where µ(x,y,E) = 0 are associated with the locations of a system’s states [62], changes in a system’s topological marker necessarily imply changes in the structure of its states. A detailed mathematical discussion of Eq. (9), its essential properties, and its relation to atomic limits is given in Supplementary Secs. SI.E-G. In particular, Examples SI.11 and SI.12 show the form of the two different classes of atomic limits distinguished by ζE.

Summarizing our derivation, we first used a system’s physical symmetries to define a transpose-like matrix operation that translates the physical symmetries to matrix symmetries of the system’s H, X, and Y . Then, we found a change of basis that transformed this matrix operation into the standard matrix transpose, such that in this atypical basis the system’s operators were either symmetric or skew-symmetric. Finally, by tensoring these operators using the Pauli matrices, we formed a single skew-symmetric matrix whose Pfaffian’s sign discriminates between which atomic limits a given system can be connected to without closing the system’s local gap. Altogether, by using results from matrix homotopy, this argument yields an energy-resolved invariant for classifying fragile topology as well as a quantitative measure of topological protection.

Having derived a classification framework applicable to finite systems, we demonstrate its use in a fourband model that is a low-energy approximation of TBG and exhibits fragile topology [18, 21]. This model con-

# 3

sists of a bilayer honeycomb lattice, as schematically shown in Fig. 1(a), where t1 and t2 represent the intraand inter-layer hopping amplitudes, respectively. The blue lines spirally connecting inter-layer sites represent next-nearest neighbor (NNN) hoppings with the hopping phase ±ϕ, which can induce a nontrivial fragile band gap. We have provided the expressions of the Hamiltonian in both position and momentum space the End Matter and further information in Supplementary Sec. SII.

Comparison of the bulk band structure of the infinite four-band TBG model with the local gap of a finite system confirms that the locations in (x,y,E)-space with µ(x,y,E) ≈ 0 indicate the presence of states at the specified energies and positions, see Figs. 1(a),(b). For choices of E residing within the spectral extent of the bulk bands, extended Bloch states are distributed throughout the system, whereas within the bulk band gap, only localized states exist at the system’s boundaries. Note that the fluctuation pattern of µ(x,0,E) only intermittently touching zero near the band gap inherently suggests the weak topological nature of this fragile system; strong topological phases instead exhibit a spheroid of appropriate dimension where µ(x,E) = 0 (see Supplementary Sec. SI.G).

Within the bulk band gap, the energy-resolved marker ζE confirms the finite system’s fragile topology, while the large local gap at the rotation center indicates this phase’s strong topological protection, see Fig. 1(c). For energies above and below the bulk gap, ζE maintains a nontrivial value of −1 until the first closing points of µ(0,0,E), beyond which it switches to +1. Although the exact energy where µ(0,0,E) = 0 may vary with the parameter κ (see Supplementary Sec. SIII), these spectral regions with small local gaps are not topologically robust, as very small system perturbations are able to change the topology.

To confirm that the local fragile marker ζE captures phase transitions, we uniformly vary ϕ between all NNN sites from −π to π. As can be seen in Fig. 2(a), the width of the bulk spectral gap under this alteration is symmetric about ϕ = 0 and touches zero twice at ϕ = π/3 and ϕ = 2π/3. Similarly, the local gap closes at precisely the same points where Egap = 0 and ζE changes across these values of ϕ, indicating a change in the material’s fragile topological phase.

As our framework works directly with a finite system expressed in position-space, it can inherently be applied to disordered and aperiodic systems. To illustrate this capability, we consider an ensemble of disordered variants of the four-band TBG model where the hopping phases ϕjk between each pair of NNN sites j and k are randomly assigned a value within an angle range of 2S from ±i from a uniform distribution while preserving C2T -symmetry. Therefore, S represents the median value of the disorder strength, allowing us to investigate the phase diagram of the disordered system based on this variable. In Figs. 2(d), (e), and (f), we present Egap, µ(0,0,E), and ζE as functions of S for 10 different disorder realizations. We numerically observe that the disordered samples exhibit

