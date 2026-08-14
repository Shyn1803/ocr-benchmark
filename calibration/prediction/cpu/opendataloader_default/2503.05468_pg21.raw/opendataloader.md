ASYMPTOTIC EXPANSION OF SOLUTIONS TO MARKOV RENEWAL EQUATIONS 21

Nn to each individual

We can then assign a label from the inﬁnite Ulam-Harris tree I := n∈N

0

- u = (u1,...,un) = u1 ...un ∈ I according to its ancestral line, namely, ∅ → u1 → u1u2 → ... → u1...un = u,

where u1 is the u1-th child of the ancestor, u1u2 is the u2-th child of u1, and so on. We write |u| = n if u ∈ Nn.

Now let ξu = (ξui,j)i,j=1,...,p, u ∈ I \ {∅} be a family of i.i.d. copies of ξ =: ξ∅. We suppose that (Ω,A,P) is a probability space on which all ξu, u ∈ I are deﬁned and i.i.d. and independent of τ(∅), the random variable that gives the ancestor’s type. We write Pi if the ancestor’s type is i ∈ [p ]. We denote the associated expected value operators by E and Ei, respectively.

Each individual u ∈ T that is ever born has a clearly deﬁned type τ(u) ∈ [p ] and a time of birth S(u), namely, S(∅) = 0 and, recursively,

S(uk) = S(u) + Xu,k, u ∈ I, k ∈ N. For completeness, we write S(u) = ∞ if individual u is never born.

Now suppose that for each u ∈ I there exist a random vector ζu = (ζu1,...,ζup)T taking values in [0,∞]p and a product-measurable, separable random characteristic ϕu = (ϕ1u,...,ϕpu)T : Ω × R → Rp (taking values in the space of p-dimensional real column vectors) such that the

(ξu,ζu), u ∈ I are i.i.d. and the ϕu, u ∈ I are identically distributed. Further, we assume throughout that for every n ∈ N, the ϕu, u ∈ Nn are independent and independent of the (ξu,ζu,ϕu), |u| < n. These assumptions are satisﬁed, for instance, when the (ξu,ζu,ϕu), u ∈ I are i.i.d. However, our assumption is weaker and allows ϕu to be a function of the (ξuv,ζuv),

- v ∈ I. The variable ζui is viewed as the lifetime of the potential individual u given that its type is i. The function ϕiu(t) is some kind of score assigned to the individual u at the age t given that its type is i. Hence, for u ∈ T , we deﬁne ζu := ζuτ(u) as the lifetime of individual u and


ϕu(t) := ϕuτ(u)(t) = eTτ(u)ϕu(t) as the score assigned to individual u at the age t. For t ≥ 0 and j ∈ [p ], deﬁne

Ztj :=

u∈T

{j}(τ(u)) [0,ζ

u)(t − S(u)),

i.e., Ztj is the number of individuals of type j alive at time t. Now write Zt := (Zt1,...,Ztp)

for the associated row vector. Then (Zt)t≥0 is the multi-type general branching process. We are interested in the asymptotic behavior of Ei[Zt] as t → ∞ for i = 1,...,p. More generally, we are interested in the asymptotic behavior of Ei[Ztϕ] as t → ∞ for the multi-type general branching process counted with characteristic ϕ deﬁned via

Ztϕ :=

ϕu(t − S(u)), t ∈ R.

u∈T

Notice that introducing a general score ϕ indeed generalizes the model since we may write Ztj = Ztϕ for ϕu with

ϕiu(t) =

0 for i = j, [0,ζuj) for i = j.

