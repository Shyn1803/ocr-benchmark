To derive the asymptotic properties of the MCLEs, we use results obtained in [8] and [9]. In [8] we considered sums of square increments of an isotropic fractional Brownian ﬁeld based on the edges of the Delaunay triangles and provided asymptotic results using Malliavin calculus (see Theorem 1 in [8]). In [9] we considered sums of square increments of the pointwise maximum of two independent isotropic fractional Brownian ﬁelds and showed that the asymptotic behaviors of the sums depend on the local time at the level 0 of the diﬀerence between the two fractional Brownian ﬁelds and no more on the Gaussian limits of the sums of square increments of each isotropic fractional Brownian ﬁeld (see Theorem 2 in [9]). In this paper we generalize this result to the max-stable Brown-Resnick random ﬁeld which is built as the pointwise maximum of an inﬁnite number of isotropic fractional Brownian ﬁelds (see Theorem 3). Using approximations of the pairwise and triplewise CL objective functions, we then derive the asymptotic properties of the MCLEs (see Theorem 6). The rates of convergence of the estimators as well as their limit distributions are not standard and are speciﬁc to the structure of the max-stable process. It is important to identify them in order to avoid using the Gaussian distributions typically obtained with data from multiple time observations.

It is noteworthy that we only consider isotropic fractional Brownian ﬁelds with Hurst index in (0,1/2) as in [8] and [9]. This is not a very restrictive constraint since almost all empirical studies that use the spatial Brown-Resnick random ﬁeld obtain estimates in this interval (see e.g. [12, 13, 19, 20]).

Our paper is organized as follows. In Section 2 we present the family of stationary Brown-Resnick random ﬁelds introduced in [27], then we review some established concepts related to the Delaunay triangulation, and we end with the deﬁnition of the local time between two independent and identically distributed fractional Brownian random ﬁelds. In section 3, we ﬁrst study the asymptotic distributions of the “normalized” increments of the logarithm of the Brown-Resnick random ﬁeld based on pairs and triples of sites as the distances between sites tend to zero. We then provide asymptotic results for squared increment sums of the max-stable Brown-Resnick random ﬁeld. In Section 4, we introduce the randomized sampling scheme and deﬁne the CL estimators of the scale and Hurst parameters. The asymptotic properties of the MCLEs for these parameters are then given. The proofs and some intermediate results are deferred to Section 5 and Section 6.

# 2 Preliminaries

## 2.1 Max-stable Brown-Resnick random ﬁelds

In this paper we are concerned with the class of max-stable random ﬁelds known as Brown-Resnick random ﬁelds introduced in [27]. This class of random ﬁelds is based on Gaussian random ﬁelds with linear stationary increments. Recall that a random process (W (x))x∈Rd is said to have linear stationary increments if the law of (W (x + x0) − W (x0))x∈Rd does not depend on the choice of x0 ∈ Rd. A prominent example is the isotropic fractional Brownian ﬁeld where W (0) = 0 a.s. and semi-variogram given by

σ2 x α 2

var(W (x)) 2

γ (x) =

=

(2.1)

![](<2503.05880_pg5_images/imageFile1.png>)

![](<2503.05880_pg5_images/imageFile2.png>)

for some α ∈ (0,2) and σ2 > 0, where x is the Euclidean norm of x. The parameter σ is called the scale parameter while α is called the range parameter (H = α/2 is also known as the Hurst parameter and relates to the Ho¨lder continuity exponent of W). It is noteworthy that W is a self-similar random

5

