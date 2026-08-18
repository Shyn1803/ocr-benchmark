where the constant c is independent of A and n (but does depend on the dimension of Ran( P )). We use that   ∞ 1 t s − 2 dt < ∞ for s < 1 to bound the second term. Thus, there exists a constant C ( s ) such that

$$

$$

for all maximally dissipative A , where C ( s ) is independent of n and Ran( P ). Using that   n ∈ Z 1 1+( | n |− 1) 2 < ∞ , we can therefore bound the right hand side of ( 9 ) for all | z | > 1. If | z | < 1, we drop a minus sign in both norms in ( 9 ) and use that i   F z and i   F − 1 z are dissipative. Repeating the arguments from above yields the bound for all | z | < 1. ( i ) ( j )

The case x = y is significantly easier: We can directly take α = ω x and do not need β . The operators F z and   F z act on C 3 , while all other estimates still hold. The integrals in ( 9 ) can be similarly bounded by Lemma 1 .

We state a simplified version of Lemma 3.1 from [ 3 ], which we use to bound the integrals in the proof of Theorem 2 .

Lemma 1. Let H be a separable Hilbert space, A be a maximally dissipative operator with strictly positive imaginary part and M 1 ,M 2 : H → H be Hilbert-Schmidt operators. Then there exists a constant c independent of A , M 1 and M 2 such that for any t > 0 :

$$
1 {x € Rs.t. IIM1 (A + t 2) ~1
$$

where | · | denotes the Lebesgue measure.

# 4.2 The boundary of a box

We want to define a ”box” Λ L for any size L ∈ N 2 , whose sides have lengths L 1 and L 2 , such that the Quantum Walker is unable to cross the boundary of Λ L . Restricting the Walker to some box Λ L is achieved by changing the coin matrix at specific lattice sites on the boundary of Λ L . In other words, we want to obtain unitary operators U ( L ) ω = U Λ L ω ⊕ U Λ C L ω and subspaces H L ⊕ H C L = H such that H L , respectively H C L , are invariant under U Λ L ω , respectively U Λ C L ω . Note that we call a subspace H ′ ⊂ H invariant under U if U H ′ ⊂ H ′ . Recalling the definition of H j,k ( 4 ), we use that C 0 induces a fully localized Quantum Walk, see section 2 , and define the invariant subspaces:

$$
HL = H HL. <k<L2 -1 j+k>-L1-L2 Hj,k ~L2
$$

The choice j + k > − L 1 − L 2 is not necessary, but simplifies the structure of Λ L , see Figure 3 . We call the number of Γ A -vertices in Λ L the volume of Λ L , that is:

$$
vol (AL) = 4L1L2 = 1 and IL| = + (10)
$$

To obtain a Quantum Walk such that these two subspaces are invariant, we need to change the coin matrix at specific lattice sites from C to C 0 . In particular, we use the coin matrix C 0 at all Γ B sites in

$$
S.t. Or Or (j = L1, ~L2 < k < L2 = 2) Or
$$

