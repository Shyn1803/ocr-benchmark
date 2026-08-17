# E ON THE BEST CURVATURE SPLITTING PROBLEM (see Section 4 )

In Section 4 we examined how to achieve the optimal splitting for a given objective F = f 1 − f 2 by subtracting the same curvature term λ ∥·∥ 2 2 in both functions. We concluded that if µ 1 ≤ µ 2 , the best splitting is achieved by shifting the lower curvature of f 1 to 0, i.e., make it convex. Conversely, when µ 1 > µ 2 , the best splitting is achieved for some f 2 weakly convex, with lower curvature µ 2 − λ < 0.

Within this section, we provide additional numerical experiments. In Figure 10 we provide an example with fixed curvature bounds of a nonconvex-nonconcave objective function F , namely µ F = − 0 . 5 and L F = 1 . 5, and illustrate all possible regimes after one iteration. Note that µ F = µ 1 − L 2 and L F = L 1 − µ 2 ; further on, we examine the regimes based on the ranges of L 2 and µ 2 . The condition µ 1 ≥ 0 implies that L 2 = µ 1 − µ F ≥ − µ F , while the condition µ 1 + µ 2 > 0 that µ 2 > − µ 1 = L 2 + µ F . The contour lines represent the values of the denominators p i , with i = 1 , 2 , 3 , 4. The red points mark the initial curvature values of L 2 and µ 2 , whereas the green dots indicate the points with the largest possible p i obtained through the optimal choice of λ . Since these shifts are linear in λ , the dashed lines connecting the dots have a slope of one.

For example, in the case where L 2 = 1 and µ 2 = 0 . 75, we have µ 1 < µ 2 and the best splitting is obtained by shifting to the lowest possible value of L 2 , corresponding to µ 1 = 0. In all other examples, µ 1 > µ 2 and the optimal splittings are found within regime p 3 , where µ 2 < 0.

![](<2503.04486_pg21_images/imageFile1.png>)

B = 0

2.5

1.5

0.5

0.5

1.5

2.5

L 2

p4

p3

p2

Figure 10: All regimes for a fixed objective function F with µ F = − 0 . 5 and L F = 1 . 5, along with several mappings of the optimal splittings, shown as transitions from red to green dots along dashed lines with a slope of 1.

