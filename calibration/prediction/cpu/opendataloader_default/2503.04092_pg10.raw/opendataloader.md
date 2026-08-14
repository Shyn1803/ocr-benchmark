with Tc = 0.8 and T = 0.36. The physical parameters are set as seen in Table 1. The forward problem is solved using

<table>
  <tr>
    <td>Parameter</td>
    <td>Value</td>
  </tr>
  <tr>
    <td>ρ (gr · cm3) µ (P) U (cm · s−1) Tc (s) T (s) κ (s−1)<br><br></td>
    <td>1.2 0.035 75 0.80 0.36 70</td>
  </tr>
</table>


<table>
  <tr>
    <td> </td>
    <td>Γ1<br><br></td>
    <td>Γ2</td>
    <td>Γ3<br><br></td>
    <td>Γ4</td>
  </tr>
  <tr>
    <td>Rp (dyn · s · cm−5) Rd (dyn · s · cm−5) C (dyn−1 · cm5)</td>
    <td>480<br><br>7200<br><br>4 · 10−4<br><br></td>
    <td>520 11520 3 · 10−4<br><br></td>
    <td>520 11520 3 · 10−4</td>
    <td>200<br><br>4800<br><br>4 · 10−4</td>
  </tr>
</table>


Table 1: Physical parameters and numerical values of the three-element Windkessel parameters for every outlet.

a semi-implicit 3D-0D coupling scheme as seen in [9]. The full algorithm is detailed in the appendix.

# 3.1.2 Synthetic measurements

The forward solution is generated with a time step of dt = 1ms and undersampled in time to dtmeas = 15ms, leading to a total of 56 measurements. From the solution of the forward problem, we simulate a PC-MRI acquisition by subsampling into a rectangular measurement mesh with a resolution of [2mm,2mm,2mm] and then applying the process described in Section 2.1 with a venc of double the maximal velocity. The magnitude is modelled as

M(x) =

1.0 if x is in the lumen of the vessel 0.5 otherwise.

(16)

Finally a complex Gaussian noise ϵ ∈ CN is added with a signal-to-noise ratio (SNR) of 15. Fifty independent realizations of the noise were generated.

For comparison, we reconstructed velocity measurements from these synthetic measurements using the Berkeley Advanced Reconstruction Toolbox (BART)[11]. BART is a command-line-based software that provides a flexible framework of compressed sensing methods, as well as tools for simulation, pre-processing, and image reconstruction, providing a multitude of different regularization options. In this work, we have used this toolbox for compressed sensing reconstructions of the velocities, using total variation in time as for the regularization.

Next, the sampling mask is applied to these simulated frequency space measurements. We take a 2D subsampled mask in the x − y-plane and sample fully in the z-direction as in [4]. We consider different subsampling rates R = NNsampled

= 8,16,32, with two different masks: the pseudo-spiral mask and the pseudo-random Gaussian mask, which is sampled according to a Gaussian probability distribution, as shown in Figure 2. For the pseudo-spiral mask, the points are placed evenly on a cartesian grid along a spiral with six turns and a final radius reaching the edge of the mask.

total

10

