In this manuscript, we investigate Finslerian exponentially harmonic functions. Analogous to the Riemannian case, a function u deﬁned on a Finsler metric measure space (M,F,µ) is said to be exponentially harmonic if it satisﬁes

∆˜µu := divµ(V (u)Du) = 0, (1.1)

where V (u) = exp(12F∗2(Du)) represents the energy density of u. Such a function arises as a critical point of the exponential energy functional (see Theorem 3.1). Finsler

![](<2503.07623_pg2_images/imageFile1.png>)

metric measure spaces encompass a richer set of geometric tensors compared to Riemannian manifolds (cf. [11]). It is important to emphasize that (1.1) is not merely a quasilinear elliptic equation, as the underlying space is an anisotropic and asymmetric manifold. Within this framework, we establish the following theorem.

Theorem 1.1. Let (M,F,µ) be a forward complete n-dimensional Finsler metric measure space with ﬁnite misalignment α. Assume that the mixed weighted Ricci curvature mRic∞ of M is nonnegative, and that the S-curvature as well as the nonRiemannian curvatures U, T and divC = FCijk|idxj ⊗ dxk satisfy the norm bound F−1|S|+F(U)+F(T )+ divC HS(V ) ≤ K0, for any (x,V ) ∈ SM. Then, any bounded exponentially harmonic function u on M is constant.

# 2 Related concepts and notations of the Finsler metric measure spaces

A Finsler metric measure space is a triple (M,F,µ), where M is a diﬀerentiable manifold equipped with a Finsler metric F and a Borel measure µ. The Cartan tensor is deﬁned by

∂3F2(x,y) ∂yi∂yj∂yk

1 4

XiY jZk,

C(X,Y,Z) := CijkXiY jZk =

![](<2503.07623_pg2_images/imageFile2.png>)

![](<2503.07623_pg2_images/imageFile3.png>)

for any local vector ﬁelds X,Y,Z. We always adopt the Chern connection, which is uniquely determined by

∇XY − ∇Y X = [X,Y ]; Z(gy(X,Y )) − gy(∇ZX,Y )−gy(X,∇ZY ) = 2Cy(∇Zy,X,Y ),

for any X,Y,Z ∈ TM \ {0}, where Cy is the Cartan tensor. The coeﬃcients of the Chern connection are locally expressed as Γijk(x,y) in natural coordinates. These coeﬃcients induce the spray coeﬃcients as Gi = 12Γijkyjyk. The spray is given by

![](<2503.07623_pg2_images/imageFile4.png>)

δ δxi

G = yi

![](<2503.07623_pg2_images/imageFile5.png>)

∂ ∂xi − 2Gi

= yi

![](<2503.07623_pg2_images/imageFile6.png>)

∂ ∂yi

, (2.1)

![](<2503.07623_pg2_images/imageFile7.png>)

where δxδi = ∂x∂i − Nij ∂y∂j , and the nonlinear connection coeﬃcients Nji are locally derived from the spray coeﬃcients as Nji = ∂G

![](<2503.07623_pg2_images/imageFile8.png>)

![](<2503.07623_pg2_images/imageFile9.png>)

![](<2503.07623_pg2_images/imageFile10.png>)

i

∂yj . By convention, the horizontal Chern derivative is denoted by “|” and the vertical Chern derivative by “;”. Let Dˆ denote the Levi-Civita connection of the induced Riemannian metric gˆ = gY , and let {ei}

![](<2503.07623_pg2_images/imageFile11.png>)

2

