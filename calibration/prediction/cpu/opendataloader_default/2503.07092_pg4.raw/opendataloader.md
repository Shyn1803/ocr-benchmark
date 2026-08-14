deﬁne the set S ⊆ {1,2,...,n}×{1,2,...,f+g},and assume the entry Atrue Btrue

is given for all (i,j) ∈ S.

ij

The set of systems compatible with the prior knowledge is given by

Σpk(S) := (A,B) | A B

= Atrue Btrue

ij

∀(i,j) ∈ S .

ij

(6)

Subsequently, we deﬁne the set of systems compatible with both the data and the prior knowledge as

Σ := Σd ∩ Σpk(S). (7)

Note that the case that all entries of Atrue and Btrue are unknown can be captured by setting S = ∅, which implies Σ = Σd. It is clear from (2) and (6) that the system (Atrue,Btrue) belongs to Σ. However, in general, Σ contains other systems because the data may not uniquely determine Atrue and Btrue, even if some entries of Atrue and Btrue are known.

The goal of this paper is to ﬁnd a controller that stabilizes the origin of the system (Atrue,Btrue). Since on the basis of the data and the prior knowledge we cannot distinguish between (Atrue,Btrue) and any other system in Σ, we need to ﬁnd a single controller that stabilizes the origin of all systems in Σ. This motivates the following deﬁnition of informative data for stabilization of polynomial systems. In the rest of the paper, we assume that

F(0) = 0.

Deﬁnition 1 The data (X˙,X,U) are called informative for stabilization if there exist a radially unbounded function V ∈ V and a continuous controller K : Rn → Rm such that K(0) = 0 and

∂V (x) ∂x

(AF(x)+BG(x)K(x)) < 0 ∀x ∈ Rn\{0}, (8) for all (A,B) ∈ Σ. Note that for a controller K satisfying K(0) = 0, the origin of the closed-loop system

![](<2503.07092_pg4_images/imageFile1.png>)

x˙ = AF(x) + BG(x)K(x), (9)

is an equilibrium point, as F(0) = 0. If (8) holds then the origin is globally asymptotically stable for all closedloop systems obtained by interconnecting any system (A,B) ∈ Σ with the controller u = K(x).

In this paper, we study the following two problems.

Problem 1 (Informativity) Find conditions under which the data (X˙,X,U) are informative for stabilization.

Problem 2 (Controller design) Suppose the data (X˙,X,U) are informative for stabilization. Find a controller u = K(x) satisfying K(0) = 0 and (8).

3 Connection to previous work

Current approaches for data-driven control of polynomial systems [8,9] build on the model-based method proposed in [15]. These methods do not incorporate prior knowledge and instead focus on designing a common stabilizing controller for all systems compatible with the data. In these works, the controller is considered to be of the form

K(x) = Y (x)PZ(x), where Y ∈ Rm×p[x], P ∈ Sp is positive deﬁnite, and Z ∈ Rp[x] is radially unbounded satisfying

F(x) = H(x)Z(x), (10)

for some H ∈ Rf×p[x]. The choice of candidate Lyapunov function

V (x) = Z⊤(x)PZ(x), (11) then leads to

∂V ∂x

(x)(AF(x) + BG(x)K(x)) = 2Z⊤(x)PΘ(x)PZ(x),

![](<2503.07092_pg4_images/imageFile2.png>)

where

∂Z ∂x

(x) A B

Θ(x) :=

![](<2503.07092_pg4_images/imageFile3.png>)

H(x)P−1 G(x)Y (x)

.

The main idea in this line of work is to ﬁnd P and Y (x) such that

−Θ(x) − Θ⊤(x) > 0 ∀x ∈ Rn \ {0}, (12)

for all systems (A,B) compatible with the data. In the earlier work [8], H(x) is taken to be equal to the identity matrix, which implies that Z(x) = F(x). In contrast, [9] considers more general Z(x) satisfying (10). This strategy is appealing because it leads to data-based linear matrix inequalities for control design. Unfortunately, however, the method also has some major limitations.

(1) The matrix ∂Z∂x (x) must have full row rank for all x ∈ Rn \ {0}.

![](<2503.07092_pg4_images/imageFile4.png>)

Indeed, suppose that there exists a nonzero x

such that ∂Z∂x (x) does not have full row rank. Then Θ(x) is singular, which implies that (12) does not

![](<2503.07092_pg4_images/imageFile5.png>)

hold. Note that the full row rank condition can only hold if p ≤ n, i.e., the number of polynomials in Z is less than or equal to the state-space dimension of the system. This limits the class of Lyapunov functions of the form (11) that can be considered by the

4

