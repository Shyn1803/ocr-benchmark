Prior to proceed let us consider the the product Dpx. Since Dp is an n × n matrix with entries in Qp and x is an n-tuple with entries in Qp, the result Dpx is an n-tuple with entries in Qp. Formally, if Dp = (dij) and x = (x1,x2,...,xn), then the i-th component of Dpx is given by:

n

dijxj ∈ Qp

(Dpx)i =

j=1

The p-adic norm | · |p is applied component-wise to the resulting n-tuple Dpx. For each component (Dpx)i of Dpx, we have:

1 pordp((Dpx)i)

|(Dpx)i|p =

![](<2503.04182_pg3_images/imageFile1.png>)

where ordp((Dpx)i) is the highest power of p dividing (Dpx)i.

Since the p-adic norm |·|p maps elements of Qp to Qp, applying it componentwise to an n-tuple will result in another n-tuple with entries in Qp. Therefore, |Dpx|p is an n-tuple with entries in Qp.

Thus, δp(x) = |Dpx|p ∈ Qnp, hence, the map δp is well-deﬁned. As we have seens previous we can deﬁne the p-adic Ducci sequence the

sequence Deﬁnition 0.4 (p-adic Ducci sequence).

x,δp(x),δp2 = δp(δp(x)) = δp ◦ δp,...,δpn(x),...

with initial seed x ∈ Qnp respect to Dp ∈ Mn×n(Qp). In this p-adic context, we deﬁne a p-adic Ducci map associated with a p-adic matrix Dp as a function that maps a p-adic vector x to |Dpx|p, where | · |p is applied elementwise.

Without loss of generality we can deﬁne the following For convergence to zero, we analyze when xk → 0 as k → ∞.

Prior to move forward we recall the following

Remark 1. In the ﬁeld of p-adic numbers Qp, the p-adic absolute value |x|p of a nonzero element x is deﬁned as:

p(x),

|x|p = p−v

where vp(x) is the p-adic valuation of x. The valuation vp(x) is the highest power of p that divides x in Qp.

If |x|p < 1 and x = 0, this means that vp(x) > 0, so x is divisible by p. The possible values of |x|p in this case are:

|x|p = p−k, where k ∈ N and k ≥ 1. Thus, the possible values of |x|p when |x|p < 1 are:

p−1,p−2,p−3,... .

3

