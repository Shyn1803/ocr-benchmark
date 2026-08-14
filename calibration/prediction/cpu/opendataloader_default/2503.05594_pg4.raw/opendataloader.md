agent is not trading. If ρ is a.s. symmetric and uniformly positive definite in time, this term induces an exponential decay of the price deviation to zero. This reflects that, following a trade, new orders gradually replenish the order book – a phenomenon known as the resilience effect. We emphasize, however, that our results do not require ρ to be a.s. symmetric and uniformly positive definite in time. Instead, we impose only weaker assumptions (see, e.g., Assumption 4.3 and Remark 4.4). In particular, our framework also accommodates models where price impact exhibits self-exciting behavior. For a discussion of qualitative effects of such negative resilience in the single-asset situation, we refer to [4]. Furthermore, note that ρ is not necessarily diagonal, making it another potential source of cross-effects in our model.

In addition to reaching the required terminal position ξ, the aim of the agent is to incur minimal costs associated with her trading activities. Let us consider the costs of a block trade at the time s ∈ [0,T] when trading according to a strategy X ∈ Afv(x,d) with the associated deviation DX. Observe that immediately prior to s we have the deviation DX(s−). By (1) the block trade ∆X(s) shifts the deviation DX(s−) to

DX(s) = DX(s−) + ∆DX(s) = DX(s−) + γ(s)∆X(s).

We next take the mid-prices and multiply the mid-prices by the amount of the traded shares. The block trade ∆X(s) is thus assigned the costs

DX(s−) + 21γ(s)∆X(s) ⊤∆X(s) = DX(s−)∆X(s−) + 12(∆X(s))⊤γ(s)∆X(s).

This explanation for the costs of a single block trade motivates the definition of the pathwise costs C(x,d,X) over the whole trading interval [0,T] by

C(x,d,X) =

- 1

- 2 [0,T]


(DX(s−))⊤ dX(s) +

(∆X(s))⊤γ(s)dX(s).

[0,T]

Then E[C(x,d,X)] describes the expected costs due to illiquidity when trading according to the finite-variation execution strategy X. This is one of the two summands in the definition of the costs

Jfv(x,d,X) = E[C(x,d,X)] + E

T

(X(s) − ζ(s))⊤Ξ(s)(X(s) − ζ(s))ds (2)

0

that are to be minimized.

The other summand in these costs, E[ 0 T(X(s) − ζ(s))⊤Ξ(s)(X(s) − ζ(s))ds], can be used to incorporate some kind of risk preference into the model via the choice of the matrix-valued process Ξ, which acts as a penalization, and the Rn-valued process ζ, which acts as a running target. We refer to Horst & Xia [36, Section 1.1] for an illustrative example of a possible choice for Ξ. The risk term is a further possible source of crosseffects in our model, since Ξ does not need to be diagonal.

To summarize, the stochastic control problem to minimize the costs (2) over all strategies X ∈ Afv(x,d) models the agent’s task to reach the terminal position ξ from the

4

