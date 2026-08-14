0

log ( ( ) ( ))T T2

Trunc. SVD

6

graphon

10

8

log ( ( ) ( ))T T2

log ( ( ) ( ))T T2

10

20

0 1000 2000 3000 4000 5000

3

<table>
  <tr>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
  </tr>
  <tr>
    <td> </td>
    <td> </td>
    <td> </td>
    <td>n</td>
    <td> </td>
    <td> </td>
    <td> </td>
  </tr>
  <tr>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
  </tr>
  <tr>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
  </tr>
  <tr>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
  </tr>
</table>


12

2

14

rank

1

16

0

0 1000 2000 3000 4000 5000

0 200 400 600 800 1000

n

n

graphon

12

Trunc. SVD(A )

13

14

15

16

250 500 750 1000 1250 1500

n

Figure 1: Upper Left: difference between target functions for optimal interventions of a network on n vertices sampled from (1,1/2)-H¨lder graphon W1(x,y) = |x − y| and interventions based on hard-thresholding estimator. Lower Left: Rank of the hard-thresholding estimator for a network on n vertices sampled from W1(x,y). Midlle: Difference between target functions for optimal interventions of a network on n-vertices sampled from SBM with 4 comminties and interventions computed using a) graphon b) hard-thersholding estimator. Right: The difference between target functions for optimal interventions of a network A of size 10000 sampled from SBM with 4 communities and interventions based on a) graphon b) hard-thersholding estimator comupted for other network A′ of size n.

# 6 Conclusion

Driven by applications in graphon games, we developed an estimator for an unknown graphon based on a sampled network. Under standard regularity conditions for the graphon, our estimator possesses two key features: (i) it approximates the unknown graphon in the operator norm, and (ii) it is of low rank. We established upper bounds for the convergence rate and rank of the estimator. Furthermore, we demonstrated that the estimator yields near-optimal solutions for the social welfare problem in linear-quadratic graphon games, with efficient computation. We also quantified the convergence rates of the associated costs and the computational complexity relative to the network size.

# References

[Bandeira and van Handel, 2016] Bandeira, A. S. and van Handel, R. (2016). Sharp nonasymptotic bounds on the norm of random matrices with independent entries. The Annals of Probability, 44(4):2479–2506.

[Bisgard, 2020] Bisgard, J. (2020). Analysis and linear algebra: the singular value decomposition and applications, volume 94. American Mathematical Soc.

16

