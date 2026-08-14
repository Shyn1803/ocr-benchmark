values for the sensitivity and the mismatch, this is a conservative estimate, as also indicated in Fig. 4c where the actual decrease is 6.1%.

V. DISCUSSION

The paper provides formulas for analysis of sensitivity of OFO. The results are validated in a synthetic case study, showing that the formulas can be used instead of finite differences to compute the sensitivities in both unconstrained and constrained optimization problems. The synthetic case study also indicated that the sensitivities of OFO depend on how long the OFO controller has been running. If the time was insufficient, the sensitivities of OFO increase as the optimum is not reached. Conversely, if OFO reaches the optimum, then it becomes less sensitive to changes in parameters. These results suggest that future work could focus on analysis of sensitivity with respect to time.

The second numerical case study presents an application of sensitivity analysis with respect to the model mismatch in a gas lift optimization problem. The case study further demonstrated that the sensitivity of OFO depends on how long the controller was running. In particular, the sensitivities to the model mismatch in a single time step decrease with time, which suggests that iterative algorithms with accuracy improving with iterations may be used for gradient estimation while preserving the optimum.

The results for the case with coupling constraints emphasize the dependence on time in OFO. The formulas in Section III were derived by setting a constant final time TF and treating OFO as a system of equations parametrised by p:

# ΦT

=Φ(uT

,yT

,p)

F

F

F

y0 =h(u0) u1 =u0 + α σα(u0,y0,p)

.

yk =h(uk) uk+1 =uk + α σα(uk,yk,p)

(32)

. yT

F−1) uT

F−1 =h(uT

F−1 + α σα(uT

F−1,yT

F−1,p)

=uT

F

where σα(uk,yk,p) is the solution to (9) at iteration k. This assumption is equivalent to discretizing a continuous gradient flow algorithm with a constant time step [6]. However, (32) can be equivalently summarised as a nonlinear equation:

# F(ΦT

F

,u,y,p) = 0 (33)

treating all arguments as independent variables, with no explicit dependence on time. A natural extension to the sensitivity analysis will now be to consider the impact of time, both as time step and the final time.

VI. CONCLUSIONS AND FUTURE WORKS

The objective of the paper is to facilitate the analysis of Online Feedback Optimization controllers with respect to

their parameters. The importance of analysing the impact of the parameters of an optimization-based controller has been shown and used for traditional controllers, such as Model Predictive Control, but the analysis for Online Feedback Optimization remains under-explored. This paper addresses this gap by providing closed-form expressions for the sensitivity of Online Feedback Optimization to its parameters.

In the future, the sensitivities can be used for tuning of the parameters of the controller, as well as checking robustness to model mismatch. Future work will also include the analysis of sensitivity with respect to time.

REFERENCES

- [1] B. Amos, I. Jimenez, J. Sacks, B. Boots, and J. Z. Kolter. Differentiable MPC for end-to-end planning and control. Advances in neural information processing systems, 31, 2018.
- [2] B. Amos and J. Zico Kolter. OptNet: Differentiable optimization as a layer in neural networks. In Doina Precup and Yee Whye Teh, editors, Proceedings of the 34th International Conference on Machine Learning, volume 70 of Proceedings of Machine Learning Research, pages 136–145. PMLR, 06–11 Aug 2017.
- [3] J. R. Andersen, L. Imsland, and A. Pavlov. Data-driven derivativefree trust-region model-based method for resource allocation problems. Computers & Chemical Engineering, 176:108282, August 2023.
- [4] J. C. G. Boot. On sensitivity analysis in convex quadratic programming problems. Operations Research, 11(5):771–786, October 1963.
- [5] M. Colombino, J. W. Simpson-Porco, and A. Bernstein. Towards robustness guarantees for feedback-based optimization. In 2019 IEEE 58th Conference on Decision and Control (CDC) Palais des Congr`es et des Expositions Nice Acropolis Nice, France, December 11-13, 2019. IEEE, 2019.
- [6] V. H¨aberle, A. Hauswirth, L. Ortmann, S. Bolognani, and F. D¨orfler. Non-convex feedback optimization with input and output constraints. IEEE Control Systems Letters, 5(1):343–348, 2020.
- [7] A. Hauswirth, S. Bolognani, G. Hug, and F. D¨orfler. Optimization algorithms as robust feedback controllers. Annual Reviews in Control, 57:100941, 2024.
- [8] Z. He, S. Bolognani, J. He, F. D¨orfler, and X. Guan. Model-free nonlinear feedback optimization. IEEE Transactions on Automatic Control, pages 1–16, 2023.
- [9] J. R. Magnus. Matrix Differential Calculus with Applications in Statistics and Econometrics. Wiley, February 2019.
- [10] P. Mestres, A. Allibhoy, and J. Cort´es. Regularity properties of optimization-based controllers. November 2023.
- [11] J. Nocedal and S. J. Wright. Numerical Optimization. Springer-Verlag New York, first edition, 1999.
- [12] L. Ortmann, F. B¨ohm, F. Klein-Helmkamp, A. Ulbig, S. Bolognani, and F. D¨orfler. Tuning and testing an online feedback optimization controller to provide curative distribution grid flexibility. Electric Power Systems Research, 234:110660, 2024.
- [13] L. Ortmann, A. Hauswirth, I. Caduff, F. D¨orfler, and S. Bolognani. Experimental validation of feedback optimization in power distribution grids. Electric Power Systems Research, 189:106782, 2020.
- [14] A. Rohatgi. Webplotdigitizer, v. 4.1, 2018. automeris.io/ WebPlotDigitizer, accessed: 8 Nov 2024.
- [15] S. Surjanovic and D. Bingham. Virtual library of simulation experiments: Test functions and datasets. Retrieved November 8, 2024, from https://www.sfu.ca/˜ssurjano/stybtang.html.
- [16] M. Thombre, Z. J. Yu, J. J¨aschke, and L. T. Biegler. Sensitivity-assisted multistage nonlinear model predictive control: Robustness, stability and computational efficiency. Computers & Chemical Engineering, 148:107269, 2021.
- [17] P.J. Werbos. Backpropagation through time: what it does and how to do it. Proceedings of the IEEE, 78(10):1550–1560, 1990.
- [18] M. Zagorowska, L. Ortmann, A. Rupenyan, M. Mercang¨oz, and L. Imsland. Tuning of online feedback optimization for setpoint tracking in centrifugal compressors. IFAC-PapersOnLine, 58(14):881– 886, 2024.


