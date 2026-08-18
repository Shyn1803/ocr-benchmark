where F h ( x ) enumerates independent sets fixed by non-identity elements h ∈ H p . This proves part (ii)(c) of Theorem 3.1.

Proof. Each term b j in the polynomial modulo p counts exactly those independent sets with nontrivial stabilizers. By definition, these are precisely sets that are fixed by some non-identity element h ∈ H p . Thus, summing over non-identity elements gives the generating function for fixed independent sets, proving the equivalence stated in (ii)(c) of Theorem 3.1.

The orbit structure established in Lemma 3.4 implies the modular collapse behavior described in Theorem 3.1.

# 3.3 Algebraic Completion via Frobenius

Building upon the results established in Lemmas 3.3 and 3.1, we now give an algebraic characterization involving polynomial congruences modulo prime divisors of n . This analysis directly ties into the orbit-stabilizer theorem and the modular collapse phenomenon, demonstrating how independent sets are constrained under the action of H p . For prime n , we have established that I ( C ⊠ d ,x ) 1 (mod n ) . For composite n with prime divisor p , the

n ≡ subgroup H p partitions independent sets into orbits of size exactly p , ensuring that the number of such sets satisfies congruences modulo p . This leads to specific conditions under which I ( C ⊠ d n ,x ) exhibits structured congruences.

Frobenius Automorphism and Its Role The Frobenius automorphism , denoted Frob p , is a key tool in understanding the structure of field extensions in characteristic p . It is defined as the mapping:

$$
Frobp aP
$$

for any element a in a field of characteristic p . This automorphism preserves the algebraic structure of the field while raising each element to the power of p , which naturally extends to polynomials and their roots. Applying this iteratively, we obtain:

$$
+1 (mod p)
$$

Polynomial Congruences and Frobenius Completion Let us examine when the congruence I ( C ⊠ d n ,x ) ≡ ( x + 1) m (mod p ) holds for some m ≤ p d :

Proposition 3.5. Let n be composite with prime divisor p . Then I ( C ⊠ d n ,x ) ≡ c · ( x + 1) m (mod p ) for some constant c ∈ F × p and m ≤ p d if and only if the only H p -invariant independent sets are those consisting entirely of vertices fixed point wise by the action of H p .

Proof. Let F p be the set of all independent sets that are fixed by at least one non-identity element of H p . The generating function for these sets is:

$$
F(x) =
$$

By the orbit-stabilizer theorem, each H p -invariant independent set belongs to an orbit whose size divides p , leading to constraints on I ( C ⊠ d n ,x ) . When F p contains only independent sets consisting of vertices fixed point wise by H p , F ( x ) takes the form ( x +1) m − 1 for some m ≤ p d , representing all possible subsets of the fixed vertex set minus the empty set. Under these conditions, we have:

Under these conditions; we have:

$$
(mod p)
$$

Conversely; if implying that the only invariant sets are those built from fixed vertices-

Applying the Frobenius automorphism, we recall:

