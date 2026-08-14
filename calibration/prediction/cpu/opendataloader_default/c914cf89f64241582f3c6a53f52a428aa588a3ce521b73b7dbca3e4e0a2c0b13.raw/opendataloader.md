Lemma 2 (Kantorovich duality) Let c : R × R → [0,∞] be a lower semicontinuous function and Φc the set of all functions (ϕ,ψ) ∈ L1 (dµ0) ×L1 (dµ1) with

ϕ(y0) + ψ (y1) ≤ c(y0,y1) (3)

Then,

inf

π∈Π(µ0,µ1)

c(y0,y1)dπ = sup

(ϕ,ψ)∈Φc

ϕ(y0)dµ0 + ψ (y1)dµ1 . (4)

Also, the inﬁmum in the left-hand side of (4) and the supremum in the right-hand side of (4) are both attainable, and the value of the supremum in the right-hand side does not change if one restricts (ϕ,ψ) to be bounded and continuous.

Remark 1 Note that the cost function c(y0,y1) may be inﬁnite for some (y0,y1) ∈ R2. Since c is a nonnegative function, the integral c(y0,y1)dπ ∈ [0,∞] is well-deﬁned.

This dual formulation provides a key to solve the optimization problem (2); I can overcome the diﬃculty associated with picking the maximizer joint distribution in the set Π(µ0,µ1) by solving optimization with respect to given marginal distributions. The dual functions ϕ(y0) and ψ (y1) are Lagrange multipliers corresponding to the constraints π (y0 × R) = µ0 (y0) and π (R × y1) = µ1 (y1), respectively, for each y0 and y1 in Y0 and Y1. Henceforth they are both assumed to be bounded and continuous without loss of generality. By the condition (3), each pair (ϕ,ψ) in Φc satisﬁes

ϕ(y0) ≤ inf

y1∈R

{c(y0,y1) − ψ (y1)}, (5)

ψ (y1) ≤ inf

{c(y0,y1) − ϕ(y0)}.

y0∈R

At the optimum for (y0,y1) in the support of the optimal joint distribution, the inequality in (3) holds with equality and there exists a pair of dual functions (ϕ,ψ) that satisﬁes both inequalities in (5) with equalities.

In recent years, this dual formulation has turned out to be powerful and useful for various problems related to the equilibrium and decentralization in economics. See Ekeland (2005, 2010), Carlier (2010), Chiappori et al. (2010), Chernozhukov et al. (2010), and Galichon and Salani´e (2012). In econometrics, Galichon and Henry (2009) and Ekeland et al. (2010) showed that the dual formulation yields a test statistic for a set of theoretical restrictions in partially identiﬁed economic models. They set the cost function as an indicator for incompatibility of the structure with the data and derived a Kolmogorov Smirnov type test statistic from a well known dual representation theorem; see Lemma 3 below. Similarly, Galichon and Henry (2011) showed that the identiﬁed set of structural parameters in game theoretic models with pure strategy

13

