around 2000 due to the studies of quantum computers. As well known, Grover’s algorithm can ﬁnd targets much faster than the corresponding classical algorithm, and it can be considered as a quantum walk on a graph [4]. For database search in quantum computers, quantum walks have been focused on in quantum informations [5].

The major study in quantum walks is their ﬁnding probabilities and they have been investigated numerically or analytically. Analytic researches have resulted in long-time limit theorems in mathematics. The limit theorems are useful to understand how the quantum walkers distribute in space after they have repeated their unitary processes a lot of times. The ﬁrst limit theorem was proved in 2002 and it stated a long-time limit distribution which was diﬀerent from the limit distributions of classical random walks [6]. Since then, many limit theorems have been demonstrated and they told us interesting behavior of quantum walks [7].

In 2015, a remarkable behavior was discovered [8]. A quantum walk held a gap in distribution and the walker was never observed around the launching location. After the paper had been published, two types of quantum walk were reported and they also had a gap in distribution. One of them was a 3-state quantum walk in 2006 and its probability distribution showed a gap and localization [9]. The other was a 2-state walk in 2018 and its model was complicated [10]. Motivated by the quantum walk in 2018, we try to seek a simpler model which makes a probability distribution with a gap. We deﬁne a quantum walk in the next section and numerically observe its probability distribution. Since the numerical experiments let us expect that the quantum walk distributes with a gap, we will work on limit distributions in Sect. 3 so that the quantum walk is proved to hold a gap in distribution.

# 2 Deﬁnition of a quantum walk

The quantum walker with two coin states |0 and |1 is supposed to locate at points, whose set is represented by Z = {0,±1,±2,...}, in superposition. Its system is described on a tensor Hilbert space Hp ⊗ Hc. The Hilbert space Hp represents the locations and it is spanned by the orthogonal normalized basis {|x : x ∈ Z}. Also, the Hilbert space Hc represents the coin states and it is spanned by the orthogonal normalized basis {|0 ,|1 }. Let us deﬁne

|0 =

1 0

, |1 =

- 0
- 1


, (1)

for the Hilbert space Hc in this paper. Given two unitary operations, the coin states and the position states of the walker are operated with them. More precisely, the system of quantum walk at time t(= 0,1,2,...), represented by |Ψt ∈ Hp ⊗ Hc, gets a new system at time t + 1, represeted by |Ψt+1 ∈ Hp ⊗ Hc, with unitary operations U1 and U2,

|Ψt+1 = U2U1 |Ψt , (2)

2

