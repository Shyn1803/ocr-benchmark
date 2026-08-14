16 CHRISTIAN PÖTZSCHE AND ROBERT SKIBA

By compactness we can now cover the interval [a,b] with a finite number of such neighborhoods Uλ

n ⊆ R. If (3.1) V := N(T(λ1)∗) + N(T(λ2)∗) + ... + N(T(λn)∗) ⊂ L∞(R), then dimV < ∞ and R(T(λ)) + V = L∞(R) for all λ ∈ [a,b].

,...,Uλ

1

(IV) This step is inspired by Step 3 in the proof of [41, Thm. 5.3]. Keeping τ > 0 fixed, consider the family of operators

S(λ) : D(S(λ)) → L∞[−τ,τ], [S(λ)y](t) := y˙(t) − A(t,λ)y(t) for a.a. t ∈ [−τ,τ], which due to Lemma 2.1(a) is well-defined on the domain

D(S(λ)) := u ∈ W1,∞[−τ,τ] | u(−τ) ∈ N(Pλ−(−τ)), u(τ) ∈ R(Pλ+(τ)) . (IV.1) Claim: dimN(S(λ)) = dimN(T(λ)) < ∞.

Consider the commutative diagram

W1,∞(R) T(λ) L∞(R)

(3.2)

p D(S(λ)) S(λ)

iλ

L∞[−τ,τ],

where p is the restriction of functions in L∞(R) to L∞[−τ,τ] given by p(u) := u|[−τ,τ] and a canonical map iλ : D(S(λ)) → W1,∞(R) defined by extending a given function u ∈ D(S(λ)) to the intervals (−∞,−τ) and (τ,∞) as solution of (Vλ). Observe that iλ is injective and iλ N(S(λ)) = N(T(λ)) holds, where iλ N(S(λ)) ⊆ N(T(λ)) results directly due to the construction of iλ, while iλ N(S(λ)) ⊇ N(T(λ)) as converse inclusion follows from the fact that privided u ∈ N(T(λ)), then u(τ) ∈ R(Pλ+(τ)) and u(−τ) ∈ N(Pλ−(−τ)) for any τ > 0 (recall (2.3)). Finally, this yields the assertion.

(IV.2) We decompose [−τ,τ] = [−τ,0] ∪ [0,τ] and define the spaces X+ := {u ∈ W1,∞[0,τ] | u(τ) ∈ R(Pλ+(τ))}, Y+ := L∞[0,τ], X− := {u ∈ W1,∞[−τ,0] | u(−τ) ∈ N(Pλ−(−τ))}, Y− := L∞[−τ,0].

Consider the following linear operators S±(λ) : X± → Y± pointwise defined as

[S±(λ)y](t) = y˙(t) − D2f(t,ϕλ(t),λ)y(t) for a.e. t ∈ R±. Next consider the following commutative diagram

−(λ)⊕S+(λ) Y− ⊕ Y+

X− ⊕ X+ S

(3.3) J

Jλ

D(S(λ)) S(λ)

L∞[−τ,τ],

where J : L∞[−τ,τ] → Y− ⊕ Y+ and Jλ: D(S(λ)) → X− ⊕ X+ are defined by

Ju := (u−,u+) and Jλv := (v−,v+)

with u+ and v+ (resp. u− and v−) being the corresponding restrictions to [0,τ] (resp. to the interval [−τ,0]). It is clear that J is an isomorphism, while Jλ is injective with range R(Jλ) = {(v−,v+) | v−(0) = v+(0)}. Defining the mapping Σ: X− ⊕ X+ → Rd by

