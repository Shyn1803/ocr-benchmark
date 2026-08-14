with global minima at index i0 there are exactly ii0=1−1(k − 1)ki−1 descents by Theorem 5.3. The number of inversions can be expressed through the values of the permutation before the minimum: I(k,n,w) = k

n(k−1) 4

n(k−1) 4

n i=1(kn−i − kn−i−(cw)i) = k

i0−1 i=1 (kn−i − kn−i−wi+1).

Now, we describe some bounds on the number of descents and inversion in the stable configuration depending on the permutation. We start with permutations with an increasing tail.

Proposition 6.1. Given permutation w, if there exists an i0 ∈ N such that for all indices i ≥ i0, we

have wi < wi+1, then Ck,n,w has at most ij0=1−1(k −1)kj−1 descents and at most k2 ii0=1−1 ki−1 kn2−i inversions.

Proof. Because wi < wi+1 for all integers i such that i ≥ i0, we find that (cw)i = 0 for all i ≥ i0. Therefore, the support of cw is a subset of [i0 − 1]. Thus, by Theorem 5.3, we have that there are at most ij0=1−1(k − 1)kj−1 descents in Ck,n,w.

Because (cw)i = 0 for all i ≥ i0, we have

i0−1

i0−1

k(cw)i 2

k − 1 4

k 2

(k2n−i − k2n−i−(cw)i).

k2n−2i−2(cw)i =

ki−1

I(k,n,w) =

i=1

i=1

Since for each i, we have (cw)i ≤ n − i by definition of Lehmer code, we obtain

i0−1

i0−1

i0−1

kn−i 2

kn(k − 1) 4

k(k − 1) 4

k 2

(kn−i−kn−i−(n−i)) =

kn−1(kn−i−1) =

ki−1

I(k,n,w) ≤

.

i=1

i=1

i=1

<table>
  <tr>
    <td> </td>
  </tr>
</table>


One can observe that the upper bounds on the number of inversions and descents in Proposition 6.1 are tight.

Example 24. Consider any positive integers i0,n,k such that i0 < n and k ≥ 2. Let w be a permutation in Sn defined by wi = n+1−i for i ∈ [i0−1] and wi = i−i0+1 for i ∈ {i0,i0+1,...,n}. This is a special case of a valley permutation, where the increasing part consists of smaller numbers than the decreasing part. We obtain that the Lehmer code of this permutation is (cw)j = n − i for each i ∈ [i0 − 1] and (cw)i = 0 for i ∈ {i + 1,i + 2,...,n}. Therefore we obtain from Theorem 4.1 that the number of inversions in the stable configuration Ck,n,w resulting from firing strategy Fw is

i0−1 i=1 ki−1 kn2−i . This is exactly the upper bound on the number of inversions in Ck,n,w for w

k 2

with increasing tail starting at i0. Also observe that Theorem 5.3 and the fact that supp(cw) = [i0 −1] imply that Ck,n,w has exactly

i0−1 i=1 (k − 1)kk−1 descents. This is equal to the upper bound on the number of descents in Ck,n,w

from Proposition 6.1.

On a similar note, we calculate the lower bound for the number of inversions and descents in Ck,n,w in the case where w has a decreasing tail.

20

