Next, F is compact. In fact, let B ⊂ C 0 ([ t 0 ,T ]; R d ) be a bounded set, let us show that F ( B ) is compact. First, F ( B ) ⊂ C 0 ([ t 0 ,T ]; R d ) is bounded by ( 3.22 ). It remains to prove that for all t ∗ ∈ [ t 0 ,T ], the following holds

$$
0 (3.23) t-+t* zeB
$$

$$
(3.24)
$$

for every t ∈ [ t 0 ,T ]. This proves ( 3.23 ) and, therefore, that F is compact by the Ascoli-Arzelà theorem. Finally, the set { z ∈ C 0 ([ t 0 ,T ]; R d ) | z = θ F ( z )for some θ ∈ [0 , 1] } is bounded thanks to ( 3.21 ) and ( 3.22 ). According to Schaefer’s ﬁxed point theorem, F admits at least one ﬁxed point z ∈ C 0 ([ t 0 ,T ]; R d ), i.e., z = F ( z ) = x u z .  

Remark 3.7. It is worth noting that one can also deﬁne the map F with the following control function

$$
to (3.25) 21
$$

# 4. CONCLUSION

This work extends the methodology of control synthesis to general control-aﬃne systems of the form ( 1.1 ), thereby advancing the theory of nonlinear controllability and providing a constructive framework for control design that is amenable to both numerical veriﬁcation and practical implementation.

The global controllability results established in Section 2 for systems of the form ˙ x ( t ) = N t ( x ( t ))+ B ( t ) u ( t ) have broad applicability, including to recurrent neural networks of Hopﬁeldtype [ 12 ], as illustrated in Example 4 , and more generally to nonlinear systems in Lur’e form (see, for instance, [ 8 ] and references therein). In particular, we derived suﬃcient conditions—natural nonlinear extensions of classical criteria from the linear setting—that guarantee that the reachable set from any given initial state x 0 ∈ R d covers the entire space R d .

While these results represent a substantial contribution to the study of nonlinear control, it is important to emphasize that the obtained controllability results are pointwise in nature, in the sense that the suﬃcient conditions explicitly depend on the initial state x 0 . A natural avenue for future work is to investigate whether these conditions could be shown to be both necessary and uniform across the state space, thereby providing a complete characterization of global controllability for the class of systems considered. Such a result would mirror the celebrated equivalence between controllability and Gramian invertibility in the linear case, thus achieving a deeper understanding of the nonlinear counterpart.

# APPENDIX A. PROOFS OF SOME OF THE RESULTS STATED IN THE MAIN TEXT

In this section, we present the proof of some of the results presented in the main text. We start with the following.

