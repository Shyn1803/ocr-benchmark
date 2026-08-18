values; ii) in the strongly underdamped case, the secondorder phase transition turns into a first-order phase transition (note the jump in the curve for m = 10 ), which is in line with what has been reported before [ 26 , 27 ]. In any case, for all inspected values of the mass, the

asynchronous state ( r ≪ 1 ) always exists over a finite range of mean coupling strengths. In this parameter region the temporal statistics of the dynamics is independent of K . In the remainder of the study, we will set K = 0 .

# B. Power Spectrum Calculation

To further analyze the fluctuations in the incoherent regime, we compute the power spectrum of individual oscillators, denoted as S x ℓ ( ω ) , where x ℓ = e iθ ℓ . The power spectrum is defined as:

$$
lim ĩe(w) = eiwtze(t) dt,
$$

where ˜ x ℓ ( ω ) is the Fourier transform of x ℓ ( t ) computed over a finite time interval T . Common temporal statistics are characterized by the averaged power spectrum,

$$
Sz(w) = (6
$$

We obtain these spectra by integrating the full set of second-order differential equations (Eq. ( 1 )) using a fourth-order Runge-Kutta method with a relative tolerance of 10 − 8 . We refer to this direct numerical integration as the network dynamics (ND) method and use it as a benchmark against the iterative mean-field (IMF) method introduced in the following section. In Fig. 2 and Fig. 3 , the ND results are shown as black dashed lines for comparison with the IMF method. The simulation is run for a total time period T (with

T = 10 5 for Fig. 2 and T = 10 4 otherwise), discarding the initial time t d = 1000 to eliminate transients. To allow oscillator-resolved analysis, the natural frequencies ω ℓ are drawn from the prescribed distribution and held fixed, as is the Gaussian-distributed connectivity matrix K ℓm . The system size is chosen as N = 10 4 to minimize dependence on the specific realization of the connectivity matrix K ℓm , which is also drawn from a Gaussian distribution.

The power spectrum is computed using the fast Fourier transform (FFT). The single-oscillator power spectrum S x ℓ ( ω ) is evaluated for a selected oscillator ( ℓ = 3 in our case), while the mean power spectrum S z ( ω ) is obtained by averaging over all oscillators:

$$
N Sz (w) = N
$$

The results are smoothed by binning neighboring frequency points to improve spectral accuracy. We divided the frequency axis into M = with T/(Mdt) frequency points averaged per bin using an accumulation method to reduce statistical noise

# III. ITERATIVE MEAN FIELD METHOD

In this study, we employ the iterative mean field (IMF) method, often also referred to as dynamic mean field method [ 28 ], to analyze the asynchronous states of the Kuramoto model with inertia and disorder in coupling and natural frequencies. This method provides a selfconsistent approach to compute the power spectra of single oscillators, approximating the network noise experienced by each oscillator as a Gaussian process, iteratively refined until convergence. The method has been used for spin systems in the early 1990’s [ 29 ], for networks of spiking neurons [ 19 – 21 ], and specifically for the Kuramoto model with disorder in the coupling coefficients (but without inertia) in [ 4 – 6 , 30 ]. For our system with inertia, we start from the equa-

tions of motion for the oscillators Eq. ( 1 ) and express the coupling term in the dynamics as a multiplicative network noise:

$$
=We + Im (8)
$$

where the network noise ζ ℓ ( t ) is defined as:

$$
Se(t) = m=l Keme
$$

For large networks in the asynchronous regime (excluding the Volcano transition case observed with symmetric coupling coefficients, see [ 30 , 31 ]), this noise behaves as a superposition of independent Gaussian processes due to the central limit theorem. The autocorrelation of the network noise can be written as:

$$
(Se(t)Se(t')) = Kem (t)) k2 K2 (ei(0mC (t) ) . N N2 ml,nl (10)
$$

Assuming uncorrelated oscillators yields

$$
(t')~0n (t)) ) (11)
$$

leading to the simplified form

$$
(S(t)S(t)) = (k2 + K? /N) (12)
$$

The right-hand side thus represents the autocorrelation of a single oscillator’s phase pointer. In the Fourier domain, the network noise spectrum S ζ ( ω ) is proportional to the power spectrum of a single oscillator averaged over the network:

$$
Sc(w) = 4 (13) (k2
$$

