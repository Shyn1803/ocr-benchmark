Published in Transactions on Machine Learning Research (02/2025)

The efficiency of simulated annealing around Tc has been reported in numerous studies. Kirkpatrick et al. (1983) demonstrated that during phase transition, the search becomes more efficient. Strobl & Barker (2016) showed that when using simulated annealing to solve phylogeny reconstruction, the search is constrained to a small valley of the search space when the temperature is below Tc. The search efficiency around Tc can also be seen in Figure 2 of (Cai & Ma, 2010b).

While some algorithms (Basu & Frazer, 1990; Cai & Ma, 2010a) have used critical temperature Tc to design the initial and final temperatures, its use for reheating is less common. Abramson et al. (1999) proposes a reheating strategy tied to function cost that implicitly involves Tc. However, this method lacks theoretical support and is sensitive to hyperparameters. Instead, our approach directly reheats to the critical temperature, which injects just the right amount of stochastic energy back into the system, enabling it to escape “wandering in contours” without incurring excessive randomness of a high-temperature regime.

# 5.2.2 Specific Heat

Determining the critical temperature in simulated annealing requires identifying the phase transition point during optimization, which is characterized by peaks in specific heat (Kirkpatrick et al., 1983; Strobl & Barker, 2016). In statistical physics, the system’s energy at temperature T, denoted as E(T), adheres to the Boltzmann distribution. Thus, the expected energy of a system can be seen as a function of the temperature, E[E(T)]. The specific heat at temperature T, denoted as CT, is traditionally defined in thermodynamics as the rate of change of the expected energy E[E(T)] to temperature (Aarts et al., 1987), given by CT = ∂E[∂TE(T)]. Integrating over the Boltzmann distribution allows deriving specific heat in terms of energy variance:

σ2(E(T)) T2

(9) where σ2(E(T)) is the variance of the system energy at T.

CT =

# 5.2.3 Determination of Critical Temperature

To determine the critical temperature based on specific heat, we first denote T(t) as the temperature at step t, C(t) as the specific heat at temperature T(t), and xt as the solution sampled at step t, then by selecting an appropriate sample size M, we define the approximation of C(t) as :

σ2({f(xt−M+1),··· ,f(xt)}) T(t)2

Cˆ(t) =

, t ≥ M (10)

where σ2({f(xt−M+1),··· ,f(xt)}) represents the variance in objective values over the M most recent steps. The critical temperature Tc can be determined as T(t∗), where t∗ = arg max

Cˆ(t). However, SA with

t≥M

gradient-based discrete samplers convergences rapidly in the initial stage, resulting in an abnormal initial peak in specific heat (due to the high variance). As the annealing progresses, the specific heat quickly decreases, eventually stabilizing at a level more typical of a critical temperature. This behavior is shown in Figure 4a&4b.

To address the abnormal peak, we introduce a “skip step” threshold, denoted as tskip, ensuring that the initial transient behavior is excluded from the analysis. Thus, the critical temperature is identified as T(t˜∗), where

Cˆ(t). (11)

t˜∗ = arg max

t≥tskip

Our method diverges from traditional SA reheat strategies (Abramson et al., 1999) by accounting for inhomogeneous chains and addressing gradient-based methods’ unique abnormal peaks.

# 5.3 Reheated Gradient-based Discrete Sampling for Combinatorial Optimization

Combining results in Section 5.1 and 5.2, we obtain the Reheated Sampling for Combinatorial Optimization algorithm (ReSCO), which is summarized in Algorithm 1. ReSCO is compatible with any gradient-based

8

