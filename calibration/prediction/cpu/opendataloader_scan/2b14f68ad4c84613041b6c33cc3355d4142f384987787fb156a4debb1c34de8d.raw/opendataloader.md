dephasing channels are noisy for quantum information. For the dephasing channel E under consideration the preferential orthonormal basis is {| 0   , | 1  } ⊗ M ∈ H ⊗ M S , for M parallel uses of the channel, i.e., M classical bits can be transmitted noiselessly over M copies of the channel.

# B. Quantum Capacity

Consider the communication system shown in Fig. 1. Quantum information is encoded into the system spin via a unitary transformation. The system spin is then transmitted to the receiver, over the spin-star channel. In general, one must perform the maximization of the coherent information I c over the n -fold tensor product Hilbert space H ⊗ n S . However, Devetak and Shor recently established dephasing channels as degradable channels [51]. Therefore the single channel-use formula Q = Q 1 applies, and the maximization as in Eq. (5) over the larger Hilbert space is avoided. Moreover, Arrigo et al. [28] showed that for dephasing channels the coherent information I c is maximized by separable input states diagonalized in the reference basis. Therefore, we set the initial state of the system spin as

$$
1 Ps(0) (20)
$$

Initially, the system spin ρ S (0) is coupled to a reference system R such that the total system SR is pure. The reference system does not undergo any dynamical evolution; it is introduced as a mathematical device to purify the initial state of the system spin. The joint initial state of the total system SR is given by the maximally entangled state

$$
= (21)
$$

Dephasing channels are unital channels, i.e., E ( I ) = I , therefore the state of system spin is unaltered after interacting with the Ising bath

$$
1 ps(t) Ps(0) = (22) 2
$$

However, the total system SR decoheres as a result of the interaction and is mapped to a mixed state, whose diagonal elements (“populations”) are unaffected, but whose off-diagonal elements (“coherences”) are:

$$
psR(t) = (€ (Kij I) , i,j 2 +2iatẼ; +e (23)
$$

The quantum capacity Q of the dephasing channel is now obtained by using Eq. (5), making use of the single channel-use

$$
Q1 = max S[€(ps)] = S[(€ PseHs ~S[(€ 4 S[I/2] S[psR(t)] (24)
$$

This yields:

$$
Q(t) = 1 + Xk Xk , (25) k=l log2
$$

where χ 1 = χ 2 = 0 and

$$
X3 2[1 + X4 2[1
$$

are the eigenvalues of the state ρ SR ( t ) , and where

$$
IIv (t) = (26) i=0
$$

Next we calculate the entanglement-assisted capacities of the dephasing channel.

# C. Entanglement-Assisted Capacities

The communication protocol of entanglement-assisted capacities can also be described using Fig. 1. Prior to the communication the sender and receiver share a maximally entangled state given by Eq. (21). The ﬁrst qubit of the entangled pair belongs to the sender: ρ S (0) = Tr R ( | Φ    Φ | ) = I/ 2 , and interacts with the bath. Unlike the quantum capacity protocol, the second qubit is not a mathematical device and corresponds to the qubit in possession of the receiver prior to the communication. Therefore, it is again considered to have been transmitted over the identity channel. Now note that in our case, since and ,

S ( ρ S ) = 1 Q = Q 1 it follows from Eqs. (5) and (7) that the quantum capacity is related to the entanglement-assisted classical capacity via the simple formula

$$
CE = 1+ Q = 2+ Xi Xi , (27) i=1
$$

while the entanglement-assisted quantum capacity is

$$
CE QE = =1+ Xi Xi (28) 2 2 i=1 log2
$$

Next, we are interested in the classical capacity assisted by limited entanglement. Consider the situation when instead of

