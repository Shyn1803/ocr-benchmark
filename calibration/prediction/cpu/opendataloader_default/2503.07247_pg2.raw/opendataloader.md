2 AOI WAKUDA

by the WINGS-FMSP program at the Graduate School of Mathematical Sciences, the University of Tokyo.

2. isometries on hyperbolic plane

Let H be the upper half-plane model in hyperbolic geometry. The group of isometries of H is given by

a b c d

PSL±2 (R) = ±

a,b,c,d ∈ R,ad − bc = ±1 .

Each isometry g ∈ PSL±2 (R) is classified according to the absolute value of its trace (for example, see [5]):

- - Case 1: detg = 1 (Orientation-preserving isometries)

- • Elliptic if |Trg| < 2. In this case, g has a unique fixed point in H.
- • Parabolic if |Trg| = 2. In this case, g has a unique fixed point on the real axis.
- • Hyperbolic if |Trg| > 2. In this case, g has exactly two fixed points on the real axis.


- - Case 2: detg = −1 (Orientation-reversing isometries)


- • Reflection if Trg = 0. In this case, g is an involution with a geodesic of fixed points.
- • Glide-reflection if Trg ̸= 0. In this case, g has two fixed points on the real axis.


For each g ∈ PSL±2 (R), the translation length tg is defined as: tg = inf

d(z,gz).

z∈H

If tg is positive, we call g a positive translation isometry. For a positive translation isometry g, the absolute value of the trace of g satisfies the following:

 

tg 2

, if g is hyperbolic, 2sinh

2cosh

|Trg| =

(1)

tg 2



, if g is a glide-reflection.

For a positive translation isometry g ∈ PSL±2 (R), we define Ag as the axis of g, i.e., the geodesic joining the two fixed points of g, and let ρA

be the reflection with respect to Ag. We state the following result from [1, Theorem 7.38.6] because it will be used later.

g

- Theorem 2.1. [1, Theorem 7.38.6] Let g and h be hyperbolic transformations of the hyperbolic plane and suppose that Ag and Ah intersect at a point P. Denote by θP the angle at P between forward direction of Ag and Ah. Then the composition g ◦ h is hyperbolic and

- 1

- 2|Trgh| = cosh


tg 2

cosh

th 2

+ sinh

tg 2

sinh

th 2

cos(θP). (2)

Now, we generalize the above theorem to positive translation isometries. The proof of [1, Theorem 7.38.6] uses the law of cosines for the triangle formed by the three axes Ag, Ah, and Agh to compute the absolute value of the trace. In this paper we compute the absolute value of the trace by matrix computations as follows.

- Theorem 2.2. Let g and h be positive translation isometries and suppose that Ag and Ah intersect at a point P. Denote by θP the angle at P between forward direction of Ag and Ah. Then, the following hold.


- Case 1: If g is a glide-reflection and h is a hyperbolic element, tg

- 1

- 2|Trgh| = sinh


2

cosh

th 2

+ cosh

tg 2

sinh

th 2

cosθP . (3)

- Case 2: If both g and h are glide-reflections,


- 1

- 2|Trgh| = sinh


tg 2

sinh

th 2

+ cosh

tg 2

cosh

th 2

cosθP . (4)

Proof. Without loss of generality, we may assume the axis Ag equals the imaginary axis with the intersection point P ∈ Ag ∩ Ah located at i ∈ H . See Figure 1.

