DoF tuples achievable by classical coding schemes. The NS-assisted DoF region D NS is defined as the closure of all DoF tuples achievable by NS-assisted coding schemes. In particular, the classical sum-DoF d Σ , the NS-assisted sum-DoF d NS Σ are defined as d Σ ≜ max ( d 1 , ··· ,d K ) ∈D ( d 1 + ··· + d K ) , d NS Σ ≜ max ( d 1 , ··· ,d K ) ∈D NS ( d 1 + ··· + d K ) , respectively.

# 3 Results

# 3.1 Fully Connected CoMP BC

Our first result, stated in the following theorem, shows that NS-assistance does not improve the DoF region, or even the capacity region, in the fully-connected (Definition 3) CoMP BC.

Theorem 1 (Fully Connected CoMP BC Capacity and DoF Regions) . For a fully-connected CoMP BC network, the capacity regions with and without NS-assistance are characterized, under the F q model as,

$$
C(q) RK) € RK + RK < C1(q) } , (17) CNS ,
$$

and under the Gaussian model as,

$$
RK) € RK R1 + R2 + 4 (18) CNS , RK
$$

where C 1 ( q ) ,C 1 ( P ) represent the single-user capacity of Rx1 under the two models. Note that C 1 ( q ) = log 2 ( q ) . The corresponding DoF regions, under both the F q model and the Gaussian model, are characterized as,

$$
= D = {(d1,d2, dK) € RK (19) DNS
$$

The key to Theorem 1 is the statistical-equivalence , or the same-marginals property of the receivers, which makes them indistinguishable from the transmitter’s perspective. The same-marginals argument [25,26] is a standard line of reasoning in classical literature that makes use of the fact that the probabilities of error experienced by the receivers for an arbitrary (classical) coding scheme depend only on the marginal channel distribution of each receiver. In our fully connected CoMP BC since the marginal distributions are identical across receivers, the same-marginals property ensures that the capacity and DoF regions remain unchanged if every receiver has exactly the same channel realizations as Rx1 , in every channel-use. Once all receivers observe the same channel output, even allowing full cooperation among the receivers cannot change the capacity or DoF regions. Therefore the sum-capacity cannot exceed the single-user capacity, and any allocation of rates across messages that does not exceed the single-user capacity is trivially achievable, implying immediately the classical capacity and DoF regions in Theorem 1. Beyond the classical case, in order to show that NS-assistance cannot improve the capacity and DoF regions, two additional facts are needed.

Fact 1: For a point to point (single user) channel, NS assistance cannot improve the capacity. Fortunately, this non-trivial fact is already well-established, as noted in Lemma 1 [8–10].

Fact 2: The same-marginals property still holds under NS-assistance, even when NS-assistance is available to all parties. 5

5 The same-marginals property has been shown in [16] for a BC with NS-assistance available to only the decoders, i.e., receivers, when the metric of interest is the sum of probabilities of error of the receivers.

