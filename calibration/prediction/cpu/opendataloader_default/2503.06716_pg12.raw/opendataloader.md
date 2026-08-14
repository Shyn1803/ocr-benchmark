12 CHAKRABORTY & SARKAR

We are now ready to present the proof of the Bianchi-Egnell type stability for the fractional Hardy-Sobolev inequality (1.1).

Proof of Theorem 1.3. Clearly the sharpness of the result follows from the Lemma 3.2 above. Suppose that the theorem is not true. Then we can ﬁnd a sequence (uk)k≥1 in H˙ s RN such that

−t 2∗

uk 2H˙ s − µs,t |x|

s(t)uk 22∗

![](<2503.06716_pg12_images/imageFile1.png>)

s(t) d(uk,M)2

= 0 (3.8)

lim

![](<2503.06716_pg12_images/imageFile2.png>)

k→∞

Since the ratio in (3.8) is homogeneous of degree 2 in uk, we may also suppose that uk 2H˙ s = µs,t for all k ≥ 1. Moreover, 0 ∈ M implies that d(uk,M) ≤ d(uk,0) = uk H ˙ s = √µs,t < ∞. Thus, up to a subsequence still denoted by uk, we see that d(uk,M) → L ∈ 0,√µs,t .

![](<2503.06716_pg12_images/imageFile3.png>)

![](<2503.06716_pg12_images/imageFile4.png>)

We now consider two cases, speciﬁcally L = 0 and L > 0. When L = 0 < √µs,t ; we can assume (if required up to a further subsequence still denoted by uk) that for

![](<2503.06716_pg12_images/imageFile5.png>)

all k ≥ 1 one has d(uk,M) < √µs,t = uk H ˙ s. Lemma 3.1 now gives that the above ratio is greater than or equal to α + O (1) → α > 0 as k → ∞ and it’s a contradiction to (3.8).

![](<2503.06716_pg12_images/imageFile6.png>)

Thus L > 0 and then we must have that the numerator of the above ratio goes to 0 as k → ∞, this in turn satisﬁes the hypothesis of Lemma 3.3. Consequently, we obtain

uk − Us,tλk H ˙ s = 0 and this gives us the desired contradiction.

L = lim

d(uk,M) ≤ lim

k→∞

k→∞

4. Palais-Smale decomposition

Although the energy functional associated with our problem (1.3) is given as in (3.7), for purely technical reasons, we consider the following normalized functional

- 1

![](<2503.06716_pg12_images/imageFile7.png>)

- 2


Is,t(u) :=

- 1

![](<2503.06716_pg12_images/imageFile8.png>)

- 2∗s(t) |x|−


t 2∗

u 2H˙ s −

![](<2503.06716_pg12_images/imageFile9.png>)

s(t)u

2∗s(t) 2∗s(t)

. (4.1)

There is a one-to-one correspondence between the critical points of (4.1) and the critical points of (3.7). Speciﬁcally, one has that u ∈ H˙ s RN is a weak solution to (1.3) (i.e., a critical point of (3.7)) if and only if µ

1 2∗

![](<2503.06716_pg12_images/imageFile10.png>)

s(t)−2

s,t u is a weak solution to the normalized Euler-Lagrange equation

 

2∗ s(t)−2u |x|t ;u ∈ H˙ s RN

(−∆)su = |u|

![](<2503.06716_pg12_images/imageFile11.png>)

(4.2)



u > 0 in RN

(i.e., a critical point of (4.1)). Due to this one-one correspondence, all the crucial properties of the energy functional are unchanged, therefore we only analyze the normalized functional moving onward.

Deﬁnition 4.1. We say that the sequence (un)n≥1 ⊂ H˙ s(RN) is a Palais-Smale sequence for Is,t at level β ((PS)β condition in-short ), if Is,t(un) → β and (Is,t)′(un) → 0 in ÄH˙ s RN ä′ as n → ∞. The functional Is,t is said to satisfy (PS)β condition if every (PS)β sequence has a convergent subsequence in H˙ s RN .

It is easy to see that the weak limit of a (PS) sequence solves (4.2) except for the positivity. However, the main diﬃculty is that the (PS) sequence may not converge strongly and the weak limit can be zero even if β > 0. The content of this section is the classiﬁcation of (PS) sequences of the functional Is,t which is given in the next proposition and the proof follows by arguments analogous to [4, Theorem 2.1].

Proposition 4.2. Let (un)n≥1 ⊂ H˙ s RN be a Palais-Smale sequence for Is,t at level β. Then up to a subsequence (still denoted by un) the following properties hold:

