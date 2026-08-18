# C. Orthogonality Condition for Base Matrices

A necessary and sufficient condition for a pair of QC-LDPC codes to satisfy the symplectic inner product condition is given in [29]. We revisit the even multiplicity condition described therein first. Definition 1 (Even multiplicity): A vector is said to have even multiplicity if, for every integer ,

Definition (Even multiplicity): A vector / = is said to have even multiplicity if, for every integer k € Z, the number of indices i € {1,2, n such that /; = k is even.

By definition; the vector has even multiplicity if each integer entry in / appears an even number of times while discounting the -0 entries Or the empty cells if any.

B m × n L , where the entries b i,j ∈ { ∞ , 0 , 1 ,...,L − 1 } . Define the i -th row vector r i for i = 1 , 2 ,...,m as r i =   b i, 1 , b i, 2 , ··· , b i,n   . If the moduloL difference of any two distinct rows r i and r j : i.e., r = r i − r j , moduloL , has even multiplicity, then the corresponding binary matrices after lifting   ( r i ) and   ( r j ) are orthogonal [29], [30]. The minus − operation is performed moduloL and for the ∞ entries is as follows: b i,j − ∞ = ∞ − b i,j = ∞ − ∞ := −∞ . Theorem 1: LP-QLDPC code PCMs H and H are orthogonal if the rows of quasi-cyclic base matrices B and B have

Theorem I: LP-QLDPC code PCMs Hx and Hz are orthogonal if the rows of quasi-cyclic base matrices Bx and Bz have even multiplicity.

multiplicity property for the base matrices B X and B Z . Their rows obey the condition for orthogonality the even multiplicity of integers in the moduloL differences of the rows, where L is the circulant size. Take any pair of rows such that r i is taken from B X , and r j from B Z . These rows can be split based on the left part and right part with exactly one overlap in each of the parts. Thus, the difference r = r i − r j , moduloL will only have two integer terms. Suppose that the two overlapping terms are equal; then, the resulting difference vector has a pair of zeros. If the overlapping terms p and q are not equal, p ̸ = q , then the corresponding terms in the difference appear as p − q and q ∗ − p ∗ , respectively. Since the conjugate terms are q ∗ = L − q and p ∗ = L − p , the overlapping terms are indeed equal, satisfying the even multiplicity condition. Therefore, the two parity check matrices are orthogonal to each other. □

# IV. M INIMUM D ISTANCE OF LP-QLDPC C ODES

In the following, we examine the symmetric LP-QLDPC codes constructed from type-1 quasi-cyclic base matrices to understand how certain combinations of CPM values reduce the quantum minimum distance d Q min from the minimum distance of the base code d C min . We first show how the minimum distance is limited to the Hamming weight of the stabilizer generators. We also prove that using a base matrix with only two rows ( m = 2 as in Eq. (11)) always limits the LP-QLDPC code to have a minimum distance d Q min ≤ n +2 . In general, we are interested in the following question: What constraints on the base code of an LP-QLDPC code reduce its minimum distance? This will guide us toward code construction recipes guarantee degeneracy for the obtained LP-QLDPC code. First, we provide examples of the choices of base codes of different sizes: m and n to demonstrate the reduction of the minimum distance of LP-QLDPC codes.

Example 1 Continued: Consider the LP-QLDPC code constructed from the example base matrix we saw earlier with m

$$
1 2 B = (23) 6 5 3
$$

We start with a classical LDPC code C : [21 , 8 , 6] . Hence, the desired minimum distance of LP code is d C min = 6 . However, we verified that the d Q min = m + n = 5 . Note that for quasi-cyclic base matrices, it is enough to look at equivalent base matrices expressed in canonical form. Two base matrices are equivalent if their respective Tanner graphs are identical upon variable and/or check node permutations. Given a base matrix, B exchanging rows/columns, or adding a fixed integer to each element in row/column maintains equivalence. The rows and columns of the quasi-cyclic code can be reordered to put 0s in the first row and column to make an equivalent parity check matrix making the analysis easier. For instance, we have the equivalent matrix 0 0 0

$$
0 0 0 B = (24 0 1 3
$$

Example 2: Classical code C : [104 , 30 , 14] with the base matrix given in Example 3 of [18]. We obtain the base matrix for the classical LDPC code C : [104 , 30 , 14] . The base matrix B in Eq. (25) corresponds to a (3 , 4) regular LDPC code with circulant size L = 26 . The minimum distance of the base code is d C min = 14 .

$$
B = 6 10 (25) 0 8 14 22
$$

We now construct a symmetric LP-QLDPC code from Eq. (25) to get a [[650, 50, 7]] code. Here, we have N = 26 × (3 2 +4 2 ) physical qubits encoding K = 50 logical qubits with a minimum distance d Q min = 7 instead of 14. Note that the quantum minimum distance is again equal to m + n .

