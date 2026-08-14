16 CYPRIEN TAMEKUE AND SHINUNG CHING

Next, F is compact. In fact, let B ⊂ C0([t0,T];Rd) be a bounded set, let us show that F(B) is compact. First, F(B) ⊂ C0([t0,T];Rd) is bounded by (3.22). It remains to prove that for all t∗ ∈ [t0,T], the following holds

![](<2503.05606_pg16_images/imageFile1.png>)

|F(z)(t) − F(z)(t∗)| −−−→

0. (3.23)

sup

t→t∗

z∈B

One has immediately from (3.21) and (3.22) that for some M1 > 0, it holds |F(z)(t)−F(z)(t∗)| = |xuz(t)−xuz(t∗)| ≤ (Λ3 xuz ∞+ B ∞ uz ∞+ f ∞)|t−t∗| ≤ M1|t−t∗|

(3.24) for every t ∈ [t0,T]. This proves (3.23) and, therefore, that F is compact by the Ascoli-Arzelà theorem. Finally, the set {z ∈ C0([t0,T];Rd) | z = θF(z)for some θ ∈ [0,1]} is bounded thanks to (3.21) and (3.22). According to Schaefer’s ﬁxed point theorem, F admits at least one ﬁxed point z ∈ C0([t0,T];Rd), i.e., z = F(z) = xuz.

Remark 3.7. It is worth noting that one can also deﬁne the map F with the following control function

vz(t) = Bz(t)⊤DΦzt,T(xvz(t))⊤(N2z(vz))−1 x1 − Φzt0,T(x0) −

T

DΦzs,T(xvz(s))f(s,z(s))ds . (3.25)

t0

4. Conclusion

This work extends the methodology of control synthesis to general control-aﬃne systems of the form (1.1), thereby advancing the theory of nonlinear controllability and providing a constructive framework for control design that is amenable to both numerical veriﬁcation and practical implementation.

The global controllability results established in Section 2 for systems of the form x˙(t) = Nt(x(t))+B(t)u(t) have broad applicability, including to recurrent neural networks of Hopﬁeldtype [12], as illustrated in Example 4, and more generally to nonlinear systems in Lur’e form (see, for instance, [8] and references therein). In particular, we derived suﬃcient conditions—natural nonlinear extensions of classical criteria from the linear setting—that guarantee that the reachable set from any given initial state x0 ∈ Rd covers the entire space Rd.

While these results represent a substantial contribution to the study of nonlinear control, it is important to emphasize that the obtained controllability results are pointwise in nature, in the sense that the suﬃcient conditions explicitly depend on the initial state x0. A natural avenue for future work is to investigate whether these conditions could be shown to be both necessary and uniform across the state space, thereby providing a complete characterization of global controllability for the class of systems considered. Such a result would mirror the celebrated equivalence between controllability and Gramian invertibility in the linear case, thus achieving a deeper understanding of the nonlinear counterpart.

Appendix A. Proofs of some of the results stated in the main text

In this section, we present the proof of some of the results presented in the main text. We start with the following.

