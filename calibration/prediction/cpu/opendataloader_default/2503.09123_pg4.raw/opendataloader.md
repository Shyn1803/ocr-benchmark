matrix, referred to later as the input regularization) or to penalize the rate of change of the control (with t tf

u˙⊤(t)Ru˙(t)dt, referred to later as the input rate regularization). For DOPs with a large number of input variables and complex structures, managing the regularization to limit its impact on solution optimality can be quite difﬁcult.

0

On the other hand, the integrated residual approach, as a generalization of the collocation method, offers greater ﬂexibility in balancing solution accuracy and optimality on a given discretization mesh [4]. It is also more reliable when handling challenging problems where DC encounters difﬁculties [3]. However, this ﬂexibility can be a double-edged sword. While it allows for more accurate solutions of the DOP on coarser meshes, potentially saving computation time, it also requires additional expertise and care. For instance, the scaling of the variables and dynamic constraints, as well as the choice of trade-offs in different aspects of the numerical optimal solution (e.g. optimality vs. accuracy), can signiﬁcantly affect the solution process. Moreover, efﬁcient and reliable implementations of QPM require specialized DDOP solver designs, and both QPM and DAIR necessitate additional conﬁguration parameters in comparison to DC.

III. INTEGRATED RESIDUAL REGULARIZED DIRECT COLLOCATION

The development of IRR-DC aims to bring the beneﬁt of integrated residual approaches in handling challenging problems to the DC framework, while maintaining DC’s ease of implementation and computational efﬁciency as much as possible.

The DDOP formulation arising from IRR-DC is as follows: min

- 1

![](<2503.09123_pg4_images/imageFile1.png>)

- 2ρ


R(χ,υ,t0,tf,p) (12a) subject to, for all k ∈ IK and i ∈ IN(k),

Jh (χ,υ,t0,tf,p) +

χ,υ,p,t0,tf

f x˜ ˙(k)(di(k)),x˜(k)(d(ik)),u˜(k)(d(ik)),d(ik),p = 0, (12b) γ(k) χ(k),υ(k),t0,tf,p ≤ 0, (12c)

and for some ki ∈ IK and kj ∈ IK, φE χ1(ki),χ(Nkj)

,υ1(ki),υN(ki)

,t0,tf,p = 0, (12d) φI χ1(ki),χ(Nkj)

(K)

(K)

,υ1(ki),υN(ki)

,t0,tf,p ≤ 0. (12e)

(K)

(K)

For DOPs with consistent overdetermined constraints [4], [5], (12b) may make the DDOP infeasible leading to convergence challenges. Under the IRR-DC framework with the integrated residuals directly penalized in the objective, it is also possible to relax (12b) to

−ǫ ≤ f x˜ ˙(k)(d(ik)),x˜(k)(d(ik)),u˜(k)(d(ik)),d(ik),p ≤ ǫ,

(12f) instead, with ǫ a vector of suitably chosen small constants.

The choice of ρ in IRR-DC can be seen as a mechanism for balancing solution accuracy and optimality for a given discretization mesh design. A large value of ρ drives the solution of (12) towards the DC solution, prioritizing the reduction of the original objective. However, as later shown

in Figure 2 with the example problem, a low objective value reported by the DDOP solver may be misleading. As ρ decreases, the method can automatically converge to a more accurate solution when multiple solutions exist with minimal or negligible differences in nominal cost. Further reduction of ρ leads to a solution that is heavily biased towards higher accuracy, albeit at the cost of a higher objective value.

The practical advantage of IRR-DC is that, with (12b) or (12f), the need for carefully selecting conﬁguration parameters (e.g. for ρ) and scaling parameters (e.g. for dynamic constraints) is signiﬁcantly reduced compared to QPM. This allows the problem to be directly solved using most offthe-shelf DDOP solvers, in contrast to QPM, which prefers a tailored DDOP solver. Additionally, compared to the alternating iterative process of DAIR, IRR-DC is easier to implement, demands less prior knowledge and requires fewer conﬁguration parameters.

IV. EXAMPLE PROBLEMS

Here, we present two example problems to demonstrate the main advantages of the IRR-DC. Both DOPs are transcribed using the optimal control software ICLOCS2 [9], and numerically solved to a tolerance of 10−9 with NLP solver IPOPT [10] (version 3.12.9).

A. Singular Control Example: Goddard Rocket

The Goddard rocket problem [11] is a frequently used example for the analysis of optimal control problems with singular arcs. The problem aims to maximize the highest altitude reachable by a rocket using a ﬁxed amount of propellant. Depending on the ﬁdelity of the modeling of the atmospheric drag, different solution structures have been identiﬁed for the optimal control input. When neglecting or considering linear drag only, the solution is shown to be bang-bang, i.e. to exhaust all propellant with maximum thrust at launch and initial ascent, and then coasting to the highest point. With a quadratic drag model commonly used in subsonic ﬂights [12], the optimal solution structure changes to bang-singular-bang with an intermediate low thrust proﬁle.

1) Suppression of singular arc ﬂuctuations: In this example, we implement the Goddard rocket problem as described in [2, Ex. 4.9]. Using DC, it is known for the solution to be oscillatory on the singular arc if no special treatment is implemented. To remove the singular arc oscillations, a multiphase formulation is typically used with additional constraints known as singular arc conditions imposed speciﬁcally for the second phase, which corresponds to the one with singular control.

In [4], the ability of the integrated residual method of DAIR to alleviate the oscillations on the singular arc has been demonstrated on a ﬁxed equidistant discretization mesh. The IRR-DC method yields similar improvements to the results: the large ﬂuctuations on the singular arc have been suppressed (Figure 1), obtaining solutions of much higher accuracy in all measures (Table I).

