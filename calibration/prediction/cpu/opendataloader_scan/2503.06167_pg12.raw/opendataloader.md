where η > 0 is the step-rate, k is the time step, N i denotes the set of neighbours of agent i , W ij is the consensus weighting factor on the shared information over link ( j,i ), 0 ≤ µ < 1 is the momentum-rate, and variable y i ( k ) denotes the momentum term of node i at time k . The momentum term y i is added to improve the convergence rate and accelerate the solution. For initialization, the agents set their initial state values as x i (0) = b i and y i (0) = 0.

# 3.2. Solution Subject to Sector-Bound Nonlinearity

The data transmission channels (or the communication links) between agents might be subject to nonlinear constraints. This implies that the sent data ∂ x j f j ( k ) over a link ( j,i ) is delivered to agent i as g l ( ∂ x j f j ( k )), where g l : R  → R denotes the nonlinear mapping. Then, the decentralized solution is updated as,

$$
(12)
$$

$$
(13)
$$

where the weight matrix W is only weight-balanced and not necessarily stochastic.

Assumption 3. The nonlinear function g l ( · ) is assumed to be odd, strongly sign-preserving, and sector-bound.

One example of such link nonlinearity is saturation or clipping. Another example is log-scale quantization [55, 56] illustrated in Fig. 2 with its formula as follows:

$$
(14)
$$

with g u ( u ) := ρ   u ρ   (the operator [ · ] as rounding to the nearest integer) and ρ > 0 as the quantization level.

