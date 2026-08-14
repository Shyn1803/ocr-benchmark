<table>
  <tr>
    <td>n<br><br></td>
    <td>p(z)<br><br></td>
    <td>g(z)</td>
    <td>a, b<br><br></td>
    <td>N z4<br><br>p(z)</td>
  </tr>
</table>


<table>
  <tr>
    <td>4<br><br></td>
    <td>z4 − 1</td>
    <td>-<br><br></td>
    <td>-</td>
    <td>z(z4+3) 4<br><br></td>
  </tr>
  <tr>
    <td>3</td>
    <td>(z − 1)2(z2 + az + b)<br><br></td>
    <td>(a − 2)z2+ (−3a + 2b)z − 4b<br><br></td>
    <td>a = 2<br>b = 3<br></td>
    <td>z(z3+z2+z+9) 12<br><br></td>
  </tr>
  <tr>
    <td>2</td>
    <td>(i) (z − 1)2(z − a)2<br><br></td>
    <td>2(2a − (a + 1)z)</td>
    <td>a = −1</td>
    <td>z(z2+3) 4<br><br></td>
  </tr>
  <tr>
    <td>2<br><br></td>
    <td>(ii) (z − 1)3(z − a)<br><br></td>
    <td>−(a + 3)z + 4a</td>
    <td>a = −3</td>
    <td>z(z2+2z+9) 12<br><br></td>
  </tr>
  <tr>
    <td>1</td>
    <td>(z − 1)4<br><br></td>
    <td>4<br><br></td>
    <td>-</td>
    <td>z(z+3) 4<br><br></td>
  </tr>
</table>


# Table 1: Newton maps N z4

p(z)

with an exceptional point

- 1. Let p be generic. If p is linear, then it follows from the Scaling property that NR(z) is conjugate to N z

z−1

. Let p be non-linear. As p is generic and N zd

p(z)

is a polynomial, we have zp′(z) − dp(z) = α for some non-zero α. Letting y = p(z), we have the first-order linear differential equation y′ − dzy = αz . The solution is

y ·

1 zd

=

α z ·

1 zd

dz + β = −

α dzd

+ β,

for an arbitrary constant β. Therefore, p(z) = βzd− αd and R(z) = βzzd

d−αd . Consider c such that cd = dβα and use the Scaling property to see that NR is conjugate to NβR(cz). We are done since βR(cz) = zzd

d−1 and the resulting Newton map is

zd+1+(d−1)z

d .

- 2. Let n denote the number of distinct roots of p. Using the Scaling property, we assume without loss of generality that 1 is a multiple root of p whenever p is not generic. Along with this, what is going to be repeatedly used in all the following cases is that g(z) is a non-zero constant (see Equation (3.1)).


- (a) Let deg(p) = 3. Then there are three cases depending on the values of n. If n = 3, then p is generic, and from the first part of this theorem, it follows that p(z) = z3 −1, and hence NR(z) = 13z(z3 +2). If n = 2, then p has a root with multiplicity 2 and therefore p(z) = (z−1)2(z−a), where a ̸= 0,1. In this case, g(z) = −(a + 2)z + 3a and therefore a = −2. Thus, NR(z) = z6(z2 + z + 4). If n = 1, then p(z) = (z − 1)3, and we get NR(z) = 13z(z + 2).

- (b) Let deg(p) = 4. All possible cases of p and the resulting Newton maps are

- given in Table 1.

(c) For deg(p) = 5, all the possible forms of p and resulting Newton maps are

- given in Table 2.




10

