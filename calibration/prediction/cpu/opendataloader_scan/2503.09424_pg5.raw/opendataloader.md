al. [14], enhance fuel eﬃciency but impose high computational costs due to system nonlinearities. An alternative approach, the Equivalent Consumption Minimization Strategy (ECMS) [25], reduces computational complexity while delivering near-optimal fuel savings by relying on instantaneous slope data. Both predictive and non-predictive strategies are viable for connected automated vehicles (CAVs), yet achieving a balance between fuel eﬃciency and computational feasibility remains a key challenge for practical deployment.

# 1.2 Outline of the paper

In Section 2 we introduce a convex relaxation of the problem. In Section 3 we brieﬂy sketch the exactness result for this relaxation (under suitable assumptions) when we drop the boundary condition w n = w ﬁn at step n , already proved in our paper [2]. Moreover, we show that the relaxation is not exact any more as soon as we include also the boundary condition. In Section 4 we introduce a feasibility-based bound tightening technique, while in Section 5 we prove that the addition of the lower limit for the variables obtained through the bound tightening procedure makes the convex relaxation exact. Next, in Section 6 we introduce further feasibility-based bound tightening techniques. In Section 7 we prove that the feasible region of our problem is a lattice and from that we derive a necessary and suﬃcient condition to establish its non-emptiness, also discussing a procedure to verify such condition, based on the iterated application of the bound tightening techniques discussed in Sections 4 and 6. Finally, in Section 8 we draw some conclusions.

# 2 Convex relaxation of the problem

problem are the following:

$$
M 1 (Wi+1 Pmax h Vwi
$$

$$
Z(wi+1 ~ i € {1,. . . ,n _ 1} (5) h
$$

$$
7(wi+1 = (6)
$$

$$
max Wi i € {1,
$$

$$
Wj 2 0 i € {1, n}
$$

$$
Wn Wfin . (9) Winit ,
$$

We rewrite constraints (7)–(9) as follows:

$$
max Wi i € {1, , n} (10)
$$

$$
min W; 2 Wi n} (11)
$$

where w min i = 0, for i ∈ { 2 ,... ,n − 1 } , while w min 1 = w max 1 = w init and w min n = w max n = w ﬁn (note that the two boundary conditions (9) are split into the constraints w init ≤ w 1 ≤ w init and w ﬁn ≤ w n ≤ w ﬁn ). Moreover, after introducing the variables t i ,f i , i = 1 ,... ,n − 1, we can replace the maximum power constraints (4) with the following constraints:

$$
ti i € {1,... ,n _ 1} (12) Wi
$$

$$
M fi ti i € {1,. . . ,n _ 1} (13) Pmax
$$

$$
fi = (14) h
$$

