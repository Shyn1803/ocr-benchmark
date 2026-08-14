Proof. In the first case, we set vp = (∇X|p)−1wp and apply the Cauchy-Schwarz inequality to obtain

X,vp⟩ = ⟨wp,(∇X|p)−1wp⟩ ≤ ∥(∇X|p)−1∥∥wp∥2 = ∥(∇X|p)−1∥∥∇vp

X|∥2

⟨∇vp

so −supp∈U ∥(∇X|p)−1∥ can be taken as an upper bound for αp. In the second case, we choose vp = rp + βnp where rp ∈ Range(∇X|∗p), β ∈ R and np ∈ ker(∇X|p) ̸= 0. Then, the condition (25) reads

X∥2 where β is arbitrary. Therefore, it is necessary that ⟨∇rp

⟨∇rp

X,rp⟩ + β⟨∇rp

X,np⟩ ≤ −α∥∇rp

X,np⟩ = 0 which is true for all choices of rp and np if and only if ∇rp

X ∈ Range(∇X|∗p). By definition, the set of all ∇rp

X|p is precisely Range(∇X|p), so we conclude that one must have Range(∇X|p) = Range(∇X|∗p). The proof is completed in the same way as in the non-singular case, by restricting ∇X|p to Range(∇X|∗p).

<table>
  <tr>
    <td> </td>
  </tr>
</table>


Note that this proposition does not ensure that the vector field X is cocoercive since it might happen (as in the bound of the proof) that α < 0.

A coordinate formula for the cocoercivity constant. We give a concrete formula for the cocoercivity constant when it exists. Suppose we have introduced local coordinates x1,...,xd. Now g is to be interpreted as a d × d matrix with elements gij = ⟨∂xi,∂xj⟩. The matrix of the operator ∇X|p is denoted AX,p. We assume that we can compute its reduced singular value decomposition AX,p = UΣV T where U,V ∈ Rd×r have orthonormal columns and Σ ∈ Rr×r is diagonal and positive definite and where r is the rank of AX,p. Thanks to Proposition 12 we can write U = V Q where Q is orthogonal and r × r, i.e. Q = V TU. We are interested in finding the largest possible αp such that

vpTgAX,pvp ≤ −αpvpTATX,pgAX,pvp, ∀vp ∈ Rd It is easy to show that −αp can be chosen as the largest eigenvalue

M + MT 2

−αp = max

λi

1≤i≤d

with

- 1

- 2 , g˜ = UTgU.


- 1

- 2 Σ−1 V TU g˜


M = g˜− To find α it suffices to maximize αp over the domain U ⊂ M. Formulas for µ+ and µ− in Theorems 6 and 9 can be derived similarly. In the case of ∇X non-singular, we obtain

M− + M−T 2

M+ + M+T 2

µ+ = λmax

, µ− = λmax

,

where λmax(A) denotes the maximum eigenvalue A and with M+ = −G1/2(I − PX)∇X−1G−1/2, M− = −G1/2PX∇X−1G−1/2.

25

