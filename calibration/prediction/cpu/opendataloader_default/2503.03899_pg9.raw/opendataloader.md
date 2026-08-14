DISTRIBUTION OF THE SUM OF RECIPROCAL PARTS FOR DISTINCT PARTS PARTITIONS 9

Proposition A.1. For fixed 0 < δ < 14, we have

 inf

  < 0.

1 √n

Xk − L(t) > n−14+δ

n−δ log Pn

limsup

t≥0

k≤t√n

n→∞

Remark. In particular, we have

 sup

  = 1.

1 √n

Xk − L(t) ≤ n−14+δ

lim

Pn

n→∞

k≤t√n

t≥0

Proof. Let d(n) be the number of distinct parts partitions of n. We require only a weak form of the well-known asymptotic expansion of d(n) [11],

2√n

A +O(logn). Let an,bn ∈ N0 and define αn,βn by

d(n) = e

an = αn√n, bn = βn√n. Assume that αn,βn ≥ n−14+δ. We use the saddle point bound to write, for any xn ∈ R,

 

  1

√n k≤a

Pn

Xk = bn

n

1 d(n)

[qn][ζbn]

(1 + ζqk)

(1 + qk)

=

k≤an

k>an

1 d(n)

qn−ne−bnxn

(1 + exnqnk)

(1 + qnk)

≤

k≤an

k>an

 

 .

√n A − log d(n) − βnxn√n +

k

k A√n

log 1 + exn−

log 1 + e−

A√n +

= exp

k≤an

k>an

We will take xn ∈ {±n−14}, where the sign will depend on bn. By Taylor’s Theorem,

k A√n

k A√n

e−

ex−

x2n 2

k

k

A√n − log 1 + e−

log 1 + exn−

A√n − xn

≤

sup

2

k A√n

1 + e−

k A√n

1 + ex−

|x|≤n41

k A√n

e−

≤ x2n

2.

k A√n

1 + 12e−

Thus,

  1

√n k≤a

Pn

n

  ≤ exp

Xk = bn

 

√n A − log d(n) +

k≥1

k A√n

e−

+xn

k A√n

1 + e−

k≤an

A√n − βnxn√n

k

log 1 + e−

  x2n

  

  .

k A√n

e−

+ O

2

k A√n

1 + 12e−

k≤an

