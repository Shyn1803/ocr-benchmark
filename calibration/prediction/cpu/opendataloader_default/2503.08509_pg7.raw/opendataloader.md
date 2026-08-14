Here, p(d|m) is the likelihood and p(m) is the prior distribution of the model. In the EnKF, Bayes’ theorem is used recursively to update the model at each observation point by using the last posterior model as the current prior p(mi) = p(mi−1|di−1). In the following, we will omit the time index, i, and only focus on updates at a single measurement point.

Assuming that all variables have Gaussian distributions and that there is a linear relationship between the earth model and the EM-response, one can derive an analytical solution for the mean and covariance of the conditional distribution [21]. Approximating all instances of covariance and mean by Monte-Carlo estimates results in the ensemble update equation, see, e.g. [14]

Ma = Mp + CM,g(M) Cg(M) + Cd −1 (D − g(Mp) + E). (2)

Here, M denotes the ensemble matrix where each column is a realization of the earth model: Mp is the prior ensemble for a given step; Ma is the ensemble ”analysis” matrix, conditioned to the new measurements. The shorthand g(M) denotes that the map from the model to synthetic EM-log has been applied to all columns (ensemble members) of M, D is an ensemble matrix where each column is a copy of the current observation, and E is an ensemble matrix of measurement perturbations where each column (ϵj) is a realization of the Gaussian measurement error ϵj ∝ N(0,Cd). Cd denotes the covariance matrix for the current measurements, CM,g(M) denotes the Monte-Carlo estimate of the cross-covariance between the model and the predicted data, and Cg(M) denotes the Monte-Carlo estimate of the auto-covariance matrix for the predicted data.

The updated ”analysis” ensemble of models, Ma, from the EnKF is the input to the optimization.

# 2.3 Optimization with approximate dynamic programming for decisions

The DISTINGUISH workflow incorporates an optimization step using ’naiveoptimistic’ ADP to optimize the remaining drilling trajectory based on updated GAN-geomodels. This method effectively navigates the high-dimensional space of possible trajectories, identifying the path that maximizes the operational objective by balancing geological target zones and operational constraints.

For each realization of GAN-geomodel in the ”analysis” ensemble, our ADP method constructs a reward matrix R that quantifies the geological and operational desirability of drilling various segments. Each entry Ri,j(m) in this matrix represents the potential reward of steering the drill bit from point i to point j, given a realization of GANgeomodel m. The goal is to find a sequential path πk∗(m) among the potential paths πk (starting from point k) that maximizes the cumulative reward:

πk∗(m) = arg max

Ri,j(m). (3)

πk

(i,j)∈πk

7

