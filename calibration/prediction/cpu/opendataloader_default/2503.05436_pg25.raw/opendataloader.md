REVERSIBLE VECTOR FIELDS OF TYPE (2;1) 25

Therefore σ conjugates ϕ and Q. In particular it follows that Fix(Q) ⊂ Rm is sub vector space of dimension r. From (6) we know that Q is an involution. Thus from statements (i) and (ii) we have that there is a linear change of variables such that in these new variables Q is given by,

Q(x1,...,xm) = (x1,...,xr,−xr+1,...,−xm). The result now follows from the fact that ϕ is Ck-conjugated to Q by σ.

Appendix B. Poincar´e Compactification

Let X be a planar polynomial vector ﬁeld of degree n as our polynomial diﬀerential systems of Theorem 1. The Poincare´ compactiﬁed vector ﬁeld p(X) is an analytic vector ﬁeld on S2 constructed as follow (for more details see [17, Chapter 5]).

First we identify R2 with the plane (x1,x2,1) in R3 and deﬁne the Poincare´ sphere as S2 = {y = (y1,y2,y3) ∈ R3 : y12 + y22 + y32 = 1}. We deﬁne the northern hemisphere, the southern hemisphere and the equator respectively by H+ = {y ∈ S2 : y3 > 0}, H− = {y ∈ S2 : y3 < 0} and S1 = {y ∈ S2 : y3 = 0}.

Consider now the projections f± : R2 → H± given by

f±(x1,x2) = ±∆(x1,x2)(x1,x2,1), where ∆(x1,x2) = (x21 + x22 + 1)−21. These two maps deﬁne two copies of X, one copy X+ in H+ and one copy X− in H−. Consider the vector ﬁeld X′ = X+ ∪X− deﬁned in S2\S1. Note that the inﬁnity of R2 is identiﬁed with the equator S1. The Poincar´e compactiﬁed vector ﬁeld p(X) is the analytic extension of X′ from S2\S1 to S2 given by y3n−1X′. The Poincare´ disk D is the projection of the closed northern hemisphere to y3 = 0 under (y1,y2,y3)  → (y1,y2) (the vector ﬁeld given by this projection is also denoted by p(X)). Note that to know the behavior p(X) near S1 is the same than to know the behavior of X near the inﬁnity. We deﬁne the local charts of S2 by Ui = {y ∈ S2 : yi > 0} and Vi = {y ∈ S2 : yi < 0} for i ∈ {1,2,3}. In these charts we deﬁne φi : Ui → R2 and ψi : Vi → R2 by

![](<2503.05436_pg25_images/imageFile1.png>)

ym yi

yn yi

φi(y1,y2,y3) = −ψi(y1,y2,y3) =

,

,

![](<2503.05436_pg25_images/imageFile2.png>)

![](<2503.05436_pg25_images/imageFile3.png>)

where m = i, n = i and m < n. Denoting by (u,v) the image of φi and ψi in every chart (therefore (u,v) play diﬀerent roles in each chart) one can see the following expressions for p(X):

1 v

1 v

1 v

- u

![](<2503.05436_pg25_images/imageFile4.png>)

- v − uP


- u

![](<2503.05436_pg25_images/imageFile5.png>)

- v


- u

![](<2503.05436_pg25_images/imageFile6.png>)

- v


vn m(u,v) Q

,−vP

in U1,

,

,

,

![](<2503.05436_pg25_images/imageFile7.png>)

![](<2503.05436_pg25_images/imageFile8.png>)

![](<2503.05436_pg25_images/imageFile9.png>)

1 v − uQ

1 v

1 v

- u

![](<2503.05436_pg25_images/imageFile10.png>)

- v


- u

![](<2503.05436_pg25_images/imageFile11.png>)

- v


- u

![](<2503.05436_pg25_images/imageFile12.png>)

- v


vn m(u,v) P

in U2, m(u,v)(P(u,v),Q(u,v)) in U3,

,−vQ

,

,

,

![](<2503.05436_pg25_images/imageFile13.png>)

![](<2503.05436_pg25_images/imageFile14.png>)

![](<2503.05436_pg25_images/imageFile15.png>)

where m(u,v) = (u2 + v2 + 1)−21(n−1). We can omit the term m(u,v) by a time rescaling of p(X). Therefore, we obtain a polynomial expression of p(X) in each Ui. The expressions of p(X) in each Vi is the same as that for each Ui, except by a multiplicative factor of (−1)n−1. In these coordinates for i ∈ {1,2}, v = 0 always represents the points of S1 and thus the inﬁnity of R2. Note that S1 is invariant under the ﬂow of p(X).

![](<2503.05436_pg25_images/imageFile16.png>)

