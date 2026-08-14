As the state us depends on control fs, then us can also be written as us = us(fs) and so from now we can use notation Js(fs) instead of Js(us(fs), fs). In the above problem 3.1,3.2,3.3 we are going to ﬁnd a optimal control f¯s ∈ Uad ⊂ L2(Ω) in a such a way that the corresponding solution of u¯s together with f¯s satisﬁes the minimization of the cost function, i.e.,

Js(f¯s) := min

Js(fs),

fs∈Uad

and corresponding optimal control of classical Poisson equation with homogeneous boundary conditions is the following

- 1

![](<2503.09386_pg6_images/imageFile1.png>)

- 2


 ∇u 2L2(Ω) + µ f 2L2(Ω) (3.4) subject to (the Poisson equation)

minJ(u, f) =

(−∆)u = f, x ∈ Ω, u = 0, x ∈ ∂Ω,

(3.5)

and the control constraints

a ≤ f L2(Ω) ≤ b. (3.6) Our main objective is to ﬁnd the optimal control f¯ such that

J(f¯) = min

J(f).

f∈Uad

- Proposition 3.1 (see [3]). Let Fs = {fs}0<s<1 ⊂ H−s(Ω) be the sequence satisfying fs H−s(Ω) uniformly bounded with respect to s and fs ⇀ f weakly in H−1(Ω) as s → 1−,

then us → u strongly in H01−δ(Ω) for some C > 0 and 0 < δ ≤ 1.

Here, we will extend this proposition 2.2 to optimal control of fractional PDE in our main result.

The ﬁrst proposition represents about the Poincar´e inequality in fractional Sobolev space and the second refers to the minimizer of a function deﬁned on a suitable space.

- Proposition 3.2 (Poincar´e inequality, [4]). Let s ∈ (0, 1), Ω ⊂ RN be an open and bounded set then we have

u 22 ≤ C(N, Ω, s)[u]2Hs(Ω). where some constant C(N, Ω, s) depending upon N, Ωands.

- Proposition 3.3. Let the admissible control space Uad be weakly closed, bounded subset of L2(Ω) with Js : Uad → R is weakly lower semi-continuous. Then Js has minimizer in Uad.


The existence and uniqueness of optimal control via strict convex and lower semicontinuous is discussed in the following proposition.

6

