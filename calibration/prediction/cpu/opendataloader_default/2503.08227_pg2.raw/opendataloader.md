![](<2503.08227_pg2_images/imageFile1.png>)

Figure 1: Example of a domain reduction using known internal symmetries.

# on the border ∂Ω [1], having for instance the form

∂2f ∂xi∂xj

= g , (1)

aij

where aij and g are known functions of ⃗r(x1,x2,x3) and f(⃗r) is the function searched on Ω. Usual solving methods are the finite element (FEM) [2] and the finite difference (FDM) [3]. They both rely on the discretization of space forming a mesh of N points Mn,n = 1,...,N covering Ω and the linearization of the PDE to solve. The methods lead to the build up of a linear problem

AX = b, (2)

where X is the unknown vector of component f(Mn),n = 1,...,N, b is a constant vector defined by specific values given on Ω and ∂Ω and A is a square matrix of rank N. The boundary conditions (BC) on ∂Ω are usually of Dirichlet type (D), when f is known, or Neumann (N), when ∂f/∂⃗n is known (⃗n normal to ∂Ω ), or a combination of the two. When Ω is large or the need for accuracy is high, N becomes rapidly very large ( N ≫ 106) and the computer solving and the numerical storing of the inverse matrix A−1, solution of Eq. 2, can become problematic. It is generally of interest to reduce the problem size by considering all the symmetries applying both on Ω, ∂Ω and g. An example of such a domain reduction from Ω down to

2

