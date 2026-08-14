10 D. CORRO, A. MORENO, AND M. ZAREI Proof. We show that there exists 0 < t0 < b such that the hypothesis of Theorem 2.14 hold for the sequence of ﬂows g˜i(t) = gi(t0 + t) for t ∈ (−t0,b − t0).

Since Rm(gi(t)) ≤ C for all t ∈ [0,b], then by Proposition 2.16 there exists a constant K := n

√

![](<2503.05896_pg10_images/imageFile1.png>)

C ≥ 0 such that for all i ∈ N we have for t ∈ [0,b] we have

(1) e−2Ktgi(0) ≤ gi(t) ≤ e2Ktgi(0).

Fix p ∈ M, and consider two orthonormal vectors u,v ∈ TpM. Let {e1,e2,... ,en} be an orthonormal basis of TpM with e1 = u, e2 = v. Then we have that

|Sec(gi(t))(u ∧ v)|2 = (Sec(gi(t))(u ∧ v))2

= (Rm(gi(t))(u,v,u,v))2

= Rm(gi(t))21212(p) ≤

n

Rm(gi(t))2ijkℓ(p)

i,j,k,ℓ=1

= Rm(gi(t)) 2(p) ≤ C2. Thus there exists ∆ > 0 such that |Sec(gi(t))| ≤ ∆ for all i ∈ N and t ∈ [0,b].

Fix t0 ∈ (0,b), and consider a C1-continuous curve γi: [0,1] → Mi. We have the following relation between the length of γi with respect to gi(0), denoted by ℓ(gi(0))(γi), and the length of γi with respect to gi(0), denoted by ℓ(gi(t0))(γi):

1

![](<2503.05896_pg10_images/imageFile2.png>)

gi(0)(γ′(s),γ′(s)) ds

ℓ(gi(0))(γi) =

0

1

![](<2503.05896_pg10_images/imageFile3.png>)

e−2Kt0gi(t0)(γ′(s),γ′(s)) ds

≥

0

1

≥e−Kt0

![](<2503.05896_pg10_images/imageFile4.png>)

gi(t0)(γ′(s),γ′(s))ds

0

= e−Kt0ℓ(gi(t0))(γi). From this, it follows that for all i ∈ N and arbitrary xi,yi ∈ Mi we have dgi(0)(xi,yi) ≥ e−Kt0dgi(t0)(xi,yi). For pi ﬁxed and r > 0, let qi ∈ Beg−i(0)Kt0r(pi). Then since e−Kt0r > dgi(0)(pi,qi), it follows that r > eKt0dgi(0)(pi,qi) ≥ dgi(t0)(pi,qi),

That is the open ball Beg−i(0)Kt0r(pi) of radius e−Kt0r centered at pi with respect to gi(0) is contained in the open ball of radius r centered at pi with respect to gi(t0), i.e.

Beg−i(0)Kt0r(pi) ⊂ Brgi(t0)(pi).

Observe that since t0 ∈ (0,b) and K > 0, then we have 1 ≥ e−Kt0 ≥ e−Kb, and 1 ≥ e−Knt0 ≥ e−Knb. Choose 2r0 = min{ν0,2}. Then we have that 2e−Kt0r0 ≤ 2r0 ≤ ν0 ≤ Injrad(gi(0)) for all i ∈ N. Then by [12, Proposition 14], there exists a constant A(n), which depends only on the dimension n, such that:

A(n) nn

vol(gi(0)) Beg−i(0)Kt0r

r0ne−Knt0. for each i ∈ N and all xi ∈ Mi.

(xi) ≥

![](<2503.05896_pg10_images/imageFile5.png>)

0

