al. [14], enhance fuel eﬃciency but impose high computational costs due to system nonlinearities. An alternative approach, the Equivalent Consumption Minimization Strategy (ECMS) [25], reduces computational complexity while delivering near-optimal fuel savings by relying on instantaneous slope data. Both predictive and non-predictive strategies are viable for connected automated vehicles (CAVs), yet achieving a balance between fuel eﬃciency and computational feasibility remains a key challenge for practical deployment.

## 1.2 Outline of the paper

In Section 2 we introduce a convex relaxation of the problem. In Section 3 we brieﬂy sketch the exactness result for this relaxation (under suitable assumptions) when we drop the boundary condition wn = wﬁn at step n, already proved in our paper [2]. Moreover, we show that the relaxation is not exact any more as soon as we include also the boundary condition. In Section 4 we introduce a feasibility-based bound tightening technique, while in Section 5 we prove that the addition of the lower limit for the variables obtained through the bound tightening procedure makes the convex relaxation exact. Next, in Section 6 we introduce further feasibility-based bound tightening techniques. In Section 7 we prove that the feasible region of our problem is a lattice and from that we derive a necessary and suﬃcient condition to establish its non-emptiness, also discussing a procedure to verify such condition, based on the iterated application of the bound tightening techniques discussed in Sections 4 and 6. Finally, in Section 8 we draw some conclusions.

# 2 Convex relaxation of the problem

The constraints of our problem are the following: M Pmax√wi ≥

1 h

(wi+1 − wi) + γwi + g(sin αi + c) i ∈ {1,... ,n − 1} (4)

![](<2503.09424_pg5_images/imageFile1.png>)

![](<2503.09424_pg5_images/imageFile2.png>)

![](<2503.09424_pg5_images/imageFile3.png>)

1 h

(wi+1 − wi) + γwi + g(sin αi + c) ≤ gµ i ∈ {1,... ,n − 1} (5)

![](<2503.09424_pg5_images/imageFile4.png>)

1 h

(wi+1 − wi) + γwi + g(sin αi + c) ≥ −gµ i ∈ {1,... ,n − 1} (6) wi ≤ wimax i ∈ {1,... ,n} (7) wi ≥ 0 i ∈ {1,... ,n} (8) w1 = winit, wn = wﬁn. (9)

![](<2503.09424_pg5_images/imageFile5.png>)

We rewrite constraints (7)–(9) as follows:

wi ≤ wimax i ∈ {1,... ,n} (10) wi ≥ wimin i ∈ {1,... ,n}, (11)

where wimin = 0, for i ∈ {2,... ,n − 1}, while w1min = w1max = winit and wnmin = wnmax = wﬁn (note that the two boundary conditions (9) are split into the constraints winit ≤ w1 ≤ winit and wﬁn ≤ wn ≤ wﬁn). Moreover, after introducing the variables ti,fi, i = 1,... ,n − 1, we can replace the maximum power constraints (4) with the following constraints:

1 √wi

ti =

![](<2503.09424_pg5_images/imageFile6.png>)

![](<2503.09424_pg5_images/imageFile7.png>)

i ∈ {1,... ,n − 1} (12)

Mfi Pmax

ti ≥

![](<2503.09424_pg5_images/imageFile8.png>)

i ∈ {1,... ,n − 1} (13)

1 h

(wi+1 − wi) + γwi + g(sin αi + c) i ∈ {1,... ,n − 1}. (14)

fi =

![](<2503.09424_pg5_images/imageFile9.png>)

5

