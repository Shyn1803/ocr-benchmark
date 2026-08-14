- [19] F. A. Potra and V. Ptak´ , Nondiscrete Induction and Iterative Processes, Pitman, Boston, Massachusetts, 1984.
- [20] L. B. Rall, Convergence of the Newton process to multiple solutions, Numer. Math., 9 (1966), pp. 23–37.
- [21] S. J. Reddi, S. Kale, and S. Kumar, On the convergence of adam and beyond, in International Conference on Learning Representations, 2018.
- [22] G. W. Reddien, On Newton’s method for singular problems, SIAM J. Numer. Anal., 15 (1978), pp. 993–996.
- [23] H. Royden and P. Fitzpatrick, Real Analysis, Pearson, 4th ed., 2010.
- [24] H. Schwetlick, Numerische L¨osung Nichtlinearer Gleichungen, VEB, Berlin, Germany, 1979.
- [25] W. Sun and Y.-X. Yuan, Optimization Theory and Methods: Nonlinear Programming, vol. 1, Springer, 2006.
- [26] J. F. Traub, Iterative Methods for the Solution of Equations, Prentice-Hall, Englewood Cliffs, NJ, 1964. Reprinted by Chelsea Publishing Company, 1982; Reprinted by AMS Chelsea Publishing, 2016.


Appendix A. Q-Superlinear Implies UP-Superlinear. Proof of Theorem 3.2. Define

ξk = ∥xk − x∗∥, f(k) = −lnξk. By Q-superlinear convergence,

lim

k→∞

Taking logarithms, define

ξk+1 ξkq

= Qq, q > 1, 0 < Qq < ∞.

- (A.1) d(k) = f(k + 1) − qf(k) = −ln

ξk+1 ξkq

.

Then

lim

k→∞

d(k) = −lnQq := d, so that {d(k)} is bounded; i.e., there exists M > 0 with |d(k)| ≤ M. Unrolling the recurrence

f(k + 1) = qf(k) + d(k) yields

f(k) = q k−1f(1) +

k−1

j=1

q k−1−jd(j).

Dividing by qk, we have

f(k) qk

=

f(1) q

+

k−1

j=1

d(j) q j+1

.

Since the tail of the series is bounded by

∞

j=k

|d(j)| q j+1 ≤ M

∞

j=k

1 q j+1

,

the limit

- (A.2) s = lim k→∞


∞

f(1) q

d(j) q j+1

f(k) qk

=

+

j=1

23

