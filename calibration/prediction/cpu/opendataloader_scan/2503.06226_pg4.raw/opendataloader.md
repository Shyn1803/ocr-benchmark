Di ﬀ erent from the state reconstruction given in ( 8 ) which is speciﬁc to the discrete-time systems, an alternative way to obtain the state information is to use a state observer to estimate the real state. Concretely, the state of system ( 1 ) can be estimated by using the following Luenberger observer:

$$
(10)
$$

It is known that the Luenberger observer ( 10 ) has the property that lim k →∞ ˆ x ( k ) = x ( k ) when all the eigenvaluesof ( A − LC ) are set within the unit circle under the observability condition. As given in Rizvi & Lin ( 2019 ), by setting ˆ x ( k ) = 0 , the estimated state ˆ x ( k ) can be parametrized by

$$
Ê(k) = Wyw(k) + Wuo(k) = Wy Wu (11) 0(k)
$$

where the parameterization matrices W y ∈ R n × np and W u ∈ R n × nm are determined by the coe ﬃ cients of the numerators in the transfer function matrix of the Luenberger observer system ( 10 ) with y ( k ) and u ( k ) being the inputs to the observer system, and the dynamics of ω ( k ) and σ ( k ) are given as

$$
B,y(k), 0(0) =0
$$

$$

$$

$$

$$

where A y ∈ and A u ∈ are user-deﬁned matrices determined by the eigenvalues of ( A − LC ), and ¯ B y ∈ R np × p and ¯ B u ∈ R nm × m are also user-deﬁned matrices which can make ( ¯ A y , ¯ B y ) and ( ¯ A u , ¯ B u ) controllable. It is easy to see that the data of ω ( k ) and σ ( k ) are available since their system matrices ( ¯ A y , ¯ B y ) and ( ¯ A u , ¯ B u ) are user-deﬁned.

Using the state parameterization in ( 11 ), the LQR problem can be solved by

$$
(12)
$$

when the state of the observer system convergesto the real state. It is worth mentioning that, if all the eigenvalues of ( A − LC ) are chosen as 0, the observer state ˆ x ( k ) converges to the real state x ( k ) when k ≥ n .

Thus, by using the state reconstruction in ( 8 ) or the state parameterization in ( 11 ), the LQR problem can be solved by the output feedback controller ( 9 ) or ( 12 ) when the accurate knowledge of system matrices are known.

# 2.3. Problem Formulation

In this paper, we aim to solve the LQR problem of linear discrete-time systems with completely unknown system matrices and unmeasurable state, which can be formulated as follows:

Problem 1. For system ( 1 ) where the system matrices A, B, and C are unknown, and the state x is unmeasurable,ﬁnd an optimal control policy sequence u ( k ) to satisfy

$$
V(x(o)) = k=0
$$

where P ∗ is the solution to ARE ( 6 ) .

The challenges of Problem 1 arise from the solution of ARE ( 6 ) and the design of the parameterization matrix ¯ M or ¯ W , which becomes di ﬃ cult in the absence of knowledge of the system matrices A , B , and C .

By combining the ADP method with a series of historical data of input and output, some ADP-based output feedback learning approaches focused on estimating the optimal control gain K ¯ M and K ¯ W directly, for instance, Chen et al. ( 2023 ); Gao et al. ( 2016 ); Lewis & Vamvoudakis ( 2011 ); Rizvi & Lin ( 2019 , 2020 , 2023 ). Particularly, it is proven in Rizvi & Lin ( 2023 ) that the requirement on the full row rank of ¯ W is necessary to guarantee the convergence performance of the aforementioned ADP-based output feedback learning approaches, so is the same requirementon ¯ M along the similar proof. However, as we can see from ( 8 ), under Assumption 1, the parameterization matrix ¯ M may not be of full row rank when the system matrix A has the eigenvalue 0. It follows from Rizvi & Lin ( 2023 , Theorem 4) that the parameterization matrix ¯ W may not be of full row rank when the matrices ( A − LC ) and A have common eigenvalues. On the other hand, as stated in Postoyan et al. ( 2016 ), the stability of the closed-loop system under the learning controlapproach proposed in Lewis & Vamvoudakis ( 2011 ) cannot be guaranteed. Although this issue was eliminated in Chen et al. ( 2023 ); Rizvi & Lin ( 2019 , 2023 ), the requirement of the convergence of state observer is needed to ensure the equivalence of the dynamic output feedback controller with the state feedback controller. This implies that the observer error will inﬂuence the convergence and optimality performance of the ADP-based output feedback learning control approaches in Chen et al. ( 2023 ); Rizvi & Lin ( 2019 , 2023 ).

To deal with the above issues, the objective of this paper is to provide a generalized learning based output feedback solution to Problem 1 and a detailed analysis of convergence, stability, and optimality for the proposed output feedback learning control approach.

In this section, we propose a novel output feedback learning control approach to solve the LQR problem. In particular, a new dynamic output feedback controller is designed that is equal to a static state feedback controller. Then, a data-driven learning algorithm is established to estimate the optimal control gain without prior knowledge of system matrices. Finally, the convergence, stability, and optimality analyses of the proposed learning control approach are given.

# 3.1. Dynamic Output Feedback Controller Design

Now we present a generalized dynamic output feedback controller design method, where the internal model is established without using any prior knowledge of the system dynamics. Moreover, the equivalence relationship between the proposed output feedback controller and the state feedback controller always holds even in the presence of observer error.

