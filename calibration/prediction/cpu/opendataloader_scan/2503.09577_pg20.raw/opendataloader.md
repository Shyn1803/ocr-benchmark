descents by Theorem 5.3. The number of inversions can be expressed through the values of the permutation before the minimum: I(k, n, w) = (kn-i kn-i-(cw)i) kn (k_1)

Now, we describe some bounds on the number of descents and inversion in the stable configuration depending on the permutation. We start with permutations with an increasing tail.

Proposition 6.1. Given permutation w , if there exists an i 0 ∈ N such that for all indices i ≥ i 0 , we have w i < w i +1 , then C k,n,w has at most   i 0 − 1 j =1 ( k − 1) k j − 1 descents and at most   k 2     i 0 − 1 i =1 k i − 1   k n − i 2   inversions.

Proof. Because w i < w i +1 for all integers i such that i ≥ i 0 , we find that ( c w ) i = 0 for all i ≥ i 0 . Therefore, the support of c w is a subset of [ i 0 − 1]. Thus, by Theorem 5.3, we have that there are at most   i 0 − 1 j =1 ( k − 1) k j − 1 descents in C k,n,w .

Because ( c w ) i = 0 for all i ≥ i 0 , we have

$$
io =1 io =1 k k _ 1 I(k, n, w) = ki_1 (cw)i 2 2 i=1 ( k(cw)i (k2n-i k2n-i _
$$

Since for each i , we have ( c w ) i ≤ n − i by definition of Lehmer code, we obtain

$$
io =1 I(k, n, w) k" (k = 1) ~k"-i-(n-i)) = k(k = 1) ki-1 2 2 1=1 i=1 ( kn (kn-i
$$

One can observe that the upper bounds on the number of inversions and descents in Proposition 6.1 are tight.

Example 24. Consider any positive integers i 0 ,n,k such that i 0 < n and k ≥ 2. Let w be a permutation in S n defined by w i = n +1 − i for i ∈ [ i 0 − 1] and w i = i − i 0 +1 for i ∈ { i 0 ,i 0 +1 ,...,n } . This is a special case of a valley permutation, where the increasing part consists of smaller numbers than the decreasing part. We obtain that the Lehmer code of this permutation is ( c w ) j = n − i for each i ∈ [ i 0 − 1] and ( c w ) i = 0 for i ∈ { i + 1 ,i + 2 ,...,n } . Therefore we obtain from Theorem 4.1 that the number of inversions in the stable configuration C k,n,w resulting from firing strategy F w is   k 2     i 0 − 1 i =1 k i − 1   k n − i 2   . This is exactly the upper bound on the number of inversions in C k,n,w for w with increasing tail starting at i 0 .

Also observe that Theorem 5.3 and the fact that supp( c w ) = [ i 0 − 1] imply that C k,n,w has exactly   i 0 − 1 i =1 ( k − 1) k k − 1 descents. This is equal to the upper bound on the number of descents in C k,n,w from Proposition 6.1.

On a similar note, we calculate the lower C k,n,w in the case where w has a decreasing tail.

