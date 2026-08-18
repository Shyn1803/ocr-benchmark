Remark 2.10 . In Proposition 2.8 and all of our computation examples, there is a symmetry between the x i and y i coordinates of X ∆ n ( N 2n ) for all i . Antoine de SaintGermain has kindly pointed out to the second author that the x i   → y i direction of this symmetry has the following names in diﬀerent contexts:

the Auslander–Reiten translate in ﬁnite-dimensional representation theory; the Fomin–Zelevinsky twist in Lie theory (cf. [dSG23, §5.6];

the Fomin-Zelevinsky twist in Lie theory (cf. [dSG23, 85.6];

the Donaldson–Thomas transformation in Calabi–Yau theory;

the maximal green sequence in combinatorics.

2.4. Eﬀective bounds. As before, let A ∆ n = ( a i,j ) be a Cartan matrix for Dynkin type ∆ n . Denote its inverse by A − 1 ∆ n = ( a − 1 i,j ) . Deﬁne the following associated values:

$$

$$

$$
= j=1 aj,k bi,An Ci,An
$$

$$
j=1
$$

Muller [Mul23, Proposition 2.3 and Example 3.1] gives bounds on frieze entries in terms of these values.

Lemma 2.11 . [Mul23, Proposition 2.3 and Example 3.1] Let F be a positive integral ∆ n -frieze. Then there is the following upper bound on the product of entries in its i -th row:   P ∆ n j = 1 F i,j ≤ b P ∆ n i,∆ n . Furthermore, if all entries in F are at least 2 , then   P ∆ n j = 1 F i,j ≤ c P ∆ n i,∆ n .

Remark 2.12 . There is a misprint in [Mul23, Example 3.1]: the bound ( 151875 16384 ) 16 ≈ 2 51 on the eighth row of an E 8 -frieze should be c 16 8,E 8 = ( 177347025604248046875 144115188075855872 ) 16 ≈ 2 164 .

An immediate consequence of Lemma 2.11 and Proposition 2.3 is that if the frieze F corresponds to the point ( x 1 ,... ,x n ; y 1 ,... ,y n ) ∈ X ∆ n ( N 2n ) , then x i ≤ b P ∆ n i,∆ n . Furthermore, if all entries in F are at least 2 , then x i ≤ c P ∆ n i,∆ n . The Diophantine model of friezes allows us to ﬁnd a minimal element in each

Z /P ∆ n Z -orbit on which we can reduce existing bounds by a power of P

Proposition 2.13 . Let F be a positive integral ∆ n -frieze and ﬁx an i ∈ { 1,... ,n } . There is a ∆ n -frieze F ′ corresponding to ( x 1 ,... ,x n ; y 1 ,... ,y n ) ∈ X ∆ n ( N 2n ) such that F is a horizontal translation of F ′ and x i ≤ b i,∆ n . Furthermore, if all entries in F are at least 2 , then x i ≤ c i,∆ n .

Proof. Each ∆ n -frieze F is a horizontal translation of a frieze F ′ in its Z /P ∆ n Z -orbit such that F ′ i,1 ≤ F ′ i,j for all 1 ≤ j ≤ P ∆ n . By Lemma 2.11, there is a bound on   P ∆ n j = 1 F ′ i,j ≤ b P ∆ n i,∆ n . But x i = F ′ i,1 is the smallest factor in the product of P ∆ n -many terms, hence x i ≤ b i,∆ n . If the entries of F are all at least 2 , then the entries of the translation F ′ are also all at least 2 . Hence the same argument gives the bound in terms of c i,∆ n instead of b i,∆ n .  

