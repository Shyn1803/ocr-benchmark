# Natural Gradient Descent for Control

Adib Yaghmaie Hamidreza Modares

** Ramin Esmzad Farnaz

∗ Department of Mechanical Engineering, Michigan State University, East Lansing, MI 48824, USA (e-mails: { esmzadra, modaresh @msu.edu).

modaresh} @msu.edu

Linkoping; Sweden e-mail: farnazadib.yaghmaie@liu.se

Abstract: This paper bridges optimization and control, and presents a novel closed-loop control framework based on natural gradient descent, offering a trajectory-oriented alternative to traditional cost-function tuning. By leveraging the Fisher Information Matrix, we formulate a preconditioned gradient descent update that explicitly shapes system trajectories. We show that, in sharp contrast to traditional controllers, our approach provides flexibility to shape the system’s low-level behavior. To this end, the proposed method parameterizes closedloop dynamics in terms of stationary covariance and an unknown cost function, providing a geometric interpretation of control adjustments. We establish theoretical stability conditions. The simulation results on a rotary inverted pendulum benchmark highlight the advantages of natural gradient descent in trajectory shaping.

Keywords: Natural Gradient Descent, Trajectory Optimization, Stationary Covariance, Fisher Information Matrix (FIM).

# 1. INTRODUCTION

Optimization techniques, particularly gradient descent (GD) and its numerous variants (Ruder, 2017; Laborde and Oberman, 2020; Rattray et al., 1998; Martens, 2020), have become fundamental in modern control and machine learning. These methods are broadly classified into two categories when applied to control systems: GDbased control , where gradient methods optimize controller parameters, and controlled GD , where control-theoretic tools improve the convergence properties of a gradientbased optimizer (Lessard et al., 2016; Padmanabhan and Seiler, 2024; Nayyer et al., 2022). GD-based methods have demonstrated significant success in learning controllers for uncertain environments (Narendra and Parthasarathy, 1990; Sutton, 2018; Kiumarsi et al., 2018; Luo et al., 2017), as well as in system identification (Ljung, 1998; Hardt et al., 2018) and adaptive control (Gaudio et al., 2019; Ioannou and Sun, 2012; Cheng et al., 2024; Landau et al., 2011).

Despite their effectiveness; a challenge   persists: the closed trajectory behavior how system states evolve over time is typically an indirect outcome of   weight tuning or cost-function optimization. Traditional methods key loop rely on defining an objective function; applying an optimization algorithm; and then observing the resulting state trajectories (Cothren et al. 2021 ). If these trajectories do not meet performance expectations; the objective function often requires manual adjustments; leading to a cumbersome iterative tuning  process_ Furthermore; this process is susceptible to "reward hacking; ' where the optimized policy achieves a low-cost function value but deviates from the designer's intended behavior (Skalse et al. 2022) .

⋆ This work is supported in part by the National Science Foundation under award ECCS-2227311.

Farnaz Adib Yaghmaie is supported by the Excellence Center at Link¨oping–Lund in Information Technology (ELLIIT), ZENITH, and partially by Sensor informatics and Decision-making for the Digital Transformation (SEDDIT). This work was partly performed within the Competence Center SEDDIT-Sensor Informatics and Decision making for the Digital Transformation, supported by Sweden’s Innovation Agency within the research and innovation program Advanced digitalization.

In our previous work (Esmzad and Modares, 2024), we proposed a fundamentally different perspective by directly shaping system trajectories through a gradient-descentlike closed-loop approach. We introduced a novel parameterization of the stable closed-loop dynamics

$$
A+ BK = I _ 2TP
$$

− where A, B are the system matrices, K is a feedback gain, and Γ ,P ≻ 0 represent a GD step and a quadratic Lyapunov cost matrix, respectively. This formulation ensures that the closed-loop system behaves analogously to a GD update applied to the Lyapunov function V ( x k ) = x ⊤ k Px k , leading to the explicit trajectory update dynamic

$$
k FVzk V(sk)
$$

k +1 k − ∇ x k k Rather than iteratively adjusting an unknown cost function to produce desired state trajectories, we directly impose a controlled gradient flow on the system states.

This trajectory-oriented perspective offers several advantages. Firstly, it provides explicit trajectory control. The gradient formulation provides direct control over the trajectory shape, eliminating the need for trial-and-error cost function tuning. Secondly, it quantifies robustness by the step size. For a small step size, closed-loop eigenvalues have small variations. Lastly, it unifies with a Linear Quadratic

