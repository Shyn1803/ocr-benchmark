10 -10

10 -15

10 -20

10 -25

100 200 300 400 500

(a)

10 -5

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
  <tr>
    <td> </td>
    <td> </td>
    <td> </td>
  </tr>
</table>


10 -10

10 -15

10 -20

10 -25

10 -30

10 -35

2000 4000 6000 8000 10000

(b)

Figure 6: The values of ∆p(t;1/2,2). The top curve corresponds to p = 8 implemented in double precision, the middle curve in gray color (the bottom curve) correspond to p = 8 and (respectively, p = 12) impemented in quadruple precision.

was chosen because ζ(s) does not grow too rapidly as t → +∞ in this strip, unlike in any strip where Re(s) < 1/2. The results of these computations are presented in Figure 6.

The top graph shows the error ∆8(t;1/2,2), where ζ8(s) was implemented in double precision (the benchmark values ζ(s) were computed in higher precision). We observe that rounding errors dominate the approximation error for t > 200. These rounding errors primarily arise when computing χ(s) and evaluating the values of n−s and ns−1 for s = σ + it with even moderatly large t. Indeed, it is easy to verify numerically that when computing the value of 2it in double precision for t of the order 102, precision of the result will be around 10−14, and when t increases to 103, the precision drops to about 10−13. This suggests that we lose one decimal digit of precision every time t increases by a factor of ten. Precision is also lost due to cancellation errors when we add many terms in the main sum in (3), though this effect likely plays a lesser role compared to rounding errors.

The middle graph in Figure 6 (shown in gray) displays the errors ∆8(t;1/2,2), where this time ζ8(s) was implemented in quadruple precision. We observe that rounding errors do not affect the results in this range of t. The quadruple precision implementation of ζ8(s) produces errors smaller than 10−13 for t > 250 and smaller than 10−15 for t > 2000 in the strip 1/2 ≤ σ ≤ 2. Of course, when t becomes very large (of the order 1010 or greater), rounding errors will eventually become noticeable.

The bottom graph on Figure 6 shows the errors ∆12(t;1/2,2) for the quadruple precision implementation of ζ12(s). These errors are significantly smaller: we find that ∆12(t;1/2,2) < 10−25 for t > 5000. The effects of rounding errors become clearly noticeable for t > 2000, though they do not pose a significant issue in this range, as the maximum approximation error remains larger than the rounding errors. However, when t reacher 105 or greater, rounding errors will dominate the approximation error, and the graph will resemble the top graph (though with a much smaller overall error, of order 10−27).

Now that we have (hopefully) convinced the reader of the accuracy of our approximations, it is time to discuss how they were derived and to present an algorithm for computing the coefficients ωp,j and λp,j.

7

