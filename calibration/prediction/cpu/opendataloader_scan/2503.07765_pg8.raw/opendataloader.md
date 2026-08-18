![](<2503.07765_pg8_images/imageFile1.png>)

1 . 0

0 . 5

7.2

45 ◦

0 . 0

Orthogonal

Non-orthogonal

~10

~0.5

0 . 0

0 . 5

1 . 0

Fig. 2. Constellation in terms of the basis formed by the decision boundaries [ d 0 d 1 ] when the signal vectors are orthogonal and not orthogonal.

# B. Upper Bound for Quasi-Biorthogonal Signaling

Here, we divert our attention to the case where M > 2 . Let A i + be the event of detecting + s i , and A i − be the event of detecting − s i . Then, the probability of a symbol error given + s i was transmitted is given by

$$
M =1 Pelsi = Pr U (Aj+U A;-) U Ai _ (75) j=0 j#i
$$

The right-hand side of (75) should be stated as the probability of one or more the indicated events happens. Then, taking note that for any pair of events A and B , Pr[ A ∪ B ] ≤ Pr[ A ] + Pr[ B ] , (75) implies

$$
M _1 Pr [Aj+ U Aj - U Ai _ +8; sent] (76) j=0 j#i Pelsi
$$

Making use of the results in Section V-A, this result can be written as

$$
Pelsi 1 = 1 = Q 77) No j=0 k=0 j#i
$$

where

$$
Pi,j,0 Isi = sj (78) Si Sj Pi,j,1 = Is; +Sjl
$$

(77) and assuming that the data symbols + Si, for i = 0,1, N 1, are equally likely to be transmitted,  one Using will find that the probability of a symbol error, Pe, is upper bounded by

$$
2 € p?j,k Pe < 1 _ =Q M No i=0 j=0 k=0 (79) jzi
$$

The simulation results presented in the next section reveal that this upper bound becomes tight as the SNR increases. This observation may be explained as follows. As the SNR increases, the events referred to on the right-hand side of (75) become nearly non-overlapping, equivalently, it will be unlikely that any pair of these events happen simultaneously. In that case, the inequality in (76) will become closer to an equality.

# C. Upper Bound for Quasi-Orthogonal Signaling

The desired bound here can be derived following those of the biorthogonal case with some minor modifications. First, for the case where M = 2 , the decision boundary that separates s 0 and s 1 is the bisect line between them. This is the line in the direction d 1 in Fig. 1(a). With this observation, the probability of a symbol error here is found to be

$$
Pe = (80) No
$$

Next, following the same line of thoughts as those in Section V-B, and removing A j − and A i − from the right-hand side (75) and subsequent equations, it is not hard to arrive at the following upper bound for probability of symbol error for the present case.

$$
2 € Pe (81) M No i=0 j=0
$$

# VI. N UMERICAL R ESULTS

In this section, to get insight to the theoretical findings of the previous sections, we present a set of numerical results that compare the symbol error rates (SERs) of the quasiorthogonal and quasi-biorthogonal signaling methods against their respective orthogonal and biorthogonal counterparts. The goal here is to explore the amount of performance loss incurred as the non-orthogonality of the symbol vectors increases. Also, through numerical results, we examine the tightness of the upper bounds that were derived in Section V. Here, to generate a set of non-orthogonal codes, we begin

with generating a random correlation matrix W with diagonal elements of unity. For W to be a valid correlation matrix, it should be symmetric, i.e., W T = W , and all of its eigenvalues should be non-negative. To satisfy these conditions, first, the off diagonal elements in the upper triangular part of R are chosen to be random and independent taken from a uniform distribution in the interval [ − ρ max , + ρ max ] . These elements are then copied to the lower triangular part of W so that to satisfy the symmetry condition W T = W . Finally, to make

