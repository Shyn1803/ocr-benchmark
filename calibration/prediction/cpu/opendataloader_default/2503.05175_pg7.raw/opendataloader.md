Self-Supervised Learning for Robust Optimization 7

Application 2 (Inventory Management Problem). We consider an inventory management problem inspired by the classical newsvendor model, extended to a multi-retailer system with a centralized warehouse, with a formulation adopted from [16]. N retailers face uncertain demand dz = d0z + Qzu, where d0z is the expected demand, u is a k-dimensional vector of uncertainty factors, and Qz is a matrix capturing the sensitivity of retailers’ demand to these factors. The stocking decisions x aim to maximize proﬁt across all retailers. Considering an auxiliary second stage variable y(u) representing sales (as in [16]), the problem is formulated as the following two-stage adjustable robust optimization:

maxx∈X,P∈IR P s.t. P ≤ rz⊤y(u) − coz⊤x ∀u ∈ U(z)

y(u) = min(x,d0z + Qzu) ∀u ∈ U(z) 1⊤x ≤ Cz

where the vector x is contained in X = {x : 0 ≤ x ≤ c}, and rz and coz are the revenue and cost per unit sold respectively. Using a linear decision rule [10] for

the second-stage decisions, i.e., y(u) = Y u+y0, we derive the following one-stage robust problem:

maxP∈IR,Y∈IRN×k,y0∈IRN,x∈X P

s.t. P ≤ rz⊤(Y u + y0) − c0z⊤x ∀u ∈ Uz Y u + y0 ≤ x, ∀u ∈ Uz Y u + y0 ≤ d0z + Qzu, ∀u ∈ Uz 1⊤x ≤ Cz.

We generate a synthetic dataset D = {(ri,c0i,d0i,Qi,uˆi)}Ni=1 for the inventory management problem, where uˆi represents the nominal value of the uncertainty factor.

For each application, we use a synthetically generated dataset to train a twolayer fully connected neural network with problem-speciﬁc activation functions, as described in Section 2, to approximate the optimal solution of the parametric optimization problem. The dataset is split into training (70%), validation (15%), and testing (15%). At test time, we compute the optimal robust solution using the Gurobi solver and evaluate the performance of our method based on feasibility, optimality, and computational eﬃciency. To assess feasibility, we compute the average maximum constraint violation over the test set, deﬁned as maxj g ¯zj (h(z)) , where g¯zj is given in Assumption 2, and report the percentage of feasible solutions produced by the learned model. For optimality, we measure regret deﬁned as (fz∗ − fˆz)/fz∗, where fz∗ is the optimal objective value obtained by Gurobi, and fˆz is the objective value of the solution provided by the learned model. Finally, to evaluate computational eﬃciency, we compare the average computational time required by both Gurobi and the learned solver reported in seconds.

Compared to the supervised learning approach, the solution provided by our method achieves a high level of feasibility, as shown in Table 1, whereby

