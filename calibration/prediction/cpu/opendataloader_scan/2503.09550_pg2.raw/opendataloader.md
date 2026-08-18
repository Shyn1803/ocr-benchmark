Cutoﬀ describes a phase transition: as we run the family of Markov chains on X n , the total variation distance is almost equal to 1 , and then suddenly it drops and approaches zero as n goes to inﬁnity. The formal deﬁnition of cutoﬀ is given below.

Deﬁnition 2. A family of Markov chains on X n is said to have cutoﬀ at time t n with window w n = o ( t n ) if and only if

$$
lim lim (tn CWn ) =1 and lim lim d(n) (tn + cwn) = 0, C00 nl=00
$$

where d ( n ) x ( t ) denotes the total variation distance of the n –th Markov chain after t steps starting at x .

Given a Markov chain exhibiting cutoﬀ, one can ask for more precise control on the exact distance from stationarity. This is known as the limit proﬁle with respect to the sequences ( t n ) and ( w n ) , deﬁned as:

$$
= lim d(n) (tn + cWn) = for all c € R n-0
$$

if this limit exists.

The limit proﬁle is known for only a few Markov chains, such as the riﬄe shuﬄe [2], the asymmetric exclusion process on the segment [4], the simple exclusion process on the cycle [14], and the simple random walk on Ramanujan graphs [16], etc. Teyssier [25] determined the limit proﬁle for random transpositions. Using representation theory of the symmetric group S n , he used Fourier transform arguments for studying limit proﬁles that work for random walks on groups using a generating set that is a conjugacy class. The same limit proﬁle is proved to be true for the k -cycle card shuﬄe [18], under the assumption that k = o ( n ) and for star transposition [17]. Olesker–Taylor and Schmid also studied the limit proﬁle for the Bernoulli–Laplace chain [21]. In Section 6 we give a more extensive presentation of the above results.

Furthermore, if P is aperiodic, irreducible and reversible on X , then the spectrum of P satisﬁes

$$
=1 Bjx| < < 82 < B1 = 1,
$$

and there is an orthonormal eigenbasis { f j : X n → R } . The main assumption on P is that there is a continuous (or bounded) function g on R such that

for all c ∈ R .

$$
Xn lim sup w2 tcwn)(I-B;) < g(c), n-0 i=2 e-2(tn
$$

Theorem 3. Let P n be the transition matrix of a reversible Markov chain on X n that exhibits cutoﬀ at t n with window w n and satisﬁes (2) . Assume that Φ x , the total variation limit proﬁle with respect to the sequences ( t n ) and ( w n ) at x , exists. Then Φ x is continuous for every

