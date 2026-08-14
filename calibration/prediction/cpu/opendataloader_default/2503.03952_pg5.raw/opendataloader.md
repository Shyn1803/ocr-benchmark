Also taking the limit u → 0, the single letter index is given by

t − q 1 − q

f(t,0;q) =

. (2.8)

In this case, the corresponding index is known as the “half-index” (of Neumann boundary condition) [14]. Due to an obvious symmetry between t and u, the limit t → 0 is essentially same as u → 0. However, in the analysis in the next subsection, these two limits look different, and lead to the equivalent result non-trivially.

Finally, if we set u = q/t, the resulting index is known as the flavored Schur index. The single letter index is now given by

t + q/t − 2q 1 − q

. (2.9)

f(t,q/t;q) =

For the further specialization to t = q1/2 (i.e., u = q1/2), the index IN(q1/2,q1/2;q) is nothing but the original Schur index [3, 4].

We stress that all of them are obtained from the index (2.10) as special limits. The reduced index IN(t,u;q) is regarded as a two-parameter deformation of the Schur index IN(q1/2,q1/2;q). As mentioned in the introductory section, we refer to IN(t,u;q) as the deformed Schur index.

# 2.2 Exact evaluation of deformed Schur indices

In this subsection, we evaluate the matrix integral of the deformed Schur index exactly. When v = p = 0, we can rewrite the integral representation (2.4) as a more convenient form in terms of the q-Pochhammer symbol:

IN(t,u;q) =

(q;q)N∞(tu;q)N∞ (t;q)N∞(u;q)N∞ TN

1 N!

N

(xi/xj;q)∞(tuxi/xj;q)∞ (txi/xj;q)∞(uxi/xj;q)∞

dxi 2πixi 1≤i̸=j≤N

. (2.10)

i=1

This is a starting point of our analysis. The q-Pochhammer symbol is defined by

(x;q)∞ =

∞

(1 − xqk), (x;q)n =

k=0

n−1

(1 − xqk), (x;q)0 = 1, (2.11)

k=0

and we have used an identity,

(x;q)∞ 1 − x

, (2.12)

(qx;q)∞ =

to derive (2.10). A method to perform the integral (2.10) is simple. The computation consists of three steps.

In the first step, we recognize that the integrand of (2.10) includes a weight function of Macdonald polynomials of type AN−1. In Appendix A, we review basics on the Macdonald polynomials of type A, based on [15, 16], for the reader’s convenience. The weight function of the Macdonald polynomials of type AN−1 is given by

(xi/xj;q)∞ (txi/xj;q)∞

w(x) =

. (2.13)

1≤i̸=j≤N

– 4 –

