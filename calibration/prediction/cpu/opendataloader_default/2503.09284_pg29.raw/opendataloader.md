GH-CONVERGENCE OF MAXIMAL GROMOV HYPERBOLIC SPACES AND THEIR BOUNDARIES 29

exist some t1 with 0 < t1 < t < t0 such that dX(o,γ(t1)) ≤ R, contradicting the deﬁnition of t0. Thus, γ(t0) is an accumulation point of Coneo(U) and γ(t0) ∈ SX(o,R).

Suppose p is an accumulation point of Coneo(U) and p ∈ SX(o,R). Then there exists a sequence pn ∈ Coneo(U) such that pn → p as n → ∞. Let xn ∈ [o,pn] ∩ U for some geodesic segment joining o to pn.

dX(xn,p) ≤ dX(xn,pn) + dX(pn,p)

= dX(o,pn) − dX(o,xn) + dX(pn,p)

= dX(o,pn) − R + dX(pn,p) −−−−→n→∞ dX(o,p) − R + 0 = 0.

Thus xn → p as n → ∞. Since U is a connected component of S, it is closed, and we have p ∈ U. From this above discussion, we get γ(t0) ∈ U.

Deﬁne t1 := sup{t ≥ 0 | dX(o,γ(t)) ≤ R}, then similarly we can argue that γ(t1) ∈ V . Note that

dX(γ1(t),γ2(t)) = dX(γ1(t),γ(t0)) + dX(γ(t0),γ(t1)) + dX(γ(t1),γ2(t)),

- dX(o,γ1(t)) = dX(o,γ1(R)) + dX(γ1(R),γ1(t)) = R + dX(γ1(R),γ1(t)),
- dX(o,γ2(t)) = dX(o,γ2(R)) + dX(γ2(R),γ2(t)) = R + dX(γ2(R),γ2(t)),


which gives,

(42)

2(γ1(t)|γ2(t))o =2R − dX(γ(t0),γ(t1))

+ dX(γ1(t),γ(t0)) − dX(γ1(R),γ1(t))

+ dX(γ(t1),γ2(t)) − dX(γ2(R),γ2(t)).

For x ∈ U and y ∈ V we have 2(x|y)o = dX(x,o) + dX(y,o) − dX(x,y) = 2R − dX(x,y). Thus from (42) and application of the triangle inequality we get,

(43)

2 (γ1(t)|γ2(t))o − (x|y)o ≤ dX(x,y) − dX(γ(t0),γ(t1))

+ dX(γ1(t),γ(t0)) − dX(γ1(R),γ1(t)) + dX(γ(t1),γ2(t)) − dX(γ2(R),γ2(t))

≤ dX(x,γ(t0)) + dX(γ(t1),y) + dX(γ(t0),γ1(R)) + dX(γ(t1),γ2(R)) ≤ 2(diam(U) + diam(V ))

We know from property of Gromov product space lim

(γ1(t)|γ2(t))o = (ξ|η)o.

t→∞

Therefore, from (43) we can conclude the desired claim (40) (by taking limit t → ∞ on the left hand side).

For proving (41), consider geodesic rays γ1 and γ2 joining o to ξ and η, respectively, as above. Then (γ1(t)|γ2(t))o ↑ (ξ|η)o as t → ∞. Note γ1(R),γ2(R) ∈ U. Thus,

- 1

![](<2503.09284_pg29_images/imageFile1.png>)

- 2


(ξ|η)o ≥ (γ1(R)|γ2(R))o =

diam(U) 2

dX(o,γ1(R)) + dx(o,γ2(R)) − dX(γ1(R),γ2(R)) ≥ R −

.

![](<2503.09284_pg29_images/imageFile2.png>)

Now we are well equipped to give the proof of Theorem 1.5. Proof of Theorem 1.5. Since (Xn,xn) is a maximal Gromov product space, it is isometric to M(∂PXn,ρx

),

n

for each n, via the visual embedding (see Proposition 2.2.6). Similarly, (X,x) is isometric to M(∂PX,ρx). Deﬁne the sequence of antipodal spaces (Zn,ρn) = (∂PXn,ρx

) for all n and (Z,ρ0) = (∂PX,ρx), where Z is a ﬁnite set of cardinality m < ∞.

n

By the given hypothesis the Moebius spaces (M(Zn),ρn) −−−−−−→GH conv. (M(Z),ρ0). We will demonstrate that for any given δ > 0, it is possible to construct δ-isometries fn: (Zn,ρn) → (Z,ρ0) for all suﬃciently large n. Thus, by Remark 3.5, this will be suﬃcient to conclude (Zn,ρn) −−−−−−→AI conv. (Z,ρ0), i.e. (∂PXn,ρx

) −−−−−→AIconv. (∂PX,ρx). Since (M(Zn),ρn) −−−−−−→GH conv. (M(Z),ρ0), for every R > 0, there exists ǫn-isometries Fn: BM(Z)(ρ0,R) → BM(Z

n

n)(ρn,R) such that ǫn → 0+ and Fn(ρ0) = ρn.

The antipodal space (Z,ρ0) is of ﬁnite cardinality, let us label Z = {1,2,··· ,m}. By [BP24, Theorem 1.1], the maximal Gromov hyperbolic spaces M(Z,ρ0) is isometric to a polyhedral complex such that

