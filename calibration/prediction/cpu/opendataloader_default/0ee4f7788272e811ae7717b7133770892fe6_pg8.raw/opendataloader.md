05.04.8 Chapter 05.04

Table 3 Velocity as a function of time.

<table>
  <tr>
    <td>t (s)</td>
    <td>v(t) (m/s)</td>
  </tr>
  <tr>
    <td>0</td>
    <td>0</td>
  </tr>
  <tr>
    <td>10</td>
    <td>227.04</td>
  </tr>
  <tr>
    <td>15</td>
    <td>362.78</td>
  </tr>
  <tr>
    <td>20</td>
    <td>517.35</td>
  </tr>
  <tr>
    <td>22.5</td>
    <td>602.97</td>
  </tr>
  <tr>
    <td>30</td>
    <td>901.67</td>
  </tr>
</table>


- a) Determine the value of the velocity at t 16 seconds using quadratic splines.
- b) Using the quadratic splines as velocity functions, find the distance covered by the rocket from t 11s to t 16s.
- c) Using the quadratic splines as velocity functions, find the acceleration of the rocket at t 16s.


# Solution

a) Since there are six data points, five quadratic splines pass through them. v(t)  a1t2 b1t  c1, 0  t 10

-  a2t2  b2t  c2 , 10  t 15
-  a3t2 b3t  c3 , 15  t  20
-  a4t2  b4t  c4 , 20  t  22.5
-  a5t2  b5t  c5 , 22.5  t  30


The equations are found as follows.

1. Each quadratic spline passes through two consecutive data points.

a1t  b t  c passes through t  0 and t 10.

2

1 1

a1(0)2  b1(0)  c1  0 (1) a1(10)2  b1(10)  c1  227.04 (2)

a2t  b t  c passes through t 10 and t 15.

2

2 2

a2(10)2  b2(10)  c2  227.04 (3) a2(15)2  b2(15)  c2  362.78 (4)

a3t  b t  c passes through t 15 and t  20.

2

3 3

a3(15)2 b3(15)c3  362.78 (5) a3(20)2  b3(20)  c3  517.35 (6)

a4t  b t  c passes through t  20 and t  22.5.

2

4 4

a4(20)2  b4(20)  c4  517.35 (7) a4(22.5)2  b4(22.5)  c4  602.97 (8)

