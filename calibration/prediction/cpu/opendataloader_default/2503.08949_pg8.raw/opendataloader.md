8 AMOL AGGARWAL AND PATRICK LOPATTO

2. Shape of the Eigenfunction vs,E: To precisely understand how λs,E varies in E, we must not only understand the operator Fs,E but also the associated eigenfunction vs,E. This diﬀers from prior work, such as [Bap14], which circumvented the analysis of vs,E by instead estimating the action of Fs,E on certain test vectors (which loses careful control on λs,E for E ≈ E0). We approximate the eigenfunction vs,E in Section 8, where we begin by deﬁning an explicit function u˜ by

u˜(x) = (t2 lnK)−1 · {|x| ≤ Ct2} + |x|−(2−s) · {Ct2 ≤ |x|}. (1.10) Observe that, if s is very close to 1, the function u˜(x) behaves as (t2 ln K)−1 for x ≤ Ct2 and as x−1 for x ≥ Ct2. This is the general behavior we expect for the eigenfunction vs,E. However, the precise location and nature of the crossover around x = O(t2), at which vs,E(x) changes from behaving as x−1 ∼ t−2 to as (t2 lnK)−1, is not transparent to us. So, instead of comparing vs,E directly to u˜, we will compare Fs,Evs,E to Fs,Eu˜. Speciﬁcally, as Lemma 8.5, we show that

c(FEu˜)(x) ≤ (Fs,Evs,E)(x) ≤ C(FEu˜)(x), (1.11)

where the constants c and C are uniform in K. While useful, this does not explain how vs,E varies with E and, indeed, we do not know how to do this.

We bypass this by making use of the identity lnλs,E = lim

ln FEnu˜ 1 n

. (1.12)

![](<2503.08949_pg8_images/imageFile1.png>)

n→∞

The beneﬁt of this representation is that it replaces vs,E with the function u˜ that is independent of E. However, it comes at the expense of having to compute high powers of Fs,E when applied to u˜.

3. Estimating Iterates of Fs,E: To deduce the monotonicity of λs,E, we analyze the diﬀerence lnλs,E

using (1.12). We have

− lnλs,E

1

2

∞

− Fs,En

(Fs,En

u˜ 1 − Fs,En

Fs,En

)˜u (x)dx. (1.13) We note the identity

u˜ 1 =

1

2

1

2

−∞

n−1

(F◦)Fs,Ej

Fs,En−j−1

− Fs,En

Fs,En

, (1.14)

=

1

2

1

2

j=0

where we deﬁne (F◦u)(x) = (Fs,E

∞

t2−s |x|2−s

(−y − t2x−1) u(y)dy.

(−y − t2x−1) − ρs,E

)u(x) =

− Fs,E

ρs,E

![](<2503.08949_pg8_images/imageFile2.png>)

1

2

1

2

−∞

When |x| ≥ Ct2 and y is close to 0 (which is where the above integral will mainly be supported), (1.9) implies that ρs,E

(−y − t2/x) < c(E2 − E1). This suggests that F◦ should acts as a negative operator for functions supported outside of [−Ct2,Ct2].

(−y − t2/x) − ρs,E

1

2

- In Section 9, we study F◦ by justifying this reasoning. In particular, as Lemma 9.3, we conﬁrm

that F◦Fju˜(x) is negative for |x| ≥ Ct2 and bound it away from zero. The contribution from |x| ≤ Ct2 might be positive, so we also provide a bound on this quantity in the same Lemma 9.3, using (1.8). Throughout these analyses, we make repeated use of (1.11), to bound high powers of Fs,E applied to u˜ by a multiple of vs,E (on which Fs,E acts diagonally).

- In Section 10, we use the estimates from Lemma 9.3 as inputs to show that the negative contri-


butions from the regime |x| ≥ Ct2 outweigh the positive ones from when |x| ≤ Ct2. We therefore deduce that the Fs,En−j−1

(F◦)Fs,Ej

from (1.14) essentially act as nonpositive operators on u˜, when E1 < E2 are close to E0. Combining (1.13) and (1.14), we ﬁnd Fs,En

2

1

2 1 − Fs,En

1 1 ≤ 0. Then (1.12) shows that λs,E is weakly decreasing near E0, which is stated as Lemma 10.2. This argument

