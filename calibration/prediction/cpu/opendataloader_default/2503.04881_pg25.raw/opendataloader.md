25

# 3. Non-uniform mesh spacing

We have emperically found it advantageous to use the following non-uniform mesh structure for evolving the subextremal Q0 = 0.999 and extremal Q0 = 1 cases studied in this paper.

For the sub-extremal grid, we space cells evenly in VEF from VEF = VEF,0 to VEF = 1000, and then logarithmically from VEF = 1000 to VEF = 10000, before adding a single point at vMRT = π/2 (null infinity). In the exterior, we then space evenly in UEF from UEF = UEF,0 to UEF = 950, before adding a single point at uMRT = 0 (the horizon) and then reflecting the grid across the horizon into the black hole interior. Due to the exponential sensitivity of the horizon redshift effect (Eq. 12), we cannot go past UEF = 950 before hitting machine precision (we use quadruple precision floating point arithmetic).

For the extremal grid, we use the same spacing in V . But for U, we space evenly in UEF from UEF = UEF,0 to UEF = 1500, and then logarithmically from UEF = 1500 to UEF = 105, before adding a single point at uMRT = 0 (the horizon) and reflecting the grid across the horizon into the interior. Since there is no redshift effect of the extremal horizon, we can to push much larger values of UEF with quadruple precision floating point arithmetic and still obtain convergent solutions.

# 4. Convergence

Here, we demonstrate convergence of our code. To do so, we need to compare the code output at (at least) three different grid resolutions. Since we use a non-uniform mesh, the way we define “different” resolutions here is we choose one specific mesh as our base “low” resolution mesh, then define each successively higher resolution meshes as the immediately lower resolution mesh with each cell cut into quarters (as measured in compactified MRT coordinates). In other words, we double the resolution at each step. Consequently, for a second order accurate evolution scheme as we employ, in the convergent regime we expect global truncation error to drop by a factor of four per doubling step.

For our low resolution mesh, we construct it as described above with the exterior portion of the mesh having 20000 cells in the V direction and 10000 cells in the U direction. We then runs simulations at twice and four times this resolution. For some quantity Φ output from these simulations, we compute the point-wise convergence parameter C (see e.g. [41])

- Φ0 − Φ1

- Φ1 − Φ2


C ≡

, (D9)

where Φ0 is the field from the low resolution run, with Φ1,Φ2 getting progressively finer. For second order convergence, we expect C → 4.

The convergence factor C on the future horizon and at null infinity is plotted in Figure 14 for a representative set of parameters.

P on Horizon

10

<table>
  <tr>
    <td> </td>
    <td colspan="5" rowspan="3"> </td>
  </tr>
  <tr>
    <td> </td>
  </tr>
  <tr>
    <td> </td>
  </tr>
  <tr>
    <td> </td>
    <td colspan="5" rowspan="2"> </td>
  </tr>
  <tr>
    <td> </td>
  </tr>
  <tr>
    <td colspan="2"> </td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
  </tr>
</table>


8

6

4

2

0

200 400 600 800

VEF

Convergence of Matter Fields

Q on Horizon

P on Null Infinity

10

10

<table>
  <tr>
    <td> </td>
    <td colspan="5" rowspan="3"> </td>
  </tr>
  <tr>
    <td> </td>
  </tr>
  <tr>
    <td> </td>
  </tr>
  <tr>
    <td> </td>
    <td colspan="5" rowspan="2"> </td>
  </tr>
  <tr>
    <td> </td>
  </tr>
  <tr>
    <td colspan="2"> </td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
  </tr>
</table>


<table>
  <tr>
    <td> </td>
    <td colspan="5" rowspan="3"> </td>
  </tr>
  <tr>
    <td> </td>
  </tr>
  <tr>
    <td> </td>
  </tr>
  <tr>
    <td> </td>
    <td colspan="5" rowspan="2"> </td>
  </tr>
  <tr>
    <td> </td>
  </tr>
  <tr>
    <td colspan="2"> </td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
  </tr>
</table>


8

8

6

6

4

4

2

2

0

0

200 400 600 800

200 400 600 800

UEF

VEF

Q on Null Infinity

10

<table>
  <tr>
    <td> </td>
    <td colspan="5" rowspan="3"> </td>
  </tr>
  <tr>
    <td> </td>
  </tr>
  <tr>
    <td> </td>
  </tr>
  <tr>
    <td> </td>
    <td colspan="5" rowspan="2"> </td>
  </tr>
  <tr>
    <td> </td>
  </tr>
  <tr>
    <td colspan="2"> </td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
  </tr>
</table>


8

6

4

2

0

200 400 600 800

UEF

FIG. 14. Convergence factor for P and Q at the boundaries of the black hole exterior for the numerical simulation with Q0 = 1.0, eQ0 = 0.6, and ω˜ = 0.0. The idealized value C = 4 is shown as a black dashed line in each panel.

We see that in all cases, C is scattered around its idealized value of 4, with the scatter in that of Q typically being significantly smaller than that of P at a fixed resolution.

