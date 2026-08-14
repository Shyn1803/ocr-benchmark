The rational function ψs+2(−hA) is uniformly bounded and satisﬁes ψs+2(0) = 0 due to (15a). The second and third term of (16) are thus bounded as in the previous theorem. For the term with ψs+1, we use the fact that due to (12) and (15b)

ψs+1(−hA) = ψs+1(−hA) − ψs+1(0) = hA · ψs(1)+1(−hA) with ψs(1)+1(0) = 0. Thus, we have

hs+1ψs+1(−hA)f(s)(tn) = hs+1+βψs(1)+1(−hA)(h A)1−β · A A−1 · Aβf(s)(tn).

With the help of Lemma 2, this term can be bounded in the desired way, which concludes the proof.

Remark The restriction to β ≤ 1 in Theorem 3 was made just for simplicity. If the source term has higher spatial regularity, and if further conditions of the type (15) are fulﬁlled, then we can also show higher temporal order of convergence. The additional conditions can be derived by expanding the defect in (16) even further, and it can be shown as in Lemma 3 that they are implied by the underlying quadrature rule being of higher order. In particular, full (classical) order is achieved for suﬃciently smooth source term with periodic boundary conditions.

Example To illustrate the sharpness of the bounds in Theorem 3, we consider the linear parabolic problem

∂U ∂t

(x,t) −

∂2U ∂x2

(x,t) = 2 + x(1 − x) et (17)

for x ∈ [0,1] and t ∈ [0,1], subject to homogeneous Dirichlet boundary conditions. For the initial value x(1−x), the exact solution is U(x,t) = x(1−x)et.

We discretize this problem in space by standard ﬁnite diﬀerences, and in time by the exponential 2-stage Gauss method, respectively. The numerically observed temporal orders of convergence in diﬀerent norms are displayed in Table 1.

<table>
  <tr>
    <td>N</td>
    <td> </td>
    <td>H1<br><br></td>
    <td>L1</td>
    <td>L2<br><br></td>
    <td>L∞</td>
  </tr>
  <tr>
    <td>50</td>
    <td> </td>
    <td>2.80<br><br></td>
    <td>3.53</td>
    <td>3.27<br><br></td>
    <td>3.00</td>
  </tr>
  <tr>
    <td>100</td>
    <td> </td>
    <td>2.76<br><br></td>
    <td>3.50</td>
    <td>3.26</td>
    <td>3.01<br><br></td>
  </tr>
  <tr>
    <td colspan="3">200 2.75<br><br></td>
    <td>3.50</td>
    <td>3.25<br><br></td>
    <td>3.00</td>
  </tr>
</table>


Table 1 Numerically observed temporal orders of convergence in diﬀerent norms for discretizations with N spatial degrees of freedom and h = 1/128.

The attainable value of β in Theorem 3 relies on the characterization of the domains of fractional powers of elliptic operators. The source function in (17)

9

