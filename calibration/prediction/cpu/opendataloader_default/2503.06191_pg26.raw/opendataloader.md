26 HADDAD, LANGHARST, LIVSHYTS, AND PUTTERMAN Corollary 31. Fix m,n ∈ N. Let ψ : Rn → R+ be an even C1 function with ψ,|∇ψ|2 ∈ L1(Rn,γ

m

nm+1) and Dmψ,|∇Dmψ|2 ∈ L1(Rnm,γn,m). Then,

![](<2503.06191_pg26_images/imageFile1.png>)

1 m + 1

m + 1 m

Varγn,m Dmψ

ψ +

Var

m

![](<2503.06191_pg26_images/imageFile2.png>)

![](<2503.06191_pg26_images/imageFile3.png>)

![](<2503.06191_pg26_images/imageFile4.png>)

- m+1
- n


γ

- 1

![](<2503.06191_pg26_images/imageFile5.png>)

- 2


≤

1 m + 1 Rnm

|∇Dmψ(x)|2dγn,m(x) +

![](<2503.06191_pg26_images/imageFile6.png>)

m

|∇ψ(x)|2dγ

![](<2503.06191_pg26_images/imageFile7.png>)

nm+1(x) .

Rn

Observe that ∇ψ refers to taking the gradient of ψ on Rn while ∇Dmψ contains the gradient on Rnm. The quantity |∇Dmψ|2 seems a bit mysterious, but in fact it is not so complicated. Since ∇ respects the product structure of Rnm, one has that

m

m

∇Dmψ(x1,... ,xm) = ∇ψ(xi) − ∇ψ −

xi

.

i=1

i=1

Thus,

2

m

m

|∇Dmψ(x1,... ,xm)|2 =

∇ψ(xi) − ∇ψ −

xi

.

i=1

i=1

Proof. Using standard approximation techniques, and the fast decay of the densities of the measures γ

m

![](<2503.06191_pg26_images/imageFile8.png>)

nm+1 and γn,m, we may assume that ψ is compactly supported. In Theorem 4, write f = e−V and switch the roles of V and V ⋆. Then, one can take logarithm to obtain

e−mm+1V⋆(x)dx + log

e−Dm(V (x))dx

mlog

![](<2503.06191_pg26_images/imageFile9.png>)

Rnm

Rn

(45)

|·|2

|x|2

e−mm+1

e−Dm

2 (x)dx .

≤ mlog

2 dx + log

![](<2503.06191_pg26_images/imageFile10.png>)

![](<2503.06191_pg26_images/imageFile11.png>)

![](<2503.06191_pg26_images/imageFile12.png>)

Rn

Rnm

2

We consider the case when V (x) = Vε(x) = |x|

2 +εψ(x). Focusing on the second integral in (45), we have

![](<2503.06191_pg26_images/imageFile13.png>)

log

e−Dm(Vε(x))dx − log

Rnm

|·|2

e−Dm

2 (x)dx

![](<2503.06191_pg26_images/imageFile14.png>)

Rnm

exp (−εDm (ψ(x)))dγn,m(x)

= log

Rnm

ε2 2

Dmψ(x) +

(Dmψ(x))2 dγn,m(x) + o(ε3)

= log 1 − ε

![](<2503.06191_pg26_images/imageFile15.png>)

Rnm

ε2 2

Dmψ(x)dγn,m(x) +

Varγn,m Dmψ + o(ε3).

= −ε

![](<2503.06191_pg26_images/imageFile16.png>)

Rnm

We next need the well-known fact that if ψ ∈ C1(Rn) is compactly supported, then

ε2 2 |∇ψ|2 + o(ε3),

Vε⋆ = |x|2

2 − εψ(x) +

![](<2503.06191_pg26_images/imageFile17.png>)

![](<2503.06191_pg26_images/imageFile18.png>)

