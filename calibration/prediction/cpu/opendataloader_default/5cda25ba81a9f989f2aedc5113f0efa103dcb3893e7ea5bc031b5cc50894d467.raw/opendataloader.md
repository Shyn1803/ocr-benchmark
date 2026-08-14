using the isolation theorem.

Remark: The above corollary validates decoding on isolated subgraphs that are induced by trapping sets and this property is useful for deriving good update rules. Note that the number of iterations required for a subgraph to satisfy the isolation assumption in order to converge becomes an important parameter. Also the notion of critical number can now be extended for multilevel decoders as well.

IV. 3-BIT DECODERS FOR 3-LEFT-REGULAR LDPC CODES

We provide two particularly good 3-bit decoders: a 7-level LT decoder, and a 5-level NLT decoder for 3-left-regular LDPC codes. These were derived by considering a systemtatic hierarchy of trapping sets called trapping set ontology [12], and using the approach described in the previous section. Some important criteria to be considered in the derivation of the rules are increase in critical number and convergence in fewer iterations. Due to space constraints, we do not give details of deriving good rules in this paper but we shall demonstrate how multilevel decoders can correct certain error patterns uncorrectable by even ﬂoating-point algorithms.

The function Φv can be uniquely deﬁned by setting constraints on the magnitudes and thresholds. We shall use this approach to deﬁne the decoders.

For the 7-level LT decoder, the constraints that uniquely deﬁne the decoder are L1 < C < 2L1, L2 = 2L1 + C, L3 = 2L2 + C, and T1 = L1, T2 = L2, T3 = L3.

For the 5-level NLT decoder, the constraints that specify the decoder are C = L1, L2 = 3L1, T1 = L1, T2 = L2, and the channel weight function used to compute ωc is given by

ωc = Ω(m1,m2)

= 1 − sign(m1) ⊕ sign(m2) · δ(|m1| + |m2| − 2L2).

As an example, we now illustrate how a 3-error pattern on a n = 786, R = 0.75 quasicyclic code [17] that was uncorrectable by min-sum decoder, is correctable by the 7level LT decoder.

Example 2: Let H be the subgraph induced by the (9,5) trapping set which contains a (6,2) and has three degree-one checks as shown in Fig. 2. Consider the 3-error pattern shown in the ﬁgure where • denotes an initially wrong variable node.

v1 v2 v3

c1 c2 c3 c4 c5 c6

c8

c7

v7

v4 v5 v6

v9

c13

c9

c11

c14

c12

c10

v8

Fig. 2. Subgraph induced by (9,5) trapping set that contains a (6,2)

Under the isolation assumption, let us analyze the decoding of 7-level LT decoder on the subgraph with the help of the isolation theorem. Let mk(vi,:) denote all outgoing messages of node vi in the ﬁrst half of kth iteration and let mk(:,vi)

denote all incoming messages to node vi from checks in the second half of kth iteration. We will show only messages passed by certain crucial nodes in each iteration. Assume that all messages are initially zero.

In ﬁrst half of iteration 1, all outgoing messages are ±L1, i,e, m1(vi,:) = (−L1,−L1,−L1) for i ∈ {1,2,3} and m1(vi,:) = (L1,L1,L1) for i ∈/ {1,2,3}. In the second half, check nodes send their messages by the isolation assumption. Then m1(:,vi) = (−L1,−L1,−L1) for i ∈ {4,5}.

In the ﬁrst half of iteration 2, because Φv(L1,L1,−C) = 0, and Φv(−L1,−L1,C) = 0, this update rule helps prevent nodes v4 and v5 from sending wrong messages. Then m2(vi,: ) = 0 for i ∈ {1 to 5}. Check nodes send their messages in the second half and m2(:,vi) = (0,0,L1) for i ∈ {1,2}.

Finally in the ﬁrst half of iteration 3, nodes v1 and v2 are the only nodes that can send wrong messages. But because Φv(0,L1,−C) = 0, the nodes send zero instead, and the decoder converges at the end of iteration 3.

Remark: From the above example, we see that certain outputs of Φv were crucial for preventing propagation of wrong messages and convergence within 3 iterations. Whereas the min-sum decoder requires 4 iterations under the isolation assumption to converge on the same 3-error pattern. Now if subgraph H contained in G satisﬁes the isolation assumption for only 3 iterations, then min-sum is not guaranteed to correct three errors. For the quasicyclic code, this particular 3-error pattern on such a subgraph fails to be corrected by min-sum but is corrected by 7-level LT decoder. In fact, 7-level LT decoder corrects all 3-error patterns on the code.

Although we considered error patterns that failed to decode by the min-sum in example 2, the same analysis can be carried out on error patterns that failed to decode by BP as well. The rules can be derived to correct such patterns in a similar fashion by ensuring convergence in fewest number of iterations under the isolation assumption. For example, the 7-level LT decoder did not fail for any 4-error patterns on the same quasicyclic code whereas the BP and min-sum decoders failed in the region of simulation in Fig. 4.

V. NUMERICAL RESULTS

Simulations for frame error rate (FER) were carried out on three different codes: 1) n = 155, R = 0.4, Tanner code, 2) n = 768, R = 0.75, Quasicyclic code with dmin = 12, and 3) a n = 4085, R = 0.82, MacKay code. The codes were chosen to cover a broad spectrum of LDPC codes in order to validate our approach. The Tanner code is well-understood and has been analyzed for many different decoders. The high-rate quasicyclic code was chosen since the error ﬂoor problem is much more challenging for high-rate codes. A MacKay code was chosen as an example of a high-rate random code. Fig. 3, Fig. 4, and Fig. 5 show the simulation results. The maximum number of iterations used was 100 for all decoders. Structures of these three codes can be found in [17].

For all three codes, the 3-bit decoders signiﬁcantly outperform BP in the error ﬂoor region. Notice the difference in slopes in the FER curves. For the Tanner code, the 5-NLT

