agent seeks to maximize its cumulative reward. Let vector b = ( b (1) ,b (2) ,...,b ( |S| )) denote the belief state where b ( s ) is the probability that the true system state is s ∈ S . Starting from belief b at time t , the agent updates belief to b ′ at time t + 1 after executing action a and observing o as

$$
6(s') P(s'ls,a)b(s) Vs € $ . (2.1) P(olb, a)
$$

Naturally,   s ∈S b ( s ) = 1. The initial belief, b 0 , provides the probability distribution of the state at the beginning of the planning horizon. The beliefs derived from an initial belief, via a feasible sequence of actions and observations are called reachable belief points .

Figure 1 shows the belief states that are reachable from the initial belief state, b 0 = (0 . 5 , 0 . 5) in one stage for the well-known tiger problem presented by Kaelbling et al. (1998), considering three actions, Listen ( a 1 ), Open Left Door ( a 2 ), Open Right Door ( a 3 ), and two observations resulting from each action, under the assumption that opening a (left or right) door restarts the problem and resets the belief to (0 . 5 , 0 . 5). Appendix B contains a detailed description of the tiger problem.

![](<2503.08982_pg4_images/imageFile1.png>)

bo

(0.5,9.5)

a2

01

t+1

(0.85,0.15)

(0.15,0.85)

(0.5,0.5)

(0.5,0.5)

(0.5,0.5)

(0.5,0.5)

Figure 1: Tree structure of a two-stage tiger problem (Kaelbling et al. 1998). Circles represent belief states observed right before taking an action in each stage.

A policy π provides the sequence of actions to be taken over the planning horizon as a function of the belief state. The value function represents the expected cumulative reward obtained under the optimal policy, π ∗ . For a finite horizon problem, the following backward recursion computes the value function, V t ( b ), as,

$$
max b(s)R(s,a) + V b € (2.2) a€A seS 0€0 Bu, ,T _
$$

where B ⊔ denotes the |S| -dimensional belief space. The optimal policy for belief state b at time period t is defined as

$$
T* (b) = arg max b(s)R(s,a) + P(olb,a)Vt+1(b') (2.3) a€A 0€0
$$

Sondik (1971) showed that the value function is represented exactly by a piecewise-linear and convex function such that the value function for a specific period is represented by a set of |S| -

