The r is a positive scalar function and the r is the unit vector from the origin to the point on the sphere with spherical coordinates (θ,ϕ).

In practice, when performing coordinate-based calculations at least two charts are required for radial manifolds in order to overcome singularities that occur from the topology in the surface coordinate frames, such as poles when using spherical angles. To this end, when using our numerical methods we consider two coordinate charts as in [25, 26]. The first chart we call Chart A and has coordinate singularities at the north and south pole, while the latter chart we call Chart B which has coordinate singularities at the east and west poles, see [25, 26]. In practice, for a given (θ,ϕ) ∈ [0,2π) × [0,π], we typically restrict usage of a chart for ϕ ∈ [π5, 45π]. For chart A, we parameterize the manifold in the embedding space R3 as

x(θ,ˆ ϕˆ) = r(θ,ˆ ϕˆ)r(θ,ˆ ϕˆ), r(θ,ˆ ϕˆ) = sin ϕ ˆ cos θ ˆ ,sin ϕ ˆ sin θ ˆ ,cos ϕ ˆ . (24) For Chart B, we use

x(θ,¯ ϕ¯) = r(θ,¯ ϕ¯)r(θ,¯ ϕ¯), r(θ,¯ ϕ¯) = cos ϕ ¯ ,sin ϕ ¯ sin θ ¯ ,sin ϕ ¯ cos θ ¯ . (25) Using these parametrizations, we can compute the basis ∂ϕ,∂θ for the tangent space as

σϕ(θ,ϕ) = rϕ(θ,ϕ)r(θ,ϕ) + r(θ,ϕ)rϕ(θ,ϕ), (26) σθ(θ,ϕ) = rθ(θ,ϕ)r(θ,ϕ) + r(θ,ϕ)rθ(θ,ϕ). (27)

Expressions for rϕ,rθ can be found using equations 24 and 25 depending on which chart is being used. These can also be used to compute all the relevant quantities described in Appendix A.

We use radial manifolds in training and validation of the GNPs. We use spherical harmonics to generate radial functions r(θ,ϕ) for the radial manifolds. In order to have a rich class of shapes for training, we consider a range of complexities for the radial functions. We sample complex coefficients aml for m = 0,...,l from a normal distribution with mean 0 and standard deviation 1l , to obtain the radial function

L

l

aml Ylm(θ,ϕ), (28)

r(θ,ϕ) =

m=−l

l=0

where Ylm are the spherical harmonics. We choose aml for m < 0 to ensure that r(θ,ϕ) is realvalued. In order to have a range of complexities in the geometry, we truncate the series at

L = 3,6,8,10,12,15,18,22. Further, we translate and scale r(θ,ϕ) so that it has mean 1 and satisfies 0.7 ≤ r(θ,ϕ) ≤ 1.3 for all (θ,ϕ).

For validation of the GNPs, we also consider toroidal manifolds. These are surfaces that are diffeomorphic to a torus. We consider the general parametrizations of

σ(u,v) = ((a(u,v)cos(v) + b(u,v))cos(u),(a(u,v)cos(v) + b(u,v))sin(u),a(u,v)sin(v)), (29)

for u,v ∈ [0,2π). One can choose a(u,v) = a,b(u,v) = b to obtain a standard torus. We consider functions a(u,v),b(u,v) of the form

- a(u,v) = a0 + r0 sin(A0u)cos(B0v),
- b(u,v) = b0 + r1 sin(A1u)cos(B1v).


(30)

Page 14 of 15

