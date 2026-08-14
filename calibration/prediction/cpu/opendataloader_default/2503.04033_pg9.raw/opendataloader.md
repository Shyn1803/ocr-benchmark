 

 

 

  =

 

 . (8)

A11 A15 A22 A25 A51 A52 A55

- u1
- u2 u5


- f1
- f2 f5


Au = f ≡

Here u is the solution and f is the body load on the interior of Ω, split into the two subdomains and shared boundary. Because an elliptic PDO is a local operator there is no interaction through A on f1 by u2 or f2 by u1, so A = 0 in those submatrices. However, both u1 and u2, are local to the shared boundary where u5 lies, so they both interact with the body load there, f5, through A. To interpret the first two block rows, note that

A11u1 + A15u5 = f1 ⇐⇒ u1 = −A−111A15u5 + A−111f1 (9)

This is similar to our solution operator formulation shown in (4), with the part of the subdomain boundary on ∂Ω now folded into u1. Next, let u˜1 = A−111f1 and u˜2 = A−221f2. If we supply these vectors in place of u1,u2 in (8) and set u5 = 0, then the equation still holds with the same body loads f1 and f2. Thus u˜1 and u˜2 are the particular solutions to our PDE on the interiors of Ω(1), and Ω(2) with u5 = 0. Now consider an upper triangular matrix U that satisfies

 

 

 

I A−111A15 I A−221A25

I

U

  =

- u1
- u2 u5


 . (10)

 

- u˜1
- u˜2 u5


This linear system can be confirmed with (9). U decouples our solutions u1,u2 into the particular solutions u˜1,u˜2 which are derived from our global Dirichlet BC without the subdomain-only (shared face) Dirichlet BC, and u5 which is that subdomain-only boundary condition. Thus U−1 collects both components of our solutions - in effect it represents the end of solving the merged system, where we use u3 and u5 to get u1, and u4 and u5 to get u2. Next, let L be a lower triangular matrix defined such that

 

 

# I

I A51A−111 A52A−221 I

L

  

   =

- f1
- f2


f5 − A51A−111f1 − A52A−221f2

˜f5

 

 . (11)

- f1
- f2 f5


9

