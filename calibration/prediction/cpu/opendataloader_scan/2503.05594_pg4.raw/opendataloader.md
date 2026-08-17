agent is not trading. If ρ is a.s. symmetric and uniformly positive definite in time, this term induces an exponential decay of the price deviation to zero. This reflects that, following a trade, new orders gradually replenish the order book – a phenomenon known as the resilience effect. We emphasize, however, that our results do not require ρ to be a.s. symmetric and uniformly positive definite in time. Instead, we impose only weaker assumptions (see, e.g., Assumption 4.3 and Remark 4.4). In particular, our framework also accommodates models where price impact exhibits self-exciting behavior. For a discussion of qualitative effects of such negative resilience in the single-asset situation, we refer to [4]. Furthermore, note that ρ is not necessarily diagonal, making it another potential source of cross-effects in our model.

In addition to reaching the required terminal position ξ , the aim of the agent is to incur minimal costs associated with her trading activities. Let us consider the costs of a block trade at the time s ∈ [0 ,T ] when trading according to a strategy X ∈ A fv ( x,d ) with the associated deviation D X . Observe that immediately prior to s we have the deviation D X ( s − ) . By (1) the block trade ∆ X ( s ) shifts the deviation D X ( s − ) to

$$
(s) = DX (s-) + ADX(s) = DX
$$

We next take the mid-prices and multiply the mid-prices by the amount of the traded shares. The block trade ∆ X ( s ) is thus assigned the costs

$$
(s-)AX(s-) + 4(AX(s)) Ta(s)A.X(s) DX
$$

pathwise costs C ( x,d,X ) over the whole trading interval [0 ,T ] by

$$
C(s,d, X) = (s-))T dX(s) 2 (AX(s)) Tn(s) dX(s) (DX
$$

Then E [ C ( x,d,X )] describes the expected costs due to illiquidity when trading according to the finite-variation execution strategy X . This is one of the two summands in the definition of the costs

$$
~
$$

that are to be minimized.

The other summand in these costs, E [   T 0 ( X ( s ) − ζ ( s )) ⊤ Ξ( s )( X ( s ) − ζ ( s )) ds ] , can be used to incorporate some kind of risk preference into the model via the choice of the matrix-valued process Ξ , which acts as a penalization, and the R n -valued process ζ , which acts as a running target. We refer to Horst & Xia [36, Section 1.1] for an illustrative example of a possible choice for Ξ . The risk term is a further possible source of cross-

To summarize, the stochastic control problem to minimize the costs (2) over all strategies X ∈ A fv ( x,d ) models the agent’s task to reach the terminal position ξ from the

