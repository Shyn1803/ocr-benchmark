values for the sensitivity and the mismatch, this is a conservative estimate, as also indicated in Fig. 4c where the actual decrease is 6.1%.

# V. D ISCUSSION

The paper provides formulas for analysis of sensitivity of OFO. The results are validated in a synthetic case study, showing that the formulas can be used instead of finite differences to compute the sensitivities in both unconstrained and constrained optimization problems. The synthetic case study also indicated that the sensitivities of OFO depend on how long the OFO controller has been running. If the time was insufficient, the sensitivities of OFO increase as the optimum is not reached. Conversely, if OFO reaches the optimum, then it becomes less sensitive to changes in parameters. These results suggest that future work could focus on analysis of sensitivity with respect to time. The second numerical case study presents an application

of sensitivity analysis with respect to the model mismatch in a gas lift optimization problem. The case study further demonstrated that the sensitivity of OFO depends on how long the controller was running. In particular, the sensitivities to the model mismatch in a single time step decrease with time, which suggests that iterative algorithms with accuracy improving with iterations may be used for gradient estimation while preserving the optimum. The results for the case with coupling constraints empha-

size the dependence on time in OFO. The formulas in Section III were derived by setting a constant final time T F and treating OFO as a system of equations parametrised by p :

$$
p) y0 =h(u%) ul =uo + p) yk =h(uk ) (32) uk+l =uk + ,p) uTr (uTr -1 =uTf-1
$$

  where   σ α ( u k ,y k , p ) is the solution to (9) at iteration k . This assumption is equivalent to discretizing a continuous gradient flow algorithm with a constant time step [6]. However, (32) can be equivalently summarised as a nonlinear equation:

$$
u,Y,p) = 0 (33)
$$

treating all arguments as independent variables, with no explicit dependence on time. A natural extension to the sensitivity analysis will now be to consider the impact of time, both as time step and the final time.

# VI. C ONCLUSIONS AND FUTURE WORKS

The objective of the paper is to facilitate the analysis of to their parameters The importance of analysing the impact of the parameters of an optimization-based controller has been shown and used as Model Predictive Control, but the analysis for Online Feedback Optimization remains under-explored. This paper addresses this gap by providing closed-form expressions for the sensitivity of Online Feedback Optimization to its parameters.

of Online Feedback Optimization to its parameters. In the future, the sensitivities can be used for tuning of the parameters of the controller, as well as checking robustness to model mismatch. Future work will also include the analysis of sensitivity with respect to time.

# R EFERENCES

Kolter: Differen tiable MPC for end-to-end planning and control. Advances in neural information processing systems; 31, 2018_

[2] a layer in neural networks. In Doina Precup and Yee Whye Teh, editors, Proceedings of the 34th International Conference on Machine Learning , volume 70 of Proceedings of Machine Learning Research , pages 136–145. PMLR, 06–11 Aug 2017. [3] J. R. Andersen, L. Imsland, and A. Pavlov. Data-driven derivative-

R Andersen; L Imsland, and A Pavlov. trust-region model-based method for resource allocation problems _ Computers & Chemical Engineering, 176.108282, August 2023 free

J.C. G. Boot. On sensitivity analysis in convex quadratic programming problems . Operations Research, 11(5).771-786, October 1963

robustness guarantees for feedback-based optimization. In 2019 IEEE 58th Conference on Decision and Control (CDC) Palais des Congr` es et des Expositions Nice Acropolis Nice, France, December 11-13, 2019 . IEEE, 2019. [6] V. H¨ aberle, A. Hauswirth, L. Ortmann, S. Bolognani, and F. D¨ orfler.

Hauswirth, L Ortmann; S. Bolognani; and F. Non-convex feedback optimization with input and output constraints. IEEE Control Systems Letters, 5(1).343-348, 2020.

A Hauswirth, S Bolognani_ G Optimization algorithms as robust feedback controllers_ Annual Reviews in Control ,

[8] Z. He, S. Bolognani, J. He, F. D¨ orfler, and X. Guan. Model-free nonlinear feedback optimization. IEEE Transactions on Automatic Control , pages 1–16, 2023. [9] J. R. Magnus. Matrix Differential Calculus with Applications in

J. R Magnus Matrix   Differential Calculus with   Applications in Statistics and Econometrics. February 2019. Wiley.

Mestres, Allibhoy; and Cortés Regularity   properties of optimization-based controllers.  November 2023.

11] J. Nocedal and S. J. Wright. Numerical Optimization: Springer New York, first edition; 1999 Verlag

L. Ortmann F F. Klein-Helmkamp, A Ulbig, S. Bolognani Tuning and testing an online feedback  optimization grid   flexibility. Electric Power Systems Research, 234:110660, 2024

L. Ortmann, Hauswirth Caduff, F. DWrfler; and S. Bolognani_ Experimental validation of feedback optimization in power distribution grids Electric Power Systems Research, 189.106782, 2020.

A Rohatgi. Webplotdigitizer; 4.1, 2018 automeris io/ WebPlotDigitizer, accessed: 8 Nov 2024.

S. Surjanovic and D. Bingham. Virtual library of simulation experi ments: Test functions and datasetsRetrieved November 8, 2024, from https WWW sfu ca ssurjano/stybtang html

M. Thombre; Z. J. Yu; J. Jaschke, and L. T. Biegler. Sensitivity-assisted control:   Robustness;  stability and computational  efficiency. Computers Chemical  Engineering, 148.107269, 2021_

PJ. Werbos_ Backpropagation through time: what it does and how to 1990.

M. Zagorowska, L. Ortmann; Rupenyan, M Mercangõz, and L. Imsland. Tuning   of   online  feedback ` optimization for   setpoint 886, 2024

