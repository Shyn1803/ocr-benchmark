obtained from validating whether the LB method satisﬁes the stability structure [38, 50], but also the convergence proof of the nonlinear problems can be established [30, 29]. Nevertheless, such stability has only been demonstrated for the D2Q9 orthogonal MRT model and how to prove it for many other MRT models is still unclear. To bridge this knowledge gap, Yong et al. [48] put forward an automatic approach for the stability analysis of MRT-LB models and applied it to ten diﬀerent MRT-LB models [20, 21, 41, 32, 35, 17, 23]. The key step in this approach is to decompose the Jacobian matrix of the collision term in the LB model into the product of a symmetric semi-negative deﬁnite matrix and a diagonally positive deﬁnite matrix, in particular, this decomposition process can be automatically veriﬁed by a simple computer code. With the aid of this work [48], in our current study, we will develop a high-order LB model for (1) and present its explicit stability structure preserving condition.

The remainder of this paper is structured as follows. In Section 2, we present the MRT-LB model for the ddimensionaldiagonal-anisotropicdiﬀusion equation. In Section 3, throughthe direct Taylor expansion, we ﬁrst deduce the conditions that ensure the present MRT-LB model to be fourth-order consistent with the diagonal-anisotropic diﬀusion equation, and then present the fourth-order initialization scheme for the MRT-LB model. Thereafter, the condition which guarantees that the MRT-LB model can satisfy the stability structure is provided, and the relationship between the stability structure preserving condition and the L2 stability of the MRT-LB model is also discussed. Some numerical experiments are carried out in Section 4, and ﬁnally some conclusions are summarized in Section 5.

2. The MRT-LB model for the diagonal-anisotropic diﬀusion equation

In this section, we will present a uniﬁed MRT-LB model for the diagonal-anisotropic diﬀusion equation (1), where the transformation matrix constructed in a natural way and the DdQ(2d2 + 1) lattice structure are employed. In particular, for the isotropic diﬀusion equation, another MRT-LB model with the DdQ(2d + 1) lattice structure [fewer discrete velocities than the DdQ(2d2 + 1) lattice structure] is also provided.

- 2.1. Spatial and temporal discretization For the sake of brevity and to facilitate the following analysis, the physical domain Ω is ﬁrst discretized into a

uniform mesh L with a lattice spacing ∆x > 0, where L = ∆xZd, and the corresponding lattice node is denoted by xi. The time is uniformly discretized as tn = n∆t, where ∆t > 0 represents the time step. The lattice velocity in the LB method can then be expressed as c = ∆x/∆t. For the diagonal-anisotropic diﬀusion equation (1), the diﬀusive scaling (∆t ∝ ∆x2) is adopted in this work. Without loss of generality, we can also take ∆t = ξ∆x2, where the parameter ξ ∈ R+ and ξ = 0 when ∆x, ∆t → 0.

- 2.2. The MRT-LB model


To develop a high-order LB method for the diagonal-anisotropic diﬀusion equation (1), we here adopt the general MRT-LB model [21, 6, 7] with some additional adjustable relaxation parameters, which can be used to eliminate some certain high-order truncation errors of the LB method, in which the evolution equation can be written as

q

fk(x + ck∆t, t + ∆t) = fk(x, t) −

i=1

q

Λki fi − fieq (x, t) + ∆t

i=1

Λ 2 ki

Ri (x, t), k ∈ 1, q , 1 (2)

I −

![](<2503.06817_pg3_images/imageFile1.png>)

where fk(x, t), fkeq(x, t), and Rk represent the distribution function, equilibrium distribution function, and discrete source term at position x and time t, respectively. In terms of the present MRT-LB model (2) for (1), we consider the

DdQq lattice structure with the number of the discrete velocities q = (2d2 + 1). To be speciﬁc, the velocity set c of the

3

