Remark 3.15. Another interesting situation is when we have two foliated manifolds (M,FM) and (N,FN), and a local diffeomorphism — say, a covering map — F : M N which sends leaves of FM into leaves of FN, and we want to move affine information between them. Note that F∗ maps FM-vertical vectors into FN-vertical vectors, but not necessarily surjectively. It will become clear that it is necessary that only FM-vertical vectors are mapped into FN-vertical vectors. For example, consider id : R3 R3, where the first R3 is foliated by TF1 = R∂y∂ and the second one is foliated by TF2 = R∂x∂ ⊕R∂y∂ . It is clear that id is a foliated diffeomorphism. The usual flat connection ∇flat of R3 is a transverse affine connection to both foliations, albeit associated with different partner connections ω1 and ω2 (each of them is just ∇flat restricted to the respective vertical distributions). However, id∗∇flat = ∇flat and id∗ω2 = ω2, which does not result in a transverse affine connection in the source foliation.

To achieve our goal, we must require furthermore that FM and FN are of the same dimension, so that vertical vectors on TM are in one-to-one correspondence with the vertical vectors in TN. Indeed, if (N,FN) is endowed with a transverse affine connection ∇ˆ N, we can define the pullback F∗∇ˆ N as follows: for X,Y ∈ X(M), we set (F∗∇ˆ N)XY = Z, where Z is given by: For p ∈ M, let U be any neighborhood of p for which Φ := F|U is a diffeomorphism onto its (open) image. Then, Z(p) := dΦ−p 1 ∇ ˆ NΦ∗XΦ∗Y

. If ωN is the partner connection associated with

Φ(p)

∇ˆ N, then we can check that, for any V ∈ X(FM) and any X ∈ X(M) we have (F∗∇ˆ N)XV = (F∗ωN)XV, (F∗∇ˆ N)V X = [V,X] + (F∗ωN)XV.

As for the holonomy invariance condition, given V ∈ X(FM), and X,Y ∈ L(FM) we have

(LV (F∗∇ˆ N))(X,Y ) = [V,(F∗∇ˆ N)XY ] − (F∗∇ˆ N)[V,X]Y − (F∗∇ˆ N)X[V,Y ]. Note that the two properties that we already established imply that the two last terms above are vertical. As for the first one, note that since F is locally a diffeomorphism, on a neighborhood of each point we can write V = Φ−∗ 1(W) for some W ∈ X(FN). Then we are left with

[V,(F∗∇ˆ N)XY ] = Φ−∗ 1(W),Φ−∗ 1 ∇ ˆ NΦ∗XΦ∗Y = Φ−∗ 1 W,∇ˆ NΦ∗XΦ∗Y ,

which is vertical because ∇ˆ N is a transverse affine connection and Φ∗ stablishes a one-to-one correspondence between vertical vectors.

In the converse direction, if now (M,FM) is given a transverse affine connection ∇ˆ M, the necessary and sufficient condition for the existence of the pushforward via F is that F is oneto-one, (that is, a full diffeomorphism). When this is the case, we can set the pushforward (F∗∇ˆ M)XY = W, for X,Y ∈ X(N), where W is constructed as: given q ∈ N, let U be any neighborhood of p = F−1(q) for which Φ := F|U is a diffeomorphism. Put W(q) := dΦp ∇ ˆ Φ∗XΦ∗Y

. As before, since vertical vectors in TM and in TN are in bijection, we obtain that F∗∇ˆ M is a transverse affine connection with partner connection given by F∗ωM.

p

The next important consistency check arises by considering semi-Riemannian foliations. We show that any one such gives rise to a unique transverse affine structure — a result that works as an analogue of the fundamental theorem of semi-Riemannian geometry.

Theorem 3.16. Let g⊺ be a transverse semi-Riemannian metric on (M,F). There exists a unique transverse affine structure [∇] on (M,F) such that, for any ∇ˆ ∈ [∇]

- (i) the torsion tensor Tor(∇ˆ ) takes values in Γ(TF), and
- (ii) Xg⊺(Y,Z) = g⊺(∇ˆ XY,Z) + g⊺(Y,∇ˆ XZ),∀X,Y,Z ∈ X(M). 15


