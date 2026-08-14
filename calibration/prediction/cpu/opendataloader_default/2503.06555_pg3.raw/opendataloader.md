3

classical nonlinear shock-capturing methods [19, 32, 42, 49]: the ﬁrst is the uniqueness of approximation solution; and the second is that only a convergence rate of order O(h1/2) can be proven in the energy norm for the linear element approximation, though numerical experiments demonstrating the optimal convergence rate O(h).

In this paper, we develop a modiﬁed nonlinear DD ﬁnite element method for the convection-diﬀusion-reaction model (1.1), give results of existence and uniqueness for discrete solution, and derive a priori error estimates. Compared with [56], our main contributions lie in the following aspects:

- • The considered model (1.1) is more general where the velocity β is not necessarily divergence free and the reaction coeﬃcient σ is a function, while in [56] it has been assumed that ∇ · β = 0 and σ is a constant;
- • We modify the artiﬁcial diﬀusivity term to a proper dimensional scale, thus unify the two alternative variants of the artiﬁcial diﬀusion in [56] into one form. In the proof of the existence of approximation solutions, we do not assume the boundedness of the maximum norm of the gradient of functions in approximation space (see Remark 4.1). We further prove the uniqueness of approximation solution for the modiﬁed DD method under an assumption on small mesh size.
- • We prove the optimal convergence rate O(h) in the energy norm of approximation error plus a dissipative term for the modiﬁed DD method.


This paper is organized as follows. Section 2 gives notations and weak formulations of the model problem. Section 3 presents the modiﬁed DD scheme. Section 4 proves the existence and uniqueness of discrete solutions for the modiﬁed DD method, and also contains some preliminary results at the beginning of this section. Section 5 analyzes the optimal convergence order for the modiﬁed DD method. Finally, section 6 provides some numerical tests to support our theoretical results.

# 2 Notation and weak formulation

For any subdomain ω of Ω, denote   ·  m,p,ω (resp. |· |m,p,ω) the standard norm (resp. semi-norm) in the Sobolev space Wm,p(ω). In case of p = 2, Wm,2(ω) = Hm(ω) (H0(ω) = L2(ω)) is the Hilbert space (with the inner product (·,·)ω) and is equipped with norm · m,ω (resp. | · |m,ω ); in case of m = 0,p = ∞, W0,∞(ω) = L∞(ω) is the Lebesgue space with norm · 0,∞,ω. We omit the symbol Ω in the notations above if ω = Ω, and also set

HD1 (Ω) = {v ∈ H1(Ω) : v|ΓD

= 0}.

Let Th be a shape regular triangulation of Ω into triangles/tetrahedrons, and denote by h the mesh-size function with h|T = hT := diam(T) for any T ∈ Th. Let Vh ⊂ H1(Ω) be the usual linear element space, and ψT be the

