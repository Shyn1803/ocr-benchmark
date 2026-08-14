Lemma 2 (Kantorovich duality) Let c : R × R → [0 , ∞ ] be a lower semicontinuous function and Φ c the set

$$
(3)
$$

Then,

$$
inf J c (yo, Y1) dT = sup U 4 (yo) dpo +
$$

Also, the inﬁmum in the left-hand side of (4) and the supremum in the right-hand side of (4) are both attainable, and the value of the supremum in the right-hand side does not change if one restricts ( ϕ,ψ ) to be bounded and continuous.

Remark 1 Since c is 0 nonneg-

This dual formulation provides a key to solve the optimization problem (2); I can overcome the diﬃculty associated with picking the maximizer joint distribution in the set Π( µ 0 ,µ 1 ) by solving optimization with respect to given marginal distributions. The dual functions ϕ ( y 0 ) and ψ ( y 1 ) are Lagrange multipliers corresponding to the constraints π ( y 0 × R ) = µ 0 ( y 0 ) and π ( R × y 1 ) = µ 1 ( y 1 ) , respectively, for each y 0 and y 1 in Y 0 and Y 1 . Henceforth they are both assumed to be bounded and continuous without loss of generality. By the condition (3), each pair ( ϕ,ψ ) in Φ c satisﬁes

$$
4 (yo) < U1 €R Uo€R
$$

At the optimum for ( y 0 ,y 1 ) in the support of the optimal joint distribution, the inequality in (3) holds with equality and there exists a pair of dual functions ( ϕ,ψ ) that satisﬁes both inequalities in (5) with equalities.

In recent years, this dual formulation has turned out to be powerful and useful for various problems related to the equilibrium and decentralization in economics. See Ekeland (2005, 2010), Carlier (2010), Chiappori et al. (2010), Chernozhukov et al. (2010), and Galichon and Salani´e (2012). In econometrics, Galichon and Henry (2009) and Ekeland et al. (2010) showed that the dual formulation yields a test statistic for a set of theoretical restrictions in partially identiﬁed economic models. They set the cost function as an indicator for incompatibility of the structure with the data and derived a Kolmogorov Smirnov type test statistic from a well known dual representation theorem; see Lemma 3 below. Similarly, Galichon and Henry (2011) showed that the identiﬁed set of structural parameters in game theoretic models with pure strategy

