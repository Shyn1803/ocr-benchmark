3

![](<2503.04407_pg3_images/imageFile1.png>)

<table>
  <tr>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td> </td>
    <td colspan="2"> </td>
    <td> </td>
    <td colspan="2"> </td>
    <td> </td>
    <td colspan="2"> </td>
    <td> </td>
  </tr>
  <tr>
    <td colspan="8">M M Movable Antennas M<br><br></td>
    <td colspan="3"> </td>
    <td colspan="3">Fixed Antennas</td>
    <td colspan="2"> </td>
  </tr>
</table>


RF Chain RF Chain RF Chain RF Chain RF Chain

RF Chain

Radar Signal Processing

Radar Signal Processing

Transmitter Receiver

Fig. 1. Proposed MA-enabled FH-MIMO radar system.

achieve improved performance in various tasks, e.g., if better resolution of target angles (velocity or distance) is required, the antenna positions can be adjusted to improve the performance of the ambiguity function in the angular (Doppler or delay) domain.

The remainder of this paper is organized as follows. Section II describes the considered MA-enabled FH-MIMO radar system model and the corresponding ambiguity function. In Section III, we analyze the relationship between the ambiguity function and the antenna positions. In Section IV, we propose a low complexity algorithm to solve the antenna position optimization problem. Section V provides the numerical results and discussions. Finally, we conclude this paper in Section VI.

Notations: Scalars, vectors and matrices are respectively denoted by lower/upper case, boldface lower case and boldface upper case letters. For an arbitrary matrix A, AT, A∗ and AH denote its transpose, conjugate and conjugate transpose respectively. · denotes the Euclidean norm of a complex vector, and |·| denotes the absolute value of a complex scalar. ⌈·⌉ represents the round-up operator. For a complex number x, ℜ{x} denotes its real part and ∠x denotes its angle. I and 0 denote an identity matrix and an all-zero vector with appropriate dimensions, respectively. Cn×m denotes the space of n × m complex matrices.

II. SIGNAL MODEL A. MA-Enabled FH-MIMO Radar System

As shown in Fig. 1, we consider an MA-enabled FHMIMO radar system equipped with a colocated transmitter and receiver, which are comprised of linear arrays with Mt and Mr antennas, respectively. Since the transmit antenna array is the primary factor that affects the ambiguity function, we assume that the transmit antennas are movable while the receive antenna positions are ﬁxed with half wavelength spacing for ease of analysis [8]. Each MA is attached to an electrical machinery, such that the interval between two adjacent antennas can be dynamically adjusted [26]. Let dt,i (dr,i), 1 ≤ i ≤ Mt − 1 (1 ≤ i ≤ Mr − 1) denote the interval between the (i − 1)-th and i-th transmit (receive) antenna and deﬁne dt,0 = 0, dr,0 = 0, dr,i = λ2,i ∈ Mr

![](<2503.04407_pg3_images/imageFile2.png>)

[1,2,··· ,Mr − 1]. Then, the transmit antenna position vector can be denoted by xt = [xt,0,xt,1,··· ,xt,M

t−1]T, where

xt,0 = 0 and xt,m = mi=0 dt,i,m ∈ Mt [1,2,··· ,Mt−1]. Similarly, the receive antenna position vector can be expressed

r−1]T, where xr,0 = 0 and

as xr = [xr,0,xr,1,··· ,xr,M

xr,m = λ2m,m ∈ Mr. Accordingly, the steering vectors of the transmit and receive antenna arrays are respectively

![](<2503.04407_pg3_images/imageFile3.png>)

given by a(xt,α) = [1,ej2λπxt,1 sinα,··· ,ej2λπxt,Mt−1 sinα]T and b(xr,α) = [1,ejπsinα,··· ,ejπ(M

![](<2503.04407_pg3_images/imageFile4.png>)

![](<2503.04407_pg3_images/imageFile5.png>)

r−1) sinα]T, where λ denotes the signal wavelength and α is the steering angle of the array.

Consider a target at (ˆτ,v,θˆ ), where τˆ denotes the delay corresponding to the target range, vˆ is the Doppler frequency of the target and θ ∈ [−π2, π2] represents the direction angle of the target. Then, the received signal can be represented by

![](<2503.04407_pg3_images/imageFile6.png>)

![](<2503.04407_pg3_images/imageFile7.png>)

yτ,ˆ v,θˆ (t) = a(xt, θ)Tφ(t − τˆ)b(xr, θ)ej2πvtˆ + n(t), (1)

t−1(t)]T, n(t) = [n0(t),n1(t),··· ,nM

where φ(t) = [φ0(t),φ1(t),··· ,φM

r−1(t)]T, φm(t) represents the FH waveform transmitted from the m-th transmit antenna and nm(t) denotes the Gaussian noise received by the m-th receive antenna.

As the FH waveform, the pulse width Tw is divided into Q sub-pulses of width ∆t = Tw/Q each [35]. Therefore, the m-th FH waveform during each pulse can be further expressed as [8]

Q−1

ej2πcm,q∆fts(t − q∆t), (2)

φm(t) =

q=0

where cm,q ∈ K is the FH code with K {1,2,··· ,K} being the set of available hops, ∆f represents the frequency hopping interval and s(t) represents the pulse function which is deﬁned as

1, 0 < t < ∆t, 0, otherwise.

s(t) =

(3)

Note that the waveforms in an FH-MIMO radar system are required to be orthogonal for zero Doppler and zero delay (see [8]), thus the condition cm,q = cm′,q,∀q,m = m′ must be satisﬁed during each sub-pulse that comprises the radar pulse. This implies that the transmit antenna number Mt that can be employed is upper bounded by the hop number Q. In this paper, our main focus is to investigate the radar performance enhancement brought by MA, and the FH code is designed by adopting the method presented in [13].

