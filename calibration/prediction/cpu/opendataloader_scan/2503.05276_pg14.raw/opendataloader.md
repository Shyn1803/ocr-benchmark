To address these issues, we introduce Constrained Reinforcement Learning (CRL), a reinforcement learning algorithm specifically designed for constrained MDPs. This algorithm, operating online, learns the values of post-decision states, V t ( s ), while also enabling constrained action selection within the feasible mixed-integer space using solvers like Gurobi. Similar to Eq. (10), which defines the Bellman equation for the pre-decision state x , we now formulate the Bellman function for the post-decision state s as follows:

$$
VA(s) = P {Ot = 0t} min (11)
$$

Q-values, Q ( x,a ), which represent the expected total cost when taking action a in state x and following the optimal policy thereafter. In our context, this is given by:

$$
Q(x,a) = cr(a) + (12)
$$

Q-learning is effective in traditional RL problems because immediate action costs are often uncertain or challenging to estimate. However, as in most operations research problems, our costs are explicitly defined, such as c x ( a ), including the selling profit and transportation costs. Instead of following the conventional approach of policy improvement through Q-learning, we leverage this structure by separating the Q-value into its easily calculable immediate costs of c x ( a ), and predicting only V ( s ), given as:

$$
Q(x,a) = cz(a) +V(s). (13)
$$

This separated approach reduces unnecessary computational overhead in estimating current action costs, and helps the model to solely focus learning V ( s ). Moreover, as demonstrated in previous research (Sun et al. 2022), learning post-decision state values is generally a more effective approach compared to learning of the action values. Consequently, our CRL holds significant potential for broader application in other constrained MDPs commonly encountered in operations research.

The proposed algorithm is detailed in Algorithm 1. It focuses on learning an approximation to V ( s ) ≈ ˆ v w ( s ) : = w ⊺ ψ ( s ), using a differentiable value function parameterization with features, ψ w ( s ). The estimated value for the post-decision state is calculated as a weighted linear combination of these features. The algorithm iteratively refines the feature weights, w , to improve the action selection process.

