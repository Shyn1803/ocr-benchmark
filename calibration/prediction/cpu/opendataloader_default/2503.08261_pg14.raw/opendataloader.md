Multiplicity result of mixed local-nonlocal singular problem in two dimension 14

Proof. We split the proof into two cases. Case-I: We assume 0 < λ < Λǫ. In view of Perron’s method, we consider the solutions u and u to the equations

![](<2503.08261_pg14_images/imageFile1.png>)

![](<2503.08261_pg14_images/imageFile2.png>)

 

Mǫu = uδλ(x) in Ω, u > 0 in Ω and u = 0 in R2 \ Ω,

![](<2503.08261_pg14_images/imageFile3.png>)

(4.10)



and

 

![](<2503.08261_pg14_images/imageFile4.png>)

Mǫu = uδλ(x) + h(x,u) in Ω, u > 0 in Ω and u = 0 in R2 \ Ω,

![](<2503.08261_pg14_images/imageFile5.png>)

(4.11)



![](<2503.08261_pg14_images/imageFile6.png>)

respectively, where λ ∈ (λ,Λǫ). For the existence of u, we refer to [25]. It is immediate to show that u and u are sub and super solutions of the equation (Pλǫ), respectively. Claim: u ≤ u in Ω. To this concern, deﬁne a non-decreasing smooth function ψ : R → R such that

![](<2503.08261_pg14_images/imageFile7.png>)

![](<2503.08261_pg14_images/imageFile8.png>)

![](<2503.08261_pg14_images/imageFile9.png>)

![](<2503.08261_pg14_images/imageFile10.png>)

![](<2503.08261_pg14_images/imageFile11.png>)

ψ(t) =   

1 if t ≥ 1, 0 if t ≤ 0.

(4.12)

Let ψγ(t) = ψ(γt ), for γ > 0. Incorporating φ = ψγ(u − u) in the weak formulations of (4.10) and (4.11), then subtracting one from the other, we obtain

![](<2503.08261_pg14_images/imageFile12.png>)

![](<2503.08261_pg14_images/imageFile13.png>)

![](<2503.08261_pg14_images/imageFile14.png>)

Bǫ(u − u,φ) = ˆ

![](<2503.08261_pg14_images/imageFile15.png>)

![](<2503.08261_pg14_images/imageFile16.png>)

Ω

≥ λˆ

Ω

![](<2503.08261_pg14_images/imageFile17.png>)

λ uδ(x)

λ uδ(x) −

![](<2503.08261_pg14_images/imageFile18.png>)

![](<2503.08261_pg14_images/imageFile19.png>)

![](<2503.08261_pg14_images/imageFile20.png>)

![](<2503.08261_pg14_images/imageFile21.png>)

1 uδ(x)

1 uδ(x) −

![](<2503.08261_pg14_images/imageFile22.png>)

![](<2503.08261_pg14_images/imageFile23.png>)

![](<2503.08261_pg14_images/imageFile24.png>)

![](<2503.08261_pg14_images/imageFile25.png>)

By using the monotone property of ψ, (4.13) yields

φ dx + ˆ

Ω

h(x,u)φ dx

![](<2503.08261_pg14_images/imageFile26.png>)

φ dx. (4.13)

λˆ

Ω

1 uδ(x) −

1 uδ(x)

![](<2503.08261_pg14_images/imageFile27.png>)

![](<2503.08261_pg14_images/imageFile28.png>)

![](<2503.08261_pg14_images/imageFile29.png>)

![](<2503.08261_pg14_images/imageFile30.png>)

which reveals

φ dx ≤ −ˆ

|∇(u − u)|2ψγ′ (u − u) dx

![](<2503.08261_pg14_images/imageFile31.png>)

![](<2503.08261_pg14_images/imageFile32.png>)

![](<2503.08261_pg14_images/imageFile33.png>)

![](<2503.08261_pg14_images/imageFile34.png>)

Ω

((u − u)(x) − (u − u)(y))(φ(x) − φ(y)) |x − y|2+2s

+ ˆ

ˆ

![](<2503.08261_pg14_images/imageFile35.png>)

![](<2503.08261_pg14_images/imageFile36.png>)

dx dy ≤ 0,

![](<2503.08261_pg14_images/imageFile37.png>)

![](<2503.08261_pg14_images/imageFile38.png>)

![](<2503.08261_pg14_images/imageFile39.png>)

R2

R2

|{x ∈ Ω : u > u}| = 0. Consequently, u ≤ u in Ω. Now, we deﬁne

![](<2503.08261_pg14_images/imageFile40.png>)

![](<2503.08261_pg14_images/imageFile41.png>)

![](<2503.08261_pg14_images/imageFile42.png>)

![](<2503.08261_pg14_images/imageFile43.png>)

M := {u ∈ X : u ≤ u ≤ u in Ω},

![](<2503.08261_pg14_images/imageFile44.png>)

![](<2503.08261_pg14_images/imageFile45.png>)

which is a closed and convex subset of X. Deﬁne m := infM Eλ,ǫ(u). We claim that this inﬁmum is achieved by a solution of the equation (Pλǫ). To this end, we suppose {un}n∈IN be

