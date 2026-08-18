by performing actions, making observations, and receiving rewards, all without prior knowledge of the source’s dynamics, the potential usefulness of the updates to be queried, or the status of the update channels. Within this framework, the hub takes an action

a ( t ) ∈ A while the environment is in state s ( t ) ∈ S during the t -th slot. The action is passed to the environment, and after consulting the updated knowledge base, the hub observes the new state of the environment, s ( t + 1) . Based on this transition, the immediate net reward r ( t ) resulting from the chosen action is computed. The recurring interaction between the hub and the environment over T e steps is represented as a sequence ⟨ s ( t ) ,a ( t ) ,r ( t ) ,s ( t + 1) ⟩ T e t =0 . Specifically, the reward r ( t ) at the t -th slot is given by

$$
r(t) = Tu(s(t), a(t), s(t + 1)) vcpt (GoE(t + 1)) = uvcpt ( fc(a(t))) (18)
$$

where J is the Lagrange multiplier (see Section IV).

S space A , and the net rewards of the modeled CMDP in Section III-B . Leveraging the model-free approach, we develop a learningbased iterative algorithm to derive policies for solving the dual scheduling problem, i.e.,   P , from Section IV-A .

# B. Learning-Based Iterative Algorithm

We adopt a similar iterative process to that outlined in Algorithm 1 . The main distinction here is that we use modelfree, learning-based solutions to find the class of effect-aware scheduling policies, π , within the inner loop. 1) Computing π : To derive the scheduling policies, we

adapt two prominent on-policy DRL algorithms, advantage actor-critic (A2C) [ 35 ] and proximal policy optimization (PPO) [ 36 ], along with an off-policy algorithm, Deep Qnetwork (DQN) [ 37 ]. These algorithms are particularly wellsuited for decision-making in high-dimensional spaces. In each algorithm, the Q-function or the corresponding value

In each algorithm; the Q-function or the corresponding value function is computed based on the net reward defined in 18).

Algorithm 1 to determine the optimal Lagrange multiplier for a given policy from the inner loop. In this context, the bisection search method is employed in the outer loop to iteratively and gradually identify the minimum Lagrange multiplier that meets the cost constraint of the scheduling problem P , as formulated in ( 6 ).

# VI. S IMULATION R ESULTS

In this section, we evaluate the performance of the proposed model-based and model-free solutions outlined in Sections IV and V , respectively, within the context of effect-aware query scheduling. To assess their effectiveness, we compare these solutions against several well-established benchmark approaches.

# A. Setup and Assumptions

We consider system with N = 4 SAs observing a source characterized by M = actions over T = 1,000 slots. The usefulness of an update on the m-th attribute is mapped to a value within the range [0, 1], determined by applying

TABLE I P ARAMETERS FOR SIMULATION RESULTS .

<table>
  <tr>
    <th>Parameter</th>
    <th>Symbol</th>
    <th>Value</th>
    <th>Parameter</th>
    <th>Symbol</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>Number of</td>
    <td>T</td>
    <td>T 10 3</td>
    <td rowspan="3">Parameters shaping 4 2 4 Refs. point</td>
    <td> </td>
    <td rowspan="2">0.5</td>
  </tr>
  <tr>
    <td>Number of</td>
    <td>N</td>
    <td> </td>
    <td>Bcpt</td>
  </tr>
  <tr>
    <td>Number of Number of</td>
    <td>M</td>
    <td> </td>
    <td>Acpt</td>
    <td> </td>
  </tr>
  <tr>
    <td>Number of AAs</td>
    <td>K</td>
    <td> </td>
    <td>Refs. point</td>
    <td>GoEref</td>
    <td>0.2</td>
  </tr>
  <tr>
    <td>Corr:.  observation probability</td>
    <td>po,nm ,</td>
    <td>0.8</td>
    <td>Cost per</td>
    <td>fc(1)</td>
    <td>0.5</td>
  </tr>
  <tr>
    <td>Required attributes</td>
    <td> </td>
    <td> </td>
    <td>2 Cost flex.</td>
    <td> </td>
    <td>0.75</td>
  </tr>
  <tr>
    <td>Erasure probability</td>
    <td>Pe,n , Vn</td>
    <td>0.2</td>
    <td>Maximum</td>
    <td> </td>
    <td> </td>
  </tr>
  <tr>
    <td>Discount factor</td>
    <td> </td>
    <td>0.9</td>
    <td> </td>
    <td> </td>
    <td rowspan="2">10-6</td>
  </tr>
  <tr>
    <td>Shape parameters</td>
    <td> </td>
    <td> </td>
    <td>Tolerance sens</td>
    <td> </td>
  </tr>
  <tr>
    <td>for gm</td>
    <td> </td>
    <td>{0.5,5}</td>
    <td>Mixing factor</td>
    <td> </td>
    <td>0.5</td>
  </tr>
  <tr>
    <td>Size of usefulness</td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
  </tr>
</table>


$$
Qm =1 Bm 1 Ym (t)(1 Um (t)) (19) Bm B(am;
$$

at the t -th slot, where α m ,β m > 0 , ∀ m , are shape parameters, and B( · , · ) is Beta function. Besides, we consider GoE m ( t ) = u m ( t ) ∆ m ( t ) , ∀ m , and the CPT-based value function for an arbitrary x ∈ R is given by [ 12 ]

$$
(x Tref; (x) = Bcpt vcpt (x) = (xref 1 Jref , (20) Ucpt
$$

with α cpt = β cpt = 0 . 5 , and λ cpt = 2 being shape parameters under the given reference point x ref . For simplicity and to facilitate comparison with non-probabilistic scheduling methods, we assume w cpt ( x ) = x, ∀ x .

Finally, the cost constraint is enforced by introducing a cost flexibility index C flex multiplied by the discounted cumulative cost incurred from querying across all slots. Thus, we have

$$
vcpt ( fc(1)) (21) Cmax CAex
$$

where f c (1) indicates the fixed cost per query. Unless stated otherwise, the default simulation parameter values are outlined in Table I .

To implement the DRL algorithms, namely A2C, PPO, and DQN, we follow the default hyperparameter settings as considered in their respective original papers, i.e., [ 35 ], [ 36 ], and [ 37 ]. However, we adjust the discount factor according to Table I . We employ the Adaptive Moment Estimation (Adam) optimizer for both DQN and PPO, whereas the Root Mean Square Propagation (RMSprop) optimizer is used for A2C. For each DRL algorithm, a model is trained over 100 episodes of interaction. Each episode comprises 10 , 000 time slots, generating a total of T e = 10 6 environment steps. The key hyperparameters for these algorithms, along with their initial configurations, are summarized in Table II .

