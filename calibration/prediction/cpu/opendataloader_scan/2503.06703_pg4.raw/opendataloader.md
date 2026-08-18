being inspected at the same time. We then denote by S m ⊂ S the subset of sensing regions inspected by transmit AP m , with S the complete set of all clusters such that |S| = S . On the contrary, receive APs are responsible for only detecting a single target within their sensing region. During the tracking phase, the goal is to confirm the pres-

ence of already detected targets and update their parameters. In this case, transmit AP m tracks the detected targets within the subset L m , and the receive AP focuses on one or more targets. Obviously, the network has no control over the position of the detected targets, and it can happen that close targets are to be tracked: mutual interference effects are thus to be properly taken into account. This is discussed further in Section IV.

θ m ′ ,m m m According to [24], the Rician factors can be defined as

$$
Cm,m' PLoS (dmsm' 1 PLoS (dm,m'
$$

where p LoS ( d m,m ′ ) is the LoS probability that depends on the distance d m,m ′ between AP m and m ′ [25, Table B.1.2.1-2]. Finally, assuming LoS propagation between the targets and

Finally; assuming LoS propagation between the targets and the involved a convenient expression for Hp,m,' APs,

$$
(Pm,P; Hp,m,m' 0m,P am
$$

# III. S YSTEM M ODEL

We now describe the proposed scalable ISAC-enabled CFmMIMO system model, focusing mainly on the sensing tasks: detection at positions p i , with i ∈ S , and tracking at positions p l , with l ∈ { 1 ,...,L } . Assuming block fading channel and OFDM modulation, each coherence block consists of τ c timefrequency samples during which channels and reflections are constant and flat. This way, t ∈ { 1 ,...,τ c } will denote the index for the symbols transmitted within a single coherence block to sense the positions p i (detection) or p l (tracking). H

In that sense, h k,m ( h k,m ) denotes the N -dimensional UL (DL) 1 channel from UE k to AP m ; G m,m ′ is the ( N × N ) dimensional matrix representing the channel from AP m ′ ∈ M tx to AP m ∈ M rx ; and H p ,m,m ′ refers to the ( N × N ) dimensional matrix for the composite channel linking transmit AP m ′ to receive AP m through the reflection from the target located in position p (either p i or p l ).

# Propagation Channels

Under the above assumptions, the N -dimensional UL channel from UE k to AP m is [23]

$$
~ CN(0, Ck,m) , hk,m
$$

where C k,m ∈ C N × N refers to the spatial correlation matrix of the Rayleigh-distributed non-line-of-sight (NLoS) components. The corresponding large-scale fading coefficient (LSF), which includes path loss, is tr( C k,m ) /N . For the AP-AP link, we adopt a Rician modeling:

For the AP-AP link, we Rician modeling: adopt

$$
(Gm,m' Vcm,m'ejum,m Vm,m' 1 + Cm,m' (2) bm.m Gm,m'
$$

where b m,m ′ is the LSF coefficient, c m,m ′ is the Rician factor, ¯ G m,m ′ ∈ C N × N contains the correlated 2 NLoS components such that ¯ g m,m ′ = vec( ¯ G m,m ′ ) ∼ CN ( 0 N 2 , Q m,m ′ ) , ψ m,m ′ ∼ U [0 , 2 π ] is the phase offset, and V m,m ′ ∈ C N × N is the equivalent array response at the LoS direction:

$$
H m,mn am ,m , 0m' ,m) (3) (Pm,m' @m,m' am'
$$

1 We assume that system operations happen within one channel coherence interval, and that time-division-duplex (TDD) protocol is used, to ensure equivalence (reciprocity) of UL and DL channels. 2 In line with [11], a popular choice for the channel covariance matrix

2In   line with [11], popular   choice for  the channel covariance   matrix Qm_ is the well-known Kronecker   model. However; we leave this un m specified until the simulations section to our analysis general. keep with am the response of the array (or steering vector) for the azimuth Pm,m' m and elevation angles of arrival (departure) from AP m to AP m' (Pm' (@m'_

where ˜ α p ,m,m ′ = α p ,m,m ′   β p ,m,m ′ is a complex scalar coefficient, with α p ,m,m ′ the target reflectivity, or radar crosssection (RCS), and β p ,m,m ′ the product of the path loss from transmit AP m ′ to the target at position p and that from the target to receive AP m . As previously mentioned, we follow the Swerling-I model for the RCS, in which α p ,m,m ′ is kept constant over consecutive symbols within the coherence block [11]. Moreover, φ m, p ,θ m, p are the azimuth and elevation angle of the position p with respect to (w.r.t.) the antenna array of AP m . A similar meaning have the quantities φ m ′ , p and θ m ′ , p w.r.t. AP m ′ .

# Uplink Channel Estimation

Assuming perfect CSI can be overly optimistic in many applications. In practice, obtaining such channel knowledge locally at the APs via UL orthogonal pilots is more realistic. This approach enables the characterization of the sufficient statistics of the channels [26].

A feasible option could be the minimum mean-square error (MMSE) estimation [27, Subsection V-B]:

$$
= VTpnlk hk,m Ak,m
$$

where number of pilots, 7Jk is the UL training power; and Ak,m

$$
K + 0? Zjz1
$$

    denotes the covariance matrix of the least-squares observations φ k,m ∈ C N providing sufficient statistics, i.e.,

$$
(8) Pk,m 'j=1 Wk,m ;
$$

with π k ∈ C τ p the sequence of pilots sent by UE k to estimate the channel, and ω k,m ∈ C N the equalized ambient noise with variance σ 2 ω [23, Subsection II-B].

# C. Downlink Transmission

Assuming to be in the DL transmission and sensing phase, AP m ∈ M tx sends data to the UEs in the set K m plus additional beams to first, detect the presence of potential targets within the surveillance area and later, track their location.

