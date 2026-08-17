(ii) The Referee calculates c R ¼ ½   AR <   RB   2 f 0 ; 1 g and sends it to Bob (1 bit).

(iii) After reception of jA' Bob calculates B = and [0, T[. He determines the index jB = of the sector where his angle and the bit CB = on jB, CA, CR, CB, %B and he outputs b = B with probability JB (%B ARB and b = = B with probability JB 1 in Table I. ARB'

As explicitly shown in the Supplemental Material [ 36 ], the above protocol gives the desired probability P ð a ¼ b j   A ;  B Þ¼ sin ð   A     B 2 Þ 2 for all possible equatorial measurements, using 4 bits of communication. It can then be extended in the following way to all measurement directions on the Bloch sphere, using a similar technique as in [ 10 ]:

Protocol measurement directions and y = (sine Bcoso B,

B B B Þ (i) run Protocol 1 with input angles   A and   B ; Alice and Bob obtain intermediate outputs a 0 and b 0 .

(ii) run Protocol 1 a second time (using a new set of in dependent variables   AR ,   RB ), now with input angles a 0   A and   b 0   B ; Alice and Bob output the outcomes a and b of this second run of Protocol 1.

Thissecondprotocolnowsimulatesthedesiredcorrelation E ð x ; y Þ ¼   x   y for all possible projective measurements by Alice and Bob, with 8 bits of communication; for more details on the calculations, see Supplemental Material. Note that Protocols 1 and 2 do not simulate the correct marginals. In order to randomize the marginals, Alice can—at the very end of the protocol—generate a random bit and send it to Bob; depending on the value of this bit, they will both ﬂip their outcomes or not. All in all, the entanglement swapping correlations can thus be simulated with 9 bits of communication.

Discussion.We thus have proved that remarkably, the entanglement swapping process can be simulated with bounded communication, even in a bilocal scenario where Alice and Bob are (as in the quantum case) completely uncorrelated before the protocol is run, and therefore do not have any prior shared randomness. Our protocol provides an upper bound on the nonlocality of entanglement swapping in terms of its communication cost. It is an open question whether fewer bits of communication are actually sufﬁcient: it might indeed be possible to simulate equatorial measurements more efﬁciently than with Protocol 1, or to ﬁnd a more direct protocol that does not treat separately the azimuth and zenith angles of the measurement settings, more in the spirit of the Toner-Bacon simulation protocol for singlet correlations [ 13 ].

Next, it is natural to consider the simulation of multi stage entanglement swapping, which is essential for long distance quantum communication Now; N referees Rv) are placed on line between Alice and Bob. Two neighboring referees share a singlet state, while R1 and RN share singlet states with A and B, respectively; each referee performs a joint measurement, leaving at the end the particles of Alice and Bob entangled. Whereas the quantum protocol has a straightforward and nice iterative character, we were not able to find simulation protocol with finite amount of   communication in (N + 1) locality scenario [29]. Consider for instance the case with one additional referee Rz. Analogously to our Protocol 1, assume that Alice and R, share the random variable R1 and Rz share and Rz and Bob share all uniformly and independently distributed on some interval After some finite communication, Bob could for b = a = 1 if and only ] = [AAR, = < This   would result in the probability P(a = which scales cubically with %4-%B, and is therefore too is close to %B. It is unclear how to change the cubic scaling with finite communication. The following questions remain open: can multistage entanglement swapping be simulated with finite communication? Or can one prove, that above a certain value of N an infinite amount of communication is necessary? AAR, ARB' AAR, We thank   Jean-Daniel   Bancal,   Yeong-Cherng sions_ This work was supported by UQ Postdoctoral Research Fellowship, the NSF grant CCF-0832787, the UK EPSRC, 255961 QCS, Canada's NSERC and CIFAR, the Swiss NCCR-QSIT, the US ARO, and the European ERC-AG QORE. Liang,

J.S. Bell, Physics (Long Island N.Y) 1, 195 (1964). City, [1]

D. Salart, A Baas, C. Branciard, N. Gisin, and H. Zbinden, Nature (London) 454, 861 (2008)

[3] H. Buhrman, R. Cleve, S. Massar, and R. de Wolf, Rev. Mod. Phys. 82 , 665 (2010) . [4] A. Ekert, Phys. Rev. Lett. 67 , 661 (1991) .

A. Ekert; Phys. Lett. 67, 661 (1991) Rev.

J. Barrett, L. Hardy; and A Kent, Rev. Lett. 95, 10503 (2005). Phys.

A Acín et al., Phys. Rev. Lett. 98, 230501 (2007)

S. Pironio et al Nature (London) 464, 1021 (2010)

R: Colbeck and A. Kent, J. A 44, 095305 (2011) Phys.

T. Maudlin; Proceedings of the Biennial Meeting of the Philosophy of Science Association 1992, 404 (1992)

G. Brassard, R Cleve; and A Tapp, Phys. Rev. Lett. 83, 1874 (1999).

B. Gisin and N. Gisin; Lett. A 260, 323 (1999). Phys.

M. Steiner, Phys. Lett. A 270, 239 (2000)

B Toner and D. Bacon; Phys. Rev. Lett. 91,  187904 (2003)

[14] S. Pironio, Phys. Rev. A 68 , 062102 (2003) .

