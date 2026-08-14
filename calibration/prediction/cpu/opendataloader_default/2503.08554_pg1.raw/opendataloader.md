# LoS Blockage in Pinching-Antenna Systems: Curse or Blessing?

Zhiguo Ding, Fellow, IEEE, and H. Vincent Poor, Life Fellow, IEEE

1

arXiv:2503.08554v1 [cs.IT] 11 Mar 2025

Abstract—This letter investigates the impact of line-of-sight (LoS) blockage on pinching-antenna systems. Analytical results are developed for both single-user and multi-user cases to reveal that the presence of LoS blockage is beneﬁcial for increasing the performance gain of pinching antennas over conventional antennas. This letter also reveals that LoS blockage is particularly useful in multi-user cases, where co-channel interference can be effectively suppressed by LoS blockage.

Index Terms—Pinching antennas, line-of-sight blockage, largescale path loss, multiple-input multiple-input systems.

I. INTRODUCTION

Pinching-antenna systems have recently been recognized as a promising transmission technique for next-generation mobile networks due to the following three features [1], [2]. The ﬁrst feature is their low costs since pinching antennas are simple dielectric particles, e.g., clothes pinches, applied on waveguides. The second feature is the capability of pinching antennas to create strong line-of-sight (LoS) connections between a base station and its user, e.g., it is possible to activate a pinching antenna right next to the user, and hence the path loss experienced by the user can be very small. The third feature is that the multi-input multi-output (MIMO) systems created by pinching antennas can be ﬂexibly reconﬁgured, e.g., adding (or removing) antennas becomes straightforward.

The fundamental limits of pinching-antenna systems with different conﬁgurations, e.g., different numbers of pinching antennas, users, and waveguides, have been identiﬁed in [3]. These obtained analytical results reveal that pinching antennas achieve a signiﬁcant performance gain over conventional antennas. In [4], a low-complexity implementation to activate pinching antennas, instead of moving them, was studied, and the array gain achieved by pinching-antenna systems has been identiﬁed in [5]. In addition, sophisticated resource allocation algorithms have been developed for uplink and downlink transmissions in pinching-antenna systems [6] and [7], respectively.

Recall that one of the key features of pinching antennas is to reduce the transceiver distance, which means that in pinching-antenna systems, a user experiences less large-scale path loss and LoS blockage, compared to conventional antenna systems. However, in the literature, there is no study that formally investigated the impact of pinching antennas on LoS blockage, which motivates this letter. The contribution of this letter is two-fold. One is to focus on the singleuser special case, where analytical results are developed to analyze the outage probability achieved by pinching antennas. The presented analytical and simulation results conﬁrm the intuition that the presence of LoS blockage is beneﬁcial for increasing the performance gain of pinching antennas over conventional antennas, compared to the case without

Z. Ding is with the University of Manchester, Manchester, M1 9BB, UK, and Khalifa University, Abu Dhabi, UAE. H. V. Poor is with the Department of Electrical and Computer Engineering, Princeton University, Princeton, NJ 08544, USA.

blockage. The second contribution focuses on a general multiuser scenario. For conventional antenna systems, the existence of strong co-channel interference severely degrades the system performance. The presence of LoS blockage makes it more difﬁcult to combat co-channel interference since the LoS blockage can make a user’s channel matrix no longer full rank, and hence, many interference cancellation methods, such as zero-forcing approaches, become not applicable. However, in pinching-antenna systems, LoS blockage becomes a blessing since a user’s interference link is likely to be subject to blockage since the corresponding interfering pinching antenna could be far away from the user. This intuition is conﬁrmed by the presented analytical results, which show that the ergodic data rate gain of pinching antennas over conventional antennas is unbounded at a high signal-to-noise ratio (SNR).

II. SYSTEM MODEL

Consider a downlink pinching-antenna system with M single-antenna users, denoted by Um, in a rectangular-shaped service area, denoted by A, whose two sides are denoted by DW and DL. Assume that the service area is divided by M parallelly installed waveguides into M identical rectangles with sides being D

M and DL. To facilitate the performance analysis, assume that Um is uniformly distributed in the rectangle centered by the m-th waveguide, and Um’s location is denoted by ψm = (xm,ym,0). It is further assumed that a single pinching antenna is activated on the m-th waveguide at the location closest to Um, and hence its location can be denoted by ψmPin = (xm,βm,d), where d denotes the height of the waveguide and βm = −D

W

![](<2503.08554_pg1_images/imageFile1.png>)

2 + (m − 1)D

M + D

2M . Similar to [3], Um’s observation is given by

W

W

W

![](<2503.08554_pg1_images/imageFile2.png>)

![](<2503.08554_pg1_images/imageFile3.png>)

![](<2503.08554_pg1_images/imageFile4.png>)

M

h˜mkpmk

ym =

k=1

√

![](<2503.08554_pg1_images/imageFile5.png>)

Psm +

i =m

M

h˜mkpik

k=1

√

![](<2503.08554_pg1_images/imageFile6.png>)

Psi + wm, (1)

where ˜hmk = αmkhmk, hmk denotes the channel gain between the k-th antenna and Um, i.e., hmk = √ηe−2πj

λg |

k | |ψm−ψkPin|

λ|

k |

ψPin

0 −ψPin

ψm−ψPin

+ 1

1

![](<2503.08554_pg1_images/imageFile7.png>)

![](<2503.08554_pg1_images/imageFile8.png>)

![](<2503.08554_pg1_images/imageFile9.png>)

, the overall transmit

![](<2503.08554_pg1_images/imageFile10.png>)

power budget is denoted by P, pmk is the precoding coefﬁcient, λ and λg denote the carrier and waveguide wavelengths, respectively, η = c

2

16π2fc2, c is the speed of light, the carrier frequency is denoted by fc, wm denotes the additive noise with power σ2, sm denotes Um’s signal, and αmk is an indicator function for the LoS blockage. In particular, if there is LoS blockage between the pinching antenna on the k-th waveguide and Um, αmk = 0. Otherwise, αmk = 1. In general, LoS blockage can be modeled as follows: [8]

![](<2503.08554_pg1_images/imageFile11.png>)

Pin

P(αmk = 1) = e−φ|ψ

i −ψm|, (2)

and for ultra-dense indoor environments, the following LoS blockage model can also be used: [9]

i −ψm|2, (3)

Pin

P(αmk = 1) = e−φ|ψ

