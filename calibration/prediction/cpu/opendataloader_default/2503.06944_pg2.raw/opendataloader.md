![](<2503.06944_pg2_images/imageFile1.png>)

RIS controller

1 2 ... Mt

Ht

Hr

Hd

RIS

- 1
- 2


N reflecting elements

...

Mr

Downlink

User

BS

Fig. 1. An RIS-assisted point-to-point MIMO communication system.

predesigned codebook for RIS-assisted point-to-point MIMO communications. In contrast to the direct codeword selection from the predesigned codebook, the proposed scheme designs a set of weights for each codeword in the codebook according to the corresponding output results, yielding a new RIS RC vector. For illustration, we contrast the proposed scheme to its existing channel estimation, passive beamforming and predesigned codebook counterparts in Table I. The simulation results demonstrate that the proposed scheme has improved performance compared to existing passive beamforming and codebook schemes.

II. SYSTEM MODEL

We consider an RIS-assisted point-to-point MIMO system in a single cell as shown in Fig. 1, where a base station (BS) with Mt transmit antennas sends Ms data streams to a user with Mr antennas, with Ms ≤ min{Mt,Mr}. The RIS consists of N reﬂecting elements and is equipped with a smart controller capable of adjusting the RCs according to instructions from the BS. The signals from both the cascaded BS-RIS-user link and the direct BS-user link are superimposed at the user. We assume that the frequency-ﬂat baseband equivalent channels spanning from the BS to the RIS, from the RIS to the user, and from the BS to the user are denoted by Ht ∈ CN×Mt

,Hr ∈ CMr×N and Hd ∈ CMr×Mt, respectively.

Let ϕ = [ϕ1,ϕ2,··· ,ϕN]T represent the RIS RC vector, where ϕn = ejθ

denotes the RC of the nth RIS element with phase shift θn, satisfying θn ∈ [0,2π) for n = 1,2,··· ,N. Thus the composite end-to-end channel He ∈ CMr×Mt from the BS to the user can be expressed as

n

He = Hd + Hrdiag(ϕ)Ht. (1) During the channel training process in the uplink phase, the

]T ∈ CMr×τ

user sends the pilot signal X = [x1,x2,··· ,xM

r

to the BS, where xTm ∈ C1×τ,m = 1,2,··· ,Mr is the pilot loaded on the mth antenna at the user. The pilot matrix satisﬁes

X 2F = τpu, where pu is the average pilot power. As we consider a time-division duplexing protocol for both uplink as well as downlink transmissions and assume the channel’s reciprocity, the pilot signal received at the BS is given by

Y = HHe X + NBS, (2)

where NBS ∈ CMt×τ denotes the noise matrix at the BS with an average noise power of σBS2 , whose ith column vector follows nBS,i ∼ CN 0M

,σBS2 IM

, for i = 1,2,··· ,τ. We employ mutually orthogonal pilots, and the length of the pilot signal is designed such that τ ≥ Mr [12].

t

t

Next, we consider the downlink of data transmission where the BS applies a baseband precoder W ∈ CMt×Ms to transmit symbol s ∈ CMs×1, with E ssH = IM

. Furthermore, the

s

precoder satisﬁes W 2F ≤ pd and pd is the total transmit power at the BS. Thus the received signal at the user is obtained as

r = HeWs + nUE, (3) where nUE ∈ CMr×1 is the noise at the user with an average noise power of σUE2 , satisfying nUE ∼ CN 0M

,σUE2 IM

.

r

r

Meanwhile, we adopt the Rician channel in this paper. Speciﬁcally, the RIS-user channel can be expressed as

![](<2503.06944_pg2_images/imageFile2.png>)

![](<2503.06944_pg2_images/imageFile3.png>)

Fr Fr + 1

1 Fr + 1

![](<2503.06944_pg2_images/imageFile4.png>)

HLoSr +

HNLoSr , (4)

Hr = βr

![](<2503.06944_pg2_images/imageFile5.png>)

![](<2503.06944_pg2_images/imageFile6.png>)

where βr and Fr are the path loss and the Rician factor of RIS-user channel, respectively; HLoSr ∈ CMr×N and HNLoSr ∈ CMr×N represent the line-of-sight (LoS) and the non-line-of-sight (NLoS) components of the RIS-user channel, respectively. The element on the mrth row and the nth column of the NLoS matrix is modeled by Rayleigh fading, which follows HNLoSr m

r,n ∼ CN (0,1). Similarly, the BS-user channel and BS-RIS channel can be modeled by using (4).

Moreover, we consider a uniform linear array (ULA) at the BS, a ULA at the user, and a uniform planar array (UPA) at the RIS. Let aBS (δ) ∈ CMt×1, aUE (δ) ∈ CMr×1 and aR (ζ,γ) ∈ CN×1 denote the steering vector of the BS, the user and the RIS, respectively. Speciﬁcally, the mtth entry of aBS is denoted as ej2λπ(mt−1)dBS sin(δ),mt = 1,2,··· ,Mt, where dBS denotes the element spacing of the BS, λ denotes the signal wavelength, and δ ∈ [−π/2,π/2) denotes the angle of departure (AoD) or the angle of arrival (AoA). Similarly, the mrth entry of aUE is denoted as ej2λπ(mr−1)dUE sin(δ),mr = 1,2,··· ,Mr, where dUE denotes the element spacing of the user. The nth entry of aR is denoted as ej2πd

![](<2503.06944_pg2_images/imageFile7.png>)

![](<2503.06944_pg2_images/imageFile8.png>)

R sin(γ)[⌊nN−x1⌋sin(ζ)+((n−1)−⌊nN−x1⌋Nx) cos(ζ)]/λ,n = 1,2,··· ,N, where dR denotes the element spacing of the RIS. Nx is the number of elements deployed at each row of the RIS. ζ ∈ [0,π) and γ ∈ [−π/2,π/2) denote the azimuth and elevation AoA/AoD, respectively. Thus, the LoS component of the

![](<2503.06944_pg2_images/imageFile9.png>)

![](<2503.06944_pg2_images/imageFile10.png>)

Ht, Hr and Hd are given by aR ζtAoA,γtAoA aBS δtAoD H, aUE δrAoA aR ζrAoD,γrAoD H and aUE δdAoA aBS δdAoD H, respectively, where δtAoD, ζtAoA and γtAoA represent the AoD, the azimuth and elevation AoA from the BS to the RIS, respectively; δrAoA, ζrAoD and γrAoD represent the AoA, the azimuth and elevation AoD from the RIS to the user, respectively; δdAoA and δdAoD represent the AoA and the AoD from the BS to the user, respectively.

In the next section, unlike traditional passive beamforming and codebook schemes, the proposed scheme maximizes the channel capacity of the point-to-point MIMO systems by

