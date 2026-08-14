vacy protection across computer science, control engineering, and communication technology. Multiple types of research have been illustrated for distributed NE seeking with DP method [17]–[20]. A privacy-preserving distributed algorithm for seeking the NE was designed in [17] for aggregative games and [18] focused on quadratic network games. [19] extended privacy-preserving mechanisms for NE seeking to directed graph. Considering coupling constraints, [20] proposed a GNE seeking strategy for multi-cluster games. Though [21] investigated GNE seeking with privacy preservation, information exchange efﬁciency was not considered. Privacy and communication efﬁciency are seldom explored together in distributed GNE seeking for aggregative games though it is of great interest.

The motivation of this paper is to study aggregative games with coupling constraints and to design an efﬁcient distributed algorithm to seek GNE of the games. The principal contributions of this paper can be outlined as follows:

- 1) We provide a novel communication-efﬁcient distributed GNE seeking algorithm (Algorithm 1), combining an event-triggered mechanism to decrease transmission rounds and a stochastic compressor to minimize transmitted bits.
- 2) Besides achieving efﬁcient communication, our algorithm ensures convergence to exact GNE by developing precise step size conditions (Theorem 1). In contrast to existing GNE seeking works ensuring accuracy [21], our proposed algorithm further reduces the communication cost.
- 3) We show that (0,δ)-differential privacy is achieved under a stochastic compressor (Theorem 2). Particularly, the algorithm guarantees asymptotic convergence to the GNE and privacy protection simultaneously.


The organization of this paper is as follows: Section II presents the fundamental concepts and establishes the formulation for the problem. Section III provides an event-triggered and compressed distributed GNE seeking algorithm with an analysis of convergence and privacy. Section IV provides simulation examples to conﬁrm the obtained results, and Section V concludes the paper.

Notations: Let R (R+) denote the set of real (positive real) numbers, Z the integers, and N the natural numbers. For n ∈ N, Rn (Rn×d) represents n-dimensional real vectors (n×d real matrices). Let PT and [P]ij denote the transpose and (i,j)th entry of matrix P, respectively. The gradient of f at x is denoted by ∇f(x), with ∇if(x) as its i-th component. Deﬁne 1N (0N) as the N-dimensional all-ones (all-zeros) vector, and Id as the d-dimensional identity matrix. The inner product and Euclidean (induced-2) norm are denoted by  ·,·  and | ·|, respectively. Let ΠD(·) be the Euclidean projection onto a closed convex set D. For probability and expectation, we use P(·) and E[x]. Finally, col(x1,...,xm) = [xT1 ,...,xTm]T stacks vectors x1,...,xm.

II. PRELIMINARIES AND PROBLEM FORMULATION A. Problem Formulation

Let us examine an aggregative game comprising N players, where each participant i ∈ V = {1,2,...,N} is associated with a decision vector xi ∈ Ωi, with Ωi ⊆ Rd representing a compact convex set, and they share the constraint

N

1 N

xi ∈ Υ ⊂ Rd (1)

g(¯x) ≤ 0, x¯ =

![](<2503.08494_pg2_images/imageFile1.png>)

i=1

where g : Rd → R is the constrained function. We assume that each player aims at minimizing its local cost function Ji(xi,h(x)) : Ω → R, where x = col(x1,x2,...,xN) ∈ Ω = Ω1 ×Ω2 ×...×ΩN and h(x) = x¯ is the aggregation function. The function Ji(xi,h(x)) is continuously differentiable and convex in xi for every ﬁxed h(x). In particular, the problem is formulated as follows:

Problem 1: Each player i intends to

minimize xi ∈ Ωi

Ji(xi,x¯) subject to g(¯x) ≤ 0.

The resolution of Problem 1 yields a GNE, characterized as follows.

Deﬁnition 1. [22] A strategy proﬁle x∗ = col(x∗1,x∗2,...,x∗N) ∈ Ω ∩ Υ is called a GNE of the constrained game if

1 N

1 N

x∗j),

Ji(x∗i ,h(x∗)) ≤ Ji(xi,

xi +

![](<2503.08494_pg2_images/imageFile2.png>)

![](<2503.08494_pg2_images/imageFile3.png>)

j =i

for all xi : (xi,x∗−i) ∈ Ω ∩ Υ, where x∗−i = col(x∗1,...,x∗i−1,x∗i+1,...,x∗N).

If Ji(xi,h(x)) is regarded as a function of x, then Ji(xi,h(x)) can be written as Ji(u),u ∈ Ω for simplism and the following assumptions about the gradient are associated with the GNE.

- Assumption 1. 1) Ji(·) is Lipschitz continuous, i.e., there exists a constant lJ such that for all u,v ∈ Ω and i ∈ V,

Ji(u) − Ji(v) ≤ lJ u − v .

2) g(·) is Lipschitz continuous, i.e., there exists a constant lg such that for all u,v ∈ Rd,

g(u) − g(v) ≤ lg u − v .

The Lipschitz continuous condition implies g(·) is bounded on the compact set Rd. In other words, there exists a constant Cg > 0 such that g(·) ≤ Cg.

- Assumption 2. 1) ∇Ji(·) is Lipschitz continuous, i.e., there exists a constant GJ such that for all u,v ∈ Ω and i ∈ V,


 ∇iJi(u) − ∇iJi(v) ≤ GJ u − v .

2) ∇ig(·) is Lipschitz continuous, i.e., there exists a constant Gg such that for all u,v ∈ Rd,

 ∇ig(u) − ∇ig(v) ≤ Gg u − v .

