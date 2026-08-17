Moreover, we found that, in contrast to the random circuit setting, the k -design preparation in minimally random quantum circuits occurs in a two-step fashion similarly to what happens for purity [ 30 – 32 ] and out-oftime-ordered correlators [ 33 , 34 ] and provided an analytic description of this phenomenon in the case of dualunitary circuits. These findings suggest that that the two settings we studied here are more similar to each other than to Haar random circuits, meaning that the setting (b) represents a qualitatively more accurate modelling of non-random dynamics than the fully random circuit.

Our work raises many interesting questions for future research. In particular, we can identify two compelling directions. One is to rigorously prove some of the statements that are argued or conjectured here. For example, that the design production speed achieved by perfect tensors is the theoretical maximum achievable in a brickwork circuit and whether one can achieve this speed considering perfect tensors in the setting (a). The other is to ask, more generally, whether the our setting (a) is the optimal one for producing k -designs with a brickwork quantum circuit (i.e. the one requiring the least amount of resources) or can be further improved.

# ACKNOWLEDGMENTS

We acknowledge financial support from the Royal Society through the University Research Fellowship No. 201101 (B. B. and J. R.) and the Leverhulme Trust through the Early Career Fellowship No. ECF-2022-324 (K. K.).

# Appendix A: Proof of Property 1

Property 1 follows by straightforward adaptation of Ippoliti and Ho’s Theorem (cf. Sec. 3.C in Ref. [ 26 ]). Let us provide a brief proof considering separately the three Cases (a.1) , (a.2) , and (b.1) .

# 1. Proof for Case (a.1)

In Case (a.1) the mixed state ρ ( k ) t evolves according to

$$
Pt+1 = (Al)
$$

where U is written in terms of matrices U ( n ) ∈ A V as in Eq. ( 1 ) and

$$
Dk[] = (@2L) (@2L) (A2) ae{I,or 4-1
$$

This is very similar to the setting considered in Ref. [ 26 ]: the only difference is that A V is an open subset of U (4) and not necessarily of the dual-unitary submanifold. Therefore, we need to show that the Lemma in Appendix E of Ref. [ 26 ], the one guaranteeing that one can

$$
(UWt)n,n+l, (A3)
$$

can generate any unitary operation by varying n ∈ Z 2 L , and U,W ∈ A V . Considering W close to U we see that one can then generate any arbitrary infinitesimal unitary transformation on the qubits at position n and n + 1. Taking then sufficiently high powers one can generate any unitary transformation on the two qubits. Since n is arbitrary the statement immediately follows. Following Ref. [ 26 ] we then have that the limit

$$
lim pt (A4)
$$

exists and commutes with

$$
(A5)
$$

where U is an arbitrary unitary matrix in U (2 2 L ). These two matrices can be chosen in such a way to generate a complete gate set for each pair of qubits on the chain. Therefore, we conclude that ρ ( k ) ∞ commutes with any unitary matrix of the form U ⊗ k , with U in U (2 2 L ). The Schur–Weyl duality [ 64 , 65 ] then implies that ρ ( k ) ∞ = ρ ( k ) H .

# 2. Proof for Case (a.2)

In Case (a.2) the channel B k [ · ] can again be written as in Eq. ( A1 ). In this case, however, d is a generic integer ≥ 2 and D k [ · ] is modified to

$$
Dk[:] = (A6)
$$

Therefore the discussion in Ref. [ 26 ] does not directly apply. Specifically, we need to prove again the Lemmas in Appendix D of Ref. [ 26 ], those concerning the existence of the limit state and the fact that it commutes with the Krauss operators of the channel. By noting that, however, D k [ · ] projects the state at site 2 L on the space spanned by { P σ } σ ∈ S k , where S k is the symmetric group of of k elements and

$$
= II (A7) p=l
$$

one finds that the arguments of Ref. [ 26 ] can be straightforwardly repeated and both Lemmas continue to hold. Also the Lemma in Appendix E holds as the arguments of the previous subsection are not restricted to d = 2. Therefore, we again have that the limit

$$
lim Pt (A8)
$$

