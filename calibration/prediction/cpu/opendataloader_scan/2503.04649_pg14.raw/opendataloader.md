The r is a positive scalar function and the r is the unit vector from the origin to the point on the sphere with spherical coordinates ( θ,ϕ ).

In practice, when performing coordinate-based calculations at least two charts are required for radial manifolds in order to overcome singularities that occur from the topology in the surface coordinate frames, such as poles when using spherical angles. To this end, when using our numerical methods we consider two coordinate charts as in [ 25 , 26 ]. The first chart we call Chart A and has coordinate singularities at the north and south pole, while the latter chart we call Chart B which has coordinate singularities at the east and west poles, see [ 25 , 26 ]. In practice, for a given ( θ,ϕ ) ∈ [0 , 2 π ) × [0 ,π ], we typically restrict usage of a chart for ϕ ∈ [ π 5 , 4 π 5 ]. For chart A, we parameterize the manifold in the embedding space R 3 as

$$
r(ô,ộ) sin COS (24)
$$

For Chart B, we use

$$
2(0,%) r(0,0) sin (25)
$$

Using these parametrizations, we can compute the basis ∂ ϕ ,∂ θ for the tangent space as

$$
06(0, = = (26)
$$

$$
00 (0,0) (27)
$$

Expressions for r ϕ , r θ can be found using equations 24 and 25 depending on which chart is being used. These can also be used to compute all the relevant quantities described in Appendix A .

We use radial manifolds in training and validation of the GNPs. We use spherical harmonics to generate radial functions r ( θ,ϕ ) for the radial manifolds. In order to have a rich class of shapes for training, we consider a range of complexities for the radial functions. We sample complex coefficients a m l for m = 0 ,...,l from a normal distribution with mean 0 and standard deviation 1 l , to obtain the radial function L l

$$
r(0,0) = (28) l=0 m=-l
$$

where Y m l are the spherical harmonics. We choose a m l for m < 0 to ensure that r ( θ,ϕ ) is realvalued. In order to have a range of complexities in the geometry, we truncate the series at L = 3 , 6 , 8 , 10 , 12 , 15 , 18 , 22. Further, we translate and scale r ( θ,ϕ ) so that it has mean 1 and satisfies 0 . 7 ≤ r ( θ,ϕ ) ≤ 1 . 3 for all ( θ,ϕ ).

For validation of the GNPs, we also consider toroidal manifolds. These are surfaces that are diffeomorphic to a torus. We consider the general parametrizations of

$$
(29)
$$

for u,v ∈ [0 , 2 π ). One can choose a ( u,v ) = a,b ( u,v ) = b to obtain a standard torus. We consider functions a ( u,v ) ,b ( u,v ) of the form

$$
(30)
$$

