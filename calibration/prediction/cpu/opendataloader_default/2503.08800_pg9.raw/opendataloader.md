DIOPHANTINE ENUMERATION OF DYNKIN FRIEZES 9

Remark 2.10. In Proposition 2.8 and all of our computation examples, there is a

symmetry between the xi and yi coordinates of X∆n(N2n) for all i. Antoine de SaintGermain has kindly pointed out to the second author that the xi → yi direction of this symmetry has the following names in diﬀerent contexts:

- • the Auslander–Reiten translate in ﬁnite-dimensional representation theory;
- • the Fomin–Zelevinsky twist in Lie theory (cf. [dSG23, §5.6];
- • the Donaldson–Thomas transformation in Calabi–Yau theory;
- • the maximal green sequence in combinatorics.


2.4. Eﬀective bounds. As before, let A∆n = (ai,j) be a Cartan matrix for Dynkin type ∆n. Denote its inverse by A−∆1

= (a−i,j1). Deﬁne the following associated values:

n

n

bi,∆n :=

j=1

n

ci,∆n :=

j=1

−1 i,j

2a

1 + 2 k =i aj,k a−i,j1.

Muller [Mul23, Proposition 2.3 and Example 3.1] gives bounds on frieze entries in terms of these values.

Lemma 2.11. [Mul23, Proposition 2.3 and Example 3.1] Let F be a positive integral ∆n-frieze. Then there is the following upper bound on the product of entries in its i-th row: Pj=∆1n Fi,j ≤ bPi,∆∆n

. Furthermore, if all entries in F are at least 2, then

n

P∆n j=1 Fi,j ≤ cPi,∆∆n

.

n

Remark 2.12. There is a misprint in [Mul23, Example 3.1]: the bound (15187516384 )16 ≈ 251 on the eighth row of an E8-frieze should be c168,E

![](<2503.08800_pg9_images/imageFile1.png>)

= (177347025604248046875144115188075855872 )16 ≈ 2164. An immediate consequence of Lemma 2.11 and Proposition 2.3 is that if the frieze

![](<2503.08800_pg9_images/imageFile2.png>)

8

F corresponds to the point (x1,... ,xn;y1,... ,yn) ∈ X∆n(N2n), then xi ≤ bPi,∆∆n

. Furthermore, if all entries in F are at least 2, then xi ≤ cPi,∆∆n

n

.

n

The Diophantine model of friezes allows us to ﬁnd a minimal element in each Z/P∆nZ-orbit on which we can reduce existing bounds by a power of P1

.

![](<2503.08800_pg9_images/imageFile3.png>)

∆n

Proposition 2.13. Let F be a positive integral ∆n-frieze and ﬁx an i ∈ {1,... ,n}. There is a ∆n-frieze F′ corresponding to (x1,... ,xn;y1,... ,yn) ∈ X∆n(N2n) such that F is a horizontal translation of F′ and xi ≤ bi,∆n. Furthermore, if all entries in F are at least 2, then xi ≤ ci,∆n.

Proof. Each ∆n-frieze F is a horizontal translation of a frieze F′ in its Z/P∆nZ-orbit such that Fi,1′ ≤ Fi,j′ for all 1 ≤ j ≤ P∆n. By Lemma 2.11, there is a bound on

P∆n j=1 Fi,j′ ≤ bPi,∆∆n

. But xi = Fi,1′ is the smallest factor in the product of P∆n-many terms, hence xi ≤ bi,∆n. If the entries of F are all at least 2, then the entries of the translation F′ are also all at least 2. Hence the same argument gives the bound in terms of ci,∆n instead of bi,∆n.

n

