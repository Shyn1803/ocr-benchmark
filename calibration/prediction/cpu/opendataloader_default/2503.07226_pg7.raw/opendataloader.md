EXACT SOLUTIONS TO THE CANCER LASER ABLATION MODELING 7

3. Analytical solutions

Our objective is to build exact solutions that fit, in particular, the physiological problem under study,

τ∂tu − α∆u + Bu = f, (12) via the separable variable method, in cylindrical coordinates i.e. at the position (r,z) and the time t. Using Bernoulli–Fourier technique, we have

τX′(t) + [−α(β + η2) + B]X(t) R(r)Z(z) = f(r,z,t), (13) where the constants β,η ∈ R are arbitrary,

Radiative transfer: τ = 1/ν, α = D, B = µa and f = S in Subsection 2.1; Heat transfer: τ = ρcp, α = k, B = cbωb(t) and f = q in Subsection 2.2.

The functions X, Z and R are elementary solutions to the system of ordinary differential equations (ODE)   

X′(t) = ζX(t) Z′′(z) = η2Z(z)

(14)

rR′(r) ′ = βrR(r)

for some time parameter ζ ∈ R. The nonconstant behavior of ωb (cf. (11)) does not invalidate the application of this technique in determining an analytical solution for the heat transfer.

Firstly, a particular solution is available due to the Duhamel principle (for details, see [9] and the references therein). Secondly, let us seek for elementary solutions of the ODE system (14).

The first-order ODE in (14) admits the elementary solution X(t) = exp[

t

ζ(s)ds], t > 0. (15) The second-order ODE in (14), with constant coefficients, admits the elementary

0

solutions

Z(z) = exp[±ηz], z ∈ R. (16)

The second-order ODE in (14), with nonconstant coefficients, admits the Bessel functions of first and second kind and order 0, respectively, J0( |β|r) and Y0( |β|r) if β < 0; or the modified Bessel functions of first and second kind and order 0, respectively, I0(√βr) and K0(√βr) if β > 0 [33]. If β = 0, the elementary solutions reduce to R(r) = log[r] and the unity function.

Then, a general solution solving the homogeneous equation (13) (f = 0) is available by the above elementary solutions, if

τζ + B = α(β + η2). (17)

Finally, we analyze the PDE (12) at the period of time 0 < tj+tp < t < tj+1, for any j = 0,··· ,N −1. This case will describe the homogeneous problem, which is governed without source (f = 0), at one pulse-to-pulse interval ∆t. For the sake of simplicity, we denote the initial instant of time tj + tp by t0 throughout this subsection.

