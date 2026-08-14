additional bisection refinements: we found that quadratic interpolation produces better results in our numerical case studies.

We refer to Figure 2 for a practical implementation of the algorithm described above: the colored disks in the center panel correspond to the parameter values at which the pattern statistics was computed for predictorcorrector step as outlined above.

# 4 Assessing dependence on algorithmic parameters

We now outline the parameters that enter the algorithm and discuss how they affect accuracy and computational efficiency. The implementation of the continuation algorithm described above requires the following choices:

- 1. Feature function: We choose a feature function f that can differentiate between the patterns we want to distinguish.
- 2. Spatial discretization: We choose the number K of Fourier modes so that we can resolve the nonlinearity and the expected patterns at the expected wavelength. Alternatively, and this is how our numerical computations were conducted, we can use finite differences to solve the PDE model for a sufficiently small spatial stepsize that resolves the patterns we are interested in and use the resulting grid also for α-shapes.
- 3. Initial data: We choose two fixed functions Ub(x) and Ur(x) to construct the initial data in (2.11). The deterministic part Ub is selected to ensure that we reach the patterns we are interested in: for domain-filling patterns, Ub is typically an unstable homogeneous rest state. The function Ur that will be used for the

randomized part is given by Ur(x) = |k|≤K akek(x) for a fixed nonzero choice of coefficients (ak)|k|≤K (we set Ur = 0 for deterministic initial data).

- 4. Randomization: We select N samples of the random variables (bk(ω))|k|≤K from a uniform distribution and form the ensemble of N randomized functions Urω(x) := |k|≤K akbk(ω)ek(x). The resulting N functions U0(x) = Ub(x) + Urω(x) are then used as initial data in the numerical solver. The number N of samples that

are used to calculate the empirical measure µN,ωf (or the empirical feature mean EfN,ω if applicable) can be adjusted using, for instance, a small-sample paired t-test (which tests the null hypothesis that the mean of the difference of feature samples is zero) to ensure that there is a statistically significant difference between the two empirical measures in the argument of the bifurcation function g.

- 5. Integration time: The integration time T > 0 is chosen so that we reach the relevant pattern regime from

the initial data Ub + Urω within the time interval [0,T]. It is possible to adapt T during continuation, for instance by choosing shorter or longer values and comparing the resulting feature values.

- 6. Sublevel sets: We evaluate the feature function on the sublevel sets Uj−1((−∞,c]) of the jth component of the solution U to (2.1). We choose the index 1 ≤ j ≤ d and the threshold c ∈ R so that the corresponding sublevel sets best reflect the patterns we are interested in.
- 7. Alpha-shapes: The evaluation of the feature functions we consider require the computation of the α-shapes of the sublevel sets. We need to pick the radius α of the α-shape and the number M2 of lattice points on which we evaluate the solution to approximate the sublevel set. We usually choose M := K and set α = 10/M. We note that we can adapt M and α by comparing the resulting pattern statistics using the Wasserstein metric to ensure that they do not change upon increasing M or varying α.
- 8. Predictor-corrector steps: We need to choose the arclength stepsize s and the parameter offset h. We normally pick h := s and note that the stepsize s can be adapted based on the successive changes of the angle of the secants, which are indicative of the curvature of the curve Γ.


Our algorithm is robust with respect to these choices, and we never had to adjust them during continuation. Generally, increasing the number K of Fourier modes (or mesh points when using finite differences) for the PDE solver, the number M of lattice points on which we evaluate patterns and their features, and the ensemble size N of randomized initial data will provide smoother and more accurate continuation curves. The algorithm is

17

