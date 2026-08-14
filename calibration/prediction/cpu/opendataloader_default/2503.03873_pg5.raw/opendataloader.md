EQUIDIST OF INTEGERS VIA STD. QUAD. FORM UNDER ARITHMETIC CONSTRAINTS 5

We want to study the relations between the dual group A of A and the dual groups H and A/H of the subgroup H and the quotient group A/H. In fact, one can identify A/H with the subgroup H⊥, called the annihilator of H, deﬁned as

H⊥ := χ ∈ A : χ(x) = 1 ∀x ∈ H ,

so that if we take φ ∈ L1(A) and deﬁne φH ∈ L1(A/H) as φH(xH) = H φ(xh)dh, then by the above identiﬁcation, we get FA/H(φH) = FA(φ)|H⊥, see the proof of the theorem below, which explains this technique.

Theorem 2.1 (General Poisson summation formula). Let H be a closed subgroup of the locally compact Abelian group A. For φ ∈ L1(A), if FA(φ)|H⊥ ∈ L1(H⊥), then

FA(φ)(χ)χ(x)dχ, (2.3)

φ(xh)dh =

H⊥

H

for all x ∈ A, where Haar measure on H⊥ ∼= A/H is the Plancherel measure with respect to the chosen Haar measure on A/H.

Proof. For χ ∈ H⊥ we have χ(xh) = χ(x) for every x ∈ A and h ∈ H. We therefore get from the quotient integral formula (2.2) that

FA/H(φH)(χ) =

=

φH(xH)χ(x)d(xH)

![](<2503.03873_pg5_images/imageFile1.png>)

A/H

![](<2503.03873_pg5_images/imageFile2.png>)

φ(xh)χ(xh)dhd(xH)

A/H H

=

![](<2503.03873_pg5_images/imageFile3.png>)

φ(x)χ(x)dx = FA(φ)(χ)

A

for every χ ∈ H⊥. Moreover, if FA(φ)|H⊥ ∈ L1(H⊥) = L1 A/H , then the Fourier inversion formula implies that for all x ∈ A

φ(xh)dh = φH(xH) = FH⊥FA/H(φH)(−xH)

H

= FH⊥FA(φ)(−xH) =

![](<2503.03873_pg5_images/imageFile4.png>)

FA(φ)(χ)−xH(χ)dχ

H⊥

=

![](<2503.03873_pg5_images/imageFile5.png>)

FA(φ)(χ)χ(−x)dχ =

H⊥

FA(φ)(χ)χ(x)dχ.

H⊥

In all our applications, the group A will be of the form A = (Z/NZ)d

× Rd2

for N ∈ N+, d1, d2 ∈ N. Recall we have deﬁned the standard symmetric bilinear form on Rd2

1

as in the beginning of §1, and for any N ∈ N+, we still denote the symmetric bilinear form on (Z/NZ)d

1

by Q as deﬁned in the standard way. We then identify A with its dual group A through the pairing

A ∼= A (s, t)  → χs,t(l, ξ) = e2πi(Q(s,l) N +Q(t,ξ)),

![](<2503.03873_pg5_images/imageFile6.png>)

