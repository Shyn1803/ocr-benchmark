Cutoﬀ describes a phase transition: as we run the family of Markov chains on Xn, the total variation distance is almost equal to 1, and then suddenly it drops and approaches zero as n goes to inﬁnity. The formal deﬁnition of cutoﬀ is given below.

Deﬁnition 2. A family of Markov chains on Xn is said to have cutoﬀ at time tn with window wn = o(tn) if and only if

dx(n)(tn − cwn) = 1 and lim

lim

lim

c→∞

n→∞

c→∞

d(xn)(tn + cwn) = 0,

lim

n→∞

where d(xn)(t) denotes the total variation distance of the n–th Markov chain after t steps starting at x.

Given a Markov chain exhibiting cutoﬀ, one can ask for more precise control on the exact distance from stationarity. This is known as the limit proﬁle with respect to the sequences (tn) and (wn), deﬁned as:

d(xn) (tn + cwn) , for all c ∈ R, (1) if this limit exists.

Φx(c) := lim

n→∞

The limit proﬁle is known for only a few Markov chains, such as the riﬄe shuﬄe [2], the asymmetric exclusion process on the segment [4], the simple exclusion process on the cycle [14], and the simple random walk on Ramanujan graphs [16], etc. Teyssier [25] determined the limit proﬁle for random transpositions. Using representation theory of the symmetric group Sn, he used Fourier transform arguments for studying limit proﬁles that work for random walks on groups using a generating set that is a conjugacy class. The same limit proﬁle is proved to be true for the k-cycle card shuﬄe [18], under the assumption that k = o(n) and for star transposition [17]. Olesker–Taylor and Schmid also studied the limit proﬁle for the Bernoulli–Laplace chain [21]. In Section 6 we give a more extensive presentation of the above results.

Furthermore, if P is aperiodic, irreducible and reversible on X, then the spectrum of P satisﬁes

−1 < β|X| ≤ . . . ≤ β2 < β1 = 1,

and there is an orthonormal eigenbasis {fj : Xn → R}. The main assumption on P is that there is a continuous (or bounded) function g on R such that

|Xn|

fi(x)2 (1 − βi)2 e−2(t

wn2

n+cwn)(1−βi) ≤ g(c), (2)

limsup

n→∞

i=2

for all c ∈ R.

Theorem 3. Let Pn be the transition matrix of a reversible Markov chain on Xn that exhibits cutoﬀ at tn with window wn and satisﬁes (2). Assume that Φx, the total variation limit proﬁle with respect to the sequences (tn) and (wn) at x, exists. Then Φx is continuous for every x ∈ X.

2

