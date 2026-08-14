GLOBAL FINITE-TIME AND GLOBAL FIXED-TIME STABLE DYNAMICAL SYSTEMS FOR IQVIPS 7 Then the operator T(u) ≡ f(u)−PΦ(u)(f(u)−αu) is Lipschit continuous. Proof. By the non-expansion property of the projection operator and (2.6) we have that ∥T(u)−T(v)∥ =∥f(u)−PΦ(u)(f(u)−αu)−(f(v)−PΦ(v)(f(v)−αv))∥

≤∥f(u)− f(v)∥

+∥PΦ(u)(f(u)−αu)−PΦ(u)(f(v)−αv)+PΦ(u)(f(v)−αv)−PΦ(v)(f(v)−αv)) ≤L∥u−v∥+∥f(u)− f(v)∥+α∥u−v∥+µ∥u−v∥ ≤(2L+α +µ)∥u−v∥.

This implies that T is Lipschit continuous. □ 3. FINITE-TIME STABILITY ANALYSIS

In this section we will analyze the finite-time stability for IQVIPs (1.1). By doing so we propose a new first order dynamical system associated with the problem (1.1) such that a solution of (1.1) becomes an equilibrium point of the dynamical system. Under mild conditions for the parameters, we demonstrate that the proposed dynamical system is finite-time stable.

We first recall a characterization for the finite-time stability of solutions of a dynamical system, given by Bhat and Bernstein in [5]. This result will play an important role in studying finite-time convergence.

Theorem 3.1. [5] (Lyapunov condition for finite-time stability). Assume that there exists a continuously differentiable functionV : D → R, where D ⊆ Rn is a neighborhood of the equilibrium point u∗ for (2.1) and an open neighborhood U ⊆ D of u∗ such that

# V˙ (u) ≤ −K. V(u) p ∀u ∈ U \{u∗},

where K > 0 and p ∈ (0,1). Then, the equilibrium point u∗ of (2.1) is finite-time stable equilibrium point of (2.1). Moreover, the settling time T satisfies

V(u(0))1−p K(1− p)

T(u(0)) ≤

for any u(0) ∈ U. In addition, if D = Rn, then the equilibrium point u∗ of (2.1) is globally finite-time stable. In order to obtain a finite-time stability of solutions of inverse quasi-variational inequality

problem (1.1) we now present a novel first-order dynamical system associated with the problem (1.1). Our proposed dynamical system is as follows:

f(u)−PΦ(u)(f(u)−αu) ∥f(u)−PΦ(u)(f(u)−αu)∥

u˙(t) = −σ

, (3.1)

γ−2 γ−1

where σ > 0 is a scalar tuning gain, and γ > 2,α > 0 are two design parameters.

It is worth noting that for all u ∈ Rn such that f(u)−PΦ(u)(f(u)−αu) = 0, the expression on the right-hand side of (3.1) is still well defined for all γ > 2. In fact, it is equal to zero. Indeed, we have

f(u)−PΦ(u)(f(u)−αu) ∥f(u)−PΦ(u)(f(u)−αu)∥

γ−2 γ−1

1

= ∥f(u)−PΦ(u)(f(u)−αu)∥

# γ−1 = 0.

