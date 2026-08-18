# 6 Numerical Computations

In this section, we state numerical computations that show several phenomena discussed in the introduction. In particular, we will observe a suppression of Ostwald ripening, splitting scenarios and instabilities of flat fronts and growing particles. The numerical simulations also support the sharp interface asymptotics, as we get a good agreement between phase field computations and exact solutions of the sharp interface problem. All our numerical simulations are for the quartic potential (2.7) and the interpolation functions (2.8), (2.9) and (2.10), for a fixed value r c ∈ (0 , 1].

# 6.1 Finite element method

We assume that Ω is a polyhedral domain and let T h be a regular triangulation of Ω into disjoint open simplices. Associated with T h is the piecewise linear finite element space

$$
Sh = {S € Slo € Pi(o) Vo € Tn}
$$

where we denote by P 1 ( o ) the set of all affine linear functions on o , see [13]. Let ( · , · ) h be the usual mass lumped L 2 -inner product on Ω associated with T h , and let π h : C 0 ( Ω) → S h be the standard interpolation operator. In addition, let τ denote a chosen uniform time step size. Then our finite element approximation of (2.1) is given as follows. Let ϕ 0 h ∈ S h , e.g., ϕ 0 h = π h φ 0 if φ 0 ∈ C 0 ( Ω). Then, for n ≥ 0, find ( ϕ n +1 h ,µ n +1 h ) ∈ S h × S h such that

$$
1(08+1 + € Sh (6.1a) Xh) h_ Vxh)h Xh)h VXh
$$

$$
Vnh) + n+1 € Sh_ (6.1b) n+1
$$

We implemented the scheme (6.1) with the help of the finite element toolbox ALBERTA, see [29]. To increase computational efficiency, we employ adaptive meshes, which have a finer mesh size h f within the diffuse interfacial regions and a coarser mesh size h c away from them. In particular, we use the strategy from [5, 7], and refine an element o if η o = | max o | ϕ n h |− 1 | > 0 . 5, unless it is already of size h f , and similarly coarsen an element o if η o < 0 . 1, unless it is already of size h c . For simplicity we assume from now on that Ω =   d i =1 (0 ,L i ) ⊂ R d , with L 1 ≥ L 2 ≥ ··· ≥ L d , and then let h f = L d N f , h c = L d N c for two chosen integer parameters N f > N c . Here, unless otherwise specified, for the computations with a phase field parameter ε = (2 k π ) − 1 , k ∈ N , we choose N f = 8 N c = 2 3+ k L d . This ensures that the interfacial regions are accurately resolved, while using a relatively coarser mesh in the pure regions. For the time discretization we choose τ = 10 − 3 , unless stated otherwise.

The nonlinear system of equations arising at each time level of (6.1) are solved with the help of Newton’s method. The resulting linear systems at each iteration in two spatial dimensions are solved by direct factorization using the package UMFPACK, see [15], and in three spatial dimensions with a V -cycle multigrid solver using a block Gauss–Seidel smoother.

For the initial data φ 0 we in general choose a diffuse interface representation of a desired sharp interface, with signed distance function d 0 : Ω → R . In particular, unless otherwise stated, we let

$$
Po(s) = tanh (6.2)
$$

For the definition of S 2 in (2.2), recall (2.4), we need to specify K ± and L . For convenience, for the numerical simulations to follow, we will define the relations ρ ± = K ± 2 β ,

