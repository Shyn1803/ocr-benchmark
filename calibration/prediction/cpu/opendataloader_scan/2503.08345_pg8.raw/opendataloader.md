# 4.3 Spectral analysis

We can now derive specific spectral properties of the Koopman operator that we will leverage for state estimation. Those properties require the following additional assumptions on the nonlinear system (6).

Assumption 3 (stable hyperbolic equilibrium). The dynamics admits a stable equilibrium at the origin, whose basin of attraction contains the polydisc D n . Moreover, the eigenvalues λ j of the Jacobian matrix J F ( 0 ) are simple and satisfy Re( λ j ) < 0 for all j = 1 ,...,n .

Assumption 4 (non-resonant eigenvalues). The eigenvalues λ j of the Jacobian matrix J F ( 0 ) are nonresonant, i.e. for all ( m 1 ,...,m n ) ∈ N n satisfying   n l =1 m l ⩾ 2,

$$
muXl, Vj = 1, l=l
$$

Assumption 5 (output map). The components of the output map h belong to H 2 ( D n ).

Remark 14 Nonresonant eigenvalues are required to rely on the Poincare´-Dulac linearization theorem. However, other linearization theorems exist, with different assumptions, see e.g. the Siegle-Bruno theorem in [Bernard, 2023]. In [Krener and MingQing, 2001], similar assumptions were considered to obtain a necessary and sufficient condition for the existence of a change of variable that linearizes the dynamics up to a nonlinear injection term.

The first remarkable property resulting from those assumptions is the fact that the operators A F and A ∗ F admit a series expansion that allows to represent both operators as infinite matrices.

Lemma 15 For all f ∈ D ( A F ) ,

$$
AF f = ea QENn
$$

= (AFep,€a) AFa,B

PROOF. Since { e α } α ∈ N n is an orthonormal basis of H 2 ( D n ), any f ∈ D ( A F ) can be expanded as f =   β ∈ N n f β e β . Hence, we can prove that

$$
AF = fBAFep. (15) BENn BENn
$$

Indeed, in [Mugisho and Mauroy, 2024], it is shown that the right-hand side is given by

$$
fBAFep BENn BENn (16)
$$

It remains to show that the left-hand side of (15) is also equal to the right-hand side of (16). To do so, consider the operators A 1 and A 2 given by

$$
A1f = Vf and =F W, Azu
$$

for all f ∈ D ( A F ) and ω ∈ (Hol( D n )) n , respectively. Observe that A F = A 2 A 1 on D ( A F ). Moreover, for all f ∈ D ( A F ) and for all l = 1 ,...,n ,

$$
= BENn
$$

Hence, for all f ∈ D ( A F ),

$$
AF f = AzA1f = l=l
$$

In view of (16), it follows that identity (15) holds, which implies that

$$
AF f = (AFf,ea)ea AF ea BENn Q€Nn BENn
$$

It is proved in [Mugisho and Mauroy, 2024] that the infinite matrix representation A F of the operator A F is lower block triangular of the form

$$
[0] [fo] [0] [A11] [0] [f1] AF f (17) [0] [A21] [A22]   [0] [f2]
$$

