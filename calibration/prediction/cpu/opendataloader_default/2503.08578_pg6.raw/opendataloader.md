6 HUI HUANG, HICHAM KOUHKOUH, AND LUKANG SUN

[11, Assumption 4.1] imposes additional conditions, such as f ∈ C2(Rd) and the boundedness of ∥∇2f∥∞. In the framework of [22, Definition 8], some additional local growth conditions on f around the global minimizer are required. For our rescaled CBO we do not require these additional assumptions for the convergence proof.

• Multiple–minimizer case: Although our rescaled CBO is not specifically designed to address the multiple minimizer problem, we can still establish certain asymptotic properties in cases where the objective function f(·) has multiple minimizers, whether they are discrete points or compact subsets (see Theorem 3.9). Let us mention here that specially designed CBO models aimed at addressing multiple-minimizer problems have been introduced in [9,24].

Our results rely on two main ingredients: uniform estimates on the moments of the measure, and on a Harnack inequality on the invariant elliptic CBO equation. Indeed we need Harnack’s inequality in order to ensure that the measure has a non–null mass around minimizers, which will then allow us to prove Laplace’s principle. A summary of our findings is in section 4 at the end of the manuscript.

2. Useful estimates

We start by recalling some notation. When a measure µ has a density ϱ with respect to Lebesgue measure that we denote by dx, then µ is absolutely continuous with respect to dx, we write µ ≪ dx and ϱ = ddµx is Radon–Nikodym derivative of µ with respect to dx. Unless a confusion arises, we shall use the same notation for a measure and for its density (when it exists). We shall also denote by Wk,p(Ω), p ≥ 1,k ≥ 0 the standard Sobolev space of functions whose generalized derivatives up to order k are in Lp(Ω), and we denote by Wlock,p(Ω) the class of functions f such that χf ∈ Wk,p(Ω) for each χ ∈ Cc∞(Ω) the class of infinitely differentiable functions with compact support in Ω.

In what follows, ∥·∥ denotes the Frobenius norm of a matrix and |·| is the standard Euclidean norm in Rd; P(Rd) denotes the space of probability measures on Rd, and Pp(Rd) with p ≥ 1 contains all µ ∈ P(Rd) such that µ(| · |p) := R

d |x|pµ(dx) < ∞; it is equipped with p–Wasserstein distance Wp(·,·).

Our main assumption concerns the function f(·) to be minimized, and can be stated as follows. Assumption 2.1. We assume the following properties for the objective function.

- (1) f : Rd → R+ is bounded from below by f := minf > 0, and there exists some constant Lf > 0 such that

|f(x) − f(y)| ≤ Lf(1 + |x| + |y|)|x − y|, ∀x,y ∈ Rd .

- (2) There exist constants cℓ,cu > 0 and M > 0 such that f − f ≤ cu(|x|2 + 1), ∀x ∈ Rd and cℓ|x|2 ≤ f − f for |x| ≥ M .


