Teodor Rotaru, Panagiotis Patrinos, Franc¸ois Glineur

# E ON THE BEST CURVATURE SPLITTING PROBLEM (see Section 4)

In Section 4 we examined how to achieve the optimal splitting for a given objective F = f1 − f2 by subtracting the same curvature term λ∥·∥

2

2 in both functions. We concluded that if µ1 ≤ µ2, the best splitting is achieved by shifting the lower curvature of f1 to 0, i.e., make it convex. Conversely, when µ1 > µ2, the best splitting is achieved for some f2 weakly convex, with lower curvature µ2 − λ < 0.

Within this section, we provide additional numerical experiments. In Figure 10 we provide an example with fixed curvature bounds of a nonconvex-nonconcave objective function F, namely µF = −0.5 and LF = 1.5, and illustrate all possible regimes after one iteration. Note that µF = µ1 − L2 and LF = L1 − µ2; further on, we examine the regimes based on the ranges of L2 and µ2. The condition µ1 ≥ 0 implies that L2 = µ1 −µF ≥ −µF, while the condition µ1 + µ2 > 0 that µ2 > −µ1 = L2 + µF. The contour lines represent the values of the denominators pi, with i = 1,2,3,4. The red points mark the initial curvature values of L2 and µ2, whereas the green dots indicate the points with the largest possible pi obtained through the optimal choice of λ. Since these shifts are linear in λ, the dashed lines connecting the dots have a slope of one.

For example, in the case where L2 = 1 and µ2 = 0.75, we have µ1 < µ2 and the best splitting is obtained by shifting to the lowest possible value of L2, corresponding to µ1 = 0. In all other examples, µ1 > µ2 and the optimal splittings are found within regime p3, where µ2 < 0.

p4

3

<table>
  <tr>
    <td><table>
  <tr>
    <td>B = 0<br><br>L2 = 72</td>
  </tr>
</table>
</td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td>0<br><br>0<br><br>0.25<br><br>0.5<br><br>0.5</td>
  </tr>
  <tr>
    <td> </td>
    <td> </td>
    <td> </td>
    <td>0<br><br>0<br><br>0.25<br><br>0.25<br><br>0.5<br><br>0.5<br><br>0.75<br><br>0.75</td>
    <td> </td>
  </tr>
  <tr>
    <td> </td>
    <td> </td>
    <td>0<br><br>0.25<br><br>0.25<br><br>0.5<br><br>0.75<br><br>0.75<br><br>1</td>
    <td> </td>
    <td>0.75</td>
  </tr>
  <tr>
    <td> </td>
    <td>0<br><br>0<br><br>0.25<br><br>0.5<br><br>0.5<br><br>0.75<br><br>1<br><br>1 1.25<br><br><br>1.25<br><br>1.5</td>
    <td> </td>
    <td> </td>
    <td>0.75</td>
  </tr>
  <tr>
    <td>0<br><br>0<br><br>0.25<br><br>0.25<br><br>0.5<br><br>0.5<br><br>0.75 1.25<br><br>0.75<br><br>1<br><br>1<br><br><br>1.25<br><br>1.5<br><br>1.75<br><br>2</td>
    <td> </td>
    <td>1</td>
    <td> </td>
    <td> </td>
  </tr>
  <tr>
    <td>1.75<br><br>2 2.5</td>
    <td>1.5</td>
    <td>![](<2503.04486_pg21_images/imageFile1.png>)<br><br>1.25</td>
    <td>1<br><br>1</td>
    <td>1</td>
  </tr>
  <tr>
    <td>0<br><br>0.25<br><br>0.25<br><br>0.5<br><br>0.5<br><br>0.75<br><br>0.75<br><br>1<br><br>1<br><br>1.25<br><br>1.25<br><br>1.5<br><br>1.5<br><br>1.75<br><br>1.75<br><br>2</td>
    <td>1.25<br><br>1.5</td>
    <td>1.25<br><br>1.25</td>
    <td> </td>
    <td>1</td>
  </tr>
  <tr>
    <td> </td>
    <td>0<br><br>0<br><br>0.25<br><br>0.5<br><br>0.75<br><br>1</td>
    <td>0.25<br><br>0.5<br><br>0.5<br><br>0.75<br><br>0.75<br><br>1<br><br>1</td>
    <td>1</td>
    <td>0.75<br><br>1</td>
  </tr>
  <tr>
    <td> </td>
    <td> </td>
    <td>0<br><br>0<br><br>0.25</td>
    <td>0.25<br><br>0.5<br><br>0.75</td>
    <td>0.25<br><br>0.5<br><br>0.5<br><br>0.75</td>
  </tr>
</table>


![](<2503.04486_pg21_images/imageFile2.png>)

2.5

2

p3

1.5

1

p2

72

0.5

0

p1

-0.5

-1

--

-1.5

0.5 1 1.5 2 2.5 3

L2

Figure 10: All regimes for a fixed objective function F with µF = −0.5 and LF = 1.5, along with several mappings of the optimal splittings, shown as transitions from red to green dots along dashed lines with a slope of 1.

