vacy protection across computer science, control engineering, and communication technology. Multiple types of research have been illustrated for distributed NE seeking with DP method [17]–[20]. A privacy-preserving distributed algorithm for seeking the NE was designed in [17] for aggregative games and [18] focused on quadratic network games. [19] extended privacy-preserving mechanisms for NE seeking to directed graph. Considering coupling constraints, [20] proposed a GNE seeking strategy for multi-cluster games. Though [21] investigated GNE seeking with privacy preservation, information exchange efﬁciency was not considered. Privacy and communication efﬁciency are seldom explored together in distributed GNE seeking for aggregative games though it is of great interest.

The motivation of this paper is to study aggregative games with coupling constraints and to design an efﬁcient distributed algorithm to seek GNE of the games. The principal contributions of this paper can be outlined as follows:

1) We provide a novel communication-efﬁcient distributed GNE seeking algorithm (Algorithm 1), combining an event-triggered mechanism to decrease transmission rounds and a stochastic compressor to minimize transmitted bits.

2) Besides achieving efﬁcient communication, our algorithm ensures convergence to exact GNE by developing precise step size conditions (Theorem 1). In contrast to existing GNE seeking works ensuring accuracy [21], our proposed algorithm further reduces the communication cost.

3) We show that (0 ,δ ) -differential privacy is achieved under a stochastic compressor (Theorem 2). Particularly, the algorithm guarantees asymptotic convergence to the GNE and privacy protection simultaneously.

The organization of this paper is as follows: Section II presents the fundamental concepts and establishes the formulation for the problem. Section III provides an event-triggered and compressed distributed GNE seeking algorithm with an analysis of convergence and privacy. Section IV provides simulation examples to conﬁrm the obtained results, and Section V concludes the paper.

Notations: Let R ( R + ) denote the set of real (positive real) numbers, Z the integers, and N the natural numbers. For n ∈ N , R n ( R n × d ) represents n -dimensional real vectors ( n × d real matrices). Let P T and [ P ] ij denote the transpose and ( i,j ) th entry of matrix P , respectively. The gradient of f at x is denoted by ∇ f ( x ) , with ∇ i f ( x ) as its i -th component. Deﬁne 1 N ( 0 N ) as the N -dimensional all-ones (all-zeros) vector, and I d as the d -dimensional identity matrix. The inner product and Euclidean (induced2 ) norm are denoted by  · , ·  and | ·| , respectively. Let Π D ( · ) be the Euclidean projection onto a closed convex set D . For probability and expectation, we use P ( · ) and E [ x ] . Finally, col( x 1 ,...,x m ) = [ x T 1 ,...,x T m ] T stacks vectors x 1 ,...,x m .

# P RELIMINARIES AND P ROBLEM F ORMULATION

# A. Problem Formulation

Let us examine an aggregative game comprising N players, where each participant i ∈ V = { 1 , 2 ,...,N } is associated with a decision vector x i ∈ Ω i , with Ω i ⊆ R d representing a compact convex set, and they share the constraint

$$
N 1 g(7) < 0, N € Rd
$$

where g : R d → R is the constrained function. We assume that each player aims at minimizing its local cost function J i ( x i ,h ( x )) : Ω → R , where x = col( x 1 ,x 2 ,...,x N ) ∈ Ω = Ω 1 × Ω 2 × ... × Ω N and h ( x ) = ¯ x is the aggregation function. The function J i ( x i ,h ( x )) is continuously differentiable and convex in x i for every ﬁxed h ( x ) . In particular, the problem is formulated as follows:

Problem 1 : Each player i intends to

$$
minimize Ji(xi,=) subject to
$$

The resolution of Problem 1 yields a GNE, characterized as follows.

Deﬁnition 1 . [22] A strategy proﬁle x ∗ = col( x ∗ 1 ,x ∗ 2 ,...,x ∗ N ) ∈ Ω ∩ Υ is called a GNE of the constrained game if

$$
1 + 2 j#i
$$

for all € where 1 _i

If is regarded as function of then the following assumptions about the gradient are  associated with the GNE

Assumption 1 . 1) J i ( · ) is Lipschitz continuous, i.e., there exists a constant l J such that for all u , v ∈ Ω and i ∈ V ,

$$

$$

a constant lg such that for all u;v € Rd,

$$

$$

The Lipschitz continuous condition implies g ( · ) is bounded on the compact set R d . In other words, there exists a constant

  ·   ≤ Assumption 2 . 1) ∇ J i ( · ) is Lipschitz continuous, i.e., there exists a constant G J such that for all u , v ∈ Ω and

$$

$$

2) ∇ i g ( · ) is Lipschitz continuous, i.e., there exists a conR d

$$
IlVig(u) = Vig(v)ll < Ggllu = v.
$$

