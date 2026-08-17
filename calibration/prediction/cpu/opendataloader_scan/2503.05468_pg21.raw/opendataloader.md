We can then assign a label from the inﬁnite Ulam-Harris tree I : =   n ∈ N 0 N n to each individual u = ( u 1 ,...,u n ) = u 1 ...u n ∈ I according to its ancestral line, namely,

$$
Un U, U1.
$$

where u 1 is the u 1 -th child of the ancestor, u 1 u 2 is the u 2 -th child of u 1 , and so on. We write | u | = n if u ∈ N n . i,j ∅

Now let ξ u = ( ξ u ) i,j =1 ,...,p , u ∈ I \ { } be a family of i.i.d. copies of ξ = : ξ ∅ . We suppose that (Ω , A , P ) is a probability space on which all ξ u , u ∈ I are deﬁned and i.i.d. and independent of τ ( ∅ ), the random variable that gives the ancestor’s type. We write P i if the ancestor’s type is i ∈ [ p ]. We denote the associated expected value operators by E and E i , respectively. Each individual u ∈ T that is ever born has a clearly deﬁned type τ ( u ) ∈ [ p ] and a time of

Each individual u € T that is

$$
S(uk) = S(u) + u € I. k € N.
$$

For completeness, we write S ( u ) = ∞ if individual u is never born.

Now suppose that for each u ∈ I there exist a random vector ζ u = ( ζ 1 u ,...,ζ p u ) T taking values in [0 , ∞ ] p and a product-measurable, separable random characteristic ϕ u = ( ϕ 1 u ,...,ϕ p u ) T : Ω × R → R p (taking values in the space of p -dimensional real column vectors) such that the ( ξ u , ζ u ), u ∈ I are i.i.d. and the ϕ u , u ∈ I are identically distributed. Further, we assume throughout that for every n ∈ N , the ϕ u , u ∈ N n are independent and independent of the ( ξ u , ζ u , ϕ u ), | u | < n . These assumptions are satisﬁed, for instance, when the ( ξ u , ζ u , ϕ u ), u ∈ I are i.i.d. However, our assumption is weaker and allows ϕ u to be a function of the ( ξ uv , ζ uv ), v ∈ I . The variable ζ i u is viewed as the lifetime of the potential individual u given that its type is i . The function ϕ i u ( t ) is some kind of score assigned to the individual u at the age t given that its type is i . Hence, for u ∈ T , we deﬁne ζ u : = ζ τ ( u ) u as the lifetime of individual u and ϕ u ( t ) : = ϕ τ ( u ) u ( t ) = e T τ ( u ) ϕ u ( t ) as the score assigned to individual u at the age t . For t ≥ 0 and j ∈ [ p ], deﬁne

$$
uet
$$

Z j t is the number of individuals of type j alive at time t . Now write

$$

$$

for the associated row vector. Then ( Z t ) t ≥ 0 is the multi-type general branching process. We are interested in the asymptotic behavior of E i [ Z t ] as t → ∞ for i = 1 ,...,p . More generally, we are interested in the asymptotic behavior of E i [ Z ϕ t ] as t → ∞ for the multi-type general branching process counted with characteristic ϕ deﬁned via

$$
= Pu(t = S(u)), t € R. uet
$$

Notice that introducing a general score ϕ indeed generalizes the model since we may write j ϕ

$$
for i # j, for i = j.
$$

