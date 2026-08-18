# 3.2. Constraints

To obtain feasible solutions within this simulation-based optimization framework, it is crucial to establish suitable constraints. Constraints are tied to the simulation residuals, which guide the optimization process towards achieving the desired fitness and ensuring numerically stable results. When the residuals are below the specified thresholds, the constraints are deemed satisfied. If the residuals exceed the limits, a penalty is imposed for failing to meet the criteria. The pressure residual constraint, given by:

The pressure residual constraint, given by:

$$
Tp(b) < (11) le-3
$$

helps ensure consistent pressure values during the optimization process, preventing pressure imbalances that could result in unrealistic behavior. The velocity residuals ensure controlled and physically realistic fluid motion and are defined for both velocity components:

$$
(b) < (12) le-4 Tur
$$

$$
(b) < (13) le-4
$$

The k residual constraint, defined as:

$$
Tk (b) (14) le-4
$$

ensures that the turbulent kinetic energy remains within acceptable bounds. The ω residual constraint, set as:

$$
(15)
$$

limits the specific dissipation rate of turbulence, maintaining alignment with the fundamental physics. These constraints collectively guide the optimization process, ensuring physical realism, stability, and relevant fluid dynamics representation. All five constraints are assessed across all test cases.

# 4. Optimization procedure

The selection of the most suitable optimization algorithm for similar flow field reconstruction method was previously addressed in [ 47 ], where the performance, efficiency, robustness, and scalability of various methods were evaluated, leading to the adoption of PSO as the preferred approach for this type of modeling. Although the authors noted that optimization outcomes are case-dependent, they observed similar results across different test cases due to the synthetic nature of the simulations, despite variations in data sources. As outlined in [ 47 ], the mean square difference of the velocities at measurement points, denoted as ϵ , is

As outlined in [47], the mean square difference of the velocities at measurement points; denoted as €d, is as the fitness function in all optimization tests. The optimization is thus defined as follows: used

$$
minimize ed(b) = (uri (b))2 nMP (16) i=1 Us;
$$

$$
subject to b1< b < bu
$$

Convergence of the optimization process is considered to be achieved when the drifter error threshold, ϵ d = 1 e − 4 , is reached, corresponding to a drifter velocity error in m/s . All reconstruction results for which these threshold is met are deemed satisfactory.

