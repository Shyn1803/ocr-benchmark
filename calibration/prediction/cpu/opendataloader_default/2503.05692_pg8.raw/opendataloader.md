8 ALEXEY CHESKIDOV, ZIRONG ZENG, AND DENG ZHANG

considering solutions to the heat equation with a space-time periodic, zero-mean in space source f(t,x), ∂tu − ∆u = f. (1.6)

The long time behavior of the solution to this equations is described by what is called the pullback attractor, which, in this case, is a single trajectory

uA(t,x) := ˆ t

e(t−τ)∆f(τ,x)dτ = ˆ t t0

e(t−τ)∆f(τ,x)dτ,

−∞

for some t0, which we assume is zero appropriately translating f in time. Here the second equality follows from the time periodicity of uA(x,t). All the trajectories (solutions to (1.6)) converge to uA(t,x) in the pullback sense (as the initial time goes to minus infinity). This holds even for the 3D NSE with small forces, see [11].

If spatial oscillations of f dominate the temporal oscillations, then (−∆)−1f(t,x) is the leading term in uA(t,x). However, in applications to convex integration, the non-diagonal interactions between building blocks result in errors of type

f = PHdiv (w ⊗ w),

where w is the velocity (or magnetic field) perturbation, which, for simplicity, is assumed to be a just a T-periodic in time building block. To control the size of the error ∆w, the perturbation has to be highly intermittent (with the intermittency dimension D < 1). Then it is easy to check that

∥(−∆)−1div (w ⊗ w)∥L2

# ≫ ∥w∥L2

. Thus, temporal oscillations of the perturbation w have to dominate spatial ones. Let

x

x

ˆ T

f(τ,x)dτ, ∂t−1f(t,x) := ˆ t

1 T

f(τ,x) − f¯(x) dτ,

f¯(x) :=

0

0

where T is the time period of f. Note that ∂t−1f(t,x) is also time periodic. Then

uA(t,x) = ˆ t

e(t−τ)∆f¯(x)dτ + ∂t−1f(t,x) + ˆ t

e(t−τ)∆∆∂t−1f(τ,x)dτ. (1.7)

0

0

When the frequency of temporal oscillations is high enough, (−∆)−1f¯(x), or the first term in (1.7) is the leading term of uA(t,x). Since time averaging of f traveling along geodesics results in a larger intermittency dimension D > 1, we get

∥uA∥L2

# ≪ ∥w∥L2

, and hence uA can be used as a temporal corrector to cancel the error f.

x

x

Notations. Let N+ denote the set of positive integers. For p ∈ [1,∞] and s ∈ R, we set

Lpx := Lp(T3), Wxs,p := Ws,p(T3), Hxs := Hs(T3),

where Wxs,p is the Sobolev space and Hxs = Wxs,2. We also use L2σ for divergence free functions in L2x. Given any Banach space X, we denote by C([0,T];X) the space of continuous functions from [0,T] to X, equipped

with the norm ∥u∥CTX := sups∈[0,T] ∥u(s)∥X. In particular, for N ∈ N+ we set

∥∂tm∇ζu∥L∞([0,T];L∞x ),

∥u∥CT,xN :=

0≤m+|ζ|≤N

x22∂ζ

x11∂ζ

where ζ = (ζ1,ζ2,ζ3) denotes the multi-index and ∇ζ := ∂ζ

x33. We also use the product spaces Lpx := Lp(T3) × Lp(T3), Hxs := Hxs × Hxs, Cx1 := Cx1 × Cx1.

Throughout this paper the notation a ≲ b means that a ≤ Cb for some constant C > 0.

