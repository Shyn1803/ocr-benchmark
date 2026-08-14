# arXiv:2503.07083v1 [cond-mat.stat-mech] 10 Mar 2025

## Fluctuations of blowup time in a simple model of a super-Malthusian catastrophe

Baruch Meerson1

1Racah Institute of Physics, Hebrew University of Jerusalem, Jerusalem 91904, Israel

Motivated by the paradigm of a super-Malthusian population catastrophe, we study a simple stochastic population model which exhibits a finite-time blowup of the population size and is strongly affected by intrinsic noise. We focus on the fluctuations of the blowup time T in the asexual binary reproduction model 2A → 3A, where two identical individuals give birth to a third one. We determine exactly the average blowup time as well as the probability distribution P(T) of the blowup time and its moments. In particular, we show that the long-time tail P(T → ∞) is purely exponential. The short-time tail P(T → 0) exhibits an essential singularity at T = 0, and it is dominated by a single (the most likely) population trajectory which we determine analytically.

### I. INTRODUCTION

It is argued that the human population of the Earth exhibits a super-Malthusian (that is a faster-thanexponential) growth that should ultimately lead to a finite-time blowup [1]. In general, a finite-time blowup in a population model can occur due to a positive feedback when the population growth rate increases faster than linearly with the population size. A simple example is provided by the following nonlinear ordinary differential equation (ODE) for the population size n = n(t):

n˙(t) = βn2(t), β > 0, (1)

where the dot denotes the time derivative. The solution of this equation,

n0 1 − βn0t

, (2)

n(t) =

where n0 ≡ n(t = 0) > 0 is the initial condition, blows up in a finite time T = (βn0)−1.

In the presence of noise the blowup time becomes a random quantity, and it is interesting to determine its statistics. One way of addressing this class of problems is to interpret Eq. (1) as the equation of motion of an overdamped particle, with the coordinate n = n(t), in a repulsive potential V (n) ∼ −n3. By adding a noise term to Eq. (1), one turns this mean-field equation into a Langevin equation:

x˙(t) = βx2(t) + η(t), (3)

where η(t) is white Gaussian noise, and we have replaced n by x. The finite-time blowup statistics for this model and its extensions has been recently studied in Ref. [2], see also Refs. [3–5].

Here we take a different approach by observing that Eq. (1) also provides a mean-field description to the simple Markovian stochastic model of asexual binary reproduction 2A → 3A, where two identical A-individuals, which we will call particles, give birth to a third one. The master equation for this stochastic process is

β(n − 1)(n − 2) 2

βn(n − 1) 2

P˙n(t)=

Pn−1(t) −

Pn(t), (4)

where Pn(t) is the probability of observing n particles at time t. We suppose that there are m ≥ 2 particles at t = 0, so the initial condition is

Pn(t = 0) = δnm . (5)

By rescaling time, βt → t, we can get rid of the rate coefficient β. Therefore, from now on we set β = 1.

In Sec. II we determine exactly the average blowup time and the probability distribution of the blowup time for the 2A → 3A model. We also determine several first moments of the distribution and provide an additional insight into the short-time tail of the probability distribution of the blowup time by employing the optimal fluctuation method (OFM). In Sec. III we briefly discuss our main results and compare them with those for the Langevin equation (3), obtained in Ref. [2].

II. STATISTICS OF BLOWUP TIME

A. Average blowup time

As a warmup, let us calculate the average blowup time Θ(m) as a function of the initial number of particles m. This quantity can be determined from the backward master equation, see, e.g., Ref. [6]. For the process 2A → 3A the backward master equation is

r(m)[Θ(m + 1) − Θ(m)] = −1, (6)

where r(m) = m(m − 1)/2. The blowup, which can be viewed as the first passage to infinity, is described by the absorbing boundary condition [6]

Θ(m → +∞) = 0. (7)

The solution of the problem (6) and (7) is remarkably simple:

2 m − 1

Θ(m) =

. (8)

In particular, for m = 2 (there are exactly two particles at t = 0) we obtain Θ(2) ≡ ⟨T⟩ = 2. It is twice as large as the mean-field result t0 = 1 for the same initial number of particles. Notice that the average blowup time (8) falls off quite slowly as a function of m.

