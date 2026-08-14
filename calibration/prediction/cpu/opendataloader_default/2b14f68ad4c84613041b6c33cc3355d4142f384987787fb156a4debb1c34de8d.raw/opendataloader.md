dephasing channels are noisy for quantum information. For the dephasing channel E under consideration the preferential orthonormal basis is{|0 ,|1 }⊗M ∈ HS⊗M, for M parallel uses of the channel, i.e., M classical bits can be transmitted noiselessly over M copies of the channel.

B. Quantum Capacity

Consider the communication system shown in Fig. 1. Quantum information is encoded into the system spin via a unitary transformation. The system spin is then transmitted to the receiver, over the spin-star channel. In general, one must perform the maximization of the coherent information Ic over the n-fold tensor product Hilbert space HS⊗n. However, Devetak and Shor recently established dephasing channels as degradable channels [51]. Therefore the single channel-use formula Q = Q1 applies, and the maximization as in Eq. (5) over the larger Hilbert space is avoided. Moreover, Arrigo et al. [28] showed that for dephasing channels the coherent information Ic is maximized by separable input states diagonalized in the reference basis. Therefore, we set the initial state of the system spin as

- 1

- 2


I 2

. (20)

(|0 0| + |1 1|) =

ρS(0) =

Initially, the system spin ρS(0) is coupled to a reference system R such that the total system SR is pure. The reference system does not undergo any dynamical evolution; it is introduced as a mathematical device to purify the initial state of the system spin. The joint initial state of the total system SR is given by the maximally entangled state

|Φ =

1 √2

(|00 + |11 ). (21)

Dephasing channels are unital channels, i.e., E(I) = I, therefore the state of system spin is unaltered after interacting with the Ising bath

I 2

. (22)

ρS(t) = ρS(0) =

However, the total system SR decoheres as a result of the interaction and is mapped to a mixed state, whose diagonal elements (“populations”) are unaffected, but whose off-diagonal elements (“coherences”) are:

ρSR(t) = (E ⊗ I)(|Φ Φ|)

(Kij ⊗ I)(|Φ Φ|)(Kij† ⊗ I),

=

i,j

- 1

- 2


(|00 00| + |11 11|)

=

- 1

- 2 i


λi(e−2iαt E

|00 11|

+

i

+e+2iαt E

|11 00|). (23)

i

The quantum capacity Q of the dephasing channel is now obtained by using Eq. (5), making use of the single channel-use

4

formula Q = Q1 and the fact that the coherent information is maximized by our chosen initial state ρS(0):

S[E(ρS)] − S[(E ⊗ I)(|Φ Φ|)]

Q = Q1 = max

ρS∈HS

= S[E(I/2)] −S[(E ⊗ I)(

1 √2

1 √2

(|00 + |11 )

( 00| + 11|))]

= S[I/2] − S[ρSR(t)]. (24) This yields:

Q(t) = 1 +

where χ1 = χ2 = 0 and

4

χk log2 χk, (25)

k=1

- 1

- 2


χ3 =

1 Z |ΠN|], χ4 =

[1 +

- 1

- 2


1 Z |ΠN|],

[1 −

are the eigenvalues of the state ρSR(t), and where

2N−1

e−

ΠN(t) =

i=0

N

n=1(21βΩn+2iαtgn)(−1)in. (26)

Next we calculate the entanglement-assisted capacities of the dephasing channel.

C. Entanglement-Assisted Capacities

The communication protocol of entanglement-assisted capacities can also be described using Fig. 1. Prior to the communication the sender and receiver share a maximally entangled state given by Eq. (21). The ﬁrst qubit of the entangled pair belongs to the sender: ρS(0) = TrR(|Φ Φ|) = I/2, and interacts with the bath. Unlike the quantum capacity protocol, the second qubit is not a mathematical device and corresponds to the qubit in possession of the receiver prior to the communication. Therefore, it is again considered to have been transmitted over the identity channel.

Now note that in our case, since S(ρS) = 1 and Q = Q1, it follows from Eqs. (5) and (7) that the quantum capacity is related to the entanglement-assisted classical capacity via the simple formula

CE = 1 + Q = 2 +

4

χi log2 χi, (27)

i=1

while the entanglement-assisted quantum capacity is

CE 2

- 1

- 2


QE =

= 1 +

4

χi log2 χi. (28)

i=1

Next, we are interested in the classical capacity assisted by limited entanglement. Consider the situation when instead of

