PRL 109, 100401 (2012) P H Y S I C A L R E V I E W L E T T E R S 7 SEPTEMBERweek ending2012

- (ii) The Referee calculates cR ¼ ½ AR < RB 2 f0;1g

and sends it to Bob (1 bit).

- (iii) After reception of jA, Bob calculates ¼


sign½sinð B jA 4Þ  and 0B ¼ ð B jA 4 mod Þ 2 ½0; ½. He determines the index jB ¼ b4 0Bc 2 f0;1;2;3g of the sector where his angle 0B lies, and the bit cB ¼ ½ RB < 0B jB 4 2 f0;1g. Depending on jB, cA, cR, cB, 0B and RB, he outputs b ¼ with probability }j

cBAcRcBð 0B RBÞ, and b ¼ with probability 1 }j

cBAcRcBð 0B RBÞ, for the functions }j

cBAcRcB deﬁned in Table I.

As explicitly shown in the Supplemental Material [36], the above protocol gives the desired probability Pða¼bj A; BÞ¼sinð

2 Þ2 for all possible equatorial measurements, using 4 bits of communication. It can then be extended in the following way to all measurement directions on the Bloch sphere, using a similar technique as in [10]:

A B

Protocol 2.—For measurement directions x ¼ ðsin A cos A;sin A sin A;cos AÞ and y¼ðsin Bcos B; sin Bsin B;cos BÞ, the three parties

- (i) run Protocol 1 with input angles A and B; Alice

and Bob obtain intermediate outputs a0 and b0.

- (ii) run Protocol 1 a second time (using a new set of in


dependent variables AR, RB), now with input angles a0 A and b0 B; Alice and Bob output the outcomes a and b of this second run of Protocol 1.

Thissecondprotocolnowsimulatesthedesiredcorrelation Eðx;yÞ ¼ x y for all possible projective measurements by Alice and Bob, with 8 bits of communication; for more details on the calculations, see Supplemental Material. Note that Protocols 1 and 2 do not simulate the correct marginals. In order to randomize the marginals, Alice can—at the very end of the protocol—generate a random bit and send it to Bob; depending on the value of this bit, they will both ﬂip their outcomes or not. All in all, the entanglement swapping correlations can thus be simulated with 9 bits of communication.

Discussion.—We thus have proved that remarkably, the entanglement swapping process can be simulated with bounded communication, even in a bilocal scenario where Alice and Bob are (as in the quantum case) completely uncorrelated before the protocol is run, and therefore do not have any prior shared randomness. Our protocol provides an upper bound on the nonlocality of entanglement swapping in terms of its communication cost. It is an open question whether fewer bits of communication are actually sufﬁcient: it might indeed be possible to simulate equatorial measurements more efﬁciently than with Protocol 1, or to ﬁnd a more direct protocol that does not treat separately the azimuth and zenith angles of the measurement settings, more in the spirit of the Toner-Bacon simulation protocol for singlet correlations [13].

Next, it is natural to consider the simulation of multistage entanglement swapping, which is essential for long

distance quantum communication. Now, N referees (R1;R2;...;RN) are placed on a line between Alice and Bob. Two neighboring referees share a singlet state, while R1 and RN share singlet states with A and B, respectively; each referee performs a joint measurement, leaving at the end the particles of Alice and Bob entangled. Whereas the quantum protocol has a straightforward and nice iterative character, we were not able to ﬁnd a simulation protocol with a ﬁnite amount of communication in a (N þ 1)locality scenario [29]. Consider for instance the case with one additional referee R2. Analogously to our Protocol 1, assume that Alice and R1 share the random variable AR

, R1 and R2 share R

1

1R2, and R2 and Bob share R

2B, all uniformly and independently distributed on some interval [0, m]. After some ﬁnite communication, Bob could for instance [as in our ﬁrst attempt, before Eq. (3)] output b ¼ a ¼ 1 if and only if ½ A < AR

1R2 ¼ ½ R1R2 < R

¼ ½ AR1 < R

1

2B ¼ ½ R2B < B . This would result in the probability Pða ¼ bj A; B 2 ½0; m Þ ¼ 6m3 3 j A Bj3, which scales cubically with A- B, and is therefore too small when A is close to B. It is unclear how to change the cubic scaling with ﬁnite communication. The following questions remain open: can multistage entanglement swapping be simulated with ﬁnite communication? Or can one prove, that above a certain value of N, an inﬁnite amount of communication is necessary?

We thank Jean-Daniel Bancal, Yeong-Cherng Liang, Stefano Pironio, Tim Ra¨z, and Ronald de Wolf for discussions. This work was supported by a UQ Postdoctoral Research Fellowship, the NSF grant CCF-0832787, the UK EPSRC, the EU DIQIP, the EU FP7 grant project 255961 QCS, Canada’s NSERC and CIFAR, the Swiss NCCR-QSIT, the US ARO, and the European ERC-AG QORE.

![](<0e1cdcf74d42cf251ad3e6127439c537599c_page_5_pg1_images/imageFile1.png>)

- [1] J.S. Bell, Physics (Long Island City, N.Y.) 1, 195 (1964).
- [2] D. Salart, A. Baas, C. Branciard, N. Gisin, and H. Zbinden, Nature (London) 454, 861 (2008).
- [3] H. Buhrman, R. Cleve, S. Massar, and R. de Wolf, Rev. Mod. Phys. 82, 665 (2010).
- [4] A. Ekert, Phys. Rev. Lett. 67, 661 (1991).
- [5] J. Barrett, L. Hardy, and A. Kent, Phys. Rev. Lett. 95, 10503 (2005).
- [6] A. Acı´n et al., Phys. Rev. Lett. 98, 230501 (2007).
- [7] S. Pironio et al., Nature (London) 464, 1021 (2010).
- [8] R. Colbeck and A. Kent, J. Phys. A 44, 095305 (2011).
- [9] T. Maudlin, Proceedings of the Biennial Meeting of the Philosophy of Science Association 1992, 404 (1992).
- [10] G. Brassard, R. Cleve, and A. Tapp, Phys. Rev. Lett. 83, 1874 (1999).
- [11] B. Gisin and N. Gisin, Phys. Lett. A 260, 323 (1999).
- [12] M. Steiner, Phys. Lett. A 270, 239 (2000).
- [13] B. Toner and D. Bacon, Phys. Rev. Lett. 91, 187904

(2003).

- [14] S. Pironio, Phys. Rev. A 68, 062102 (2003).


100401-4

