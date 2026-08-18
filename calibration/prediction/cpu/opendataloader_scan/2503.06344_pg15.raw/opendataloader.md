Remark 3.15. Another interesting situation is when we have two foliated manifolds ( M, F M ) and ( N, F N ) , and a local diffeomorphism say, a covering map F : M   N which sends leaves of F M into leaves of F N , and we want to move affine information between them. Note that F ∗ maps F M -vertical vectors into F N -vertical vectors, but not necessarily surjectively. It will become clear that it is necessary that only F M -vertical vectors are mapped into F N -vertical vectors. For example, consider id : R 3   R 3 , where the first R 3 is foliated by T F 1 = R ∂ ∂y and the second one is foliated by T F 2 = R ∂ ∂x ⊕ R ∂ ∂y . It is clear that id is a foliated diffeomorphism. The usual flat connection ∇ flat of R 3 is a transverse affine connection to both foliations, albeit associated with different partner connections ω 1 and ω 2 (each of them is just ∇ flat restricted to the respective vertical distributions). However, id ∗ ∇ flat = ∇ flat and id ∗ ω 2 = ω 2 , which does not result in a transverse affine connection in the source foliation. M N

To achieve our goal, we must require furthermore that F and F are of the same dimension, so that vertical vectors on TM are in one-to-one correspondence with the vertical vectors in TN . Indeed, if ( N, F N ) is endowed with a transverse affine connection ˆ ∇ N , we can define the pullback F ∗ ˆ ∇ N as follows: for X,Y ∈ X ( M ) , we set ( F ∗ ˆ ∇ N ) X Y = Z , where Z is given by: For p ∈ M , let U be any neighborhood of p for which Φ : = F | U is a diffeomorphism onto its (open) image. Then, Z ( p ) : = d Φ − 1 p   ˆ ∇ N Φ ∗ X Φ ∗ Y   Φ( p ) . If ω N is the partner connection associated with N M

, then we can check that, for any V ∈ X ( F ) and any X ∈ X ( M ) we have

$$
(F*ĐN)xV = (F*wN)xV (F* 'VN)vX =
$$

As for the holonomy invariance condition, given V ∈ X ( F M ) , and X,Y ∈ L ( F M ) we have

$$

$$

Note that the two properties that we already established imply that the two last terms above are vertical. As for the first one, note that since F is locally a diffeomorphism, on a neighborhood of each point we can write V = Φ − 1 ∗ ( W ) for some W ∈ X ( F N ) . Then we are left with

$$
[V, ( F* 'VN)xY] = 9*1(W), =
$$

correspondence between vertical vectors.

F M ) is given a transverse affine connection ˆ ∇ M , the necessary and sufficient condition for the existence of the pushforward via F is that F is oneto-one, (that is, a full diffeomorphism). When this is the case, we can set the pushforward ( F ∗ ˆ ∇ M ) X Y = W , for X,Y ∈ X ( N ) , where W is constructed as: given q ∈ N , let U be any neighborhood of p = F − 1 ( q ) for which Φ : = F | U is a diffeomorphism. Put W ( q ) : = d Φ p   ˆ ∇ Φ ∗ X Φ ∗ Y   p . As before, since vertical vectors in TM and in TN are in bijection, we obtain that F ∗ ˆ ∇ M is a transverse affine connection with partner connection given by F ∗ ω M .

The next important consistency check arises by considering semi-Riemannian foliations. We show that any one such gives rise to a unique transverse affine structure a result that works as an analogue of the fundamental theorem of semi-Riemannian geometry.

Theorem 3.16. Let g ⊺ be a transverse semi-Riemannian metric on ( M, F ) . There exists a unique transverse affine structure [ ∇ ] on ( M, F ) such that, for any ˆ ∇ ∈ [ ∇ ]

$$

$$

