define the symplectic rotation matrix

  

    →

  

  

  

  . (13)

cos(θi) sin(θi) −sin(θi) cos(θi)

xi pi

xi pi

X(θi) :

Replacing B with X(θi)B in Eq.(10) leaves the trace invariant so there is a SO(2)n family of linear maps taking f0 to a minimal energy configuration. This family of matrices is enlarged when the symplectic eigenvalues of either V or H are degenerate.

It is interesting to compare Eq.(8) and Equation Eq.(12). Notably, the AM-GM inequality shows that ESp(2n) ≥ ESL(2n) since

n

λHi λVn+1−i ≥ 2n(det(HV ))1/2n, (14)

2

i=1

with equality iff λHi λVn+1−i ≡ const. In particular, ESp(2) = ESL(2) as expected.

C. Example 1

We first compute an easy example in n = 2. For ϵ > 0, suppose that E(z,ϵ) = x2 + ϵ2y2 + p2x + p2y. Suppose further that f0(z,R) = R 6

2|B(R)|χB(R) = R 6

2|B(R)|Θ(R2 − |z|2) is a rescaled indicator function on the ball. We compute that N = 1, c = 0, H(R) = I4, V0 = 0, d = 0, and V (ϵ) = diag(1,ϵ2,1,1). The initial energy stored in f0 is E[f0] = (3 + ϵ). For ϵ small, we should expect that ESL(4) is small since f0 can be squeezed onto the y axis via area-preserving maps. Indeed, Eq.(8) gives us that

ESL(4) = ϵ1/2. (15)

Dividing this equation by E[f0], we can alternatively compute the inaccessible energy fraction FSL(2n) := EESL[f(2n)

0] to be

4ϵ1/2 3 + ϵ2

. (16)

FSL(4) =

The distribution function after an energy minimizing linear map is f0 ◦ ϕ−1 = |B(1R)|Θ(R2 − ϵ−1/2(x2 + p2x + p2y) − ϵ3/2y2) which looks as expected.

In contrast, the linear Gromov’s nonsqueezing theorem prohibits squeezing f0 onto the y-axis via linear symplectomorphisms. This implies we should find ESp(2n) to be finite in the limit ϵ → 0+. V (ϵ) can be symplectically diagonalized by SV = diag(1,ϵ−1/2,1,ϵ1/2) giving

7

