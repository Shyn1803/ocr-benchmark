where the first inequalities are ensured by Theorem 2. However, the irreducibility condition (Hκirr) is not satisfied by κred, so uniqueness is not ensured and Proposition 1 does not apply to guarantee that N1red and N2red are non-zero. Adapting the proof of Proposition 1 to each of the strongly connected components of the graph of κ, simply reduced to {v1} and {v2}, shows that for each i ∈ {1,2}, Nired is either zero everywhere or positive on (2b,+∞). The normalization condition

∞ 0

Nired(x)dx = 1

i∈{1,2}

implies that at least for one i ∈ {1,2}, Nired is non-zero. Both N1red and N2red cannot be non-zero, otherwise Lemma 2 would work (in equality (14), we need the existence of

i ̸= j such that Nired ̸= 0 and Njred ̸= 0) and we could use it to prove the long-time convergence of system (20) towards a stationary sate (fourth step of Theorem 4). That

would contradict [6]. The only possibility is that N1red ≡ 0 and N2red(x) > 0 for x ≥ 2b or the opposite and then λ = λ2 or λ = λ1 respectively.

In the mixing case, the equations of system (GFt,v) are coupled through their source term:

 

∂

- ∂tn1(t,x) + v1∂x∂ xn1(t,x) + γ1(x)n1(t,x) = 4γ2(2x)n2(t,2x), ∂

- ∂tn2(t,x) + v2∂x∂ xn2(t,x) + γ2(x)n2(t,x) = 4γ1(2x)n1(t,2x), n1(0,x) = nin1 (x), n2(0,x) = nin2 (x),




and the irreducibility condition (Hκirr), missing in the non-mixing case, is now satisfied. We can thus apply successively Theorem 3, Proposition 1 and Theorem 4 to get eigenelements (λirr,Nirr,ϕirr) such that

2

i=1 R+

ni(t,x)e−λirrt − Niirr(x) ϕirri (x)dx −→ t→∞

0

with λirr > 0, and for i ∈ {1,2}, Niirr positive on (2b,+∞) and ϕirri > 0 on (0,+∞).

These two simple cases illustrate that the existence result (Theorem 3) holds for every probability matrix κ, in particular reducible ones. The irreducibility condition on κ comes into play to characterize the functions canceling the dissipation of entropy (Lemma 2), which then proves crucial to establish uniqueness of the steady state and convergence towards it.

# 3.2 Numerical illustration

Similarly to the previous subsection, we focus here on the special case of linear growth rates to illustrate the convergence result of Theorem 4. We numerically approximate and compare the long-time asymptotics in the presence and absence of mixing in feature.

We choose M = 3 different features, namely V = {1,2,3}, and approximate on the grid

SN := V × {x0,...x2N}, xm := 2−mk−N , m ∈ {0,...,2N}, k = 200, N = 2501, the time-evolution of the following initial data (taken identical for all features)

nin : (v,x)  → Cxa e−bx2, a = 30, b = 60, C s.t. nin L1(V×(0,x

2N)) = 1, 22

