matrix, referred to later as the input regularization) or to penalize the rate of change of the control (with   t f t 0 ˙ u ⊤ ( t ) R ˙ u ( t ) dt , referred to later as the input rate regularization). For DOPs with a large number of input variables and complex structures, managing the regularization to limit its impact on solution optimality can be quite difﬁcult.

On the other hand, the integrated residual approach, as a generalization of the collocation method, offers greater ﬂexibility in balancing solution accuracy and optimality on a given discretization mesh [4]. It is also more reliable when handling challenging problems where DC encounters difﬁculties [3]. However, this ﬂexibility can be a double-edged sword. While it allows for more accurate solutions of the DOP on coarser meshes, potentially saving computation time, it also requires additional expertise and care. For instance, the scaling of the variables and dynamic constraints, as well as the choice of trade-offs in different aspects of the numerical optimal solution (e.g. optimality vs. accuracy), can signiﬁcantly affect the solution process. Moreover, efﬁcient and reliable implementations of QPM require specialized DDOP solver designs, and both QPM and DAIR necessitate additional conﬁguration parameters in comparison to DC.

# III. I NTEGRATED R ESIDUAL R EGULARIZED D IRECT C OLLOCATION

The development of IRR-DC aims to bring the beneﬁt of integrated residual approaches in handling challenging problems to the DC framework, while maintaining DC’s ease of implementation and computational efﬁciency as much as possible.

The DDOP formulation arising from IRR-DC is as follows: 1

$$
min + (12a) X,v,psto,tf 2p
$$

subject to, for all k ∈ I K and i ∈ I N ( k ) ,

$$

$$

$$
ũ (12b) (x(k),u(k), to,tf,p) < 0, (I2c)
$$

and for some k i ∈ I K and k j ∈ I K ,

$$
(ki) =0, (12d) xfk;)
$$

$$
x{k;) (kj) v{ki) v(ki) <0. (12e) N(K) ,
$$

For DOPs with consistent overdetermined constraints [4], [5], (12b) may make the DDOP infeasible leading to convergence challenges. Under the IRR-DC framework with the integrated residuals directly penalized in the objective, it is also possible to relax (12b) to

$$
p < € (12f) ĩ(k) ũ(k)
$$

instead, with ǫ a vector of suitably chosen small constants.

The choice of p in IRR-DC can be seen as mechanism for balancing solution accuracy and optimality   for given discretization A large   value of p drives   the solution of (12) towards the reduction of the original objective. However; as later shown in Figure 2 with the example problem; a low objective value reported by the DDOP solver may be   misleading. As p decreases, the method can automatically converge to more accurate solution when multiple solutions exist with minimal Or negligible differences in nominal cost. Further   reduction of p leads to a solution that is heavily biased towards higher accuracy, albeit at the cost of a higher objective value.

The practical advantage of IRR-DC is that, with (12b) or (12f), the need for carefully selecting conﬁguration parameters (e.g. for ρ ) and scaling parameters (e.g. for dynamic constraints) is signiﬁcantly reduced compared to QPM. This allows the problem to be directly solved using most offthe-shelf DDOP solvers, in contrast to QPM, which prefers a tailored DDOP solver. Additionally, compared to the alternating iterative process of DAIR, IRR-DC is easier to implement, demands less prior knowledge and requires fewer conﬁguration parameters.

# E XAMPLE P ROBLEMS

Here, we present two example problems to demonstrate the main advantages of the IRR-DC. Both DOPs are transcribed using the optimal control software ICLOCS2 [9], and numerically solved to a tolerance of 10 − 9 with NLP solver IPOPT [10] (version 3.12.9).

# A. Singular Control Example: Goddard Rocket

The Goddard rocket problem [11] is a frequently used example for the analysis of optimal control problems with singular arcs. The problem aims to maximize the highest altitude reachable by a rocket using a ﬁxed amount of propellant. Depending on the ﬁdelity of the modeling of the atmospheric drag, different solution structures have been identiﬁed for the optimal control input. When neglecting or considering linear drag only, the solution is shown to be bang-bang , i.e. to exhaust all propellant with maximum thrust at launch and initial ascent, and then coasting to the highest point. With a quadratic drag model commonly used in subsonic ﬂights [12], the optimal solution structure changes to bang-singular-bang with an intermediate low thrust proﬁle.

1) Suppression of singular arc ﬂuctuations: In this example, we implement the Goddard rocket problem as described in [2, Ex. 4.9]. Using DC, it is known for the solution to be oscillatory on the singular arc if no special treatment is implemented. To remove the singular arc oscillations, a multiphase formulation is typically used with additional constraints known as singular arc conditions imposed speciﬁcally for the second phase, which corresponds to the one with singular control.

In [4], the ability of the integrated residual method of DAIR to alleviate the oscillations on the singular arc has been demonstrated on a ﬁxed equidistant discretization mesh. The IRR-DC method yields similar improvements to the results: the large ﬂuctuations on the singular arc have been suppressed (Figure 1), obtaining solutions of much higher accuracy in all measures (Table I).

