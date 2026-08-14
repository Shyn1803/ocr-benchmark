From [22, Section 3], for every θ, we have E[∥U(x,k∆t;θ) − Un(x,k∆t;θ)∥2] ≤ Kk∆t,U(·,0),θλ−N1+1(θ), (D.15)

where Kk∆t,U(·,0),θ is a constant depending on time k∆t and the initial condition U(·,0), and θ. Without loss of generality, we assume that Kk∆t,U(·,0),θ is non-decreasing in k (otherwise we can replace Kk∆t,U(·,0),θ with K˜k∆t,U(·,0),θ := max1≤i≤k Ki∆t,U(·,0),θ. Given the initial condition U(x,0) and PnU(x,0), we denote the probability measures of U(x,k∆t;θ) and Un(x,T;θ) by νU(·,0)(k∆t) and νn,U

n(·,0)(k∆t), respectively. Moreover, the joint probability measure of U(x,k∆t;θ),Un(x,k∆t;θ) has marginal distributions νU(·,0)(k∆t) and νn,U

n(·,0)(k∆t), respectively. From Eq. (D.15), we can deduce that: W22(νU(·,0)(k∆t),νn,U

n(·,0)(k∆t)) ≤ E[∥U(x,k∆t;θ) − Un(x,k∆t;θ)∥2] ≤ sup

KT,U(·,0),θλ−N1+1(θ).

θ,U(x,0)

(D.16) Furthermore, using the definition of the local squared W2 distance in Eq. (2.4), we have:

W22,δ,e U(·,k∆t;θ),Un(·,k∆t;θ) ≤ sup

E[∥U(x,k∆t;θ) − Un(x,k∆t;θ)∥2] ≤ sup

θ,U(x,0)

KT,U(·,0),θλ−N1+1(θ).

θ,U(x,0)

(D.17) Similarly, we can conclude that:

W22,δ,e U ˆ(·,k∆t;θˆ),Uˆn(·,k∆t;θˆ) ≤ sup

θ,Uˆ (x,0)

KT,U(·,0),θλ−N1+1(θˆ). (D.18)

Given the same initial condition U(x,0) = Uˆ(x,0), using the triangle inequality of the Wasserstein distance [14], we have

W22,δ,e(U(x,t;θ),Uˆ(x,t;θˆ)) ≤ 3W22,δ,e U(·,k∆t;θ),Un(·,k∆t;θ)

+ 3W22,δ,e U ˆ(·,k∆t;θˆ),Uˆn(·,k∆t;θˆ) + 3W22,δ,e(Un(x,t;θ),Uˆn(x,t;θˆ)) ≤ 3W22,δ,e(Un(x,t;θ),Uˆn(x,t;θˆ)) + 3 sup

KT,U(·,0),θλ−N1+1(θ)

θ,U(x,0)

KT,U(·,0),θˆλ−N1+1(θˆ).

# + 3 sup

θ,Uˆ (x,0)

(D.19)

46

