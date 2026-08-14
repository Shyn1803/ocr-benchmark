Convergence analysis of linearized ℓq penalty methods for nonconvex optimization with nonlinear equality constraints23

![](<2503.08522_pg23_images/imageFile1.png>)

Proof of Lemma 4.2 Using the optimality condition, we have:

∇f(xk) + JF(xk)T(ρsign(lF(xk+1; xk)) ◦ |lF(xk+1; xk)|q−1) + βk+1∆xk+1 = 0. Exploiting deﬁnition of Pqρ and properties of the derivative, it follows that:

∇Pqρ(xk+1)

=∇f(xk+1) + JF(xk+1)T ρsign(F(xk+1)) ◦ |F(xk+1)|q−1

=∇f(xk+1) − ∇f(xk) − βk+1∆xk+1

+ ρ JF(xk+1) − JF(xk) T sign(F(xk+1)) ◦ |F(xk+1)|q−1

+ρJF(xk)T sign(F(xk+1)) ◦ |F(xk+1)|q−1 − sign(lF(xk+1; xk)) ◦ |lF(xk+1; xk)|q−1 .

It then follows by applying the norm:  ∇Pqρ(xk+1) ≤ ∇f(xk+1) − ∇f(xk) + βk+1 ∆xk+1

+ ρ sign(F(xk+1)) ◦ |F(xk+1)|q−1 JF(xk+1) − JF(xk)

+ρ JF(xk) sign(F(xk+1)) ◦ |F(xk+1)|q−1 − sign(lF(xk+1; xk)) ◦ |lF(xk+1; xk)|q−1

(4)

≤ ∇f(xk+1) − ∇f(xk) + βk+1 ∆xk+1

+ ρ sign(F(xk+1)) ◦ |F(xk+1)|q−1 JF(xk+1) − JF(xk)

+ ρ JF(xk) 3 × m

2−q

2 F(xk+1) − lF(xk+1; xk) q−1

![](<2503.08522_pg23_images/imageFile2.png>)

=  ∇f(xk+1) − ∇f(xk) + βk+1 ∆xk+1

- 1

![](<2503.08522_pg23_images/imageFile3.png>)

- 2


m

|fi(xk+1)|2 q−1

JF(xk+1) − JF(xk)

+ ρ

i=1

2−q

2 F(xk+1) − lF(xk+1; xk) q−1 ≤ ∇f(xk+1) − ∇f(xk) + βk+1 ∆xk+1

+ ρ JF(xk) 3 × m

![](<2503.08522_pg23_images/imageFile4.png>)

2−q 2

q−1 2

m

m

![](<2503.08522_pg23_images/imageFile5.png>)

![](<2503.08522_pg23_images/imageFile6.png>)

|fi(xk+1)|2

×

1

JF(xk+1) − JF(xk)

+ ρ

i=1

i=1

2−q

2 F(xk+1) − lF(xk+1; xk) q−1

+ ρ JF(xk) 3 × m

![](<2503.08522_pg23_images/imageFile7.png>)

= ∇f(xk+1) − ∇f(xk) + βk+1 ∆xk+1

2−q

2 ρ F(xk+1) q−1 JF(xk+1) − JF(xk)

+ m

![](<2503.08522_pg23_images/imageFile8.png>)

+ ρ JF(xk) 3 × m

2−q

2 F(xk+1) − lF(xk+1; xk) q−1 ,

![](<2503.08522_pg23_images/imageFile9.png>)

where the second inequality follows from H¨older’s inequality. Moreover, using the fact that for any vector v ∈ Rm and q ∈ (1, 2], we have:

v 2 ≤ v q,

