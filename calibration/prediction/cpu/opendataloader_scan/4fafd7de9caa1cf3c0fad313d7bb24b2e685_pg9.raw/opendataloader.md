s +2 s +2 0 due to (15a). The second and third term of (16) are thus bounded as in the previous theorem. For the term with ψ s +1 , we use the fact that due to (12) and (15b)

$$
9s+1(0) = hA -
$$

with ψ (1) s +1 (0) = 0. Thus, we have

$$
AÃ-1 Ã8 f(s) (tn). hs+1
$$

With the help of Lemma 2, this term can be bounded in the desired way, which concludes the proof.  

Remark The restriction to β ≤ 1 in Theorem 3 was made just for simplicity. If the source term has higher spatial regularity, and if further conditions of the type (15) are fulﬁlled, then we can also show higher temporal order of convergence. The additional conditions can be derived by expanding the defect in (16) even further, and it can be shown as in Lemma 3 that they are implied by the underlying quadrature rule being of higher order. In particular, full (classical) order is achieved for suﬃciently smooth source term with periodic boundary conditions.

Example To illustrate the sharpness of the bounds in Theorem 3, we consider the linear parabolic problem

$$
02U (x, t) (17)
$$

for 2 € [0, 1] and t € [0, 1], subject to homogeneous Dirichlet boundary condiU(x;t) = 2(1

We discretize this problem in space by standard ﬁnite diﬀerences, and in time by the exponential 2-stage Gauss method, respectively. The numerically observed temporal orders of convergence in diﬀerent norms are displayed in Table 1.

<table>
  <tr>
    <th>N</th>
    <th>Hl</th>
    <th>Ll</th>
    <th>L 2</th>
    <th>L</th>
  </tr>
  <tr>
    <td>50</td>
    <td>2.80</td>
    <td>3.53</td>
    <td>3.27</td>
    <td>3.00</td>
  </tr>
  <tr>
    <td>100</td>
    <td>2.76</td>
    <td>3.50</td>
    <td>3.26</td>
    <td>3.01</td>
  </tr>
  <tr>
    <td>200</td>
    <td>2.75</td>
    <td>3.50</td>
    <td>3.25</td>
    <td>3.00</td>
  </tr>
</table>


Table 1

Numerically observed temporal orders of convergence in diﬀerent norms for discretizations with N spatial degrees of freedom and h = 1 / 128.

The attainable value of β in Theorem 3 relies on the characterization of the domains of fractional powers of elliptic operators. The source function in (17)

