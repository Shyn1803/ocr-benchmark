FIRST ORDER NON-INSTANTANEOUS CORRECTIONS IN COLLISIONAL KINETIC ALIGNMENT MODELS 11

where we used that F(s,t) ≤ 1. For the second term of (30a) we have due to the coordinate change from post- to pre-collisional states

εµ1,2 λ1,2

R

t

≤ελ1,2

0 R3

t

≤ελ1,2

0 R3

≤εtλ1,2 sup

0<r<t

t

0

F(r,t)

R2

∞

0

S3(s) f1 f2 − f˜1 f˜2 (v1,v2,v3)dsdv3 dv2 dr dv1

F(r,t) f1f2 − f˜1f˜2 dv1 dv2 dv3 dr

f1 − f˜1 f2 − f2 − f˜2 f ˜1 dv1 dv2 dv3 dr

M2(r) f1(·,r) − f˜1(·,r)

+ M1(r) f2(·,·,r) − f˜2(·,·,r)

L1(R)

L1(R2)

,

where we further used the trivial identity f1 f2−f˜1 f˜2 = (f1−f˜1)f2+(f2−f˜2)f˜1. Similar computations can be done for the right-hand-side of (30b). Indeed, we have

t

λ1,1 ε R2

S2 (t − s)/ε f1f1 − f˜1f˜1 ds dv1 dv2

0

t

λ1,1 ε R2

(t−s)

ε −λ1,2 0 t M1(q)dq(f1f1 − f˜1f˜1)ds dv1 dv2

e−µ

≤

1,1

0

λ1,1 ε

f1(·,s) − f˜1(·,s)

≤2t

, and

sup

M1(s) sup

L1(R)

0<s<t

0<s<t

∞

t

S3(r)(f1f2 − f˜1f˜2) (·,·,v3)dr dv3 (v1,v2)ds dv2 dv1

S2 (t − s)/ε

µ2,1 λ1,2

R2

R

0

0

t

(t−s)

ε −λ1,2 0 t M1(q)dq(f1 f2 − f˜1 f˜2)dv3 ds dv2 dv1

e−µ

=λ1,2

1,1

0 R

R2

≤tλ1,2 sup

0<s<t

M1(s) f2(·,·,s) − f˜2(·,·,s)

+ M2(s) f1(·,s) − f˜1(·,s)

L1(R2)

L1(R2)

.

These estimates can be made contractive if t is chosen small enough, giving local existence. Convergence of (M1(t),M2(t)) to (M1∞,M2∞) as t → ∞ (see (21)) allows to iterate the contraction estimate and implies a global L1-bound of (f1,f2) and therefore global existence.

□

Remark 3.1. We notice that the third estimated term, part of the right-hand-side of f2, shows a term with constant proportional to εt. This is a consequence of the fact that the dynamics of f2 are much faster than the ones of f1 and indicates that time-uniform estimates for the fast variable f2 break down for vanishing ε. Clearly the limits ε → 0 and t → 0 do not commute. Thus, we expect difficulties arising taking the the limit ε → 0 for small time t.

3.3. Instantaneous limit. We consider the mild formulation (30b) for f2ε which after the coordinate change s  → t − εs reveals its time-delay structure

t/ε

f2ε(v1,v2,t) = S2(t/ε)f2I (v1,v2) + λ1,1

S2(s)f1ε(·,t − εs)f1ε(·,t − εs) (v1,v2)ds

0

∞

t/ε

S3(r)f1ε(·,t − εs)f2ε(·,·,t − εs) (v1,v2,v3)dr dv3 ds. Taking the formal limit ε → 0 we obtain

+εµ2,1λ1,2

S2(s)

R

0

0

- (32) f2(v1,v2,t) = λ1,1

∞

0

S2(s)f1(·,t)f1(·,t) (v1,v2)ds. Now substituting it in the equation for f1 yields at leading order

- (33) ∂tf1 = 2λ1,1µ1,1 R


∞

S2(s)f1(·,t)f1(·,t) dsdv2 − 2λ1,1f1

0

f1 dv2 ,

R

