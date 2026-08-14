14 MAXIM BOGDAN

diﬀer on a set of null measure). So we have that ∇w1(x) = ∇w2(x) = 0 for a.a. x ∈ Ω \ Ω˜. We may also write that ∇w1(x)

= ∇w2(x) w2(x)

= 0 for a.a. x ∈ Ω \ Ω˜.

![](<2503.06630_pg14_images/imageFile1.png>)

![](<2503.06630_pg14_images/imageFile2.png>)

w1(x)

- Fact II: For a.a. x ∈ Ω˜ we have that ∇w1(x) w1(x)

![](<2503.06630_pg14_images/imageFile3.png>)

= ∇w2(x) w2(x)

![](<2503.06630_pg14_images/imageFile4.png>)

.

Since x ∈ Ω˜ we have that ∇w1(x),∇w2(x) = 0. But to have equalities in (43) we deduce that |∇w1(x)| · |∇w2(x)| = ∇w1(x) · ∇w2(x). This means that there is some λ(x) > 0 such that ∇w2(x) = λ(x)∇w1(x). Following the cases in which equality can occur in Lemma 4.1, having r > 1 and |∇w1(x)|,|∇w2(x)| > 0, we

are in the case (iii) from which we can write that: |∇w1(x)| w1(x)

![](<2503.06630_pg14_images/imageFile5.png>)

= |∇w2(x)| w2(x)

![](<2503.06630_pg14_images/imageFile6.png>)

=⇒

|∇w1(x)| w1(x)

![](<2503.06630_pg14_images/imageFile7.png>)

=

λ(x)|∇w1(x)| w2(x)

![](<2503.06630_pg14_images/imageFile8.png>)

=⇒

λ(x) =

w2(x) w1(x)

![](<2503.06630_pg14_images/imageFile9.png>)

. So the claim is proved, since ∇w2(x) =

w2(x) w1(x)∇w1(x).

![](<2503.06630_pg14_images/imageFile10.png>)

- Fact III: The function


w2 w1

is constant.

![](<2503.06630_pg14_images/imageFile11.png>)

= ∇w2(x) w2(x)

At this moment we have that ∇w1(x) w1(x)

a.e. on the entire domain Ω. Using now Lemma 5.1 proved

![](<2503.06630_pg14_images/imageFile12.png>)

![](<2503.06630_pg14_images/imageFile13.png>)

∇w1 w1

∇w2 w2 −

w2 w1 ∈ Wloc1,1(Ω) and: ∇

w2 w1

w2 w1

at the end of this proof, we deduce that

= 0 a.e. on Ω. Since Ω is a connected domain we infer that

=

![](<2503.06630_pg14_images/imageFile14.png>)

![](<2503.06630_pg14_images/imageFile15.png>)

![](<2503.06630_pg14_images/imageFile16.png>)

![](<2503.06630_pg14_images/imageFile17.png>)

![](<2503.06630_pg14_images/imageFile18.png>)

w2 w1

is a constant function. Let w2 = λw1 a.e. on Ω for some λ > 0. Substituting this in (54) we obtain a.e. on Ω that:

![](<2503.06630_pg14_images/imageFile19.png>)

w1

a(x,∇w1) · ∇ w1 − λrw1 = a(x,λ∇w1) · ∇

λr−1 − λw1 ⇐⇒ 1 − λr a(x,∇w1) · ∇w1 =

![](<2503.06630_pg14_images/imageFile20.png>)

1 − λr λr−1

a(x,λ∇w1) · ∇w1 ⇐⇒ 1 − λr λr−1Φ(x,|∇w1|)|∇w1| = 1 − λr Ψ(x,λ|∇w1|)λ∇w1 · ∇w1 ⇐⇒ 1 − λr λr−1Φ(x,|∇w1|)|∇w1| = 1 − λr Φ(x,λ|∇w1|)|∇w1|

![](<2503.06630_pg14_images/imageFile21.png>)

⇐⇒ 1 − λr |∇w1| Φ(x,λ|∇w1|) − λr−1Φ(x,|∇w1|) = 0.

Therefore we may have λ = 1 and the equality holds. If λ = 1 then ∇w1(x) = 0 or Φ(x,λ|∇w1|) = λr−1Φ(x,|∇w1|) for a.a. x ∈ Ω. This disjunction is equivalent to the second relation since Φ(x,0) = 0.

Φ(x,s) sr−1

is strictly increasing for a.a. x ∈ Ω (i.e. (H7’) holds), then equality can occur when λ = 1 (i.e. w1 ≡ w2). If λ = 1 then for x ∈ Ω˜ (i.e. ∇w1(x) = 0) we have that Φ(x,λ|∇w1(x)|) = λr−1Φ(x,|∇w1(x)|) which rewrites as

If we know that the function (0,∞) ∋ s  →

![](<2503.06630_pg14_images/imageFile22.png>)

Φ(x,|∇w1(x)|) |w1(x)|r−1

Φ(x,λ|∇w1(x)|) λ|w1(x)| r−1

. This equality

=

![](<2503.06630_pg14_images/imageFile23.png>)

![](<2503.06630_pg14_images/imageFile24.png>)

is impossible to hold from the strict monotony of the function involved there. So |Ω˜| = 0 which means that ∇w1 = 0 a.e. on Ω. Therefore ∇w2 = λ∇w1 = 0 a.e. on Ω. Finally, since Ω is connected we have that w1 and w2 are diﬀerent constant functions. The theorem is now completely proved.

Now we shall state and prove the lemma we have used above. Lemma 5.1. Let Ω ⊂ RN be an open, bounded and connected domain. If w1,w2 ∈ W1,p(x)(Ω) with:

- (i) w1,w2 > 0 a.e. on Ω;
- (ii)

- w1

![](<2503.06630_pg14_images/imageFile25.png>)

- w2


,

w2 w1 ∈ L∞(Ω);

![](<2503.06630_pg14_images/imageFile26.png>)

- (iii) ∇w1 w1


, ∇w2

w2 ∈ L1loc(Ω)N. Then

![](<2503.06630_pg14_images/imageFile27.png>)

![](<2503.06630_pg14_images/imageFile28.png>)

w2 w1

- w1

![](<2503.06630_pg14_images/imageFile29.png>)

- w2 ∈ Wloc1,1(Ω) and moreover:


,

![](<2503.06630_pg14_images/imageFile30.png>)

∇

w2 w1

![](<2503.06630_pg14_images/imageFile31.png>)

w1∇w2 − w2∇w1 w12

=

=

![](<2503.06630_pg14_images/imageFile32.png>)

w2 w1

![](<2503.06630_pg14_images/imageFile33.png>)

∇w1 w1

∇w2 w2 −

![](<2503.06630_pg14_images/imageFile34.png>)

![](<2503.06630_pg14_images/imageFile35.png>)

. (55)

