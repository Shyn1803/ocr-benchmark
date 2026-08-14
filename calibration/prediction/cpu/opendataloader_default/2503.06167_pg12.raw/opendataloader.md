where η > 0 is the step-rate, k is the time step, Ni denotes the set of neighbours of agent i, Wij is the consensus weighting factor on the shared information over link (j,i), 0 ≤ µ < 1 is the momentum-rate, and variable yi(k) denotes the momentum term of node i at time k. The momentum term yi is added to improve the convergence rate and accelerate the solution. For initialization, the agents set their initial state values as xi(0) = bi and yi(0) = 0.

3.2. Solution Subject to Sector-Bound Nonlinearity

The data transmission channels (or the communication links) between agents might be subject to nonlinear constraints. This implies that the sent data ∂x

fj(k)), where gl : R  → R denotes the nonlinear mapping. Then, the decentralized solution is updated as,

# fj(k) over a link (j,i) is delivered to agent i as gl(∂x

j

j

xi(k + 1) =xi(k) + µyi(k)

Wij(gl(∂xjfj(k)) − gl(∂xifi(k))), (12)

+ η

j∈Ni

yi(k + 1) =xi(k + 1) − xi(k), (13)

where the weight matrix W is only weight-balanced and not necessarily stochastic.

Assumption 3. The nonlinear function gl(·) is assumed to be odd, strongly sign-preserving, and sector-bound.

One example of such link nonlinearity is saturation or clipping. Another example is log-scale quantization [55, 56] illustrated in Fig. 2 with its formula as follows:

gl(u) := sgn(u)exp(gu(log(|u|))), (14)

with gu(u) := ρ uρ (the operator [·] as rounding to the nearest integer) and ρ > 0 as the quantization level.

10

