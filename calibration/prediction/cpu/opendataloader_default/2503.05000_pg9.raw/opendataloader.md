time-dependent Hamiltonian vector ﬁeld of τ˚BBStt starting at dxS0. Equation (2.24) is then a plain consequence of the chain rule. Since

![](<2503.05000_pg9_images/imageFile1.png>)

@f,g P C8pT˚Mq, dtf,guω “ rdf,dgs, (2.25)

equation (2.23) is obtained by usual extension from smooth functions to exact 1-forms, and then from closed forms to generic 1-forms using the Leibniz rule.

![](<2503.05000_pg9_images/imageFile2.png>)

![](<2503.05000_pg9_images/imageFile3.png>)

![](<2503.05000_pg9_images/imageFile4.png>)

![](<2503.05000_pg9_images/imageFile5.png>)

Let us illustrate Lemma 2.17. The algebroid bracket r.,.s allows us to obtain iterated derivations of the Hamilton-Jacobi equation (2.21). We spell out the order 2 :

B2ζt Bt2

“ pζtq˚rα˚θ,τ˚ζtα˚θs, (2.26) After applying Lemma 2.17 a second time, we obtain an order 3 derivation:

![](<2503.05000_pg9_images/imageFile6.png>)

B3ζt Bt3

“ pζtq˚ prα˚θ,τ˚pζtq˚rα˚θ,τ˚pζtq˚α˚θss ` rrα˚θ,τ˚pζtq˚α˚θs,τ˚pζtq˚α˚θsq. (2.27)

![](<2503.05000_pg9_images/imageFile7.png>)

# 3 A Pre-Lie approach to Hamiltonian Poisson integrators

Since G Ă T˚M, the Lagrangian bisections of G that are close to the identity section are described by graphs of time-dependent closed 1-forms. We can approximate them by using the notion of jets we developed in the previous section. In order to approximate a given Lagrangian bisection by 1-forms, we now introduce an appropriate space Jξ8 and a pre-Lie algebra structure on it. We then explain how this pre-Lie algebra encodes expansions of solutions of the Hamilton-Jacobi equation (2.21) through the introduction of Butcher series. In Section 3.3, we exhibit some algebraic simpliﬁcations arising in this expansion if the initial condition is chosen to be zero.

## 3.1 Pre-Lie formalism for Hamilton-Jacobi ﬂows

In full generality, for ξ P Ω1pGq, we are interested in the expansion of the general Hamilton-Jacobi ﬂow

Bζ Bt

“ ζt˚ξ, ζ0 P Ω10pMq. (3.1)

![](<2503.05000_pg9_images/imageFile8.png>)

We consider the inﬁnite dimensional real vector subspace Jξ8 Ă Ω1pGq spanned by ξ and stable w.r.t. the following maps: for any f,g P Jξ8,

ηpf,gq:

Ω10pMq Ñ Ω10pMq ζ ÞÑ ζ˚rf,τ˚ζ˚gs

. (3.2)

The space Jξ8 is naturally equipped with the product Ź h Ź ξpζq “ ζ˚rξ,τ˚ζ˚gs, h Ź ηpf,gq “ ηph Ź f,gq ` ηpf,h Ź gq. (3.3)

This yields a non-associative non-commutative magmatic structure on pJξ8,Źq. Note that pJξ8,Źq is not a Lie algebra as Ź is not antisymmetric.

Remark 3.1 (Jξ8 and jet spaces). The space Jξ8 is analogous to the inﬁnite jet space [1, 41, 37] on XpMq used for the analysis of Runge-Kutta and Lie-group methods. In [31, 27], the accuracy

of numerical integrators is studied via the use of Taylor expansions of ODE ﬂows. Given a vector

9

