# LoS Blockage in Pinching-Antenna Systems: Curse or Blessing?

Zhiguo Ding,

Abstract —This letter investigates the impact of line-of-sight (LoS) blockage on pinching-antenna systems. Analytical results are developed for both single-user and multi-user cases to reveal that the presence of LoS blockage is beneﬁcial for increasing the performance gain of pinching antennas over conventional antennas. This letter also reveals that LoS blockage is particularly useful in multi-user cases, where co-channel interference can be effectively suppressed by LoS blockage.

Index Terms —Pinching antennas, line-of-sight blockage, largescale path loss, multiple-input multiple-input systems.

# I. I NTRODUCTION

Pinching-antenna systems have recently been recognized as a promising transmission technique for next-generation mobile networks due to the following three features [1], [2]. The ﬁrst feature is their low costs since pinching antennas are simple dielectric particles, e.g., clothes pinches, applied on waveguides. The second feature is the capability of pinching antennas to create strong line-of-sight (LoS) connections between a base station and its user, e.g., it is possible to activate a pinching antenna right next to the user, and hence the path loss experienced by the user can be very small. The third feature is that the multi-input multi-output (MIMO) systems created by pinching antennas can be ﬂexibly reconﬁgured, e.g., adding (or removing) antennas becomes straightforward.

different conﬁgurations, e.g., different numbers of pinching antennas, users, and waveguides, have been identiﬁed in [3]. These obtained analytical results reveal that pinching antennas achieve a signiﬁcant performance gain over conventional antennas. In [4], a low-complexity implementation to activate pinching antennas, instead of moving them, was studied, and the array gain achieved by pinching-antenna systems has been identiﬁed in [5]. In addition, sophisticated resource allocation algorithms have been developed for uplink and downlink transmissions in pinching-antenna systems [6] and [7], respectively.

Recall   that one of the key features   of pinching  antennas is to reduce the transceiver   distance, which means   that in pinching-antenna systems, a user experiences less large-scale loss and LoS blockage; compared to conventional antenna systems .  However, in the  literature, no study   that formally   investigated   the impact   of   pinching antennas on LoS blockage; which motivates   this   letter. The contribution of   this   letter is   two-fold. One is to focus on the   singleuser special  case, where analytical   results are developed to analyze the outage probability achieved by pinching antennas. intuition that   the   presence of   LoS   blockage is beneficial for   increasing   the   performance of   pinching antennas over conventional antennas,   compared to the case without path gain blockage. The second contribution focuses on a general multi user scenario. For conventional antenna systems, the existence of strong co-channel interference severely degrades the performance.  The presence of LoS blockage makes it more difficult to combat co-channel interference   since the LoS blockage can make a user's channel matrix no longer full rank, and hence, interference cancellation methods, such as zero-forcing approaches; become not applicable. However; in pinching-antenna systems, LoS blockage becomes blessing since user'$ interference   link is   likely to be   subject to blockage since the corresponding interfering pinching antenna could be far away from the user. This intuition is confirmed by the presented analytical  results, which show that the ergodic data rate of pinching antennas over conventional antennas is unbounded at high signal-to-noise ratio (SNR). system many gain

Z. Ding is with the University of Manchester, Manchester, M1 9BB, UK, and Khalifa University, Abu Dhabi, UAE. H. V. Poor is with the Department of Electrical and Computer Engineering, Princeton University, Princeton, NJ 08544, USA.

# II. S YSTEM M ODEL

Consider a downlink pinching-antenna system with M single-antenna users, denoted by U m , in a rectangular-shaped service area, denoted by A , whose two sides are denoted by D W and D L . Assume that the service area is divided by M parallelly installed waveguides into M identical rectangles with sides being D W M and D L . To facilitate the performance analysis, assume that U m is uniformly distributed in the rectangle centered by the m -th waveguide, and U m ’s location is denoted by ψ m = ( x m ,y m , 0) . It is further assumed that a single pinching antenna is activated on the m -th waveguide at the location closest to U m , and hence its location can be denoted by ψ Pin m = ( x m ,β m ,d ) , where d denotes the height of the waveguide and β m = − D W 2 + ( m − 1) D W M + D W 2 M . Similar to [3], U m ’s observation is given by

Similar to [3], Um 's observation is given by

$$
M Um Psm + Psi + k=1 hmkPmk
$$

where ˜ h mk = α mk h mk , h mk denotes the channel gain between the k -th antenna and U m , i.e., h mk = √ ηe − 2 πj   1 λ | ψ m − ψ Pin k | + 1 λ g | ψ Pin 0 − ψ Pin k |   | ψ m − ψ Pin k | , the overall transmit power budget is denoted by P , p mk is the precoding coefﬁcient, λ and λ g denote the carrier and waveguide wavelengths, respectively, η = c 2 16 π 2 f 2 c , c is the speed of light, the carrier frequency is denoted by f c , w m denotes the additive noise with power σ 2 , s m denotes U m ’s signal, and α mk is an indicator function for the LoS blockage. In particular, if there is LoS blockage between the pinching antenna on the k -th waveguide and U m , α mk = 0 . Otherwise, α mk = 1 . In general, LoS blockage can be modeled as follows: [8]

$$
= 1) = P(amk
$$

and for ultra-dense indoor environments, the following LoS blockage model can also be used: [9]

$$
P(amk = 1) = (3)
$$

