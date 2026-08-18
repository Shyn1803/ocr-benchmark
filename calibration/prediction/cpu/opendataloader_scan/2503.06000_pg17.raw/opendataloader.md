to compute dose volume histograms (DVHs) and associated dosimetric indices. To this end, we voxelize the basic structures using voxel with side length of 1 . 5 mm, resulting in 21219 total voxels, of which 2140 correspond to the tumor and 19079 do not. Resulting DVHs are shown in Figure 3b.

![](<2503.06000_pg17_images/imageFile1.png>)

100

2

50

30

20

10

15

12

9 Dose (Gy)

(a) Needle configuration

DVHs

(b)

Figure 3 Clinical results

Figure 3b shows that doses among the various body structures are inhomogeneous. Specifically, the left side of the tumor surface receives higher doses compared to its right side, and there is a noticeable difference in the amount of radiation received by the boundary voxels on the left and right side of the nose. Further, the skin tissues exhibit long tails in their DVHs and most voxels on the left side of the tumor are exposed to a high dose.

In the following section, we will compare the characteristics of this clinical plan with those obtained with the approaches we propose. To make the comparison easier, we normalize the treatment plans by uniformly scaling their dwell times so that their RB V 100 are approximately the same. In this process, RB V 100 describes the volume of target tissue RB that receives 100% of the prescribed radiation dose. The maximum normalization error is 0 . 001 %. This normalization error is calculated as   RB 1 V 100 − RB 2 V 100   / max   RB 1 V 100 ,RB 2 V 100   ∗ 100 , where RB 1 V 100 and RB 2 V 100 are the dosimetric values, after normalization, for the two treatment plans compared.

In our models, we consider the five exiting planes shown in Figure 1b. To avoid negative bounds on some of the variables, which can affect the quality of relaxations of bilinear terms, we translate all of the body structures by the same vector, so that they all belong to the positive orthant. Then, all needle reference points can be chosen among the faces of the box [1 , 173] × [1 , 60] × [95 , 200] .

For all optimization models that require dose computation, we use piecewise-linear penalty function f c i ( s ) = max {− 5000 s, 0 , 5000( s − 3) } with δ i = 6 for each voxel i in a tumor region. We use

