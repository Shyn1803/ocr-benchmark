The time-one map Ψ is deﬁned by setting Ψ(x0) = x(1) for each x0 ∈ Rd. Classical results on approximation properties of shallow neural networks do not immediately apply since A(t) is ﬁxed to be a square matrix of input dimension. For this reason, the neural ODE (1) is referred to as narrow following the deﬁnition in [2].

In [11], it has been shown that ﬂows of this ODE can be used to approximate continuous maps on Rd in the uniform norm by considering a NODEs on R2d+1, provided the activation function satisﬁes a quadratic equation. In [9], it has been shown that any L2 map can be approximated using a narrow NODE. The capability NODEs for transporting probability densities have been explored in [5, 9, 2]. For Lp maps, universal approximations have been shown in [4].

The strategy used in this paper departs from the techniques of the other cited works, where either the arguments are constructive or control theoretic arguments are used. Firstly, we note that it can be shown that ﬂows of (1) can approximate ﬂows of the wide NODE

x˙(t) =

m

AiΣ(Wix + bi) x(0) = x0 (3)

i=1

This, in turn, can be used to show that ﬂow maps of (1) can be used to approximate ﬂows of any dynamical system of the form

x˙(t) = V (x,t) x(0) = x0 (4)

where V (x,t) is a time dependent vector ﬁeld and hence, V (x,t) can be approximated by an arbitrarily wide network mi=1 AiΣ(Wix + bi) for any t. Therefore, narrow neural ODEs inherit the approximation properties of their shallow but wide counterparts. This strategy is used in [5] and in [6] to study ﬂow approximation properties using narrow NODEs. In [6] it was in fact shown that the dimension of the weight parameters used to approximate maps can be taken to be m × d, with m less than the input dimension d, by additionally exploiting geometric non-commutative properties of some chosen m basis vector ﬁelds, owing to diffeormophism controllability results due to [1].

Our goal in this paper is to derive quantitative rates of approximation of (1). Existing quantitative rates are either established to approximate homoemorphism in the L2 norm [9] or for the purposes of generative modeling [9, 2]. In contrast, we are interested in quantitative rates for approximation of ﬂow maps in the uniform norm. The problem we address is how many switches are needed in A(t),W(t),b(t), to approximate the ﬂow of (3). In this way, our result complements [9, 2]. While we restrict to reference ﬂows of the differential equations of the form (3), an extension to general ﬂows is straightforward since shallow but wide neural networks are known to be dense in the set of continuous functions. Hence, quantitative approximation properties of shallow neural networks would immediately translate to quantitative approximation properties of narrow NODEs.

Before we present our analysis, we give some brief intuition behind our proof strategy. The idea behind our analysis is the following. Given a differential equation of the

2

