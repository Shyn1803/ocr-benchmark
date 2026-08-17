time-dependent Hamiltonian vector ﬁeld of τ ˚ B S t B t starting at d x S 0 . Equation (2.24) is then a plain consequence of the chain rule. Since

$$
Vf,g € C" (T* M) , d{f,g} [df , dg] , 2.25
$$

equation (2.23) is obtained by usual extension from smooth functions to exact 1-forms, and then from closed forms to generic 1-forms using the Leibniz rule.

Let us illustrate Lemma 2.17. The algebroid bracket r .,. s allows us to obtain iterated derivations of the Hamilton-Jacobi equation (2.21). We spell out the order 2 :

$$
02St 2.26) dt2
$$

After applying Lemma 2.17 a second time, we obtain an order 3 derivation:

$$
'St = (2.27) dt3
$$

# 3 A Pre-Lie approach to Hamiltonian Poisson integrators

Since G Ă T ˚ M, the Lagrangian bisections of G that are close to the identity section are described by graphs of time-dependent closed 1-forms. We can approximate them by using the notion of jets we developed in the previous section. In order to approximate a given Lagrangian bisection by 1-forms, we now introduce an appropriate space J 8 ξ and a pre-Lie algebra structure on it. We then explain how this pre-Lie algebra encodes expansions of solutions of the Hamilton-Jacobi equation (2.21) through the introduction of Butcher series. In Section 3.3, we exhibit some algebraic simpliﬁcations arising in this expansion if the initial condition is chosen to be zero.

# 3.1 Pre-Lie formalism for Hamilton-Jacobi ﬂows

In full generality, for ξ P Ω 1 p G q , we are interested in the expansion of the general Hamilton-Jacobi ﬂow B ζ

$$
St $, 5o € (3.1) dt
$$

We consider the inﬁnite dimensional real vector subspace J 8 ξ w.r.t. the following maps: for any f,g P J 8 ξ ,

$$
n(f,9) : (3.2) F>
$$

The space J 8 ξ is naturally equipped with the product

$$
(3.3)
$$

This yields a non-associative non-commutative magmatic structure on p J 8 ξ , Źq . Note that p J 8 ξ , Źq is not a Lie algebra as Ź is not antisymmetric.

Remark 3.1 ( J 8 ξ and jet spaces) . The space J 8 ξ is analogous to the inﬁnite jet space [1, 41, 37] on X p M q used for the analysis of Runge-Kutta and Lie-group methods. In [31, 27], the accuracy of numerical integrators is studied via the use of Taylor expansions of ODE ﬂows. Given a vector

