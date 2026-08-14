arXiv:2503.06205v1 [math.AP] 8 Mar 2025

THE INITIAL-TO-FINAL-STATE INVERSE PROBLEM WITH TIME-INDEPENDENT POTENTIALS

MANUEL CANIZARES,˜ PEDRO CARO, IOANNIS PARISSIS, AND THANASIS ZACHAROPOULOS

Abstract. The initial-to-ﬁnal-state inverse problem consists in determining a quantum Hamiltonian assuming the knowledge of the state of the system at some ﬁxed time, for every initial state. This problem was formulated by Caro and Ruiz and motivated by the data-driven prediction problem in quantum mechanics. Caro and Ruiz analysed the question of uniqueness for Hamiltonians of the form ´∆ ` V with an electric potential V “ V pt, xq that depends on the time and space variables. In this context, they proved that uniqueness holds in dimension n ě 2 whenever the potentials are bounded and have super-exponential decay at inﬁnity. Although their result does not seem to be optimal, one would expect at least some degree of exponential decay to be necessary for the potentials. However, in this paper, we show that by restricting the analysis to Hamiltonians with time-independent electric potentials, namely V “ V pxq, uniqueness can be established for bounded integrable potentials exhibiting only super-linear decay at inﬁnity, in any dimension n ě 2. This surprising improvement is possible because, unlike Caro and Ruiz’s approach, our argument avoids the use of complex geometrical optics (CGO). Instead, we rely on the construction of stationary states at diﬀerent energies—this is possible because the potential does not depend on time. These states will have an explicit leading term, given by a Herglotz wave, plus a correction term that will vanish as the energy grows. Besides the signiﬁcant relaxation of decay assumptions on the potential, the avoidance of CGO solutions is important in its own right, since such solutions are not readily available in more complicated geometric settings.

1. Introduction

In quantum mechanics, the family of wave functions tupt,‚q : t P r0,Tsu describes the state of the system during an interval of time r0,Ts. If the motion takes place only under the inﬂuence of an electric potential V and the initial state up0,‚q is prescribed by f, then states

u : pt,xq P r0,Ts ˆ Rn ÞÑ upt,xq P C are solutions of the initial-value problem for the Schr¨odinger equation

(1) #iBtu “ ´∆u ` V u in p0,Tq ˆ Rn, up0,‚q “ f in Rn.

It is a well known fact that, if V P L1pp0,Tq;L8pRnqq, then for every f P L2pRnq there exists a unique u P Cpr0,Ts;L2pRnqq solving (1). Moreover, the linear map f P L2pRnq ÞÑ u P Cpr0,Ts;L2pRnqq is bounded. The solutions with the previous properties will be referred to as physical.

Using the physical solutions associated to a potential V , Caro and Ruiz formulated in [9] an inverse problem consisting in determining the electric potential from data measured only at the initial and ﬁnal times. These data were modelled by the initial-to-ﬁnal-state map, which is deﬁned by

UT : f P L2pRnq ÞÑ upT,‚q P L2pRnq, where u is the solution of the problem (1). This mapping is bounded in L2pRnq. In [9], Caro and Ruiz proved that UT uniquely determines the potential V “ V pt,xq in dimension n ě 2 whenever V P L1pp0,Tq;L8pRnqq has super-exponential decay, that is, eρ|x|V P L8pp0,Tq ˆ Rnq for all ρ ą 0. The reason that explains why the super-exponential decay was needed in [9] is the use of a family of solutions, usually called complex geometrical optics (CGO) solutions, that grow exponentially at inﬁnity. In light

![](<2503.06205_pg1_images/imageFile1.png>)

Date: March 11, 2025. 2010 Mathematics Subject Classiﬁcation. 35R30, 35J10, 81U40. Key words and phrases. Initial-to-ﬁnal-state map, Schro¨dinger equation, uniqueness, inverse problem, inverse problems.

1

