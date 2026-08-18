with the homogeneous Neumann boundary condition, it is known that u has exactly a single peak (i.e. local maximum of u ). Moreover, if the single peak is on the boundary of Ω, then it is located at the point where the mean curvature of the boundary ∂ Ω reaches its maximum value. These results have not been numerically verified, which limits the further application of multiple-solution analysis.

The rest of this paper is organized as follows. In section 2, we describe the spectral Legendre–Fourier scheme we used to discretize equation (1.1) defined in an elliptic geometry. The IAOBDM is designed and presented in section 3. In section 4, ample numerical experiments are carried out to demonstrate the efficiency of this method, and to show the effect of varying geometry Ω on multiple solutions of (1.1). Finally, we end the paper with some remarks in section 5.

# 2. A Legendre–Fourier scheme for elliptic equations in an elliptic domain

first step is to provide an efficient discretization scheme. Here, we adopt a Legendre–Fourier scheme for (1.1) in an elliptic domain. Let

$$
{(x,y) 8 < 1} (2.1)
$$

The weak formulation of (1.1) with homogeneous Dirichlet boundary condition and ε = 1 is to find u ∈ H 1 0 (Ω) such that

$$
(2.2)
$$

where x = ( x,y ). We use polar transformation x = ar cos θ,y = br sin θ to transform the Dirichlet problem into polar coordinate form:

$$
W1Urr + W3Ur0 ) + r2 u(1,0) = 0, periodic in 0 (2.3)
$$

where

$$
0 sin? sin2 W1 = + W2 + W3 = (2.4) a2 b2 b2 a2 cos2
$$

The corresponding weak formulation (2.2) becomes

$$
W2Uru (2.5) 1 4 J w2v)drdo = fvdrde , Vv € H (02).
$$

Obviously, from (2.3) or (2.5), we can find that a singularity point appears at r = 0, indicating that additional polar conditions should be proposed to obtain the desired solution regularity at

