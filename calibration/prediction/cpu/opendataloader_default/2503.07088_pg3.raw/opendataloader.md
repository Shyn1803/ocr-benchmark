# 2. Preliminaries

In this section, we brieﬂy recall main deﬁnitions, notations of some basics of q-calculus that will be useful to us in this paper. These notions are presented in [1, 3, 6] among many others.

Throughout this paper we suppose 0 < q < 1. The q-analog [n]q of any positive integer n ∈ N∗ and q-analog factorial [n]q! are deﬁned as

1 − qn 1 − q

and [n]q! = [n]q × [n − 1]q × ··· × [1]q. The q-analog of (x − a)n is

[n]q =

![](<2503.07088_pg3_images/imageFile1.png>)

1 if n = 0 (x − a) × (x − qa) × ··· × (x − qn−1a) if n 1,

(x − a)nq =

and we have

n(n−1)

2 x − q1−na nq . The q-analog of the exponential function ex given by

(a − x)nq = (−1)nq

![](<2503.07088_pg3_images/imageFile2.png>)

<table>
  <tr>
    <th>exq =<br><br>+∞<br><br>k=0<br><br>xk [k]q!<br><br>![](<2503.07088_pg3_images/imageFile3.png>)</th>
    <th>.</th>
  </tr>
  <tr>
    <td>The q-analog of identity exe−x = 1 is deﬁned by exqEq−x</td>
    <td>= 1, where</td>
  </tr>
</table>


x2

The q-analog of e−

2 is given by

![](<2503.07088_pg3_images/imageFile4.png>)

Eqx = ex1

![](<2503.07088_pg3_images/imageFile5.png>)

q

+∞

=

k=0

xk [k]q!

k(k−1) 2

.

q

![](<2503.07088_pg3_images/imageFile6.png>)

![](<2503.07088_pg3_images/imageFile7.png>)

+∞

q2x2 [2]q

E−

![](<2503.07088_pg3_images/imageFile8.png>)

q2 =

k=0

qk(k+1)(q − 1)k (1 − q2)kq2

x2k.

![](<2503.07088_pg3_images/imageFile9.png>)

The q-analog of an improper integral is proper integral with limits −ν and ν where

1 √1 − q

ν = ν(q) =

.

![](<2503.07088_pg3_images/imageFile10.png>)

![](<2503.07088_pg3_images/imageFile11.png>)

For a, b ∈ R, the Jackson integral or q-integral of arbitrary function f : R → R on [a,b] is deﬁned by

+∞

b

qk bf(qkb) − af(qka) , (2.1)

f(x)dqx = (1 − q)

a

k=0

When f is continue on [a,b], we get that

lim

q→1

b

f(x)dqx =

a

b

a

f(x)dx.

3

