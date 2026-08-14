agent seeks to maximize its cumulative reward. Let vector b = (b(1),b(2),...,b(|S|)) denote the belief state where b(s) is the probability that the true system state is s ∈ S. Starting from belief b at time t, the agent updates belief to b′ at time t + 1 after executing action a and observing o as

P(o|a,s′) s∈S P(s′|s,a)b(s) s′∈S P(o|a,s′) s∈S P(s′|s,a)b(s)

- P(o|a,s′)

- P(o|b,a) s∈S


b′(s′) =

P(s′|s,a)b(s) =

,∀s ∈ S . (2.1)

Naturally, s∈S b(s) = 1. The initial belief, b0, provides the probability distribution of the state at the beginning of the planning horizon. The beliefs derived from an initial belief, via a feasible sequence of actions and observations are called reachable belief points.

Figure 1 shows the belief states that are reachable from the initial belief state, b0 = (0.5,0.5) in one stage for the well-known tiger problem presented by Kaelbling et al. (1998), considering three actions, Listen (a1), Open Left Door (a2), Open Right Door (a3), and two observations resulting from each action, under the assumption that opening a (left or right) door restarts the problem and resets the belief to (0.5,0.5). Appendix B contains a detailed description of the tiger problem.

![](<2503.08982_pg4_images/imageFile1.png>)

Figure 1: Tree structure of a two-stage tiger problem (Kaelbling et al. 1998). Circles represent belief states observed right before taking an action in each stage.

A policy π provides the sequence of actions to be taken over the planning horizon as a function of the belief state. The value function represents the expected cumulative reward obtained under the optimal policy, π∗. For a finite horizon problem, the following backward recursion computes the value function, Vt(b), as,

Vt(b) = max

a∈A s∈S

b(s)R(s,a) +

P(o|b,a)Vtπ+1∗ (b′) ,∀ b ∈ B⊔, ⊔ ∈ {′,∞,...,T − ∞} , (2.2)

o∈O

where B⊔ denotes the |S|-dimensional belief space. The optimal policy for belief state b at time period t is defined as

πt∗(b) = arg max

b(s)R(s,a) +

a∈A s∈S

P(o|b,a)Vt+1(b′) . (2.3)

o∈O

Sondik (1971) showed that the value function is represented exactly by a piecewise-linear and convex function such that the value function for a specific period is represented by a set of |S|-

4

