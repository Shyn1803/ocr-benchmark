deﬁne the set S ⊆ { 1 , 2 ,...,n }×{ 1 , 2 ,...,f + g } ,and assume the entry   A true B true   ij is given for all ( i,j ) ∈ S . The set of systems compatible with the prior knowledge is given by

$$
(A,B) | (6) Atrue V(i,j) € s} ij ij Btrue
$$

Subsequently, we deﬁne the set of systems compatible with both the data and the prior knowledge as

$$

$$

Note that the case that all entries of A true and B true are unknown can be captured by setting S = ∅ , which implies Σ = Σ d . It is clear from (2) and (6) that the system ( A true ,B true ) belongs to Σ. However, in general, Σ contains other systems because the data may not uniquely determine A true and B true , even if some entries of A true and B true are known.

The goal of this paper is to ﬁnd a controller that stabilizes the origin of the system ( A true ,B true ). Since on the basis of the data and the prior knowledge we cannot distinguish between ( A true ,B true ) and any other system in Σ, we need to ﬁnd a single controller that stabilizes the origin of all systems in Σ. This motivates the following deﬁnition of informative data for stabilization of polynomial systems. In the rest of the paper, we assume that

$$
F(0) = 0.
$$

Deﬁnition 1 The data ( ˙ X , X , U ) are called informative for stabilization if there exist a radially unbounded function V ∈ V and a continuous controller K : R n → R m such that K (0) = 0 and

$$
Vz € R" {0} (8)
$$

Note that for a controller K satisfying K (0) = 0, the origin of the closed-loop system

$$
9
$$

is an equilibrium point, as F (0) = 0. If (8) holds then the origin is globally asymptotically stable for all closedloop systems obtained by interconnecting any system ( A,B ) ∈ Σ with the controller u = K ( x ).

In this paper, we study the following two problems.

Problem 1 (Informativity) Find conditions under which the data ( ˙ X , X , U ) are informative for stabilization.

Problem 2 (Controller design) Suppose the data ( ˙ X , X , U ) are informative for stabilization. Find a controller u = K ( x ) satisfying K (0) = 0 and (8) .

# 3 Connection to previous work

Current approaches for data-driven control of polynomial systems [8,9] build on the model-based method proposed in [15]. These methods do not incorporate prior knowledge and instead focus on designing a common stabilizing controller for all systems compatible with the data. In these works, the controller is considered to be of the form

$$

$$

where Y ∈ R m × p [ x ], P ∈ S p is positive deﬁnite, and Z ∈ R p [ x ] is radially unbounded satisfying

$$
(10)
$$

for some H ∈ R f × p [ x ]. The choice of candidate Lyapunov function

$$
(11)
$$

then leads to

$$

$$

where

$$
0(x) :=
$$

The main idea in this line of work is to ﬁnd P and Y ( x ) such that

$$
(x) > 0 Vr € R" (12)
$$

for all systems ( A,B ) compatible with the data. In the earlier work [8], H ( x ) is taken to be equal to the identity matrix, which implies that Z ( x ) = F ( x ). In contrast, [9] considers more general Z ( x ) satisfying (10). This strategy is appealing because it leads to data-based linear matrix inequalities for control design. Unfortunately, however, the method also has some major limitations.

The matrix (x) must full row rank for all {0} have

such that ∂Z ∂x ( x ) does not have full row rank. Then Θ( x ) is singular, which implies that (12) does not hold. Note that the full row rank condition can only hold if p ≤ n , i.e., the number of polynomials in Z is less than or equal to the state-space dimension of the system. This limits the class of Lyapunov functions of the form (11) that can be considered by the

