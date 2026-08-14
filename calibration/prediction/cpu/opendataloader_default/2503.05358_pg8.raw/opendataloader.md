comet (t4). This is possible because the optimal flyby parameters (depth and inclination of the planetocentric hyperbola) can be computed directly from t2 and t4, thus reducing the dimensionality of the problem.

3.1.1. Earth-GA segment

For a given flyby date, the ecliptic longitude of the GA planet is computed from the ephemeris as

l2F = ΩF + ωF + nF(t2 − tFp ), (1)

where nF is the mean motion of the planet. The minimum eccentricity of the conics that connect Earth with the planet is determined by the condition of being able to reach the planet:

rE + rF 2 → emin = 1 −

amin =

rE amin

. (2)

The upper bound of eccentricity is set by the maximum characteristic energy (C3) that the launcher is capable of:

v1,max =

√

C3 + vE =

√

C3 +

µS rE

, (3)

v12,max 2 −

µS rE → amax = −µS

2Emax → emax = 1 −

Emax =

rE amax

, (4)

where E denotes the mechanical energy and µ is the gravitational parameter. Due to the condition of departure from the perihelion, the eccentricity determines the transfer angle between Earth and the planet

p

1 e

rF − 1 , (5) with p = a(1 − e2) denoting the semilatus rectum. Likewise, the transfer time t12 (only the elliptic case is shown for the sake of brevity) can be computed from e

cos(θ12) =

e + cos(θ12) 1 + ecos(θ12) → M = E − esin(E) → t12 = M

cos(E) =

a3 µS

, (6)

8

