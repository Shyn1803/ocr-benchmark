7

by performing actions, making observations, and receiving rewards, all without prior knowledge of the source’s dynamics, the potential usefulness of the updates to be queried, or the status of the update channels.

Within this framework, the hub takes an action a(t) ∈ A while the environment is in state s(t) ∈ S during the t-th slot. The action is passed to the environment, and after consulting the updated knowledge base, the hub observes the new state of the environment, s(t + 1). Based on this transition, the immediate net reward r(t) resulting from the chosen action is computed. The recurring interaction between the hub and the environment over Te steps is represented as a sequence ⟨s(t),a(t),r(t),s(t + 1)⟩T

t=0. Specifically, the reward r(t) at the t-th slot is given by

e

# r(t) = rµ(s(t),a(t),s(t + 1))

= vcpt(GoE(t + 1)) − µvcpt+ (fc(a(t))) (18) where µ is the Lagrange multiplier (see Section IV).

This formalism defines the state space S, the action space A, and the net rewards of the modeled CMDP in Section III-B. Leveraging the model-free approach, we develop a learningbased iterative algorithm to derive policies for solving the dual scheduling problem, i.e., P, from Section IV-A.

B. Learning-Based Iterative Algorithm

We adopt a similar iterative process to that outlined in Algorithm 1. The main distinction here is that we use modelfree, learning-based solutions to find the class of effect-aware scheduling policies, π, within the inner loop.

1) Computing π: To derive the scheduling policies, we adapt two prominent on-policy DRL algorithms, advantage actor-critic (A2C) [35] and proximal policy optimization (PPO) [36], along with an off-policy algorithm, Deep Qnetwork (DQN) [37]. These algorithms are particularly wellsuited for decision-making in high-dimensional spaces.

In each algorithm, the Q-function or the corresponding value function is computed based on the net reward defined in (18).

2) Computing µ∗: We employ the same method as in Algorithm 1 to determine the optimal Lagrange multiplier for a given policy from the inner loop. In this context, the bisection search method is employed in the outer loop to iteratively and gradually identify the minimum Lagrange multiplier that meets the cost constraint of the scheduling problem P, as formulated in (6).

VI. SIMULATION RESULTS

In this section, we evaluate the performance of the proposed model-based and model-free solutions outlined in Sections IV and V, respectively, within the context of effect-aware query scheduling. To assess their effectiveness, we compare these solutions against several well-established benchmark approaches.

A. Setup and Assumptions

We consider a system with N = 4 SAs observing a source characterized by M = 2 attributes and K = 4 AAs performing actions over T = 1,000 slots. The usefulness of an update on

TABLE I PARAMETERS FOR SIMULATION RESULTS.

<table>
  <tr>
    <td>Parameter<br><br></td>
    <td>Symbol<br><br></td>
    <td>Value</td>
    <td> </td>
    <td>Parameter<br><br></td>
    <td>Symbol<br><br></td>
    <td>Value</td>
  </tr>
</table>


<table>
  <tr>
    <td>Number of slots</td>
    <td>T</td>
    <td>103</td>
    <td> </td>
    <td rowspan="3">Parameters shaping vcpt(·)</td>
    <td>αcpt</td>
    <td rowspan="2">0.5</td>
  </tr>
  <tr>
    <td>Number of SAs<br><br></td>
    <td>N</td>
    <td>4</td>
    <td> </td>
    <td>βcpt</td>
  </tr>
  <tr>
    <td>Number of attributes</td>
    <td>M</td>
    <td>2</td>
    <td> </td>
    <td>λcpt<br><br></td>
    <td>2</td>
  </tr>
  <tr>
    <td>Number of AAs</td>
    <td>K<br><br></td>
    <td>4</td>
    <td> </td>
    <td>Refs. point<br><br></td>
    <td>GoEref</td>
    <td>0.2</td>
  </tr>
  <tr>
    <td>Corr. observation probability</td>
    <td>po,nm, ∀n, m<br><br></td>
    <td>0.8</td>
    <td> </td>
    <td>Cost per query<br><br></td>
    <td>fc(1)<br><br></td>
    <td>0.5</td>
  </tr>
  <tr>
    <td>Required attributes</td>
    <td>|Mk|, ∀k<br><br></td>
    <td>2</td>
    <td> </td>
    <td>Cost flex. index<br><br></td>
    <td>Cflex<br><br></td>
    <td>0.75</td>
  </tr>
  <tr>
    <td>Erasure probability</td>
    <td>pe,n, ∀n<br><br></td>
    <td>0.2</td>
    <td> </td>
    <td>Maximum AoI<br><br></td>
    <td>∆max</td>
    <td>4</td>
  </tr>
  <tr>
    <td>Discount factor</td>
    <td>γ<br><br></td>
    <td>0.9</td>
    <td> </td>
    <td>Converg. sens.<br><br></td>
    <td>ϵπ<br><br></td>
    <td rowspan="2">10−6</td>
  </tr>
  <tr>
    <td rowspan="2">Shape parameters for gm(·; ·), ∀m</td>
    <td>{α1, α2}<br><br></td>
    <td>{0.5, 2}</td>
    <td> </td>
    <td>Tolerance sens.<br><br></td>
    <td>ϵµ</td>
  </tr>
  <tr>
    <td>{β1, β2}<br><br></td>
    <td>{0.5, 5}</td>
    <td> </td>
    <td>Mixing factor</td>
    <td>η<br><br></td>
    <td>0.5</td>
  </tr>
  <tr>
    <td>Size of usefulness</td>
    <td>|U|<br><br></td>
    <td>4</td>
    <td> </td>
    <td>–<br><br></td>
    <td>–</td>
    <td>–</td>
  </tr>
</table>


the m-th attribute is mapped to a value within the range [0,1], determined by applying

m−1

m−1 B(αm,βm)

yα

m (t)(1 − ym(t))β

(19)

gm(t;ym(t)) = min 1,

at the t-th slot, where αm,βm > 0,∀m, are shape parameters, and B(·,·) is Beta function. Besides, we consider GoEm(t) =

um(t) ∆m(t),∀m, and the CPT-based value function for an arbitrary x ∈ R is given by [12]

vcpt+ (x) = (x − xref)α

# , x ≥ xref; vcpt− (x) = −λcpt(xref − x)β

cpt

vcpt(x) =

# , x < xref,

cpt

(20)

with αcpt = βcpt = 0.5, and λcpt = 2 being shape parameters under the given reference point xref. For simplicity and to facilitate comparison with non-probabilistic scheduling methods, we assume wcpt(x) = x,∀x.

Finally, the cost constraint is enforced by introducing a cost flexibility index Cflex multiplied by the discounted cumulative cost incurred from querying across all slots. Thus, we have

∞

vcpt+ fc(1) 1 − γ

γtvcpt+ fc(1) = Cflex

(21)

Cmax = Cflex

t=0

where fc(1) indicates the fixed cost per query. Unless stated otherwise, the default simulation parameter values are outlined in Table I.

To implement the DRL algorithms, namely A2C, PPO, and DQN, we follow the default hyperparameter settings as considered in their respective original papers, i.e., [35], [36], and [37]. However, we adjust the discount factor according to Table I. We employ the Adaptive Moment Estimation (Adam) optimizer for both DQN and PPO, whereas the Root Mean Square Propagation (RMSprop) optimizer is used for A2C. For each DRL algorithm, a model is trained over 100 episodes of interaction. Each episode comprises 10,000 time slots, generating a total of Te = 106 environment steps. The key hyperparameters for these algorithms, along with their initial configurations, are summarized in Table II.

