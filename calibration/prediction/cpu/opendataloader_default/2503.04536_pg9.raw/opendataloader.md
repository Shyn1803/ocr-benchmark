DOUBLE METASURFACES AND OPTIMAL TRANSPORT 9

σ(yi,t + s) as functions of s. These solve ∂sσ(yi,t + s) = F σ(yi,t + s),t + s and σ(y1,t+0) = σ(y2,t+0). Again by uniqueness, σ(y1,t+s) = σ(y2,t+s) for all |s| < δ, for some δ > 0, that is, (t − δ,t + δ) ⊂ J and so J is open.

2.3. Minimization flows and OT. Here we use the approach from [AHT03]. Let T : (Ω0,ρ0) → (Ω1,ρ1) be a measure preserving map, i.e.,

ρ0(x)dx =

T−1(E)

ρ1(x)dx

E

for each Borel set E ⊂ Ω1. Set σt(·) = σ(·,t) where σ is as before, the flow corresponding to a vector field F satisfying (2.2). The family of maps T ◦ (σt)−1 : (Ω0,ρ0) → (Ω1,ρ1) are measure preserving since

T ◦ (σt)−1 −1 (E) = σt ◦ T−1(E), E ⊂ Ω1

and

ρ0(x)dx =

(T◦(σt)−1)−1(E)

# =

# =

Consider the function of t

ρ0(x)dx

σt◦T−1(E)

ρ0(x)dx since σt preserves the measure

T−1(E)

ρ1(x)dx.

E

G(t) =

c x,T ◦ (σt)−1(x) ρ0(x)dx;

Ω0

here c x, y is a general cost. Making the change of variables x = σ(z,t) yields

G(t) =

=

c(σ(z,t),T(z)) ρ0(σ(z,t)) Jσ(z)dz

Ω0

c(σ(z,t),T(z)) ρ0(z)dz

Ω0

since ρ0(σ(z,t)) Jσ(z) = ρ0(z) because σ(E,t) ρ0(x)dx = E ρ0(x)dx for all t and all E ⊂ Ω0. If T is an optimal map with respect to the cost c, then G′(t) = 0 when

