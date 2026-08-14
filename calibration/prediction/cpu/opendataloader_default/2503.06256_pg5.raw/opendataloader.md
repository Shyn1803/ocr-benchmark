THE DISTRIBUTION OF RANDOM MULTIPLICATIVE FUNCTIONS 5

Previously it was only known (using arguments from [15]) that the low moments of these quantities should be of the same order of magnitude. Now, having shown that our variances concentrate around the mean square of an Euler product, we are in a hopeful position, since previous work of Saksman and Webb [30, Theorem 1.9] tells us that, when t is restricted to a bounded interval, we have convergence in distribution to an integral with respect to a random measure known as a critical Gaussian multiplicative chaos measure. In the following theorem, we extend their result to give convergence over the full range of integration. To state our result, we redeﬁne the Euler product over primes p ≤ x by

−1 in the Steinhaus case. This is a notational convenience that makes the statement of our theorem more natural.

F(x)(s) := p≤x 1 − fp(sp)

![](<2503.06256_pg5_images/imageFile1.png>)

Theorem 3 (Extension of Theorem 1.9 of Saksman and Webb [30]). For g ∈ Cl[a, b], denote g Cl[a,b] = lj=0 g(j) L∞[a,b]. For f a Steinhaus random multiplicative function, we have

2

(log log x)1/2 log x R

F(x)(1/2 + it) 1/2 + it

dt −→d Vcrit as x → ∞,

![](<2503.06256_pg5_images/imageFile2.png>)

![](<2503.06256_pg5_images/imageFile3.png>)

where E[Vcritq ] exists for each 0 < q < 1. Vcrit is deﬁned as the limit (in distribution) of Vn = − nn |1/g2+(t)it|

λ(dt) as n → ∞, where g(t) is a positive random continuous function

![](<2503.06256_pg5_images/imageFile4.png>)

2

such that, for each n > 0, all norms g Cl[−n,n] and 1/g Cl[−n,n] possess moments of all orders, and λ(dt) is a critical Gaussian multiplicative chaos measure. Note that g and λ

may not be independent. The random variable Vcrit is precisely the one that appears in Theorem 1.

For details of this weak convergence, see Section 7, and more speciﬁcally Section 7.2. An analogous theorem is not known in the Rademacher case (and would involve non-trivial adjustments to the argument). For this reason, we do not give a proof of Theorem 1 in the Rademacher case.

1.4. Connection to Gaussian multiplicative chaos. We now explain the connection between our variance (which we think of as mean squares of random Euler products like (1.2)) and the theory of Gaussian multiplicative chaos, restricting ourselves to the Steinhaus case. For an introduction to the theory, see Rhodes and Vargas [29]. A similar discussion can be found in the introduction of Harper [15]. Here, we put a particular emphasis on understanding the limiting distribution of our variances.

f(p) p1/2+it

We begin by noting that, for ﬁxed t, the quantity log |F(1/2 + it)| ≈ ℜ p≤

√x

![](<2503.06256_pg5_images/imageFile5.png>)

![](<2503.06256_pg5_images/imageFile6.png>)

is distributed like a Gaussian with mean 0 and variance approximately 12 p≤√x 1p =

![](<2503.06256_pg5_images/imageFile7.png>)

![](<2503.06256_pg5_images/imageFile8.png>)

![](<2503.06256_pg5_images/imageFile9.png>)

- 1

![](<2503.06256_pg5_images/imageFile10.png>)

- 2 log log x+O(1). Consequently, we think of X(t) = log |F(1/2+it)| as a Gaussian ﬁeld. The reader is reminded that a key property of Gaussian ﬁelds is that their distribution is completely determined by their means, E[X(t)] (which will be zero in the Steinhaus case), and their covariances, E[X(t1)X(t2)]. With this in mind, we rewrite our variances


1/2

1 0 e2X(t) dt. For simplicity, we have restricted ourselves to a compact interval and ignored the denominator. It is natural to normalise our integral so that the integrand has expectation one, and, if X(t) were actually Gaussian for each t ∈ [0, 1], the correct2 renormalisation would be to multiply the integrand by e−2EX(t)

in (1.2) as (log logx)

![](<2503.06256_pg5_images/imageFile11.png>)

log x

2

. This accounts

for the factor of log1x in (1.1), so our variances are roughly (1.3) (log log x)1/2

![](<2503.06256_pg5_images/imageFile12.png>)

1

exp 2X(t) − 2E X(t)2 dt,

0

![](<2503.06256_pg5_images/imageFile13.png>)

2This follows from the moment generating function for Gaussian random variables.

