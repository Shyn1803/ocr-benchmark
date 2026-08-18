2

M

![](<2503.06944_pg2_images/imageFile1.png>)

RIS controller

H,

H r

2

M r

User

RIS

N reflecting elements

Downlink

Fig. 1. An RIS-assisted point-to-point MIMO communication system. predesigned codebook for RIS-assisted point-to-point MIMO communications. In contrast to the direct codeword selection from the predesigned codebook, the proposed scheme designs a set of weights for each codeword in the codebook according to the corresponding output results, yielding a new RIS RC vector. For illustration, we contrast the proposed scheme to its existing channel estimation, passive beamforming and predesigned codebook counterparts in Table I. The simulation results demonstrate that the proposed scheme has improved performance compared to existing passive beamforming and codebook schemes.

# II. S YSTEM M ODEL

We consider an RIS-assisted point-to-point MIMO system in a single cell as shown in Fig. 1, where a base station (BS) with M t transmit antennas sends M s data streams to a user with M r antennas, with M s ≤ min { M t ,M r } . The RIS consists of N reﬂecting elements and is equipped with a smart controller capable of adjusting the RCs according to instructions from the BS. The signals from both the cascaded BS-RIS-user link and the direct BS-user link are superimposed at the user. We assume that the frequency-ﬂat baseband equivalent channels spanning from the BS to the RIS, from the RIS to the user, and from the BS to the user are denoted by H t ∈ C N × M t , H r ∈ C M r × N and H d ∈ C M r × M t , respectively. T

Let ϕ = [ ϕ 1 ,ϕ 2 , ··· ,ϕ N ] represent the RIS RC vector, where ϕ n = e jθ n denotes the RC of the n th RIS element with phase shift θ n , satisfying θ n ∈ [0 , 2 π ) for n = 1 , 2 , ··· ,N . Thus the composite end-to-end channel H e ∈ C M r × M t from the BS to the user can be expressed as

$$

$$

During the channel training process in the uplink phase, the user sends the pilot signal X = [ x 1 , x 2 , ··· , x M r ] T ∈ C M r × τ to the BS, where x T m ∈ C 1 × τ ,m = 1 , 2 , ··· ,M r is the pilot loaded on the m th antenna at the user. The pilot matrix satisﬁes   X   2 F = τp u , where p u is the average pilot power. As we consider a time-division duplexing protocol for both uplink as well as downlink transmissions and assume the channel’s reciprocity, the pilot signal received at the BS is given by H

$$
Y = HHX + NBS , (2)
$$

where N BS ∈ C M t × τ denotes the noise matrix at the BS with an average noise power of σ 2 BS , whose i th column vector follows n BS ,i ∼ CN   0 M t ,σ 2 BS I M t   , for i = 1 , 2 , ··· ,τ . We employ mutually orthogonal pilots, and the length of the pilot τ ≥ M

r Next, we consider the downlink of data transmission where the BS applies a baseband precoder W ∈ C M t × M s to transmit symbol s ∈ C M s × 1 , with E   ss H   = I M s . Furthermore, the precoder satisﬁes   W   2 F ≤ p d and p d is the total transmit power at the BS. Thus the received signal at the user is obtained as

$$
r = HeWs + (3 nUE ,
$$

where n UE ∈ C M r × 1 is the noise at the user with an average 2 n 0 2 I

UE UE   M r UE M Meanwhile, we adopt the Rician channel in this Speciﬁcally, the RIS-user channel can be expressed as

$$
Fr Hr VBr HLoS Fr + 1 Fr + 1 HNLoS
$$

where β r and F r are the path loss and the Rician factor of RIS-user channel, respectively; H LoS r ∈ C M r × N and H NLoS r ∈ C M r × N represent the line-of-sight (LoS) and the non-line-of-sight (NLoS) components of the RIS-user channel, respectively. The element on the m r th row and the n th column of the NLoS matrix is modeled by Rayleigh fading, which follows H NLoS r m r ,n ∼ CN (0 , 1) . Similarly, the BS-user channel and BS-RIS channel can be modeled by using (4).

Moreover, we consider a uniform linear array (ULA) at the BS, a ULA at the user, and a uniform planar array (UPA) at the RIS. Let a BS ( δ ) ∈ C M t × 1 , a UE ( δ ) ∈ C M r × 1 and a R ( ζ,γ ) ∈ C N × 1 denote the steering vector of the BS, the user and the RIS, respectively. Speciﬁcally, the m t th entry of a BS is denoted as e j 2 π λ ( m t − 1) d BS sin( δ ) ,m t = 1 , 2 , ··· ,M t , where d BS denotes the element spacing of the BS, λ denotes the signal wavelength, and δ ∈ [ − π/ 2 ,π/ 2) denotes the angle of departure (AoD) or the angle of arrival (AoA). Similarly, the m r th entry of a UE is denoted as e j 2 π λ ( m r − 1) d UE sin( δ ) ,m r = 1 , 2 , ··· ,M r , where d UE denotes the element spacing of the user. The n th entry of a R is denoted as e j 2 πd R sin( γ ) [ ⌊ n − 1 N x ⌋ sin( ζ )+(( n − 1) −⌊ n − 1 N x ⌋ N x ) cos( ζ ) ] /λ ,n = 1 , 2 , ··· ,N , where d R denotes the element spacing of the RIS. N x is the number of elements deployed at each row of the RIS. ζ ∈ [0 ,π ) and γ ∈ [ − π/ 2 ,π/ 2) denote the azimuth and elevation AoA/AoD, respectively. Thus, the LoS component of the H t , H r and H d are given by a R   ζ AoA t ,γ AoA t   a BS   δ AoD t   H , a UE   δ AoA r   a R   ζ AoD r ,γ AoD r   H and a UE   δ AoA d   a BS   δ AoD d   H , respectively, where δ AoD t , ζ AoA t and γ AoA t represent the AoD, the azimuth and elevation AoA from the BS to the RIS, respectively; δ AoA r , ζ AoD r and γ AoD r represent the AoA, the azimuth and elevation AoD from the RIS to the user, respectively; δ AoA d and δ AoD d represent the AoA and the AoD from the BS to the user, respectively.

In the next section, unlike traditional passive beamforming and codebook schemes, the proposed scheme maximizes the channel capacity of the point-to-point MIMO systems by

