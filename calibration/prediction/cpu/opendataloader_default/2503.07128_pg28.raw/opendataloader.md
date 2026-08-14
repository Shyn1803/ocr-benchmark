Here Bn denotes the ball of radius n centred at the origin. The following property is readily deduced from parabolic estimates:

un(t,x) = p(x) locally uniformly in (t,x) ∈ [0,+∞) × Rn. (4.10)

lim

n→+∞

We claim that the function un fulfils (4.9) for n sufficiently large, depending on ε, hence by the previous step it satisfies (4.8). Assume by contradiction that this is not the case. Then, for any n ∈ N, it holds that

tn := inf{t ≥ 0 : ∃x ∈ t W, un(t,x) ≤ u(x)} < +∞.

We know from (4.10) that tn → +∞ as n → +∞. In particular, tn > 0 for n sufficiently large and it follows from the definition of tn that

∀t ∈ [0,tn), ∀x ∈ t W, un(t,x) > u(x), (4.11) and, moreover, being tn W compact, that there exists xn ∈ tn W such that

un(tn,xn) = u(xn).

Recall that u is a strict subsolution, hence the parabolic strong maximum principle necessarily implies that xn ∈ ∂(tn W), that is, xn/tn ∈ ∂ W.

Consider now hn ∈ ZN such that ξn := xn − hn ∈ [0,1)N. We define

un(t,x) := un(tn + t,hn + x). Up to extraction of a subsequence, the following limits exist:

ξn → ξ∞ ∈ [0,1]N, xn/tn → ζ ∈ ∂ W.

Also, always up to subsequences, by standard parabolic estimates and spatial periodicity of the equation, the functions un converge to u∞, an entire solution of (1.1) which fulfils by construction (and by periodicity of u)

u∞(0,ξ∞) = u(ξ∞). (4.12) Moreover, (4.11) rewrites for the un as

∀t ∈ [−tn,0), ∀x ∈ (tn + t) W − {xn}, un(t,x + ξn) > u(x + ξn). (4.13) We assert that this entails

ε 3

∀t ≤ 0, ∀x · ν ≤ 1 −

c1(ν)t, u∞(t,x + ξ∞) ≥ u(x + ξ∞), (4.14)

where ν is the outward unit normal vector to W at the point ζ and, we recall, c1(ν) is the speed of the uppermost front of the terrace T ν in the direction ν.

The first crucial observation to derive (4.14) is that the t-dependent sets (tn + t) W expand at a given boundary point (tn+t) w(e)e with the (positive) constant normal speed w(e)e· ν, where ν is the outward normal at that point, hence e · ν > 0. The second observation is that 0 ∈ ∂ tn W − {xn} , for any n ∈ N, and that the normal at that point converges to ν. The last one is that, because W is compact and smooth, it satisfies uniform interior and exterior sphere conditions of some radius ρ > 0 on the boundary, whence its dilation (tn + t) W fulfils these conditions with radius (tn + t)ρ, which for any t tends to +∞ as n → +∞. This means that (tn + t) W “flattens” to a half-space around each of its boundary points as n → +∞. These geometric observations are made rigorous in

28

