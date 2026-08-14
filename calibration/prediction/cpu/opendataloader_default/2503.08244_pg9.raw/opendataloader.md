INTERMITTENT TWO-POINT DYNAMICS AT THE TRANSITION TO CHAOS 9

# X(ω)dP(ω). Recall that a measure µ on T is called a stationary measure if

single symbol ω ∈ Ωϑ, we write E[X] = Ω

ϑ

µ (Tω)−1 (A) dP(ω) = µ(A), for any (Borel) measurable set A ⊂ T.

Σϑ

The skew product map Θ : Σϑ × T → Σϑ × T is defined by

Θ(ω,x) := (σω,Tω0(x)). Here σ is the left shift operator σω := (ωi+1)i∈N. With a slight abuse of notation we write Tωn(x) := Tωn−1 ◦ ··· ◦ Tω0(x)

for iterates.

We compares two different trajectories by studying the random dynamical system. For ω ∈ Σϑ, the two-point map (x,y)  → Tω(2)(x,y) on T2 is the product

(x,y)  → (Tω(x),Tω(y)). This yields the random dynamical system

(xn+1,yn+1) = Tω(2)n (xn,yn). (2.3) The two-point skew product map Θ(2) : Σϑ × T2 → Σϑ × T2 is denoted by

Θ(2)(ω,x,y) = (σω,Tω(2)(x,y)). A measure µ(2) on T2 is a stationary measure of the random dynamical system Tω(2) on T2 if

µ(2) Tω(2)

Σϑ

−1

(A) dP(ω) = µ(2)(A),

for any (Borel) measurable set A ⊂ T2. 2.1. Hypotheses. We focus on random circle endomorphisms whose trajectories are not confined to subintervals of the circle but spread over the entire circle.

There is k > 0 so that for any x,y ∈ T, there is ω ∈ Σϑ so that Tωk(x) = y. (H2)

This hypothesis guarantees the existance of a unique absolutely continuous stationary measure of full support, but also has further applications that are used throughout the paper.

Proposition 2.1. Suppose the random dynamical system described by (2.2) with ωn i.i.d. picked from a uniform distribution for [−ϑ,ϑ], adheres to Hypotheses (H1), (H2).

Then the random dynamical system admits an absolutely continuous stationary measure µ with full support and smooth density.

