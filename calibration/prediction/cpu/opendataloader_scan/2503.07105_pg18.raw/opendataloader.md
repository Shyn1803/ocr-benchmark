By summing up these integrals, some terms cancel out and we get

$$
m vdz = (qi-1,1qi,2 qi,1qi-1,2) 6 i=l m 3 2 i=1
$$

For the calculation of W , we sum up these integrals with P = D i ( w ) and v = a i for all i ∈ { 1 ,...,n } . For practical reasons we write this in terms of the edges, where E denotes all edges. Let e ∈ E be an edge with vertices q e 1 ,q e 2 . Let a l ,a r ∈ R 2 be the vectors a i on the left/right side of e . We set a l = 0 or a r = 0 for the non-existing side of boundary edges. Previously, every edge was considered twice, thus we can write

$$
T 1 qẴ,192,2 1 ai dz = = Di 3 2 i=l eeE
$$

For an inner edge, the addend can be rewritten as

$$
1 q2,2 2 (w Wr_ 2
$$

# 4 Numerical algorithms

In this section, we address numerical algorithms for the solution of (Pw) .

# 4.1 Fixed-point iteration

As an optimality condition for (Pw) we derived r ( w ) = 0, cf. Theorem 2.6 . This can be transformed into the fixed-point equation w = w + τr ( w ) with τ > 0. A possible algorithm for the solution is the fixed-point iteration w k +1 := w k + τ k r ( w k ) with appropriate step sizes τ k > 0. It is not clear, how to choose these step sizes. We will see in Lemma 4.2 below, that the direction r ( w k ) is a descent direction for J . However, since J is not C 1 , Armijo step sizes could become arbitrarily small and the usual convergence proof does not work. Similarly, constant (but small) step sizes might not give a decrease of J . Instead, we can view the above iteration scheme as a discretization of an ODE. Indeed,

Instead, we can view the above iteration scheme as a discretization of an ODE. Indeed, the above update formula yields (wk+1 wk) /Tk r(wk) This is an explicit Euler scheme for the ODE

$$
w (t) = r(w(t)), (ODE(w)) w(0) =
$$

We state some simple properties for (ODE(w)) .

Lemma 4.1. The following properties hold.

The function r is globally Lipschitz continuous with constant L > 0 .

