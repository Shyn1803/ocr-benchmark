QUASI-LINEAR TIME DECODING 35

- [SSB09] Georg Schmidt, Vladimir R Sidorenko, and Martin Bossert. Collaborative decoding of interleaved reed–solomon codes and concatenated code designs. IEEE Transactions on Information Theory, 55(7):2991–3012, 2009.
- [SSB10] Georg Schmidt, Vladimir R Sidorenko, and Martin Bossert. Syndrome decoding of reed–solomon codes beyond half the minimum distance based on shift-register synthesis. IEEE Transactions on Information Theory, 56(10):5245–5252, 2010.


[Sti09] Henning Stichtenoth. Algebraic function ﬁelds and codes, volume 254. Springer Science & Business Media, 2009. [Sud97] Madhu Sudan. Decoding of Reed Solomon codes beyond the error-correction bound. Journal of complexity, 13(1):180–193, 1997. [SW99] Mohammad Amin Shokrollahi and Hal Wasserman. List decoding of algebraic-geometric codes. IEEE Transactions on Information Theory, 45(2):432–437, 1999. [Tam24] Itzhak Tamo. Tighter list-size bounds for list-decoding and recovery of folded Reed-Solomon and multiplicity codes. IEEE Transactions on Information Theory, 70(12):8659–8668, 2024.

[VH97] Conny Voss and T Hoholdt. An explicit construction of a sequence of codes attaining the tsfasman-vladut-zink bound. the ﬁrst steps. IEEE Transactions on Information Theory, 43(1):128–135, 1997.

[VZGG13] Joachim Von Zur Gathen and J¨urgen Gerhard. Modern computer algebra. Cambridge University Press, 2013.

[WKS15] Bin Wang, Haibin Kan, and Kenneth W. Shum. Hermitian codes in distributed storage systems with optimal error-correcting capacity. In 2015 IEEE International Symposium on Information Theory (ISIT), pages 601–605, 2015.

[Wu12] Yingquan Wu. Novel burst error correction algorithms for Reed-Solomon codes. IEEE Transactions on information theory, 58(2):519–529, 2012. [YLLW01] Liuguo Yin, Jianhua Lu, K Ben Letaief, and Youshou Wu. Burst-error-correcting algorithm for Reed-Solomon codes. Electronics Letters, 37(11):1, 2001.

Appendix A. The proof of Lemma 2.6

In this section, we will give a generalized version of Wu’s algorithm that can be applied to RS codes deﬁned on a non-cyclic multipoint set. Let us ﬁrst recap some notations in syndrome decoding.

Assume P = {ξ, ξα, . . ., ξαn−1} ∈ F∗q/ α is a coset of cyclic group, where α ∈ F∗q has order n. The RS[n, k] that we concerned is deﬁned as

RS[n, k] = { f(ξ), f(ξα), . . ., f(ξαn−1) | f(x) ∈ Fq[x]<k}.

Let r = n − k. For a burst interval [i, i + r − 2], we always view it as a subset of [1, n] in the following sense

[i, i + r − 2](mod n + 1) =   

[i, i + r − 2], if i + r − 2 ≤ n; [i, n] ∪ [1, (i + r − 2 mod n + 1) + 1], if i + r − 2 > n.

