# Geometric Delocalization in Two Dimensions

Laura Shou, 1 Alireza Parhizkar, 1 and Victor Galitski 1

1 Joint Quantum Institute, Department of Physics, University of Maryland, College Park 20742

We demonstrate the existence of transient two-dimensional surfaces where a random-walking particle escapes to infinity in contrast to localization in standard flat 2D space. We first prove that any rotationally symmetric 2D membrane embedded in flat 3D space cannot be transient. Then we formulate a criterion for the transience of a general asymmetric 2D membrane. We use it to explicitly construct a class of transient 2D manifolds with a non-trivial metric and height function but “zero average curvature,” which we dub tablecloth manifolds. The absence of the logarithmic infrared divergence of the Laplace–Beltrami operator in turn implies the absence of weak localization, non-existence of bound states in shallow potentials, and breakdown of the Mermin–Wagner theorem and Kosterlitz–Thouless transition on the tablecloth manifolds, which may be realizable in both quantum simulators and corrugated two-dimensional materials.

Introduction There are many seemingly disconnected physical phenomena which are related to the properties of the Laplace–Beltrami operator. They include random walk or diffusion, the standard Schr¨ odinger equation, the properties of fluctuations in symmetry broken phases, interactions between topological excitations, and many others. In particular, if the heat kernel p ( x,y ; t ) integrated over time — the Green’s function of the Laplace–Beltrami operator on a manifold is infinite it implies automatically the following properties of this space: a random-walking particle is guaranteed to return to its starting region infinitely often (recurrence), there is Anderson localization in an arbitrarily weak disorder potential, any shallow quantum potential well hosts a bound state, no longrange order with spontaneously broken continuous symmetry can exist at finite temperature in this space (Mermin–Wagner theorem), to name a few. Specifically in flat Euclidean space, the two-dimensional case is critical as the corresponding heat kernel integral diverges logarithmically:

$$
p(z, y;t) dt ơ In(Tmin/ Tmin Tmax Tmax
$$

which means that the two-dimensional flat space is recurrent, while higher dimensional flat spaces, which have finite integrals, are transient (a random-walking particle always escapes its starting region). An additional physical phenomenon tied to the Green’s function of the Laplace–Beltrami operator specific to O (2) models on two-dimensional manifolds is the behavior of topological excitations there. In the conventional flat space, the logarithmic divergence ( 1 ) is tied to logarithmic vortex-vortex interactions that in turn lead to a finite-temperature Berezinskii–Kosterlitz–Thouless transition due to the competition with entropic effects which also scale logarithmically. Due to the abundance of fundamental physical phenom-

Due to the abundance of fundamental physical phenomena tied to the LaplaceBeltrami  operator; it is reasonable to ask if there exist two-dimensional curved transient manifolds. Recent works [1, 2] have   studied some phenomena on hyperbolic manifolds and lattices; which are known to be   transient   [3-5]. Here we ask: is it pos sible to have two-dimensional membrane (i.e., twodimensional smooth manifold   embedded in flat  Euclidean three-dimensional space described by height function) that is transient; J 0o? We answer this question min in the affirmative and explicitly construct 2D transient ~tablecloth manifolds" (Fig. 1), which hence lead to the breakdown of standard two-dimensional physics.

25

![](<2503.07705_pg1_images/imageFile1.png>)

FIG. 1. Two examples of tablecloth manifolds. On the right, a generic tablecloth manifold, and on the left the simplified example constructed in Eq. ( 12 ). The colors demonstrate the ratio of the volume element at any point on the manifold,   g ( r, θ ) drdθ , to the regular flat volume element at the same point, rdrdθ . Therefore, the colors encode the value of   g ( r, θ ) /r . This allows us to compare the volume growth to the regular flat one as we go away from the origin with increasing r . Purple corresponds to the regular πr 2 volume growth of a flat disk, while other colors designate faster growths.

Transience on a 2-dimensional membrane The general form of a two dimensional Riemannian metric in polar-like coordinates, with no isometries assumed, is given by,

$$
ds = dr +2B(r, 0) dr d0 + C2 (r,0) (2)
$$

For rotationally symmetric manifolds with metric of the form ds 2 = dr 2 + f ( r ) 2 dθ 2 , a well-known result [ 6 , 7 ] is that transience is equivalent to the condition

$$
dr f (1
$$

Using this, we can find rotationally symmetric metrics ds 2 = dr 2 + f ( r ) 2 dθ 2 corresponding to transient Brownian motion, and which also satisfy an average zero curvature condition, as

