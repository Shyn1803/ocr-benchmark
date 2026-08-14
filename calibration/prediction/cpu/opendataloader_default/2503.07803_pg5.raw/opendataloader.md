value of each sampled Feynman graph to about 10−3 relative accuracy. The resulting number provides one data point for an evaluated period Feynman integral. We repeat these steps a large number of times. For example, Figure 1 summarizes all 44027 data points we obtained at 17 loops by running Algorithm 1 and the tropical sampling algorithm the same number of times.

# 3 Results

## 3.1 Histograms of Feynman integrals at large loop order

We used the methods described in the last section to generate representative samples of primitive divergent ϕ4-theory graphs and evaluate their period Feynman integrals at loop orders 8 to 17. The number of graphs we sampled at each loop order is listed in Table 1. We ran the computation in bunches at low priority on the ETH Euler computing cluster. Due to a maintenance event, our computation was interrupted, and some data points were lost. Hence, the number of samples differs slightly at each loop order, but there is no correlation between the probability of a data point being lost and its value. At 17 loops, we took fewer samples because we only had limited access to the required large-memory nodes.

Figure 1 and Figure 2 depict our results as histograms. All our obtained data points of randomly sampled Feynman graphs are also available as machine-readable tables in the ancillary material to the arXiv version of this article. We evaluated each Feynman graph to 10−3 relative accuracy using the tropical sampling approach. As this uncertainty is small compared to the statistical uncertainty that stems from the variance of the different Feynman graphs, we can neglect this uncertainty. We confirmed this explicitly by performing our analysis with the uncertainty included and obtaining identical results.

Our data suggests that the distribution of period Feynman integrals is modelled well by the distribution (2) for L → ∞. At each loop order, we fitted the parameters α,λ, and P0 by maximizing the logarithmic likelihood function

log Pi P0

log log Pi P0

log L = N (α log λ − log Γ(α)) + (α − 1)

− λ

,

i

i

where we sum over all period samples P1,...,PN at a specific loop order. As the number of samples N is large, we can estimate the uncertainties of these parameters by approximating the prior distribution using a Gaussian. The resulting parameters with uncertainties are listed in Table 1. The uncertainties of the fit parameters were extremely large for L ∈ {8,9}. So, we discarded these fits. The fitted probability distributions are depicted as red lines in Figure 1 and Figure 2.

We checked Conjecture 1 quantitatively using Pearson’s χ2 test: Let Oi be the number of evaluated period Feynman integrals that fall into the i-th percentile of the distribution (2) with the fitted maximum likelihood parameters at the respective loop order. The expectation value of the random variable Oi is obviously N/100. So, under the hypothesis that our data follows (2), the quantity χ2 = 100N i(Oi − 100N )2 is expected to follow a χ2-distribution with mean 100−3 = 97, as three parameters are fitted. Table 1 shows that the ratio χ2/97 approaches 1 with increasing loop order, consistent with Conjecture 1. Figure 2 illustrates how the distribution is approached with increasing loop number, providing further evidence for Conjecture 1.

## 3.2 Extrapolating βLprim to all loop orders using instanton input

The results of [30] suggest that the moments ⟨P(G)k⟩L diverge for L → ∞ if k ≥ 2 (see Table 8 and the discussion before eq. (4.8) of [30]). Hence, for sufficiently large loop order, the central

5

