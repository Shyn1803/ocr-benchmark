4 RAINIS HALLER, PAAVO KUUSEOK, AND MART¨ POLDVERE˜

is of µ-measure zero. (Here the key observation is that, since λa(ω) + νb(ω) = λa(ω) + νb(ω) for a.e. ω ∈ Ω, one has αa(ω) + βb(ω) = α a(ω) + β b(ω) whenever α,β ≥ 0 for a.e. ω ∈ Ω.) Redeﬁning the values of a, b, x, y, and z on H to become 0, the redeﬁned a, b, x, y, and z are the same functions in L1(µ,X) as the original ones. The existence of the desired W now follows from (♯).

The following two lemmata may be known; however, we do not know of any references for them.

Lemma 2.2. Let µ be a non-zero ﬁnite (countably additive non-negative) measure on a σ-algebra Σ of subsets of a set Ω, and let X be a Banach space. Let z ∈ SL

1(µ,X), let E ∈ Σ, and let 0 < ε < 1. (a) If z(ω) = 0 for every ω ∈ E, then there are n ∈ N and pairwise disjoint measurable subsets E0,E1,...,En of E with ni=0 Ei = E such that

- (1) µ(E0) < ε;
- (2) E

i

z dµ > (1−ε) E

i

z dµ for every i ∈ {1,...,n} with µ(Ei) > 0;

- (3) for every i ∈ {1,...,n} with µ(Ei) > 0, there is a neighbourhood Wi


of z in the relative weak topology of BL

1(µ,X) such that

- (2.1) Ei

w dµ > (1 − ε)

Ei

z dµ for every w ∈ Wi;

this neighbourhood can be chosen to be of the form Wi := w ∈ BL

1(µ,X): E

i

wi∗(w − z)dµ < δi for some wi∗ ∈ SX∗ and δi > 0. (b) There is a neighbourhood W of z in the relative weak topology of BL

1(µ,X)

such that

- (2.2) E


z dµ − ε <

E

w dµ <

E

z dµ + ε for every w ∈ W.

Proof. (a). Assume that z(ω) = 0 for every ω ∈ E. Choose a real number σ > 0 so that µ(E \ D) < 2ε where D := {ω ∈ Ω: z(ω) > σ}. Since the function z is essentially separably-valued, there is a subset N of D such that µ(N) = 0 and the set z(D \ N) is separable. It follows that there are pairwise disjoint measurable subsets Ei of E, i = 1,2,..., such that diamz(Ei) < εσ2 for every i ∈ N, and

![](<2503.09182_pg4_images/imageFile1.png>)

![](<2503.09182_pg4_images/imageFile2.png>)

- D \ N = ∞i=1 Ei. Pick an n ∈ N so that µ(C) < 2ε where C := ∞i=n+1 Ei, and set

![](<2503.09182_pg4_images/imageFile3.png>)

- E0 := (E \ D) ∪ N ∪ C. Fix an i ∈ {1,...,n} and suppose that µ(Ei) > 0. Letting zi ∈ z(Ei) be


arbitrary and picking a zi∗ ∈ SX∗ so that Re zi∗(zi) = zi , one has

z dµ ≥ Re zi∗

Ei

z dµ =

Ei

Ei

Re zi∗(zi) + Re zi∗(z − zi) dµ

≥

( zi − z − zi )dµ ≥

Ei

( z − 2 z − zi )dµ

Ei

>

( z − εσ)dµ ≥

Ei

( z − ε z )dµ = (1 − ε)

Ei

Ei

z dµ.

Now pick a wi∗ ∈ SX∗ satisfying Rewi∗ E

z dµ and set Wi := w ∈ BL

z dµ = E

i

i

wi∗(w − z)dµ < δi where δi := E

z dµ − (1 − ε) E

z dµ > 0.

1(µ,X): E

i

i

i

