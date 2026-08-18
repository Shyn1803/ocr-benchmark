so that the constants C ( n 0 ) > c ( n 0 ), given by

$$
C2 (no) = max (1 _ c2 (no) min n0 +2] 70+2
$$

$$

$$

$$

$$

are as upper and lower bounds for S n ( z ).

Clearly,

$$
2/l |z/2 Iz| C2(n0) < 1 + 1+ no + 2 no + 2
$$

which, in turn, provides an alternative proof of (4.16) for 2 − norm.

We now focus on proving (4.15). Without loss of generality we can assume η ≥ 0. Observe that, with

$$
f(s) := 1
$$

it follows that

$$
arg min f (x) = 02 + n2 |z12 02 + n2 02
$$

Thus,

Furthermore,

$$
if so no+2 c2 (no) > no+2
$$

$$
2n 02 + n2 =1 _ 1 _ no + 2 (no + 2)2 no (n0 + 2)2 +2
$$

which concludes the proof.

Finally, (4.17) is a straightforward consequence of (4.15) and (4.16).

Remark 4.4 Theorem 4.3 implies the stability of the algorithm for any z . Certainly, one might be concerned about the case where 0 < | σ | ≪ | z | due to the factor | z ||| σ − 1 | . Several key observations can be made in this situation. First, if σ is very small, we can incorporate this term into the function f and shift all calculations to the purely oscillatory integral case. On the other hand, if the second-phase algorithm is applied in its current form, we note that the estimate of the norm | (I n + 1 2 z M n ) − 1 | 2 depends on the distance of z from the discrete set of eigenvalues of M n . In practice, this distance is often larger than the pessimistic estimate derived in the proof. Therefore, the condition number of the matrix is, in practice, better than the bound established in the theorem for this case. Furthermore, a small increase or decrease in n 0 by a few units can resolve any potential ill-conditioning issues.

Finally, we emphasize that our computations never exhibited numerical instability, even in cases where the theorem suggests potential issues. □

