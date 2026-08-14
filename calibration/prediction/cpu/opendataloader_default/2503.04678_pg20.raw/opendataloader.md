ALGEBRAIC GROWTH OF THE CREMONA GROUP 20

which has 2n distinct blocks of width ≥ 2k−1. The blocks are distinct since 3d − µn > ... > 3d − µ1 > d > µ1 > ... > µn. By Lemma 4.6, the degree d′ obtained after this sequence of ℓ−1 = n2k−2 ∗-seeds is at most

n2k−1 +3 3

(5d) ≤ 5n2kd.

d′ ≤

# □

5.2. Lower bound on length increase. Here we prove the lower bound in Theorem 2.5, which we recall in the next proposition.

Proposition 5.2. There exists a sequence of proper homaloidal types (yN)N≥1 of degrees d(yN) ≤ 2N210N, such that s(yN) ≥ 2N−1. In particular, for any c < ln(2) and N large enough,

s(yN) ≥ exp(c ln(d(yN))) Proof. Let N ≥ 1 be an integer parameter. We begin by constructing recursively an auxiliary finite sequence of homaloidal types (x0,N,...,xN−1,N) whose last element will be yN. If we start with the de Jonquières homaloidal type

x0,N := (2N−1 +1; 2N−1,(1)2N) which has 1 block of width 2N, we can apply Lemma 5.1 successively N −1 times with n = 2i and k = N −i, where i = 0,...,N −2. Doing so, we obtain a sequence of homaloidal types (xi,N) = (x0,N,...,xN−1,N) of degrees d0,N = 2N−1 + 1,d1,N,...,dN−1,N such that each xi,N has 2i distinct blocks of width ≥ 2N−i. The successive degrees satisfy the inequality

di+1,N ≤ 5·2N−i ·2i ·di,N = 5·2N ·di,N. At the end,

dN−1,N ≤ 5N2N2(2N−1 +1) (5.1) ≤ 2N210N. (5.2)

We now define the homaloidal type yN := xN−1,N, so d(yN) ≤ 2N210N. Its seedbed s(yN) is larger than the number 2N−1 of blocks of width 2 that have been created. The last statement follows from the fact that when N is large, we have

ln(d(yN)) ln(2)

N ≥

(1+o(1)), (5.3)

