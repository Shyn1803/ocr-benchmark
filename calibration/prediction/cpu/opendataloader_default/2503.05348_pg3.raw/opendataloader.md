can be seen in [4, 6, 12]. Throughout the paper, ‘increasing’ means ‘non-decreasing’ and ‘decreasing’ means ‘non-increasing’. Whenever we use a derivative, an expectation or a conditional distribution, we are tacitly assuming that they exist.

If X,Y ∈ L1, then we say that:

- • X is less than Y in the stochastic order (or in the first-order stochastic domi-

nance), shortly written as X ≤ST Y , if F¯X ≤ F¯Y or, equivalently, if E(u(X)) ≤ E(u(Y )) for all increasing functions u such that these expectations exist. Then X =ST Y represents equality in law (distribution).

- • X is less than Y in the increasing concave order (or in the second-order stochastic

dominance), shortly written as X ≤ICV Y , if E(u(X)) ≤ E(u(Y )) for all increasing concave functions u such that these expectations exist or, equivalently, if

t

−∞

FX(x)dx ≥

t

−∞

FY (x)dx for all t.

- • X is less than Y in the increasing convex order (or in the stop-loss order), shortly

written as X ≤ICX Y , if E(u(X)) ≤ E(u(Y )) for all increasing convex functions u such that these expectations exist or, equivalently, if

∞

t

F¯X(x)dx ≤

∞

t

F¯Y (x)dx for all t.

The function π(t) = t ∞ F¯(x)dx is called stop-loss function (see e.g. [6], p. 19). Hence, X ≤ICX Y holds if and only if πX ≤ πY . It is also equivalent to −X ≥ICV −Y .

- • X is less than Y in the convex order, shortly written as X ≤CX Y , if E(u(X)) ≤ E(u(Y )) for all convex functions u such that these expectations exists or, equivalently, if πX ≤ πY and limt→−∞ πX(t)−πY (t) = 0. It implies E(X) = E(Y ) and V ar(X) ≤ V ar(Y ). It is also equivalent to X ≤ICX Y and E(X) = E(Y ) (see [6], p. 19) and to X ≥ICV Y and E(X) = E(Y ).
- • X is less than Y in the convolution order, shortly written as X ≤CONV Y if Y =ST X + Z where Z is a nonnegative random variable independent of X (see [12], p. 70 and [13]).


The relationships between these orders are summarized as follows: X ≤CONV Y ⇒ X ≤ST Y ⇒ X ≤ICX Y ⇐ X ≤CX Y ⇓ ⇓ ⇓ X ≥CX Y ⇒ X ≤ICV Y ⇒ E(X) ≤ E(Y ) E(X) = E(Y )

3

