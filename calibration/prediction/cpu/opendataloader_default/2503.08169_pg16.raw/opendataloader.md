so that the constants C(n0) > c(n0), given by C2(n0) := max

x∈[−n 1

0+2,n 1

c2(n0) := min

0+2,n 1

x∈[−n 1

(1 − ηx)2 + (σx)2,

0+2]

(1 − ηx)2 + (σx)2,

0+2]

are as upper and lower bounds for Sn(z). Clearly,

2|η| n0 + 2

C2(n0) ≤ 1 +

+ |z|2 (n0 + 2)2 ≤ 1 + |z| n0 + 2

2

,

which, in turn, provides an alternative proof of (4.16) for 2−norm.

We now focus on proving (4.15). Without loss of generality we can assume η ≥ 0. Observe that, with

f(x) := 1 − 2ηx + |z|2x2, it follows that

σ2 σ2 + η2

σ2 |z|2

η σ2 + η2

η |z|2

arg min

f(x) =

=

=: x0, min x∈R

f(x) = f(x0) =

=

.

x∈R

Thus,

 

σ2 |z|2, if x0 ≤ n 1

0+2, f n 1

c2(n0) ≥

0+2 , if x0 > n 1



0+2. Furthermore,

f

1 n0 + 2

2η n0 + 2

= 1 −

σ2 + η2 (n0 + 2)2

η n0 + 2

= 1 −

+

2

σ2 (n0 + 2)2

+

,

which concludes the proof. Finally, (4.17) is a straightforward consequence of (4.15) and (4.16). □

Remark 4.4 Theorem 4.3 implies the stability of the algorithm for any z. Certainly, one might be concerned about the case where 0 < |σ| ≪ |z| due to the factor |z|||σ−1|. Several key observations can be made in this situation. First, if σ is very small, we can incorporate this term into the function f and shift all calculations to the purely oscillatory integral case. On the other hand, if the second-phase algorithm is applied in its current form, we note that the estimate of the norm |(In + 12zMn)−1|2 depends on the distance of z from the discrete set of eigenvalues of Mn. In practice, this distance is often larger than the pessimistic estimate derived in the proof. Therefore, the condition number of the matrix is, in practice, better than the bound established in the theorem for this case. Furthermore, a small increase or decrease in n0 by a few units can resolve any potential ill-conditioning issues.

Finally, we emphasize that our computations never exhibited numerical instability, even in cases where the theorem suggests potential issues. □

16

