![](<2503.07617_pg27_images/imageFile1.png>)

1.5

0.5

1.5

Figure 29: [ Test Case 3 ] (Left) Reference Darcy Velocity Field. (Right) Perturbed V elocity Field.

2.5

![](<2503.07617_pg27_images/imageFile1.png>)

2.5

0.8

0.8

0.6

0.6

1.5

1.5

0.4

0.2

0.5

0.2

0.5

1.5

0.5

0.5

1.5

Figure 30: [ Test Case 3 ] Reference Concentration Field. (Left) Heat Map. (Right) Contour Map.

mesh size h = 1 / 40 and on a very ﬁne temporal mesh ∆ t = T / 800 with T = 5. The data assimilation algorithm is performed over the same spatial mesh size and on a coarser temporal ﬁltering steps ∆ t Filter = T / N t Filter where N t Filter = 50, with the same assumption on the observational operator as in Test Case 2. Since concentration transport is driven by the Darcy velocity, we assume that there are some uncertainties in the process of solving the Darcy’s ﬂow system to increase the complexity of state estimation. Thus, we add a small perturbation ξ Darcy = 0.0001 ε D to the reference Darcy velocities with ε Darcy ∼ N ( 0, I ) and input the disturbed velocity to the forward solver. The reference Darcy velocity ﬁeld and one example of the perturbed velocity ﬁeld are shown in Figure 29 on a very coarse mesh for the purpose of illustration. We can see that even with a small amount of noise, the perturbed Darcy ﬁeld is signiﬁcantly chaotic, which makes the task of state estimation challenging.

Similar to Test Case 2, we aim to investigate the performance of the United Filter under various levels of perturbation. Thus, we consider two types of disturbed noise ω in ( 14 ): ˜ ω 1 = 0.001   ∆ t Filter ˜ ǫ 1 and ˜ ω 2 = 0.1   ∆ t Filter ˜ ǫ 2 , where ˜ ǫ i ∼   ( 0, I l ) for i = 1,2. Regarding the setting for the parameter estimation, as the exact values are small, we apply the assimilation algorithm to approximate ρ i = 1 / d i , i = 1,2 and ρ γ = 1 /α γ . We choose the number of Direct Filter particles to be M = 40, and the number of iterations in the United Filter to be R = 4.

0.8

0.6

0.5

0.5

1.5

![](<2503.07617_pg27_images/imageFile2.png>)

2.5

1.5

0.5

0.8

0.6

0.5

0.3

0.5

2.5

1.5

0.5

Figure 31: [ Test Case 3 ] Heat map of estimated concentration ﬁeld by the United Filter: (Left) With noise ˜ ω 1 . (Right) With noise ˜ ω 2 .

