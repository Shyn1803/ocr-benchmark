Nash,  ||| |||−2−

with ′′ := −2

4

, and ﬁnally

![](<2503.08186_pg7_images/imageFile1.png>)

- 1

![](<2503.08186_pg7_images/imageFile2.png>)

- 2


d d

![](<2503.08186_pg7_images/imageFile3.png>)

4

ΓΩ( , ·,  ) 2L2(Ω) ≤ − ′′ ΓΩ( , ·,  ) 2+

L2(Ω) + ΓΩ( , ·,  ) 2L2(Ω).

![](<2503.08186_pg7_images/imageFile4.png>)

Denoting ( ) := ΓΩ( , ·,  ) 2L2(Ω)

− 2

![](<2503.08186_pg7_images/imageFile5.png>)

, we see therefore that

′( ) ≥

4

( ′′ − ( )),

![](<2503.08186_pg7_images/imageFile6.png>)

which implies

4

4

( ) ≥ ′′

e−

, so that in the end

![](<2503.08186_pg7_images/imageFile7.png>)

![](<2503.08186_pg7_images/imageFile8.png>)

4 −

![](<2503.08186_pg7_images/imageFile9.png>)

2

ΓΩ( , ·,  ) 2L2(Ω) ≤ ′′

![](<2503.08186_pg7_images/imageFile10.png>)

e2 − 2 .

![](<2503.08186_pg7_images/imageFile11.png>)

This yields the claimed L2 bound. For the L∞ bound, note ﬁrst that the Laplace operator is self-adjoint, so that ΓΩ( ,  , ) =

ΓΩ( ,  ,  ). By the semigroup property, we therefore ﬁnd that

ΓΩ( /2,  ,  ) ΓΩ( /2,  , ) d

ΓΩ( ,  , ) =

Ω

≤ ΓΩ( /2,  , ·) L2(Ω) ΓΩ( /2, ·,  ) L2(Ω) ≤ ΓΩ( /2, ·,  ) L2(Ω) ΓΩ( /2, ·,  ) L2(Ω),

and we use the already established L2 bound to conclude.

A direct interpolation between the L1 and L∞ estimates yields the L estimate stated in the Lemma. Finally, the self-adjointness argument leads to the second group of estimates.

In the context of the domains appearing in the proof of Proposition 5 (but keeping the notations of Lemma 11), we write down for the related geometry the following statement: Lemma 12. Fix > 0. Then there exists a constant  ,  ∗ such that for any domain

Ω := (0, ) ∩ {( ′,   ) ∈ R : > ( ′)}

for > 0 and : R −1 → R with  ∇ ∞ ≤ 111 with Ω = (0, ) ∩ { ′,   ) ∈ R : = ( ′)} and Ω = Ω \ Ω the constant Ω, ,  appearing in Lemma 11 is bounded by  ,  ∗ .

![](<2503.08186_pg7_images/imageFile12.png>)

Proof. For the domain considered in the statement, we need an extension operator for functions ∈ H1(Ω) such that | Ω = 0, for the norms H1 and L1. We can ﬁrst extend to Ω+ := {( ′,   ) ∈ R : > ( ′)} by setting 1 = 0 on Ω+ \ Ω, and

1 = on Ω. Recalling that | Ω = 0, we see that || 1|| 1→ 1 = 1 and || 1|| 1→ 1 = 1. We then use Lemma 10 (with Ω in this lemma corresponding to Ω+ here) to build the operator 2 from

![](<2503.08186_pg7_images/imageFile13.png>)

1(Ω+) to 1(R ), so that still thanks to Lemma 10, ||| 2 1||| = ||| 2||| ≤ 2 1 + 1211 2 , and we conclude the Lemma by setting := 2 1.

![](<2503.08186_pg7_images/imageFile14.png>)

We now write down an estimate which is a direct consequence of Lemma 11, and which will be used several times in the sequel.

7

