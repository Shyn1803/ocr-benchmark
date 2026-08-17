![](<2503.04407_pg3_images/imageFile1.png>)

RF Chain

Movable Antennas

RF Chain

RF Chain

RF Chain

Fixed Antennas

RF Chain

RF Chain

Radar Signal Processing

Transmitter

Radar Signal Processing

Receiver

1. Proposed MA-enabled FH-MIMO radar system.

achieve improved performance in various tasks, e.g., if better resolution of target angles (velocity or distance) is required, the antenna positions can be adjusted to improve the performance of the ambiguity function in the angular (Doppler or delay) domain.

The remainder of this paper is organized as follows. Section II describes the considered MA-enabled FH-MIMO radar system model and the corresponding ambiguity function. In Section III, we analyze the relationship between the ambiguity function and the antenna positions. In Section IV, we propose a low complexity algorithm to solve the antenna position optimization problem. Section V provides the numerical results and discussions. Finally, we conclude this paper in Section VI. Notations : Scalars, vectors and matrices are respectively

denoted by lower/upper case, boldface lower case and boldface upper case letters. For an arbitrary matrix A , A T , A ∗ and A H denote its transpose, conjugate and conjugate transpose respectively.   ·   denotes the Euclidean norm of a complex vector, and |·| denotes the absolute value of a complex scalar. ⌈·⌉ represents the round-up operator. For a complex number x , ℜ{ x } denotes its real part and ∠ x denotes its angle. I and 0 denote an identity matrix and an all-zero vector with appropriate dimensions, respectively. C n × m denotes the space of n × m complex matrices.

x t, 0 = 0 and x t,m =   m i =0 d t,i ,m ∈ M t   [1 , 2 , ··· ,M t − 1] . Similarly, the receive antenna position vector can be expressed as x r = [ x r, 0 ,x r, 1 , ··· ,x r,M r − 1 ] T , where x r, 0 = 0 and x r,m = λ 2 m,m ∈ M r . Accordingly, the steering vectors of the transmit and receive antenna arrays are respectively given by a ( x t ,α ) = [1 ,e j 2 π λ x t, 1 sin α , ··· ,e j 2 π λ x t,M t − 1 sin α ] T and b ( x r ,α ) = [1 ,e jπ sin α , ··· ,e jπ ( M r − 1) sin α ] T , where λ denotes the signal wavelength and α is the steering angle of the array.

Consider a target at (ˆ τ, ˆ v,θ ) , where ˆ τ denotes the delay corresponding to the target range, ˆ v is the Doppler frequency of the target and θ ∈ [ − π 2 , π 2 ] represents the direction angle of the target. Then, the received signal can be represented by

$$
+ n(t) , (1) @)ej2rôt
$$

where φ ( t ) = [ φ 0 ( t ) ,φ 1 ( t ) , ··· ,φ M t − 1 ( t )] T , n ( t ) = [ n 0 ( t ) ,n 1 ( t ) , ··· ,n M r − 1 ( t )] T , φ m ( t ) represents the FH waveform transmitted from the m -th transmit antenna and n m ( t ) denotes the Gaussian noise received by the m -th receive

As the FH waveform, the pulse width T w is divided into Q sub-pulses of width ∆ t = T w /Q each [35]. Therefore, the m -th FH waveform during each pulse can be further expressed as [8] Q − 1

# II. SIGNAL MODEL

# A. MA-Enabled FH-MIMO Radar System

As shown in Fig. 1, we consider an MA-enabled FHMIMO radar system equipped with a colocated transmitter and receiver, which are comprised of linear arrays with M t and M r antennas, respectively. Since the transmit antenna array is the primary factor that affects the ambiguity function, we assume that the transmit antennas are movable while the receive antenna positions are ﬁxed with half wavelength spacing for ease of analysis [8]. Each MA is attached to an electrical machinery, such that the interval between two adjacent antennas can be dynamically adjusted [26]. Let d t,i ( d r,i ) , 1 ≤ i ≤ M t − 1 (1 ≤ i ≤ M r − 1) denote the interval between the ( i − 1) -th and i -th transmit (receive) antenna and deﬁne d t, 0 = 0 , d r, 0 = 0 , d r,i = λ 2 ,i ∈ M r   [1 , 2 , ··· ,M r − 1] . Then, the transmit antenna position vector can be denoted by x t = [ x t, 0 ,x t, 1 , ··· ,x t,M t − 1 ] T , where

$$
@m (t) = 9=0
$$

where c m,q ∈ K is the FH code with K   { 1 , 2 , ··· ,K } being the set of available hops, ∆ f represents the frequency hopping interval and s ( t ) represents the pulse function which is deﬁned as 1 , 0 < t < ∆ ,

$$
0 < t < s(t) = (3 otherwise_ At ,
$$

Note that the waveforms in an FH-MIMO radar system are required to be orthogonal for zero Doppler and zero delay (see [8]), thus the condition c m,q   = c m ′ ,q , ∀ q,m   = m ′ must be satisﬁed during each sub-pulse that comprises the radar pulse. This implies that the transmit antenna number M t that can be employed is upper bounded by the hop number Q . In this paper, our main focus is to investigate the radar performance enhancement brought by MA, and the FH code is designed by adopting the method presented in [13].

