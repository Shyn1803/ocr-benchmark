4

being inspected at the same time. We then denote by Sm ⊂ S the subset of sensing regions inspected by transmit AP m, with S the complete set of all clusters such that |S| = S. On the contrary, receive APs are responsible for only detecting a single target within their sensing region.

During the tracking phase, the goal is to confirm the presence of already detected targets and update their parameters. In this case, transmit AP m tracks the detected targets within the subset Lm, and the receive AP focuses on one or more targets. Obviously, the network has no control over the position of the detected targets, and it can happen that close targets are to be tracked: mutual interference effects are thus to be properly taken into account. This is discussed further in Section IV.

III. SYSTEM MODEL

We now describe the proposed scalable ISAC-enabled CFmMIMO system model, focusing mainly on the sensing tasks: detection at positions pi, with i ∈ S, and tracking at positions pl, with l ∈ {1,...,L}. Assuming block fading channel and OFDM modulation, each coherence block consists of τc timefrequency samples during which channels and reflections are constant and flat. This way, t ∈ {1,...,τc} will denote the index for the symbols transmitted within a single coherence block to sense the positions pi (detection) or pl (tracking).

In that sense, hk,m (hHk,m) denotes the N-dimensional UL (DL)1 channel from UE k to AP m; Gm,m′ is the (N × N)dimensional matrix representing the channel from AP m′ ∈ Mtx to AP m ∈ Mrx; and Hp,m,m′ refers to the (N × N)dimensional matrix for the composite channel linking transmit AP m′ to receive AP m through the reflection from the target located in position p (either pi or pl).

A. Propagation Channels

Under the above assumptions, the N-dimensional UL channel from UE k to AP m is [23]

# hk,m ∼ CN(0,Ck,m), (1)

where Ck,m ∈ CN×N refers to the spatial correlation matrix of the Rayleigh-distributed non-line-of-sight (NLoS) components. The corresponding large-scale fading coefficient (LSF), which includes path loss, is tr(Ck,m)/N.

For the AP-AP link, we adopt a Rician modeling:

bm,m′ 1 + cm,m′

G ¯ m,m′ + √cm,m′ejψm,m′Vm,m′ ,

Gm,m′ =

(2) where bm,m′ is the LSF coefficient, cm,m′ is the Rician factor, G¯ m,m′ ∈ CN×N contains the correlated2 NLoS components such that g¯m,m′ = vec(G¯ m,m′) ∼ CN(0N2,Qm,m′), ψm,m′ ∼ U[0,2π] is the phase offset, and Vm,m′ ∈ CN×N is the equivalent array response at the LoS direction:

Vm,m′ = am (φm,m′,θm,m′)aHm′ (φm′,m,θm′,m), (3)

- 1We assume that system operations happen within one channel coherence interval, and that time-division-duplex (TDD) protocol is used, to ensure equivalence (reciprocity) of UL and DL channels.
- 2In line with [11], a popular choice for the channel covariance matrix


Qm,m′ is the well-known Kronecker model. However, we leave this unspecified until the simulations section to keep our analysis general.

with am(φm,m′,θm,m′) the response of the array (or steering vector) for the azimuth φm,m′ (φm′,m) and elevation θm,m′ (θm′,m) angles of arrival (departure) from AP m to AP m′. According to [24], the Rician factors can be defined as

pLoS (dm,m′) 1 − pLoS (dm,m′)

, (4)

cm,m′ =

where pLoS(dm,m′) is the LoS probability that depends on the distance dm,m′ between AP m and m′ [25, Table B.1.2.1-2].

Finally, assuming LoS propagation between the targets and

# the involved APs, a convenient expression for Hp,m,m′ is Hp,m,m′ = α˜p,m,m′ am (φm,p,θm,p)aHm′ (φm′,p,θm′,p)

# ,

Ap,m,m′

(5) where α˜p,m,m′ = αp,m,m′ βp,m,m′ is a complex scalar coefficient, with αp,m,m′ the target reflectivity, or radar crosssection (RCS), and βp,m,m′ the product of the path loss from transmit AP m′ to the target at position p and that from the target to receive AP m. As previously mentioned, we follow the Swerling-I model for the RCS, in which αp,m,m′ is kept constant over consecutive symbols within the coherence block [11]. Moreover, φm,p,θm,p are the azimuth and elevation angle of the position p with respect to (w.r.t.) the antenna array of AP m. A similar meaning have the quantities φm′,p and θm′,p w.r.t. AP m′.

- B. Uplink Channel Estimation

Assuming perfect CSI can be overly optimistic in many applications. In practice, obtaining such channel knowledge locally at the APs via UL orthogonal pilots is more realistic. This approach enables the characterization of the sufficient statistics of the channels [26].

A feasible option could be the minimum mean-square error

(MMSE) estimation [27, Subsection V-B]: hˆk,m =

1 τpη¯k

Λk,mφk,m, (6)

where Λk,m = τpη¯kCk,mΓ−k,m1 is the MMSE matrix, τp is the number of pilots, η¯k is the UL training power, and

Γk,m =

K j=1

τpη¯jCj,m πjHπk 2 + σm2 IL, (7)

denotes the covariance matrix of the least-squares observations φk,m ∈ CN providing sufficient statistics, i.e.,

φk,m =

K j=1

τpη¯jhj,mπjHπk + ωk,m, (8) with πk ∈ Cτ

p the sequence of pilots sent by UE k to estimate the channel, and ωk,m ∈ CN the equalized ambient noise with variance σω2 [23, Subsection II-B].

- C. Downlink Transmission Assuming to be in the DL transmission and sensing phase,


AP m ∈ Mtx sends data to the UEs in the set Km plus additional beams to first, detect the presence of potential targets within the surveillance area and later, track their location.

