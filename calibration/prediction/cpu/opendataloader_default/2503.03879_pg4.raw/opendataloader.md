![](<2503.03879_pg4_images/imageFile1.png>)

Fig. 2. Location of switch point at the end of finite element

The proposed step-equilibration approach is based on the principle that only the finite element(s) with the switch point(s) have non-uniform discretization [tl−1,tl]. The approach uses an indicator variable (η) for the switch point(s), which is determined by calculating and multiplying the sum of the complementarity variables in two consecutive finite elements.

The auxiliary variables for the sum of the complementarity variables at each finite element are defined as:

K

K

λˆl =

λl,k, νˆl =

νl,k (10a)

k=1

k=1

Then, the Hadamard product of the forward and backward sum of the complementarity variables determine if they have switched from positive to zero (or vice-versa).

πlλ = λˆl−1 ⊙ λˆl, πlν = νˆl−1 ⊙ νˆl (10b) (Here, ⊙ represents pointwise or elementwise product of vectors.)

Since at least one of the vectors πlλ or πlν is zero at each element, and they are exactly equal to zero at the element

corresponding to the switching point, the sum of the two vectors is a good candidate for the indicator function

nf

τl = πlλ + πlν, ηl =

τl,j (10c)

j=1

Since the indicator variable ηl is non-negative and only zero at the switching element, the relation between step size and indicator variable can be represented by the following complementarity constraints.

For l = 1,...,N − 1 0 ≤ (∆h+l + ∆h−l ) ⊥ ηl ≥ 0 (10d)

where hl−1 − hl = ∆h+l − ∆h−l , ∆h+l ,∆h−l ≥ 0, The finite element with switch detection (FESD) algorithm was

implemented as a package NOSNOC in [19].

As mentioned in (10), the Nurkanovic formulation augments an additional [2N{λ,ˆ νˆ}+(2N −2){πλ,πν}+(N −

- 1){τ} + (N − 1){η}] variables and [2N{(10a)} + (2N −
- 2){(10b)}+2(N −1){(10c)}+(N −1){(10d)}] constraints for each complementarity constraint. This effectively decreases the degrees of freedom by N − 1 to that of the original problem and avoids non-unique solutions for the step size variables hi.


- 2.4 Proposed Formulation

Although the Nurkanovic formulation makes the problem consistent with respect to the degrees of freedom and ensures uniform grid discretization away from the switch point(s), the formulation may be numerically unstable (i.e. the derivatives have large condition number) and increases the size of the problem, making it difficult to implement on larger optimal control problems.

Inspired by the Nurkanovic [21] formulation, we propose a modification of the approach in [1], in order to keep the degrees of the problem consistent. In our proposed approach, we first apply the formulation in [1] with cross complementarities (9f). This locates the switching point(s) (ts) at the end of the finite element(s).

We define the set of finite elements which have the switching point at the end (i.e. right) as:

χs = {l|[tl−1,tl], λl,K = νl,K = 0, λl−1,K + νl−1,K > 0 or λl+1,K + νl+1,K > 0}

(11a)

In the next step, we add additional constraints to the formulation which forces the finite elements to be equally spaced away from the switching points.

hl − hl+1 = 0 ∀l ∈ {1,...,N − 1} \ χs (11b) Also, we add constraints to force the switching to happen at the boundary of finite elements found in the first step.

λl,K + νl,K = 0 ∀l ∈ χs (11c) This formulation adds the necessary N − 1 linear constraints without any additional variables making the formulation much more adaptable and applicable for large optimal control problems.

The main assumption in our approach is that the location of the switching points in the optimal solution is independent of the step-size variables and the formulations. Thus, the switching points in the Baumrucker formulation would be the same as in the Nurkanovic formulation. The only difference between their solutions is in the value of the step size variables away from the switching elements. Therefore, we implement uniform discretization between the switch points, start time and the final time using (11) instead.

3. SOLUTION METHODS FOR MPCCS

To develop the solution strategy for the MPCC derived in the previous section, we discretize and rewrite (7) in the more general form:

min φ(x) (12a) s.t. gI(x) ≤ 0; gE(x) = 0, (12b)

0 ≤ G(x) ⊥ H(x) ≥ 0 (12c) Here the complementarity constraints (12d) represent the cross-complementarity constraints (9f) and step equilibration constraints (10e). The NLP equivalent formulation of the complementarity constraints is

G(x) ≥ 0, H(x) ≥ 0, Gi(x)Hi(x) = 0, ∀i = 1...nc

- 3.1 MPCC Basics and Stationary Points


The following index sets are defined at every feasible point x¯ of the MPCC (12):

