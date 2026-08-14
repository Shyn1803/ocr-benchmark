Hasturk: CRL for DIRP

14

To address these issues, we introduce Constrained Reinforcement Learning (CRL), a reinforcement learning algorithm specifically designed for constrained MDPs. This algorithm, operating online, learns the values of post-decision states, Vt(s), while also enabling constrained action selection within the feasible mixed-integer space using solvers like Gurobi. Similar to Eq. (10), which defines the Bellman equation for the pre-decision state x, we now formulate the Bellman function for the post-decision state s as follows:

# P{Ot = ϕt} cs(ϕt)+ min

Vt(s) =

at∈At(x)

ϕt∈Φt

{cx(at)+Vt+1(s′)} . (11)

As values of pre- and post-decision states, V (x) and V (s), there also exist traditionally adapted Q-values, Q(x,a), which represent the expected total cost when taking action a in state x and following the optimal policy thereafter. In our context, this is given by:

Q(x,a) = cx(a)+

P{O = ϕ}(cs(ϕ)+V (x′)) (12)

ϕ∈Φ

Note that t is omitted in Eq. (12) since, in the infinite-horizon setting, Qt(x,at), Vt(x), and Vt(s) converge to Q(x,a), V (x), and V (s).

Q-learning is effective in traditional RL problems because immediate action costs are often uncertain or challenging to estimate. However, as in most operations research problems, our costs are explicitly defined, such as cx(a), including the selling profit and transportation costs. Instead of following the conventional approach of policy improvement through Q-learning, we leverage this structure by separating the Q-value into its easily calculable immediate costs of cx(a), and predicting only V (s), given as:

Q(x,a) = cx(a)+V (s). (13)

This separated approach reduces unnecessary computational overhead in estimating current action costs, and helps the model to solely focus learning V (s). Moreover, as demonstrated in previous research (Sun et al. 2022), learning post-decision state values is generally a more effective approach compared to learning of the action values. Consequently, our CRL holds significant potential for broader application in other constrained MDPs commonly encountered in operations research.

The proposed algorithm is detailed in Algorithm 1. It focuses on learning an approximation to V (s) ≈ vˆw(s) := w⊺ψ(s), using a differentiable value function parameterization with features, ψw(s). The estimated value for the post-decision state is calculated as a weighted linear combination of these features. The algorithm iteratively refines the feature weights, w, to improve the action selection process.

