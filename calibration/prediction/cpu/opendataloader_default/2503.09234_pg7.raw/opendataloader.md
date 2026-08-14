AN END TO END GLUING CONSTRUCTION FOR Q-CURVATURE 7

with k − 1 punctures. We assume that both metrics are nondegenerate, that both metrics have one end with a common asymptotic necksize of ε∗, and that (M1,g1) admits a Jacobi field deforming the necksize ε∗ to first order. We then glue the two metrics together end-toend, along the end with the common asymptotic necksize of ε∗. Within this construction we have the freedom to rotate (M1,g1) relative to (M2,g2), using any element of SO(n − 1) fixing the common axis of the Delaunay asymptotes. We vary this rotation over the whole group, which then gives us a family of solutions in Mk. In Section 7 we will complete the proof of Theorem 1.5 by showing the resulting submanifold cannot be contractible. The key tool we use is the forgetful map, sending a metric in Mk to its conformal class.

Acknowledgments: Frank Pacard suggested this construction to us, and we thank him for the prompt. We also thank Jie Qing for helpful conversations about the space of conformal structures on a finitely punctured sphere and Pedro Gaspar for generously providing figures. ASA is supported by Centro de Modelamiento Matema´tico (CMM) BASAL fund FB210005 for center of excellence from ANID-Chile, RC is supported by Fondecyt grant number 11230872 and by Centro de Modelamiento Matem´atico (CMM) BASAL fund FB210005 for center of excellence from ANID-Chile and ASS is supported by CNPq grant number 408834/2023-4, 312027/2023-0, 444531/2024-6 and 403770/2024-6. Part of this research was completed while ASA visited the Center for Mathematical Modeling at the University of Chile, which we thank for their hospitality.

2. Preliminaries

In this section we recall some useful material from other sources and perform some preliminary computations.

2.1. Delaunay metrics. The Delaunay metrics are all the constant Q-curvature metrics on a twice-punctured sphere and, as we will see later, play an important role in understanding the behavior of singular constant Q-curvature metrics with isolated singularities.

g◦ on Sn\{p,q} where p and q are distinct. After a rotation and a dilation, we can assume p = N is the north pole and q = S is the south pole. Transferring to the Euclidean gauge we write g = u

4 n−4

Consider a metric g = U

4

n−4geuc where u : Rn\{0} → (0,∞). This metric has Q-curvature equal to n(n

2−4)

8 if and only if u satisfies (1.6) with a single singular point at the origin.

Frank and Ko¨nig [5] classified all the solutions of

n(n − 4)(n2 − 4) 16

u : Rn\{0} → (0,∞), ∆2u =

u

n+4

n−4, (2.1)

and we describe them here. First we perform the Emden-Fowler change of coordinates, defining

4−n

F : C∞(Br(0)\{0}) → C∞((−log r,∞) × Sn−1), F(u)(t,θ) = e

2 tu(e−tθ). (2.2) We can of course invert F, obtaining

F−1(v)(x) = |x|

4−n

# 2 v(−log |x|,θ).

