Application 2 (Inventory Management Problem). We consider an inventory management problem inspired by the classical newsvendor model, extended to a multi-retailer system with a centralized warehouse, with a formulation adopted from [16]. N retailers face uncertain demand d z = d 0 z + Q z u , where d 0 z is the expected demand, u is a k -dimensional vector of uncertainty factors, and Q z is a matrix capturing the sensitivity of retailers’ demand to these factors. The stocking decisions x aim to maximize proﬁt across all retailers. Considering an auxiliary second stage variable y ( u ) representing sales (as in [16]), the problem is formulated as the following two-stage adjustable robust optimization:

$$
maxrex ,PelR P S.t. Vu € U(z) y(u) = min(x, = 1 < Cz
$$

where the vector x is contained in X = { x : 0 ≤ x ≤ c } , and r z and c o z are the revenue and cost per unit sold respectively. Using a linear decision rule [10] for the second-stage decisions, i.e., y ( u ) = Y u + y 0 , we derive the following one-stage robust problem:

$$
maxPeR,YeRRN xk P S.t P <rT(Yu + yo) 1 Vu € Uz Yu + yo < 2, Vu € Uz Vu € Uz x < Cz. 1T
$$

We generate a synthetic dataset D = { ( r i ,c 0 i ,d 0 i ,Q i , ˆ u i ) } N i =1 for the inventory management problem, where ˆ u i represents the nominal value of the uncertainty factor.

For each application, we use a synthetically generated dataset to train a twolayer fully connected neural network with problem-speciﬁc activation functions, as described in Section 2, to approximate the optimal solution of the parametric optimization problem. The dataset is split into training (70%), validation (15%), and testing (15%). At test time, we compute the optimal robust solution using the Gurobi solver and evaluate the performance of our method based on feasibility, optimality, and computational eﬃciency. To assess feasibility, we compute the average maximum constraint violation over the test set, deﬁned as max j   ¯ g j z ( h ( z ))   , where ¯ g j z is given in Assumption 2, and report the percentage of feasible solutions produced by the learned model. For optimality, we measure regret deﬁned as ( f ∗ z − ˆ f z ) /f ∗ z , where f ∗ z is the optimal objective value obtained by Gurobi, and ˆ f z is the objective value of the solution provided by the learned model. Finally, to evaluate computational eﬃciency, we compare the average computational time required by both Gurobi and the learned solver reported in seconds.

Compared to the supervised learning approach, the solution provided by our method achieves a high level of feasibility, as shown in Table 1, whereby

