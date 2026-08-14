Mirzavand Boroujeni, Richard, Sterling, and Wilke: Optimizing needle placement in 3D-printed masks for HDR-BT

17

to compute dose volume histograms (DVHs) and associated dosimetric indices. To this end, we voxelize the basic structures using voxel with side length of 1.5mm, resulting in 21219 total voxels, of which 2140 correspond to the tumor and 19079 do not. Resulting DVHs are shown in Figure 3b.

![](<2503.06000_pg17_images/imageFile1.png>)

(a) Needle configuration

Figure 3 Clinical results

100

<table>
  <tr>
    <td> </td>
    <td> </td>
    <td> </td>
  </tr>
  <tr>
    <td> </td>
    <td> </td>
    <td> </td>
  </tr>
</table>


<table>
  <tr>
    <td>RE LE RB RS LB LS ST SW<br><br>data1</td>
  </tr>
</table>


90

80

70

Volume (%)

60

50

40

30

<table>
  <tr>
    <td> </td>
    <td> </td>
    <td colspan="2"> </td>
  </tr>
  <tr>
    <td colspan="3"> </td>
    <td> </td>
  </tr>
</table>


20

10

0

0 3 6 9 12 15 18

Dose (Gy)

(b) DVHs

Figure 3b shows that doses among the various body structures are inhomogeneous. Specifically, the left side of the tumor surface receives higher doses compared to its right side, and there is a noticeable difference in the amount of radiation received by the boundary voxels on the left and right side of the nose. Further, the skin tissues exhibit long tails in their DVHs and most voxels on the left side of the tumor are exposed to a high dose.

In the following section, we will compare the characteristics of this clinical plan with those obtained with the approaches we propose. To make the comparison easier, we normalize the treatment plans by uniformly scaling their dwell times so that their RBV

are approximately the same. In this process, RBV

100

describes the volume of target tissue RB that receives 100% of the prescribed radiation dose. The maximum normalization error is 0.001%. This normalization error is calculated as RBV1

100

are the dosimetric values, after normalization, for the two treatment plans compared.

∗100, where RBV1

and RBV2

/max RBV1

# ,RBV2

# − RBV2

100

100

100

100

100

100

In our models, we consider the five exiting planes shown in Figure 1b. To avoid negative bounds on some of the variables, which can affect the quality of relaxations of bilinear terms, we translate all of the body structures by the same vector, so that they all belong to the positive orthant. Then, all needle reference points can be chosen among the faces of the box [1,173]×[1,60]×[95,200].

For all optimization models that require dose computation, we use piecewise-linear penalty function fic(s) = max{−5000s,0,5000(s − 3)} with δi = 6 for each voxel i in a tumor region. We use

