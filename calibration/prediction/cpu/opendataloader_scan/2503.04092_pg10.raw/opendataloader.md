with T c = 0 . 8 and T = 0 . 36.

The physical parameters are set as seen in Table 1. The forward problem is solved using

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>p (gr</td>
    <td>1.2</td>
  </tr>
  <tr>
    <td>(P)</td>
    <td>0 . 035</td>
  </tr>
  <tr>
    <td>(cm s-1) ;</td>
    <td>) 75</td>
  </tr>
  <tr>
    <td>6)</td>
    <td>0 . 80</td>
  </tr>
  <tr>
    <td> </td>
    <td>0 . 36</td>
  </tr>
  <tr>
    <td>(s-1)</td>
    <td>70</td>
  </tr>
</table>


<table>
  <tr>
    <th> </th>
    <th>F1</th>
    <th> </th>
    <th>13</th>
    <th>T4</th>
  </tr>
  <tr>
    <td>R p ( dyn · s</td>
    <td>480</td>
    <td>2 520</td>
    <td>520</td>
    <td>200</td>
  </tr>
  <tr>
    <td>Ra (dyn cm~5)</td>
    <td>7200</td>
    <td>11520 4</td>
    <td>11520 4 4</td>
    <td>4800 4</td>
  </tr>
  <tr>
    <td>C ( dyn − ·</td>
    <td>4 . 10-4</td>
    <td>3 . 10-4</td>
    <td>− 3 · 10 −</td>
    <td>4</td>
  </tr>
</table>


Table 1: Physical parameters and numerical values of the three-element Windkessel parameters for every outlet.

a semi-implicit 3D-0D coupling scheme as seen in [9]. The full algorithm is detailed in the appendix.

# 3.1.2 Synthetic measurements

The forward solution is generated with a time step of dt = 1 ms and undersampled in time to dt meas = 15 ms , leading to a total of 56 measurements. From the solution of the forward problem, we simulate a PC-MRI acquisition by subsampling into a rectangular measurement mesh with a resolution of [2 mm, 2 mm, 2 mm ] and then applying the process described in Section 2.1 with a venc of double the maximal velocity. The magnitude is modelled as

$$
1.0 if z is in the lumen of the vessel (16) 0.5 otherwise.
$$

Finally a complex Gaussian noise ϵ ∈ C N is added with a signal-to-noise ratio (SNR) of 15. Fifty independent realizations of the noise were generated.

For comparison, we reconstructed velocity measurements from these synthetic measurements using the Berkeley Advanced Reconstruction Toolbox (BART)[11]. BART is a command-line-based software that provides a flexible framework of compressed sensing methods, as well as tools for simulation, pre-processing, and image reconstruction, providing a multitude of different regularization options. In this work, we have used this toolbox for compressed sensing reconstructions of the velocities, using total variation in time as for the regularization.

Next, the sampling mask is applied to these simulated frequency space measurements. We take a 2D subsampled mask in the x − y -plane and sample fully in the z -direction as in [4]. We consider different subsampling rates R = N sampled N total = 8 , 16 , 32, with two different masks: the pseudo-spiral mask and the pseudo-random Gaussian mask, which is sampled according to a Gaussian probability distribution, as shown in Figure 2. For the pseudo-spiral mask, the points are placed evenly on a cartesian grid along a spiral with six turns and a final radius reaching the edge of the mask.

