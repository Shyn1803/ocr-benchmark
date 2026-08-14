2.2 Upper bounds on the mass distribution

Our main results give lower bounds on the mass measure mν deﬁned in (1.14). It is then natural to ask about matching upper bounds. Additionally, we only give lower bounds for |k| ! ν´1{2. For |k| " ν´1{2, the dynamics should be dominated by the ν∆ dissipation, and so the lower bound should not generally hold.

- 2.2.1. The |k| ! ν´1{2 range. First, when |k| ! ν´1{2, we note the following upper bound. This bound is essentially identical to the cumulative Batchelor spectrum upper bound obtained in [BBPS21b] and relies on the uniform-in-diﬀusivity exponential mixing.

- Proposition 2.1. For all R ě 2, mνpr1,Rsq ď C log R. (2.2)

Proof. Using the exponential mixing, we note that for any α ą 0

mνpr1,Rsq “ ż 8

0

E}ΠďRϕνt }2L2

ď ż αlogR

0

E}ϕνt }2L2 ` CR2 ż 8

α log R

e´C´1t dt ď αlog R ` CR2e´C´1αlogR.

Choosing α large enough, we conclude.

![](<2503.05885_pg8_images/imageFile1.png>)

![](<2503.05885_pg8_images/imageFile2.png>)

![](<2503.05885_pg8_images/imageFile3.png>)

![](<2503.05885_pg8_images/imageFile4.png>)

One can then use Chebyshev’s inequality to obtain a log-density bound on the “overcharged” radii. We deﬁne

![](<2503.05885_pg8_images/imageFile5.png>)

Bνh,α :“ r P r1,8q : mνprr,r ` hsq ě

αh r (

![](<2503.05885_pg8_images/imageFile6.png>)

(2.3) and compute

µ1,RpBνh,αq “

![](<2503.05885_pg8_images/imageFile7.png>)

1 log R

![](<2503.05885_pg8_images/imageFile8.png>)

ż

![](<2503.05885_pg8_images/imageFile9.png>)

Bνh,αXr1,Rs

1 r

![](<2503.05885_pg8_images/imageFile10.png>)

dr ď

1 αhlog R

![](<2503.05885_pg8_images/imageFile11.png>)

ż R

1

mνprr,r`hsqdr ď

1 αlog R

![](<2503.05885_pg8_images/imageFile12.png>)

mνpr1,R`hsq ď Cα´1.

We have proven the following density estimate.

- Proposition 2.2. For all R ě 2, µ1,RpBνh,αq ď Cα´1.


![](<2503.05885_pg8_images/imageFile13.png>)

We note that, in some sense, this upper bound matches the second term of the lower bound density estimate in (1.10) or the lower bound estimate in (1.12). It however does not match the estimates (1.11) or (1.13), which do not require taking a limit in α.

- 2.2.2. The |k| " ν´1{2 range. The bound given by Proposition 2.1 holds for all R ě 2, however one can get a much sharper statement for R " ν´1{2. Computing the Itˆo diﬀerential, we have the


energy estimate

d dt

E}ψtν}2L2 “ ´2νE}∇ψtν}2L2 ` }g}2L2. By the Itˆo isometry, Duhamel’s principle, and the stationarity of the ut process,

![](<2503.05885_pg8_images/imageFile14.png>)

d dt

E}ψtν}2L2 “ E}ϕνt }2L2 ď e´C´1νt tÑ8Ñ 0.

![](<2503.05885_pg8_images/imageFile15.png>)

8

