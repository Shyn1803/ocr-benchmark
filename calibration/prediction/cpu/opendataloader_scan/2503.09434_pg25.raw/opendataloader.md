Proof. In the first case, we set v p = ( ∇ X | p ) − 1 w p and apply the Cauchy-Schwarz inequality to obtain

$$
XIII2
$$

$$
Up X, vp)
$$

∈U In the second case, we choose v p = r p + βn p where r p ∈ Range( ∇ X | ∗ p ), β ∈ R and n p ∈ ker( ∇ X | p ) ̸ = 0. Then, the condition (25) reads

$$
Tp
$$

where β is arbitrary. Therefore, it is necessary that ⟨∇ r p X,n p ⟩ = 0 which is true for all choices of r p and n p if and only if ∇ r p X ∈ Range( ∇ X | ∗ p ). By definition, the set of all ∇ r p X | p is precisely Range( ∇ X | p ), so we conclude that one must have Range( ∇ X | p ) = Range( ∇ X | ∗ p ). The proof is completed in the same way as in the non-singular case, by restricting ∇ X | p to Range( ∇ X | ∗ p ).

Note that this proposition does not ensure that the vector field X is cocoercive since it might happen (as in the bound of the proof) that α < 0.

A coordinate formula for the cocoercivity constant. We give a concrete formula for the cocoercivity constant when it exists. Suppose we have introduced local coordinates x 1 ,...,x d . Now g is to be interpreted as a d × d matrix with elements g ij = ⟨ ∂x i ,∂x j ⟩ . The matrix of the operator ∇ X | p is denoted A X,p . We assume that we can compute its reduced singular value decomposition A X,p = U Σ V T where U,V ∈ R d × r have orthonormal columns and Σ ∈ R r × r is diagonal and positive definite and where r is the rank of A X,p . Thanks to Proposition 12 we can write U = V Q where Q is orthogonal and r × r , i.e. Q = V T U . We are interested in finding the largest possible α p such that

$$
~@pvp € Rd Vvp
$$

It is easy to show that − α p can be chosen as the largest eigenvalue

$$
M + ~Qp max )i I<i<d MT
$$

with

$$

$$

To find α it suffices to maximize α p over the domain U ⊂ M .

Formulas for µ + and µ − in Theorems 6 and 9 can be derived similarly. In the case of ∇ X non-singular, we obtain

$$
M+ + ME M _ + M _ = Amax 2 2 Amax
$$

where λ max ( A ) denotes the maximum eigenvalue A and with

$$
M+ = ~G1/2(1 _ Px) VX-'G-1/2 , M _ = ~G1/2 Px VX-1G-1/2
$$

